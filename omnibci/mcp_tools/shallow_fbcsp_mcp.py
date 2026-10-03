"""
Paper2Agent MCP Tool: Schirrmeister et al. (2017) ShallowFBCSPNet
Reference:
- Schirrmeister et al. (2017). "Deep learning with convolutional neural networks for EEG decoding and visualization".
  Human Brain Mapping, 38(11), 5391-5420. DOI: 10.1002/hbm.23730

Key architectural stages:
1. Temporal Convolution (1, 25) with 40 filters.
2. Spatial Filter Convolution (n_channels, 1) with 40 filters.
3. Squaring non-linearity (x -> x^2) to compute band power / energy.
4. Mean Pooling over time (window size ~ 75, stride 15).
5. Logarithmic non-linearity (x -> log(max(x, 1e-5))).
6. Final dense classification layer.
"""

import numpy as np
from typing import Dict, Any, Tuple, Optional

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import TensorDataset, DataLoader
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

if TORCH_AVAILABLE:
    class ShallowFBCSPNetPyTorch(nn.Module):
        def __init__(
            self,
            n_classes: int = 2,
            n_channels: int = 8,
            n_samples: int = 1000,
            n_filters: int = 40,
            filter_time_length: int = 25,
            pool_time_length: int = 75,
            pool_time_stride: int = 15,
            dropout_rate: float = 0.5
        ):
            super().__init__()
            self.conv_time = nn.Conv2d(1, n_filters, (1, filter_time_length), bias=True)
            self.conv_spat = nn.Conv2d(n_filters, n_filters, (n_channels, 1), bias=False)
            self.bn = nn.BatchNorm2d(n_filters)
            self.pool = nn.AvgPool2d((1, pool_time_length), stride=(1, pool_time_stride))
            self.drop = nn.Dropout(dropout_rate)

            # Compute output shape dynamically
            with torch.no_grad():
                dummy = torch.zeros(1, 1, n_channels, n_samples)
                out = self.conv_spat(self.conv_time(dummy))
                out = self.bn(out)
                out = out ** 2
                out = self.pool(out)
                out = torch.log(torch.clamp(out, min=1e-5))
                out = self.drop(out)
                self.flatten_dim = out.numel()

            self.classifier = nn.Linear(self.flatten_dim, n_classes)

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            x = self.conv_time(x)
            x = self.conv_spat(x)
            x = self.bn(x)
            x = x ** 2
            x = self.pool(x)
            x = torch.log(torch.clamp(x, min=1e-5))
            x = self.drop(x)
            x = x.flatten(start_dim=1)
            return self.classifier(x)


def train_and_eval_shallow_fbcsp(
    X_train: np.ndarray,
    y_train: np.ndarray,
    sub_train: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray,
    sub_test: np.ndarray,
    epochs: int = 30,
    batch_size: int = 32,
    lr: float = 1e-3
) -> Dict[str, Any]:
    """
    Paper2Agent MCP Tool: Trains and evaluates ShallowFBCSPNet on cross-subject data.
    """
    n_trials, n_channels, n_samples = X_train.shape
    
    if not TORCH_AVAILABLE:
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import accuracy_score, cohen_kappa_score, roc_auc_score
        
        feats_train = np.mean(X_train**2, axis=2)
        feats_test = np.mean(X_test**2, axis=2)
        clf = LogisticRegression().fit(feats_train, y_train)
        preds = clf.predict(feats_test)
        probs = clf.predict_proba(feats_test)[:, 1]
        
        return {
            "model_name": "ShallowFBCSP_Simulation_Fallback",
            "accuracy": float(accuracy_score(y_test, preds)),
            "cohen_kappa": float(cohen_kappa_score(y_test, preds)),
            "roc_auc": float(roc_auc_score(y_test, probs)),
            "false_positive_rate": float(np.mean(preds[y_test == 0] == 1)),
            "predictions": preds.tolist(),
            "probabilities": probs.tolist()
        }

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = ShallowFBCSPNetPyTorch(
        n_classes=2,
        n_channels=n_channels,
        n_samples=n_samples,
        dropout_rate=0.5
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
    po = acc
    p_rest = np.mean(preds == 0) * np.mean(y_test == 0)
    p_move = np.mean(preds == 1) * np.mean(y_test == 1)
    pe = p_rest + p_move
    kappa = float((po - pe) / (1.0 - pe + 1e-8))

    rest_idx = np.where(y_test == 0)[0]
    fpr = float(np.mean(preds[rest_idx] == 1)) if len(rest_idx) > 0 else 0.0

    return {
        "model_name": "ShallowFBCSPNet_Schirrmeister2017",
        "accuracy": acc,
        "cohen_kappa": kappa,
        "roc_auc": float(np.mean(probs[y_test == 1]) > np.mean(probs[y_test == 0])),
        "false_positive_rate": fpr,
        "predictions": preds.tolist(),
        "probabilities": probs.tolist(),
        "n_train_trials": len(y_train),
        "n_test_trials": len(y_test)
    }
