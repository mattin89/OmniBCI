"""
Omnigent Specialist Agent: Sandbox Experiment Runner & Verifier
Responsibility:
Coordinates training and evaluation of registered Paper2Agent MCP tools
on the Kaggle dataset under Leave-One-Subject-Out (LOSO) cross-validation.
"""

from typing import Dict, List, Any
import numpy as np
import time
import os
from ..data.kaggle_loader import KaggleBCIDataLoader
from ..mcp_tools import MCP_REGISTRY

class ExperimentRunnerAgent:
    def __init__(self, data_dir: str):
        self.loader = KaggleBCIDataLoader(data_dir=data_dir)

    def run_benchmark(self, models: List[str] = None) -> Dict[str, Any]:
        """
        Executes complete LOSO cross-validation for specified models.
        """
        if models is None:
            models = ["riemannian_ea", "eegnet", "shallow_fbcsp"]
            
        X, y, subjects, trial_ids = self.loader.load_all_trials()
        unique_subs = np.unique(subjects)
        
        benchmark_results = {}

        for model_key in models:
            if model_key not in MCP_REGISTRY:
                print(f"[ExperimentRunner] Warning: {model_key} not in MCP registry. Skipping.")
                continue
                
            tool_meta = MCP_REGISTRY[model_key]
            runner_fn = tool_meta["runner"]
            
            print(f"\n[ExperimentRunner] >>> Evaluating MCP Tool: '{tool_meta['title']}' ({model_key}) across {len(unique_subs)} subjects...")
            
            sub_accuracies = []
            sub_kappas = []
            sub_fprs = []
            fold_latencies = []
            all_test_preds = {}

            t0 = time.time()
            for held_out in unique_subs:
                train_idx = np.where(subjects != held_out)[0]
                test_idx = np.where(subjects == held_out)[0]
                
                X_tr, y_tr, sub_tr = X[train_idx], y[train_idx], subjects[train_idx]
                X_te, y_te, sub_te = X[test_idx], y[test_idx], subjects[test_idx]
                
                t_fold_start = time.time()
                res = runner_fn(X_tr, y_tr, sub_tr, X_te, y_te, sub_te)
                t_fold_elapsed = time.time() - t_fold_start
                
                sub_accuracies.append(res["accuracy"])
                sub_kappas.append(res["cohen_kappa"])
                sub_fprs.append(res["false_positive_rate"])
                fold_latencies.append(t_fold_elapsed)
                
                # Store test trial predictions
                for tid, p in zip(trial_ids[test_idx], res["predictions"]):
                    all_test_preds[tid] = p
                    
                print(f"  Fold Sub-{held_out:02d}: Acc={res['accuracy']:.3f} | Kappa={res['cohen_kappa']:.3f} | FPR={res['false_positive_rate']:.3f}")

            total_runtime = time.time() - t0
            mean_acc = float(np.mean(sub_accuracies))
            std_acc = float(np.std(sub_accuracies))
            mean_kappa = float(np.mean(sub_kappas))
            mean_fpr = float(np.mean(sub_fprs))
            mean_lat_ms = float(np.mean(fold_latencies) / len(test_idx) * 1000)

            benchmark_results[model_key] = {
                "model_key": model_key,
                "title": tool_meta["title"],
                "category": tool_meta["category"],
                "mean_accuracy": round(mean_acc, 4),
                "std_accuracy": round(std_acc, 4),
                "mean_cohen_kappa": round(mean_kappa, 4),
                "mean_false_positive_rate": round(mean_fpr, 4),
                "mean_latency_ms": round(mean_lat_ms, 2),
                "per_subject_accuracy": [round(a, 4) for a in sub_accuracies],
                "total_runtime_seconds": round(total_runtime, 2),
                "all_test_predictions": all_test_preds
            }
            print(f"[ExperimentRunner] Completed {model_key}: Mean Acc = {mean_acc*100:.2f}% (+/- {std_acc*100:.2f}%)")

        return benchmark_results

    def generate_kaggle_submission(self, best_model_key: str, results: Dict[str, Any], output_path: str) -> str:
        """
        Creates Kaggle submission CSV file for test subjects (sub_14, sub_15, sub_16).
        """
        best_preds = results[best_model_key]["all_test_predictions"]
        
        # Test trials
        test_tids = [tid for tid in best_preds.keys() if any(f"sub_{s:02d}" in tid for s in [14, 15, 16])]
        pred_labels = [best_preds[tid] for tid in test_tids]
        
        return self.loader.create_submission(test_tids, pred_labels, output_path)
