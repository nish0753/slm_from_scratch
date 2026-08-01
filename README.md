# 🧠 Small Language Model (SLM) from Scratch

A custom ~10.8M parameter **Decoder-only Transformer** (nanoGPT-style) implemented from scratch in **PyTorch**. This repository includes the complete model architecture, data cleaning and character tokenization pipeline, training loop with AdamW optimization, and an autoregressive text generation engine with temperature scaling.

---

## ✨ Features

- **Custom Decoder-Only Architecture**:
  - **Causal Self-Attention**: Multi-head self-attention with causal triangular masking to prevent attending to future tokens.
  - **Pre-LayerNorm Residual Connections**: Stable gradient flow across deep transformer layers.
  - **Feed-Forward Networks**: Expand-and-contract FFN using `GELU` non-linear activation.
  - **Weight Tying**: Shares parameters between the token embedding matrix and the output linear head (`lm_head`).
- **Data & Tokenization Pipeline**:
  - Regex-based text normalization and character-level encoding.
  - Efficient binary array serialization (`np.uint16`) into `.bin` files for high-throughput PyTorch dataset loading.
- **Training Engine**:
  - Optimizes with **AdamW** optimizer and tracks cross-entropy loss across training and validation splits.
  - Saves full checkpoint dictionaries (`model_state`, `model_cfg`, `train_cfg`, `final_loss`).
- **Autoregressive Text Generation**:
  - Temperature-scaled multinomial sampling for controllable output creativity.

---

## 🏗️ Model & Training Specifications

| Parameter | Value |
| :--- | :--- |
| **Model Parameters** | ~10.8 Million |
| **Embedding Dimension (`n_embd`)** | 384 |
| **Attention Heads (`n_head`)** | 6 (64 dimensions/head) |
| **Transformer Layers (`n_layer`)** | 6 |
| **Context Window (`block_size`)** | 256 tokens |
| **Vocabulary Size (`vocab_size`)** | 75 (character-level) |
| **Training Steps (`max_iters`)** | 5,000 |
| **Batch Size (`batch_size`)** | 64 |
| **Optimizer** | AdamW (`lr=3e-4`) |

---

## 📁 Repository Structure

```
slm_from_scratch/
├── config.py           # Dataclasses defining model and training hyper-parameters
├── model.py            # PyTorch implementation of GPT architecture & blocks
├── prepare.py          # Data cleaning, tokenizer, and binary dataset splitting
├── train.py            # Training loop, loss estimation, and checkpoint saving
├── generate.py         # Autoregressive text generation script
├── data/
│   └── input.txt       # Raw text dataset (Shakespeare corpus)
└── checkpoints/        # Saved model weights (.pt files)
```

---

## 🚀 Quick Start

### 1. Prerequisites & Dependencies

Ensure you have Python 3.9+ and PyTorch installed:

```bash
pip install torch numpy
```

### 2. Prepare the Dataset

Run the pre-processing script to clean the text corpus and generate `train.bin` and `val.bin`:

```bash
python prepare.py
```

### 3. Train the Model

Train the Small Language Model for 5,000 iterations:

```bash
python train.py
```

*The trained model checkpoint will be saved to `checkpoints/base_model.pt`.*

### 4. Generate Text

Generate text using the trained model checkpoint:

```bash
python generate.py
```

---

## 📜 License

MIT License. Free to use and modify for learning and projects.
