"""
Module 3 — Step 3: Train a small LSTM to predict the next sensor reading.

Design choices and why they matter for an MCU target:
    - Keep the hidden size small (32). Every extra unit grows both the model
      and the per-step compute cost. On ESP32-S3 we have to fit in ~512 KB
      SRAM and run within the sensor's sampling period.
    - Single LSTM layer. Multiple stacked layers buy little for short windows
      and are much harder to keep fast on a microcontroller.
    - Final Linear maps the LSTM's last hidden state to one prediction per
      input channel (multi-output regression).
    - We log train and validation loss every epoch and keep the best
      validation checkpoint.

Outputs (models/):
    best_lstm.pt        - PyTorch state dict (used by the ONNX export step)
    training_curve.png  - quick visual sanity check
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


class SensorLSTM(nn.Module):
    """
    Input:  (batch, seq_len, num_features)
    Output: (batch, num_features) — predicted next-step value for every sensor.
    """

    def __init__(self, num_features: int, hidden_size: int = 32, num_layers: int = 1) -> None:
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=num_features,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
        )
        self.head = nn.Linear(hidden_size, num_features)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # TODO(Lab 3A): run the sequence through the LSTM, select the last
        # timestep, and map it to one next-step value per sensor channel.
        raise NotImplementedError("complete the LSTM forward pass")


def load_arrays(processed_dir: Path) -> dict[str, np.ndarray]:
    keys = ["X_train", "y_train", "X_val", "y_val", "X_test", "y_test"]
    return {k: np.load(processed_dir / f"{k}.npy") for k in keys}


def make_loader(X: np.ndarray, y: np.ndarray, batch_size: int, shuffle: bool, seed: int) -> DataLoader:
    ds = TensorDataset(torch.from_numpy(X), torch.from_numpy(y))
    generator = torch.Generator()
    generator.manual_seed(seed)
    return DataLoader(ds, batch_size=batch_size, shuffle=shuffle, drop_last=False, generator=generator)


def run_epoch(
    model: nn.Module,
    loader: DataLoader,
    loss_fn: nn.Module,
    optimizer: torch.optim.Optimizer | None,
    device: torch.device,
) -> float:
    # TODO(Lab 3A): implement one deterministic train/evaluation epoch. Average
    # by sample count, not by batch count, so the final short batch is weighted.
    raise NotImplementedError("complete the epoch runner")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--processed-dir", type=Path, default=root / "data" / "processed")
    parser.add_argument("--models-dir", type=Path, default=root / "models")
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--hidden-size", type=int, default=32)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    torch.use_deterministic_algorithms(True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    arrays = load_arrays(args.processed_dir)
    num_features = arrays["X_train"].shape[-1]
    print(f"num_features={num_features}, seq_len={arrays['X_train'].shape[1]}")

    train_loader = make_loader(arrays["X_train"], arrays["y_train"], args.batch_size, shuffle=True, seed=args.seed)
    val_loader = make_loader(arrays["X_val"], arrays["y_val"], args.batch_size, shuffle=False, seed=args.seed)

    model = SensorLSTM(num_features=num_features, hidden_size=args.hidden_size).to(device)
    loss_fn = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

    args.models_dir.mkdir(parents=True, exist_ok=True)
    best_val = float("inf")
    history: list[tuple[int, float, float]] = []

    for epoch in range(1, args.epochs + 1):
        train_loss = run_epoch(model, train_loader, loss_fn, optimizer, device)
        val_loss = run_epoch(model, val_loader, loss_fn, None, device)
        history.append((epoch, train_loss, val_loss))

        flag = ""
        if val_loss < best_val:
            best_val = val_loss
            torch.save(
                {
                    "state_dict": model.state_dict(),
                    "num_features": num_features,
                    "hidden_size": args.hidden_size,
                    "seq_len": arrays["X_train"].shape[1],
                },
                args.models_dir / "best_lstm.pt",
            )
            flag = "  <- best"
        print(f"Epoch {epoch:3d}/{args.epochs}  train={train_loss:.5f}  val={val_loss:.5f}{flag}")

    print(f"Best val loss: {best_val:.5f}")
    print(f"Saved best checkpoint to {args.models_dir / 'best_lstm.pt'}")

    epochs = [h[0] for h in history]
    train_losses = [h[1] for h in history]
    val_losses = [h[2] for h in history]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(epochs, train_losses, label="train")
    ax.plot(epochs, val_losses, label="val")
    ax.set_xlabel("epoch")
    ax.set_ylabel("MSE loss (normalized)")
    ax.set_title("LSTM training curve")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    out_png = args.models_dir / "training_curve.png"
    fig.savefig(out_png, dpi=120)
    print(f"Saved training curve to {out_png}")


if __name__ == "__main__":
    main()
