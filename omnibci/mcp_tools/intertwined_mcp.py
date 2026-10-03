"""
Paper2Agent MCP Tool: Duggento, De Lorenzo, et al. (2022) Intertwined Neural Network
Reference:
- Duggento, A., De Lorenzo, M., Bargione, S., Conti, A., Catrambone, V., Valenza, G., & Toschi, N. (2022).
  "An intertwined neural network model for EEG classification in brain-computer interfaces".
  arXiv:2208.08860 [eess.SP]. DOI: 10.48550/arXiv.2208.08860
GitHub: https://github.com/andreaduggento/EEG_intertwined_architecture

Key architectural stages:
1. Time-Distributed Fully Connected (tdFC):
   - Spatial projection across electrode channels at each time step.
   - Learns linear spatial filters directly from raw or filtered montage.
   - Followed by Batch Normalization and non-linear activation (ELU/LeakyReLU).
2. Space-Distributed 1D Temporal Convolutions (sdConv):
   - Convolutions applied along the time axis for each spatial feature.
   - Extracts sensorimotor oscillatory dynamics (mu/beta rhythms).
   - Batch Normalization, non-linear activation, and temporal pooling.
3. Temporal Reduction & Classification Head:
   - Global temporal pooling or recurrent aggregation across sequence steps.
   - Dense projection layer to 2-class motor intention output ('rest' vs 'move').
"""

import numpy as np
from typing import Dict, Any, Tuple, Optional
import os

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import TensorDataset, DataLoader
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


if TORCH_AVAILABLE:
    class IntertwinedEEGNetPyTorch(nn.Module):
        """
        PyTorch implementation of the Intertwined Neural Network architecture
        (Duggento, De Lorenzo, et al., arXiv:2208.08860).
        Intertwines time-distributed spatial projections (tdFC) and
        space-distributed 1D temporal convolutions (sdConv).
        """
        def __init__(
            self,
            n_classes: int = 2,
            n_channels: int = 8,
            n_samples: int = 1000,
            td_units: int = 16,
            sd_filters: int = 16,
            sd_kernel: int = 63,
            pool_size: int = 8,
            dropout_rate: float = 0.25
        ):
            super().__init__()
            self.n_classes = n_classes
            self.n_channels = n_channels
            self.n_samples = n_samples

            # 1. Block 1: Time-Distributed Fully Connected (tdFC 0)
            # Implemented as 1x1 Conv along channels or linear per time-step
            self.tdFC1 = nn.Conv1d(n_channels, td_units, kernel_size=1, bias=False)
            self.bn_td1 = nn.BatchNorm1d(td_units)
            self.act_td1 = nn.ELU()

            # 2. Block 1: Space-Distributed Temporal Convolution (sdConv 0)
            # Depthwise temporal convolution across channels
            self.sdConv1 = nn.Conv1d(
                td_units,
                sd_filters,
                kernel_size=sd_kernel,
                padding=sd_kernel // 2,
                groups=1,
                bias=False
            )
            self.bn_sd1 = nn.BatchNorm1d(sd_filters)
            self.act_sd1 = nn.ELU()
            self.pool1 = nn.AvgPool1d(kernel_size=pool_size, stride=pool_size)
            self.drop1 = nn.Dropout(dropout_rate)

            # 3. Block 2: Intertwined stage (tdFC 1 + sdConv 1)
            self.tdFC2 = nn.Conv1d(sd_filters, td_units, kernel_size=1, bias=False)
            self.bn_td2 = nn.BatchNorm1d(td_units)
            self.act_td2 = nn.ELU()

            self.sdConv2 = nn.Conv1d(
                td_units,
                sd_filters * 2,
                kernel_size=31,
                padding=15,
                bias=False
            )
            self.bn_sd2 = nn.BatchNorm1d(sd_filters * 2)
            self.act_sd2 = nn.ELU()
            self.pool2 = nn.AvgPool1d(kernel_size=4, stride=4)
            self.drop2 = nn.Dropout(dropout_rate)

            # Global Temporal Pooling (as in intertwined.py when LSnum[0] == 0)
            self.global_pool = nn.AdaptiveAvgPool1d(1)
            self.classifier = nn.Sequential(
                nn.Linear(sd_filters * 2, 32),
                nn.ELU(),
                nn.Dropout(dropout_rate),
                nn.Linear(32, n_classes)
            )

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            # x shape: (batch_size, channels, time_samples)
            # Block 1
            x = self.act_td1(self.bn_td1(self.tdFC1(x)))
            x = self.drop1(self.pool1(self.act_sd1(self.bn_sd1(self.sdConv1(x)))))

            # Block 2 (intertwined)
            x = self.act_td2(self.bn_td2(self.tdFC2(x)))
            x = self.drop2(self.pool2(self.act_sd2(self.bn_sd2(self.sdConv2(x)))))

            # Global aggregation
            x = self.global_pool(x).squeeze(-1)
            return self.classifier(x)


def train_and_eval_intertwined(
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
    Paper2Agent MCP Tool: Trains and evaluates the Intertwined Neural Network
    (Duggento & De Lorenzo et al., 2022) on cross-subject EEG data.
    """
    n_trials, n_channels, n_samples = X_train.shape

    if not TORCH_AVAILABLE:
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import accuracy_score, cohen_kappa_score, roc_auc_score

        feats_tr = np.mean(X_train**2, axis=2)
        feats_te = np.mean(X_test**2, axis=2)
        clf = LogisticRegression().fit(feats_tr, y_train)
        preds = clf.predict(feats_te)
        probs = clf.predict_proba(feats_te)[:, 1]

        return {
            "model_name": "Intertwined_Simulation_Fallback",
            "accuracy": float(accuracy_score(y_test, preds)),
            "cohen_kappa": float(cohen_kappa_score(y_test, preds)),
            "roc_auc": float(roc_auc_score(y_test, probs)),
            "false_positive_rate": float(np.mean(preds[y_test == 0] == 1)),
            "predictions": preds.tolist(),
            "probabilities": probs.tolist()
        }

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = IntertwinedEEGNetPyTorch(
        n_classes=2,
        n_channels=n_channels,
        n_samples=n_samples,
        td_units=16,
        sd_filters=16,
        sd_kernel=63,
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

    t_X_tr = torch.tensor(X_train_norm, dtype=torch.float32)
    t_y_tr = torch.tensor(y_train, dtype=torch.long)
    t_X_te = torch.tensor(X_test_norm, dtype=torch.float32).to(device)

    dataset = TensorDataset(t_X_tr, t_y_tr)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-4)

    model.train()
    for ep in range(epochs):
        for bx, by in loader:
            bx, by = bx.to(device), by.to(device)
            optimizer.zero_grad()
            out = model(bx)
            loss = criterion(out, by)
            loss.backward()
            optimizer.step()

    model.eval()
    with torch.no_grad():
        test_logits = model(t_X_te)
        test_probs = torch.softmax(test_logits, dim=1)[:, 1].cpu().numpy()
        test_preds = torch.argmax(test_logits, dim=1).cpu().numpy()

    from sklearn.metrics import accuracy_score, cohen_kappa_score, roc_auc_score

    acc = float(accuracy_score(y_test, test_preds))
    kappa = float(cohen_kappa_score(y_test, test_preds))
    try:
        auc = float(roc_auc_score(y_test, test_probs))
    except Exception:
        auc = 0.5

    rest_idx = np.where(y_test == 0)[0]
    fpr = float(np.mean(test_preds[rest_idx] == 1)) if len(rest_idx) > 0 else 0.0

    return {
        "model_name": "Intertwined_NN_Duggento2022",
        "accuracy": round(acc, 4),
        "cohen_kappa": round(kappa, 4),
        "roc_auc": round(auc, 4),
        "false_positive_rate": round(fpr, 4),
        "predictions": test_preds.tolist(),
        "probabilities": test_probs.tolist()
    }
