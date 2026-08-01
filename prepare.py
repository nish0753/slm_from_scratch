import os
import re
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

with open(os.path.join(DATA_DIR, "input.txt"), "r", encoding="utf-8") as f:
    text = f.read()

# Remove Project Gutenberg license blocks wrapped in << >>
text = re.sub(r'<<.*?>>', '', text, flags=re.DOTALL)
# Strip brackets from stage directions but keep content
text = text.replace('[', '').replace(']', '')
# &c. / &C. → etc., remaining & → and
text = text.replace('&c.', 'etc.').replace('&C.', 'etc.')
text = text.replace('&', 'and')
# <Exit / <Exeunt style stage directions → strip the leading <
text = re.sub(r'<(\w)', r'\1', text)
# Scene markers: ACT_2|SC_7 → ACT 2 SC 7
text = text.replace('_', ' ').replace('|', ' ')
# Backtick typo and brace for joint speech
text = text.replace('`', '').replace('}', ' ')

chars = sorted(list(set(text)))
vocab_size = len(chars)
print(''.join(chars))
print(vocab_size)

stoi = {ch: i for i, ch in enumerate(chars)}
itos = {i: ch for i, ch in enumerate(chars)}

encode = lambda s: [stoi[c] for c in s]
decode = lambda l: "".join([itos[i] for i in l])

data = np.array(encode(text), dtype=np.uint16)
print(f"Total tokens: {len(data):,}")

n = int(0.9 * len(data))
train_data = data[:n]
val_data = data[n:]
print(f"Train tokens: {len(train_data):,}  |  Val tokens: {len(val_data):,}")

train_data.tofile(os.path.join(DATA_DIR, "train.bin"))
val_data.tofile(os.path.join(DATA_DIR, "val.bin"))
print("Saved train.bin and val.bin")
