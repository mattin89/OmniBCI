"""
Kaggle UK BCI Consortium Dataset Loader and Harmonization Engine.
Competition: Low Cost Motor Imagery Decoding for Rehab (Cross Subject)

Implements:
1. Loading raw CSV streams (synchronized Lab Streaming Layer data).
2. Butterworth Bandpass filtering (8-30 Hz) + Notch filter (50 Hz).
3. Subject grouping and Leave-One-Subject-Out (LOSO) cross-validation folds.
4. Exporting test predictions to submission.csv format (ID, target).
"""

import os
import glob
import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt, iirnotch
from typing import Dict, List, Tuple, Generator, Optional
from .mock_benchmark_generator import create_full_benchmark_dataset, CHANNELS, SFREQ

def apply_butterworth_bandpass(
    data: np.ndarray,
    lowcut: float = 8.0,
    highcut: float = 30.0,
    fs: float = 250.0,
    order: int = 4
) -> np.ndarray:
    """
    Applies zero-phase forward-backward Butterworth bandpass filter.
    data shape: (..., n_samples)
    """
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data, axis=-1)

def apply_notch_filter(
    data: np.ndarray,
    notch_freq: float = 50.0,
    fs: float = 250.0,
    Q: float = 30.0
) -> np.ndarray:
    """
    Applies notch filter to remove power line hum (50 Hz or 60 Hz).
    """
    b, a = iirnotch(notch_freq, Q, fs)
    return filtfilt(b, a, data, axis=-1)

def preprocess_eeg_trials(
    X: np.ndarray,
    fs: float = 250.0,
    bandpass: Tuple[float, float] = (8.0, 30.0),
    notch: Optional[float] = 50.0
) -> np.ndarray:
    """
    Full preprocessing pipeline for raw EEG epochs:
    (n_trials, n_channels, n_samples)
    """
    X_filt = X.copy()
    if notch:
        X_filt = apply_notch_filter(X_filt, notch_freq=notch, fs=fs)
    if bandpass:
        X_filt = apply_butterworth_bandpass(X_filt, lowcut=bandpass[0], highcut=bandpass[1], fs=fs)
    return X_filt

class KaggleBCIDataLoader:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.train_csv = os.path.join(data_dir, "train.csv")
        self.test_csv = os.path.join(data_dir, "test.csv")
        self.ensure_dataset()

    def ensure_dataset(self):
        """
        Verifies dataset files exist; if not present, generates the 17-subject benchmark dataset.
        """
        if not os.path.exists(self.train_csv) or not os.path.exists(self.test_csv):
            print(f"[KaggleDataLoader] Dataset not found in {self.data_dir}. Generating benchmark dataset...")
            create_full_benchmark_dataset(self.data_dir, n_subjects=17)

    def load_all_trials(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Loads all raw trials from .npz or CSV.
        Returns:
            X: (N, channels, samples)
            y: (N,) integers (0: 'rest', 1: 'move')
            subjects: (N,) integer subject IDs
            trial_ids: (N,) string identifiers
        """
        npz_files = sorted(glob.glob(os.path.join(self.data_dir, "sub_*_raw.npz")))
        
        all_X = []
        all_y = []
        all_subs = []
        all_ids = []
        
        for file in npz_files:
            sub_id = int(os.path.basename(file).split("_")[1])
            data = np.load(file)
            X_sub = data["X"]
            y_sub = data["y"]
            ids_sub = data["trial_ids"]
            
            all_X.append(X_sub)
            all_y.append(y_sub)
            all_subs.append(np.full(len(y_sub), sub_id, dtype=int))
            all_ids.append(ids_sub)
            
        X = np.concatenate(all_X, axis=0)
        y = np.concatenate(all_y, axis=0)
        subjects = np.concatenate(all_subs, axis=0)
        trial_ids = np.concatenate(all_ids, axis=0)
        
        # Preprocess signals with bandpass filter
        X_clean = preprocess_eeg_trials(X, fs=SFREQ)
        return X_clean, y, subjects, trial_ids

    def get_loso_splits(self) -> Generator[Tuple[np.ndarray, np.ndarray, int], None, None]:
        """
        Yields (train_indices, test_indices, held_out_subject_id)
        for Leave-One-Subject-Out cross-validation across all subjects.
        """
        _, _, subjects, _ = self.load_all_trials()
        unique_subs = np.unique(subjects)
        
        for held_out in unique_subs:
            train_idx = np.where(subjects != held_out)[0]
            test_idx = np.where(subjects == held_out)[0]
            yield train_idx, test_idx, int(held_out)

    def create_submission(self, test_trial_ids: List[str], predictions: List[int], output_path: str):
        """
        Writes official Kaggle submission CSV file:
        ID,target
        sub_14_trial_000,rest
        sub_14_trial_001,move
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        target_labels = ["rest" if p == 0 else "move" for p in predictions]
        df = pd.DataFrame({
            "ID": test_trial_ids,
            "target": target_labels
        })
        df.to_csv(output_path, index=False)
        print(f"[KaggleDataLoader] Submission written to {output_path} ({len(df)} rows)")
        return output_path
