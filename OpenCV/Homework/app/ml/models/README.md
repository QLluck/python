# ML Models Directory

This directory stores trained ML models and training data.

## Structure

- `*.joblib` - Trained model files (RandomForest, XGBoost, scalers)
- `metadata.json` - Model version, training date, and performance metrics
- `training_data/` - Training datasets (synthetic and real user data)

## Model Versioning

Models use semantic versioning: `model_type_vMAJOR.MINOR.PATCH.joblib`

Example:
- `rf_v1.0.0.joblib` - RandomForest model version 1.0.0
- `scaler_v1.0.0.joblib` - Feature scaler version 1.0.0

## Files (will be generated during training)

- `rf_v1.0.0.joblib` - RandomForest classifier
- `xgb_v1.0.0.joblib` - XGBoost classifier (optional)
- `scaler_v1.0.0.joblib` - StandardScaler for feature normalization
- `metadata.json` - Model metadata and metrics
