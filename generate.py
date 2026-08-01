import re
import torch
from config import GPTConfig
from model import GPT

# ── rebuild tokenizer ─────────────────────────────────────────────────────────
with open("data/input.txt", "r", encoding="utf-8") as f:
    text = f.read()

text = re.sub(r'<<.*?>>', '', text, flags=re.DOTALL)
text = text.replace('[', '').replace(']', '')
text = text.replace('&c.', 'etc.').replace('&C.', 'etc.')
text = text.replace('&', 'and')
text = re.sub(r'<(\w)', r'\1', text)
text = text.replace('_', ' ').replace('|', ' ')
text = text.replace('`', '').replace('}', ' ')

chars = sorted(list(set(text)))
stoi = {ch: i for i, ch in enumerate(chars)}
itos = {i: ch for i, ch in enumerate(chars)}

encode = lambda s: [stoi[c] for c in s]
decode = lambda l: "".join([itos[i] for i in l])

# ── load checkpoint ───────────────────────────────────────────────────────────
device = "cuda" if torch.cuda.is_available() else "cpu"

checkpoint = torch.load("checkpoints/base_model.pt", map_location=device, weights_only=False)
model_cfg  = checkpoint["model_cfg"]

model = GPT(model_cfg).to(device)
model.load_state_dict(checkpoint["model_state"])
model.eval()
print(f"Model loaded | final training loss: {checkpoint['final_loss']:.4f}")

# ── generate ──────────────────────────────────────────────────────────────────
def generate(prompt, max_new_tokens=500, temperature=1.0):
    idx = torch.tensor(encode(prompt), dtype=torch.long, device=device).unsqueeze(0)

    for _ in range(max_new_tokens):
        # crop to block_size if sequence gets too long
        idx_cond = idx[:, -model_cfg.block_size:]
        logits, _ = model(idx_cond)
        # take logits at last position and apply temperature
        logits = logits[:, -1, :] / temperature
        probs = torch.softmax(logits, dim=-1)
        next_token = torch.multinomial(probs, num_samples=1)
        idx = torch.cat([idx, next_token], dim=1)

    return decode(idx[0].tolist())

# ── run ───────────────────────────────────────────────────────────────────────
prompt = "ROMEO:"
print(f"\nPrompt: {prompt}\n")
print(generate(prompt, max_new_tokens=500, temperature=0.8))
