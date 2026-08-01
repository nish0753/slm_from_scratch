import os
import numpy as np
import torch
from config import GPTConfig, TrainConfig
from model import GPT

# ── config ──────────────────────────────────────────────────────────────────
model_cfg = GPTConfig()
train_cfg = TrainConfig()

device = train_cfg.device if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

os.makedirs(train_cfg.checkpoint_dir, exist_ok=True)

# ── data ─────────────────────────────────────────────────────────────────────
def load_data(split):
    path = os.path.join(train_cfg.data_dir, f"{split}.bin")
    data = np.fromfile(path, dtype=np.uint16)
    return torch.tensor(data, dtype=torch.long)

train_data = load_data("train")
val_data   = load_data("val")

def get_batch(split):
    data = train_data if split == "train" else val_data
    ix = torch.randint(len(data) - model_cfg.block_size, (train_cfg.batch_size,))
    x = torch.stack([data[i     : i + model_cfg.block_size] for i in ix])
    y = torch.stack([data[i + 1 : i + model_cfg.block_size + 1] for i in ix])
    return x.to(device), y.to(device)

# ── model ────────────────────────────────────────────────────────────────────
model = GPT(model_cfg).to(device)
print(f"Parameters: {model.count_params():,}")

optimizer = torch.optim.AdamW(model.parameters(), lr=train_cfg.learning_rate)

# ── eval ─────────────────────────────────────────────────────────────────────
@torch.no_grad()
def estimate_loss():
    model.eval()
    losses = {}
    for split in ("train", "val"):
        split_losses = torch.zeros(train_cfg.eval_iters)
        for k in range(train_cfg.eval_iters):
            x, y = get_batch(split)
            _, loss = model(x, y)
            split_losses[k] = loss.item()
        losses[split] = split_losses.mean().item()
    model.train()
    return losses

# ── training loop ─────────────────────────────────────────────────────────────
for iteration in range(train_cfg.max_iters):

    if iteration % train_cfg.eval_interval == 0:
        losses = estimate_loss()
        print(f"step {iteration:4d} | train loss {losses['train']:.4f} | val loss {losses['val']:.4f}")

    x, y = get_batch("train")
    logits, loss = model(x, y)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

# ── save checkpoint ───────────────────────────────────────────────────────────
checkpoint_path = os.path.join(train_cfg.checkpoint_dir, "base_model.pt")
torch.save({
    "model_state": model.state_dict(),
    "model_cfg": model_cfg,
    "train_cfg": train_cfg,
    "final_loss": loss.item(),
}, checkpoint_path)
print(f"Checkpoint saved to {checkpoint_path}")
