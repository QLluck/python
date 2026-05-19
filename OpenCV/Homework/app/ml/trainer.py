"""
Model training module for ML-based segmentation.

Trains RandomForest and XGBoost models to predict optimal segmentation
method and parameters from image features.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False


class ModelTrainer:
    """
    Train ML models for segmentation parameter prediction.
    
    Supports:
    - RandomForest classifier for method prediction
    - XGBoost classifier (optional)
    - Feature scaling and normalization
    - Model evaluation and metrics
    """
    
    def __init__(self, model_dir: Optional[Path] = None):
        """
        Initialize model trainer.
        
        Args:
            model_dir: Directory to save trained models (default: app/ml/models/)
        """
        if model_dir is None:
            model_dir = Path(__file__).parent / "models"
        
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        self.scaler = StandardScaler()
        self.rf_classifier: Optional[RandomForestClassifier] = None
        self.xgb_classifier: Optional[xgb.XGBClassifier] = None
    
    def train_from_csv(
        self,
        csv_path: Path,
        test_size: float = 0.2,
        random_state: int = 42,
        use_xgboost: bool = False
    ) -> Dict:
        """
        Train models from CSV training data.
        
        Args:
            csv_path: Path to training data CSV
            test_size: Fraction of data to use for testing
            random_state: Random seed for reproducibility
            use_xgboost: Whether to train XGBoost model in addition to RandomForest
        
        Returns:
            Dictionary with training metrics and results
        """
        # Load data
        df = pd.read_csv(csv_path)
        
        # Separate features and labels
        feature_cols = [col for col in df.columns if col.startswith(('mean', 'std', 'min', 'max', 
                                                                      'median', 'entropy', 'skewness',
                                                                      'kurtosis', 'lbp_', 'glcm_',
                                                                      'edge_', 'gradient_', 'circularity',
                                                                      'compactness'))]
        
        if 'method' not in df.columns:
            raise ValueError("CSV must contain 'method' column with target labels")
        
        X = df[feature_cols].values
        y = df['method'].values
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train RandomForest
        print("Training RandomForest classifier...")
        self.rf_classifier = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=random_state,
            n_jobs=-1
        )
        self.rf_classifier.fit(X_train_scaled, y_train)
        
        # Evaluate RandomForest
        y_pred_rf = self.rf_classifier.predict(X_test_scaled)
        rf_accuracy = accuracy_score(y_test, y_pred_rf)
        print(f"RandomForest accuracy: {rf_accuracy:.4f}")
        print("\nRandomForest Classification Report:")
        print(classification_report(y_test, y_pred_rf))
        
        results = {
            "rf_accuracy": rf_accuracy,
            "rf_report": classification_report(y_test, y_pred_rf, output_dict=True),
            "train_samples": len(X_train),
            "test_samples": len(X_test),
            "feature_count": len(feature_cols),
        }
        
        # Train XGBoost if requested
        if use_xgboost and XGBOOST_AVAILABLE:
            print("\nTraining XGBoost classifier...")
            self.xgb_classifier = xgb.XGBClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=random_state,
                n_jobs=-1
            )
            self.xgb_classifier.fit(X_train_scaled, y_train)
            
            # Evaluate XGBoost
            y_pred_xgb = self.xgb_classifier.predict(X_test_scaled)
            xgb_accuracy = accuracy_score(y_test, y_pred_xgb)
            print(f"XGBoost accuracy: {xgb_accuracy:.4f}")
            print("\nXGBoost Classification Report:")
            print(classification_report(y_test, y_pred_xgb))
            
            results["xgb_accuracy"] = xgb_accuracy
            results["xgb_report"] = classification_report(y_test, y_pred_xgb, output_dict=True)
        
        return results
    
    def save_models(self, version: str = "1.0.0", metrics: Optional[Dict] = None) -> None:
        """
        Save trained models to disk.
        
        Args:
            version: Model version string (e.g., "1.0.0")
            metrics: Optional training metrics to save in metadata
        """
        if self.rf_classifier is None:
            raise ValueError("No RandomForest model trained. Call train_from_csv() first.")
        
        # Save RandomForest
        rf_path = self.model_dir / f"rf_v{version}.joblib"
        joblib.dump(self.rf_classifier, rf_path)
        print(f"Saved RandomForest model to {rf_path}")
        
        # Save XGBoost if available
        if self.xgb_classifier is not None:
            xgb_path = self.model_dir / f"xgb_v{version}.joblib"
            joblib.dump(self.xgb_classifier, xgb_path)
            print(f"Saved XGBoost model to {xgb_path}")
        
        # Save scaler
        scaler_path = self.model_dir / f"scaler_v{version}.joblib"
        joblib.dump(self.scaler, scaler_path)
        print(f"Saved feature scaler to {scaler_path}")
        
        # Save metadata
        metadata = {
            "version": version,
            "trained_date": datetime.now().isoformat(),
            "model_type": "RandomForest",
            "feature_count": self.rf_classifier.n_features_in_,
            "classes": self.rf_classifier.classes_.tolist(),
        }
        
        if metrics:
            metadata.update(metrics)
        
        metadata_path = self.model_dir / "metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"Saved metadata to {metadata_path}")
    
    def get_feature_importance(self, feature_names: list[str]) -> pd.DataFrame:
        """
        Get feature importance from trained RandomForest model.
        
        Args:
            feature_names: List of feature names
        
        Returns:
            DataFrame with features and their importance scores
        """
        if self.rf_classifier is None:
            raise ValueError("No model trained")
        
        importance = self.rf_classifier.feature_importances_
        df = pd.DataFrame({
            'feature': feature_names,
            'importance': importance
        })
        df = df.sort_values('importance', ascending=False)
        
        return df
    
    def cross_validate(
        self,
        X: np.ndarray,
        y: np.ndarray,
        cv: int = 5
    ) -> Dict[str, float]:
        """
        Perform cross-validation on the dataset.
        
        Args:
            X: Feature matrix
            y: Target labels
            cv: Number of cross-validation folds
        
        Returns:
            Dictionary with mean and std of accuracy scores
        """
        from sklearn.model_selection import cross_val_score
        
        if self.rf_classifier is None:
            self.rf_classifier = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Perform cross-validation
        scores = cross_val_score(
            self.rf_classifier,
            X_scaled,
            y,
            cv=cv,
            scoring='accuracy',
            n_jobs=-1
        )
        
        return {
            "mean_accuracy": float(scores.mean()),
            "std_accuracy": float(scores.std()),
            "scores": scores.tolist(),
        }


def train_initial_model(
    training_data_path: Path,
    output_dir: Path,
    version: str = "1.0.0",
    use_xgboost: bool = False
) -> None:
    """
    Convenience function to train and save initial model.
    
    Args:
        training_data_path: Path to training CSV file
        output_dir: Directory to save models
        version: Model version
        use_xgboost: Whether to train XGBoost model
    """
    trainer = ModelTrainer(model_dir=output_dir)
    
    print(f"Training models from {training_data_path}")
    print(f"Output directory: {output_dir}")
    print(f"Version: {version}")
    print("-" * 60)
    
    # Train models
    metrics = trainer.train_from_csv(
        training_data_path,
        test_size=0.2,
        random_state=42,
        use_xgboost=use_xgboost
    )
    
    # Save models
    trainer.save_models(version=version, metrics=metrics)
    
    print("-" * 60)
    print("Training complete!")
    print(f"RandomForest accuracy: {metrics['rf_accuracy']:.4f}")
    if 'xgb_accuracy' in metrics:
        print(f"XGBoost accuracy: {metrics['xgb_accuracy']:.4f}")


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python trainer.py <training_data.csv> [version]")
        sys.exit(1)
    
    csv_path = Path(sys.argv[1])
    version = sys.argv[2] if len(sys.argv) > 2 else "1.0.0"
    
    output_dir = Path(__file__).parent / "models"
    
    train_initial_model(
        training_data_path=csv_path,
        output_dir=output_dir,
        version=version,
        use_xgboost=False
    )
