#!/usr/bin/env python3
"""
Train ML model for segmentation parameter prediction.

This script trains a RandomForest classifier on synthetic training data
and saves the trained model for use in the application.
"""

import sys
from pathlib import Path

import pandas as pd

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.ml.trainer import ModelTrainer


def main():
    """Train the ML model."""
    # Setup paths
    project_root = Path(__file__).parent.parent
    training_csv = project_root / "app" / "ml" / "models" / "training_data" / "synthetic_v1.csv"
    models_dir = project_root / "app" / "ml" / "models"
    
    print("=" * 60)
    print("ML Model Training")
    print("=" * 60)
    
    # Check if training data exists
    if not training_csv.exists():
        print(f"\nError: Training data not found at {training_csv}")
        print("Please run: python scripts/generate_training_data.py")
        sys.exit(1)
    
    # Load and inspect data
    print(f"\nLoading training data from {training_csv}")
    df = pd.read_csv(training_csv)
    
    print(f"\nDataset Info:")
    print(f"  Total samples: {len(df)}")
    print(f"  Features: {len([c for c in df.columns if c not in ['method', 'dice_score', 'iou_score', 'grow_T', 'morph_kernel']])}")
    print(f"  Methods: {df['method'].value_counts().to_dict()}")
    print(f"  Mean Dice: {df['dice_score'].mean():.3f}")
    print(f"  Mean IoU: {df['iou_score'].mean():.3f}")
    
    # Filter samples by quality (keep samples with dice > 0.3)
    print(f"\nFiltering samples (keeping dice_score > 0.3)...")
    df_filtered = df[df['dice_score'] > 0.3].copy()
    print(f"  Samples after filtering: {len(df_filtered)} ({len(df_filtered)/len(df)*100:.1f}%)")
    
    if len(df_filtered) < 100:
        print("\nWarning: Very few high-quality samples. Using all samples.")
        df_filtered = df
    
    # Save filtered data
    filtered_csv = training_csv.parent / "synthetic_v1_filtered.csv"
    df_filtered.to_csv(filtered_csv, index=False)
    print(f"  Saved filtered data to {filtered_csv}")
    
    # Train model
    print("\n" + "=" * 60)
    print("Training RandomForest Classifier")
    print("=" * 60)
    
    trainer = ModelTrainer(model_dir=models_dir)
    
    # Train with 80/20 train/test split
    # The trainer internally handles the split
    metrics = trainer.train_from_csv(
        csv_path=filtered_csv,
        test_size=0.2,
        random_state=42,
        use_xgboost=False  # Start with RandomForest only
    )
    
    print("\n" + "=" * 60)
    print("Training Results")
    print("=" * 60)
    print(f"  RandomForest Accuracy: {metrics['rf_accuracy']:.4f}")
    print(f"  Training samples: {metrics['train_samples']}")
    print(f"  Test samples: {metrics['test_samples']}")
    print(f"  Features used: {metrics['feature_count']}")
    
    # Show per-class performance
    if 'rf_report' in metrics:
        print("\n  Per-class Performance:")
        for method, scores in metrics['rf_report'].items():
            if isinstance(scores, dict) and 'f1-score' in scores:
                print(f"    {method}: F1={scores['f1-score']:.3f}, "
                      f"Precision={scores['precision']:.3f}, "
                      f"Recall={scores['recall']:.3f}")
    
    # Save model
    print("\n" + "=" * 60)
    print("Saving Model")
    print("=" * 60)
    
    version = "1.0.0"
    trainer.save_models(version=version, metrics=metrics)
    
    print("\n" + "=" * 60)
    print("Training Complete!")
    print("=" * 60)
    print(f"\nModel files saved in: {models_dir}")
    print(f"  - rf_v{version}.joblib (RandomForest classifier)")
    print(f"  - scaler_v{version}.joblib (Feature scaler)")
    print(f"  - metadata.json (Model metadata)")
    
    print("\nNext steps:")
    print("  1. Test the model: python scripts/test_model.py")
    print("  2. Integrate with API: Implement ML endpoints")
    print("  3. Add frontend UI for Smart and Click modes")


if __name__ == "__main__":
    main()
