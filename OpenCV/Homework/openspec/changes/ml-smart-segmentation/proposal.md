## Why

Current users must manually adjust 20+ parameters to achieve good segmentation results, requiring deep understanding of image processing algorithms. This creates a high barrier to entry and leads to suboptimal results. Adding ML-based parameter prediction and click-based interactive segmentation will make the system accessible to non-experts while improving segmentation quality.

## What Changes

- Add image feature extraction module (brightness, contrast, texture, edge density, etc.)
- Implement ML parameter prediction using RandomForest/XGBoost
  - Predict optimal segmentation method (otsu_roi/region_grow/watershed)
  - Predict optimal parameters (thresholds, kernel sizes, grow_T, etc.)
  - Return confidence scores for predictions
- Add click-based interactive segmentation
  - User clicks on lesion location
  - System performs region growing from click point
  - Real-time preview of segmentation result
  - Support multiple clicks for refinement
- Enhance frontend with smart segmentation UI
  - "Smart Segmentation" button (auto-predict parameters)
  - "Click to Segment" mode (interactive)
  - Display predicted parameters and confidence
  - Allow manual parameter adjustment after prediction
- Add training data collection system
  - Record user-adjusted parameters and results
  - Build training dataset from successful segmentations
  - Support model retraining and improvement
- Add new API endpoints for ML features

## Capabilities

### New Capabilities

- `image-feature-extraction`: Extract statistical and texture features from medical images for ML analysis, including brightness, contrast, edge density, texture metrics (LBP, GLCM), and shape characteristics

- `ml-parameter-prediction`: Use machine learning models (RandomForest/XGBoost) to predict optimal segmentation parameters based on image features, including method selection, threshold values, and algorithm-specific parameters

- `click-interactive-segmentation`: Enable users to perform segmentation by clicking on lesion locations, with real-time region growing and visual feedback, supporting multiple clicks for refinement

- `smart-segmentation-ui`: Frontend interface for ML-powered segmentation with smart parameter prediction button, click-to-segment mode, confidence display, and parameter adjustment controls

- `training-data-collection`: System to collect and store successful segmentation parameters and results for continuous model improvement, including data export and model retraining capabilities

### Modified Capabilities

<!-- No existing capabilities are being modified - this is additive functionality -->

## Impact

**New Dependencies:**
- `scikit-learn` - RandomForest classifier and feature preprocessing
- `xgboost` - Gradient boosting for parameter prediction
- `joblib` - Model serialization and loading
- `pandas` - Training data management (optional)

**New Backend Files:**
- `app/ml/` - New ML module directory
  - `feature_extractor.py` - Image feature extraction
  - `parameter_predictor.py` - ML model for parameter prediction
  - `models/` - Trained model storage
  - `training/` - Training data and scripts
- `app/api/ml_routes.py` - New ML API endpoints
- `app/core/interactive.py` - Click-based segmentation logic

**Modified Backend Files:**
- `app/api/routes.py` - Add ML endpoint imports
- `app/main.py` - Register ML routes
- `requirements.txt` - Add ML dependencies

**New Frontend Files:**
- `static/ml-ui.js` - Smart segmentation UI logic
- `static/click-segment.js` - Click interaction handler

**Modified Frontend Files:**
- `static/index.html` - Add smart segmentation UI elements
- `static/style.css` - Add ML UI styling
- `static/app.js` - Integrate ML features

**New API Endpoints:**
- `POST /api/ml/predict-parameters` - Predict optimal parameters from image
- `POST /api/ml/click-segment` - Perform segmentation from click point
- `POST /api/ml/save-training-data` - Save successful parameters for training
- `GET /api/ml/model-info` - Get model version and confidence metrics

**Benefits:**
- Dramatically improved user experience (no manual parameter tuning)
- Better segmentation results through ML optimization
- Lower barrier to entry for non-experts
- Continuous improvement through data collection
- Faster workflow with click-based interaction

**Risks:**
- ML model needs training data (can start with synthetic/augmented data)
- Model accuracy depends on training data quality
- Additional computational overhead for feature extraction
- Increased complexity in codebase

**Migration:**
- Fully backward compatible - existing parameter-based workflow unchanged
- ML features are opt-in (users can still manually adjust parameters)
- No breaking changes to existing API
