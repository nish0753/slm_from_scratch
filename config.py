from dataclasses import dataclass

@dataclass
class GPTConfig:
    vocab_size: int = 75
    block_size: int = 256
    n_layer: int = 6
    n_head: int = 6
    n_embd: int = 384
    dropout: float = 0.2

@dataclass
class TrainConfig:
    batch_size: int = 64
    max_iters: int = 5000
    learning_rate: float = 3e-4
    eval_interval: int = 500
    eval_iters: int = 200
    device: str = "cuda"
    data_dir: str = "data"
    checkpoint_dir: str = "checkpoints"
