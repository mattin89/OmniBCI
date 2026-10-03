"""
Paper2Agent MCP Tool: Riemannian Geometry & Euclidean Alignment for Cross-Subject EEG
Reference:
- He & Wu (2019). "Transfer Learning for Brain-Computer Interfaces: A Euclidean Space Data Alignment Approach".
  IEEE Transactions on Biomedical Engineering, 67(2), 399-410. DOI: 10.1109/TBME.2019.2913914
- Barachant et al. (2012). "Multiclass Brain-Computer Interface Classification by Riemannian Geometry".
  IEEE TBME, 59(4), 920-928. DOI: 10.1109/TBME.2011.2172210

Functions exposed as Paper2Agent MCP tools:
1. align_euclidean(X, subject_indices): Aligns trial covariance matrices across subjects to eliminate domain shift.
2. compute_covariance_matrices(X): Computes regularized sample covariance matrices (OAS / Ledoit-Wolf).
3. project_tangent_space(covs, ref_cov=None): Projects symmetric positive-definite (SPD) matrices to Riemannian tangent space.
4. train_and_eval_riemannian_ea(X_train, y_train, sub_train, X_test, y_test, sub_test): Complete cross-subject pipeline.
"""

import numpy as np
from scipy.linalg import fractional_matrix_power, eigh
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, cohen_kappa_score, roc_auc_score
from typing import Dict, Any, Tuple, Optional

def compute_regularized_cov(X_trial: np.ndarray, reg: float = 1e-4) -> np.ndarray:
    """
    Computes sample covariance for a single trial (channels, time) with Tikhonov regularization.
    """
    n_channels, n_times = X_trial.shape
    # Center trial per channel
    X_centered = X_trial - np.mean(X_trial, axis=1, keepdims=True)
    cov = (X_centered @ X_centered.T) / (n_times - 1)
    # Regularization to ensure strict SPD
    cov += reg * np.eye(n_channels) * np.trace(cov) / n_channels
    return cov

def align_euclidean(X: np.ndarray, subject_ids: np.ndarray) -> np.ndarray:
    """
    Euclidean Space Data Alignment (EA).
    Aligns trials of each subject by whitening with the inverse square root of their mean covariance matrix:
    R_bar = (1/N) * sum_i (X_i * X_i^T)
    X_aligned = R_bar^(-1/2) * X_i
    """
    X_aligned = np.zeros_like(X)
    unique_subs = np.unique(subject_ids)
    
    for sub in unique_subs:
        idx = np.where(subject_ids == sub)[0]
        n_sub_trials = len(idx)
        if n_sub_trials == 0:
            continue
            
        # Compute mean covariance for subject
        n_channels = X.shape[1]
        R_bar = np.zeros((n_channels, n_channels))
        for i in idx:
            R_bar += compute_regularized_cov(X[i])
        R_bar /= n_sub_trials
        
        # Matrix square root inverse: R_bar^(-1/2)
        evals, evecs = eigh(R_bar)
        evals = np.maximum(evals, 1e-6)
        inv_sqrt = evecs @ np.diag(1.0 / np.sqrt(evals)) @ evecs.T
        
        for i in idx:
            X_aligned[i] = inv_sqrt @ X[i]
            
    return X_aligned

def riemannian_mean_cov(covs: np.ndarray, max_iter: int = 50, tol: float = 1e-5) -> np.ndarray:
    """
    Calculates the geometric Fréchet mean of SPD matrices under the Affine-Invariant Riemannian Metric (AIRM).
    """
    # Initialize with Euclidean mean
    P = np.mean(covs, axis=0)
    for _ in range(max_iter):
        evals, evecs = eigh(P)
        evals = np.maximum(evals, 1e-6)
        P_sqrt = evecs @ np.diag(np.sqrt(evals)) @ evecs.T
        P_inv_sqrt = evecs @ np.diag(1.0 / np.sqrt(evals)) @ evecs.T
        
        # Tangent space projection
        tangent_mean = np.zeros_like(P)
        for C in covs:
            C_proj = P_inv_sqrt @ C @ P_inv_sqrt
            c_evals, c_evecs = eigh(C_proj)
            c_evals = np.maximum(c_evals, 1e-6)
            log_C = c_evecs @ np.diag(np.log(c_evals)) @ c_evecs.T
            tangent_mean += log_C
        tangent_mean /= len(covs)
        
        # Step back onto manifold
        t_evals, t_evecs = eigh(tangent_mean)
        delta = P_sqrt @ (t_evecs @ np.diag(np.exp(t_evals)) @ t_evecs.T) @ P_sqrt
        
        if np.linalg.norm(delta - P) / np.linalg.norm(P) < tol:
            break
        P = delta
        
    return P

def project_tangent_space(covs: np.ndarray, ref_cov: Optional[np.ndarray] = None) -> Tuple[np.ndarray, np.ndarray]:
    """
    Projects a batch of SPD covariance matrices (N, C, C) into the Euclidean Tangent Space at ref_cov.
    Returns:
        features: shape (N, C*(C+1)//2)
        ref_cov: shape (C, C)
    """
    N, C, _ = covs.shape
    if ref_cov is None:
        ref_cov = riemannian_mean_cov(covs)
        
    evals, evecs = eigh(ref_cov)
    evals = np.maximum(evals, 1e-6)
    ref_inv_sqrt = evecs @ np.diag(1.0 / np.sqrt(evals)) @ evecs.T
    
    triu_idx = np.triu_indices(C)
    diag_mask = (triu_idx[0] == triu_idx[1])
    n_features = len(triu_idx[0])
    
    features = np.zeros((N, n_features))
    for i in range(N):
        C_proj = ref_inv_sqrt @ covs[i] @ ref_inv_sqrt
        c_evals, c_evecs = eigh(C_proj)
        c_evals = np.maximum(c_evals, 1e-6)
        log_C = c_evecs @ np.diag(np.log(c_evals)) @ c_evecs.T
        
        vec = log_C[triu_idx]
        # Weight off-diagonal elements by sqrt(2) to preserve Riemannian inner product norm
        vec[~diag_mask] *= np.sqrt(2.0)
        features[i] = vec
        
    return features, ref_cov

def train_and_eval_riemannian_ea(
    X_train: np.ndarray,
    y_train: np.ndarray,
    sub_train: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray,
    sub_test: np.ndarray
) -> Dict[str, Any]:
    """
    Executes the full Euclidean Alignment + Riemannian Tangent Space classification.
    """
    # 1. Apply Euclidean Alignment across training subjects
    X_train_aligned = align_euclidean(X_train, sub_train)
    # Apply Euclidean Alignment to test subjects (using their own mean covariance)
    X_test_aligned = align_euclidean(X_test, sub_test)
    
    # 2. Compute covariance matrices
    covs_train = np.stack([compute_regularized_cov(trial) for trial in X_train_aligned], axis=0)
    covs_test = np.stack([compute_regularized_cov(trial) for trial in X_test_aligned], axis=0)
    
    # 3. Project to Tangent Space anchored at training Riemannian mean
    feats_train, ref_mean = project_tangent_space(covs_train)
    feats_test, _ = project_tangent_space(covs_test, ref_cov=ref_mean)
    
    # 4. Train regularized classifier
    clf = LogisticRegression(C=1.0, max_iter=1000, random_state=42)
    clf.fit(feats_train, y_train)
    
    # 5. Evaluate
    preds = clf.predict(feats_test)
    probs = clf.predict_proba(feats_test)[:, 1]
    
    acc = float(accuracy_score(y_test, preds))
    kappa = float(cohen_kappa_score(y_test, preds))
    auc = float(roc_auc_score(y_test, probs)) if len(np.unique(y_test)) > 1 else 0.5
    
    # False positive rate (safety metric: predicting 'move' (1) when true is 'rest' (0))
    rest_idx = np.where(y_test == 0)[0]
    fpr = float(np.mean(preds[rest_idx] == 1)) if len(rest_idx) > 0 else 0.0

    return {
        "model_name": "Riemannian_EA_TangentSpace",
        "accuracy": acc,
        "cohen_kappa": kappa,
        "roc_auc": auc,
        "false_positive_rate": fpr,
        "predictions": preds.tolist(),
        "probabilities": probs.tolist(),
        "n_train_trials": len(y_train),
        "n_test_trials": len(y_test)
    }
