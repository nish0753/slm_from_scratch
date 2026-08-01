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

## 📐 System & Model Architecture Diagram

```mermaid
flowchart TD
    subgraph Data Pipeline ["1. Data Pipeline (prepare.py)"]
        RawText["Raw Text Corpus (data/input.txt)"] --> Preprocess["Text Normalization & Regex Cleaning"]
        Preprocess --> CharTokenizer["Character-Level Tokenizer (stoi / itos)"]
        CharTokenizer --> EncodedData["uint16 Token Array Serialization"]
        EncodedData --> SplitData["Train / Validation Split (90% / 10%)"]
        SplitData --> TrainBin["data/train.bin"]
        SplitData --> ValBin["data/val.bin"]
    end

    subgraph Training & Model Architecture ["2. Model Architecture & Forward Pass (model.py & train.py)"]
        InputTokens["Batch Token IDs [B, T]"] --> TokEmb["Token Embedding (vocab_size=75, n_embd=384)"]
        PosIndices["Position Indices [0..T-1]"] --> PosEmb["Position Embedding (block_size=256, n_embd=384)"]
        TokEmb --> AddEmb["Sum Embeddings + Dropout"]
        PosEmb --> AddEmb
        
        AddEmb --> BlockList["Transformer Stack (n_layer = 6 Blocks)"]
        
        subgraph TransformerBlock ["Transformer Block Structure (Block)"]
            direction TB
            InputX["Input Tensor [B, T, 384]"] --> LN1["LayerNorm 1"]
            LN1 --> MultiHeadAttn["Causal Self-Attention (6 Heads)\n[Q, K, V Projections + Triangular Mask]"]
            MultiHeadAttn --> Resid1["Residual Connection (+ InputX)"]
            Resid1 --> LN2["LayerNorm 2"]
            LN2 --> FFN["Feed-Forward Network\n[Linear(384 -> 1536) -> GELU -> Linear(1536 -> 384)]"]
            FFN --> Resid2["Residual Connection (+ Resid1)"]
        end
        
        BlockList --> FinalLN["Final LayerNorm (ln_f)"]
        FinalLN --> LMHead["Linear Output Head (lm_head)\n[Weight Tying with tok_emb]"]
        LMHead --> Logits["Logits [B, T, vocab_size]"]
        Logits --> LossCalc["Cross Entropy Loss Optimization"]
    end

    subgraph Inference Engine ["3. Inference Engine (generate.py)"]
        Prompt["Input Prompt String (e.g., 'ROMEO:')"] --> EncodePrompt["Encode to Token IDs"]
        EncodePrompt --> CondTokens["Crop to Context Window (block_size=256)"]
        CondTokens --> ForwardPass["Model Forward Pass"]
        ForwardPass --> TempScale["Temperature Scaling & Softmax"]
        TempScale --> Sample["Multinomial Probability Sampling"]
        Sample --> DecodeText["Decode Token ID to Character & Append"]
    end
```

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
