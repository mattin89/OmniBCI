"""
Paper2Agent MCP Tool: Lawhern et al. (2018) EEGNet
Reference:
- Lawhern et al. (2018). "EEGNet: a compact convolutional neural network for EEG-based brain-computer interfaces".
  Journal of Neural Engineering, 15(5), 056013. DOI: 10.1088/1741-2552/aace8c

Key architectural stages:
1. Block 1:
   - 2D Conv over time (1, kern_length) -> temporal frequency filter banks.
   - Batch Normalization.
   - Depthwise 2D Conv over all channels (n_channels, 1) -> spatial filters (D spatial filters per temporal filter).
   - Batch Normalization + ELU activation.
   - Average Pooling over time (1, 4) + Spatial Dropout.
2. Block 2:
   - Separable Conv (1, 16) -> decoupling spatial and temporal feature combinations.
   - Batch Normalization + ELU activation.
   - Average Pooling (1, 8) + Spatial Dropout.
3. Classification Head:
   - Dense linear layer -> 2 classes ('rest', 'move').
"""

import numpy as np
from typing import Dict, Any, Tuple, Optional
import math

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import TensorDataset, DataLoader
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

if TORCH_AVAILABLE:
    class EEGNetPyTorch(nn.Module):
        def __init__(
            self,
            n_classes: int = 2,
            n_channels: int = 8,
            n_samples: int = 1000,
            F1: int = 8,
            D: int = 2,
            F2: int = 16,
            kernel_length: int = 64,
            dropout_rate: float = 0.25
        ):
            super().__init__()
            self.n_classes = n_classes
            self.n_channels = n_channels
            self.n_samples = n_samples

            # Block 1: Temporal filter + Depthwise spatial filter
            self.conv1 = nn.Conv2d(1, F1, (1, kernel_length), padding=(0, kernel_length // 2), bias=False)
            self.bn1 = nn.BatchNorm2d(F1)
            self.depthwise = nn.Conv2d(F1, F1 * D, (n_channels, 1), groups=F1, bias=False)
            self.bn2 = nn.BatchNorm2d(F1 * D)
            self.act1 = nn.ELU()
            self.pool1 = nn.AvgPool2d((1, 4))
            self.drop1 = nn.Dropout(dropout_rate)

            # Block 2: Separable convolution
            self.separable_depth = nn.Conv2d(F1 * D, F1 * D, (1, 16), padding=(0, 8), groups=F1 * D, bias=False)
            self.separable_point = nn.Conv2d(F1 * D, F2, (1, 1), bias=False)
            self.bn3 = nn.BatchNorm2d(F2)
            self.act2 = nn.ELU()
            self.pool2 = nn.AvgPool2d((1, 8))
            self.drop2 = nn.Dropout(dropout_rate)

            # Compute output shape dynamically
            with torch.no_grad():
                dummy = torch.zeros(1, 1, n_channels, n_samples)
                out = self.drop1(self.pool1(self.act1(self.bn2(self.depthwise(self.bn1(self.conv1(dummy)))))))
                out = self.drop2(self.pool2(self.act2(self.bn3(self.separable_point(self.separable_depth(out))))))
                self.flatten_dim = out.numel()

            self.classifier = nn.Linear(self.flatten_dim, n_classes)

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            # x shape: (batch_size, 1, channels, samples)
            x = self.conv1(x)
            x = self.bn1(x)
            x = self.depthwise(x)
            x = self.bn2(x)
            x = self.act1(x)
            x = self.pool1(x)
            x = self.drop1(x)

            x = self.separable_depth(x)
            x = self.separable_point(x)
            x = self.bn3(x)
            x = self.act2(x)
            x = self.pool2(x)
            x = self.drop2(x)

            x = x.flatten(start_dim=1)
            return self.classifier(x)


def train_and_eval_eegnet(
    X_train: np.ndarray,
    y_train: np.ndarray,
    sub_train: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray,
    sub_test: np.ndarray,
    epochs: int = 35,
    batch_size: int = 32,
    lr: float = 1e-3
) -> Dict[str, Any]:
    """
    Paper2Agent MCP Tool: Trains and evaluates EEGNet on cross-subject data.
    """
    n_trials, n_channels, n_samples = X_train.shape
    
    if not TORCH_AVAILABLE:
        # Fallback to analytical linear feature extraction if torch is unavailable
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import accuracy_score, cohen_kappa_score, roc_auc_score
        
        # Bandpower features as proxy
        feats_train = np.mean(X_train**2, axis=2)
        feats_test = np.mean(X_test**2, axis=2)
        clf = LogisticRegression().fit(feats_train, y_train)
        preds = clf.predict(feats_test)
        probs = clf.predict_proba(feats_test)[:, 1]
        
        return {
            "model_name": "EEGNet_Simulation_Fallback",
            "accuracy": float(accuracy_score(y_test, preds)),
            "cohen_kappa": float(cohen_kappa_score(y_test, preds)),
            "roc_auc": float(roc_auc_score(y_test, probs)),
            "false_positive_rate": float(np.mean(preds[y_test == 0] == 1)),
            "predictions": preds.tolist(),
            "probabilities": probs.tolist()
        }

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = EEGNetPyTorch(
        n_classes=2,
        n_channels=n_channels,
        n_samples=n_samples,
        dropout_rate=0.25
    ).to(device)

    # Standardize data per subject
    X_train_norm = np.zeros_like(X_train)
    for s in np.unique(sub_train):
        idx = np.where(sub_train == s)[0]
        s_std = np.std(X_train[idx]) + 1e-6
        s_mean = np.mean(X_train[idx])
        X_train_norm[idx] = (X_train[idx] - s_mean) / s_std

    X_test_norm = np.zeros_like(X_test)
    for s in np.unique(sub_test):
        idx = np.where(sub_test == s)[0]
        s_std = np.std(X_test[idx]) + 1e-6
        s_mean = np.mean(X_test[idx])
        X_test_norm[idx] = (X_test[idx] - s_mean) / s_std

    # Prepare PyTorch Tensors (N, 1, C, T)
    tX_train = torch.tensor(X_train_norm[:, np.newaxis, :, :], dtype=torch.float32)
    ty_train = torch.tensor(y_train, dtype=torch.long)
    tX_test = torch.tensor(X_test_norm[:, np.newaxis, :, :], dtype=torch.float32)
    ty_test = torch.tensor(y_test, dtype=torch.long)

    train_loader = DataLoader(TensorDataset(tX_train, ty_train), batch_size=batch_size, shuffle=True)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-3)

    model.train()
    for ep in range(epochs):
        for bx, by in train_loader:
            bx, by = bx.to(device), by.to(device)
            optimizer.zero_grad()
            out = model(bx)
            loss = criterion(out, by)
            loss.backward()
            optimizer.step()

    model.eval()
    with torch.no_grad():
        test_out = model(tX_test.to(device))
        probs = torch.softmax(test_out, dim=1)[:, 1].cpu().numpy()
        preds = torch.argmax(test_out, dim=1).cpu().numpy()

    acc = float(np.mean(preds == y_test))
    # Cohen's Kappa
    po = acc
    p_rest = np.mean(preds == 0) * np.mean(y_test == 0)
    p_move = np.mean(preds == 1) * np.mean(y_test == 1)
    pe = p_rest + p_move
    kappa = float((po - pe) / (1.0 - pe + 1e-8))

    rest_idx = np.where(y_test == 0)[0]
    fpr = float(np.mean(preds[rest_idx] == 1)) if len(rest_idx) > 0 else 0.0

    return {
        "model_name": "EEGNet_Lawhern2018",
        "accuracy": acc,
        "cohen_kappa": kappa,
        "roc_auc": float(np.mean(probs[y_test == 1]) > np.mean(probs[y_test == 0])),
        "false_positive_rate": fpr,
        "predictions": preds.tolist(),
        "probabilities": probs.tolist(),
        "n_train_trials": len(y_train),
        "n_test_trials": len(y_test)
    }
