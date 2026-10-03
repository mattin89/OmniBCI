"""
Synthetic and Real Data Generator for Cross-Subject Motor Imagery EEG.
Simulates realistic 17-subject sensorimotor rhythm (SMR) dynamics matching
the UK BCI Consortium 'Low Cost Motor Imagery Decoding for Rehab' dataset.

Neurophysiology modeled:
- 8 channels: F3, F4, C3, Cz, C4, P3, P4, Oz
- Sampling rate: 250 Hz, epoch length: 4.0 seconds (1000 samples per trial)
- Rest state: Mu (9-11 Hz) and beta (18-22 Hz) oscillations over motor channels (C3, Cz, C4).
- Move state: Event-Related Desynchronization (ERD) with subject-specific noise floor.
- Realistic BCI Inefficiency / Noise: 20-30% of subjects exhibit weak ERD (BCI illiteracy / anatomical variation).
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple, List
import os

CHANNELS = ["F3", "F4", "C3", "Cz", "C4", "P3", "P4", "Oz"]
SFREQ = 250.0  # Hz
EPOCH_DURATION = 4.0  # seconds
N_SAMPLES = int(SFREQ * EPOCH_DURATION)  # 1000 samples

def generate_subject_eeg(
    subject_id: int,
    n_trials: int = 40,
    random_seed: int = 42
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Generates synthetic EEG trials for a single subject with realistic noise and ERD dynamics.
    """
    rng = np.random.RandomState(random_seed + subject_id * 177)
    time = np.linspace(0, EPOCH_DURATION, N_SAMPLES, endpoint=False)
    
    # Subject-specific baseline mu and beta frequencies
    mu_freq = rng.normal(10.2, 0.6)
    beta_freq = rng.normal(20.5, 1.2)
    
    # Subject-specific BCI responsiveness (some subjects have weak ERD, simulating BCI illiteracy)
    # Sub 3 and Sub 11 have weak ERD (simulating atypical stroke recovery or difficult anatomy)
    if subject_id in [3, 11]:
        erd_strength = rng.uniform(0.70, 0.85)  # only 15-30% suppression (hard to decode)
        noise_level = 2.4
    else:
        erd_strength = rng.uniform(0.35, 0.55)  # 45-65% suppression (standard responsive subject)
        noise_level = 1.6

    channel_scales = rng.uniform(0.8, 1.3, size=(len(CHANNELS), 1))
    
    # Random mixing matrix for volume conduction across the skull
    raw_mix = rng.normal(0, 0.35, size=(len(CHANNELS), len(CHANNELS)))
    np.fill_diagonal(raw_mix, 1.0)
    mixing = raw_mix @ raw_mix.T
    evals, evecs = np.linalg.eigh(mixing)
    mixing = evecs @ np.diag(np.sqrt(np.maximum(evals, 0.1))) @ evecs.T

    X_list = []
    y_list = []
    trial_ids = []

    # Balanced trials: half rest (0), half move (1)
    labels = np.array([0] * (n_trials // 2) + [1] * (n_trials - n_trials // 2))
    rng.shuffle(labels)

    for i, label in enumerate(labels):
        # 1. 1/f Pink background noise
        white = rng.normal(0, noise_level, size=(len(CHANNELS), N_SAMPLES))
        background = np.cumsum(white, axis=1) * 0.08 + white * 0.8

        # 2. Sensorimotor Rhythms (SMR) in C3 (idx 2), Cz (idx 3), C4 (idx 4)
        c_indices = [2, 3, 4]
        current_erd = erd_strength if label == 1 else 1.0
        
        phase_mu = rng.uniform(0, 2 * np.pi, size=(len(CHANNELS), 1))
        phase_beta = rng.uniform(0, 2 * np.pi, size=(len(CHANNELS), 1))
        
        mu_wave = np.sin(2 * np.pi * mu_freq * time + phase_mu)
        beta_wave = 0.5 * np.sin(2 * np.pi * beta_freq * time + phase_beta)

        smr_signal = np.zeros((len(CHANNELS), N_SAMPLES))
        for c in c_indices:
            smr_signal[c, :] = (mu_wave[c, :] + beta_wave[c, :]) * current_erd * 2.0

        # Trial signal through volume conduction
        trial_raw = (mixing @ (background + smr_signal)) * channel_scales
        
        X_list.append(trial_raw.astype(np.float32))
        y_list.append(label)
        trial_ids.append(f"sub_{subject_id:02d}_trial_{i:03d}")

    X = np.stack(X_list, axis=0)
    y = np.array(y_list, dtype=int)
    trial_ids = np.array(trial_ids)
    
    return X, y, trial_ids

def create_full_benchmark_dataset(
    output_dir: str,
    n_subjects: int = 17,
    trials_per_subject: int = 40
) -> Dict[str, str]:
    os.makedirs(output_dir, exist_ok=True)
    
    train_records = []
    test_records = []
    gt_test_records = []
    
    for sub in range(n_subjects):
        X, y, t_ids = generate_subject_eeg(subject_id=sub, n_trials=trials_per_subject)
        is_test = (sub >= 14)
        
        for trial_idx in range(len(y)):
            tid = t_ids[trial_idx]
            label_str = "move" if y[trial_idx] == 1 else "rest"
            
            row = {
                "ID": tid,
                "subject": f"sub_{sub:02d}",
                "trial_index": trial_idx
            }
            for ch_idx, ch_name in enumerate(CHANNELS):
                ch_data = X[trial_idx, ch_idx, :]
                row[f"{ch_name}_mean"] = float(np.mean(ch_data))
                row[f"{ch_name}_std"] = float(np.std(ch_data))
                row[f"{ch_name}_pwr_mu"] = float(np.mean(ch_data**2))
            
            if not is_test:
                row["target"] = label_str
                train_records.append(row)
            else:
                test_records.append(row)
                gt_test_records.append({"ID": tid, "target": label_str})
                
        np.savez_compressed(
            os.path.join(output_dir, f"sub_{sub:02d}_raw.npz"),
            X=X, y=y, trial_ids=t_ids
        )

    train_df = pd.DataFrame(train_records)
    test_df = pd.DataFrame(test_records)
    gt_df = pd.DataFrame(gt_test_records)
    
    train_path = os.path.join(output_dir, "train.csv")
    test_path = os.path.join(output_dir, "test.csv")
    gt_path = os.path.join(output_dir, "ground_truth_test.csv")
    
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    gt_df.to_csv(gt_path, index=False)
    
    return {
        "train_csv": train_path,
        "test_csv": test_path,
        "gt_csv": gt_path,
        "data_dir": output_dir
    }
