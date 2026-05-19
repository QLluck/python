## 1. ML Infrastructure Setup

- [x] 1.1 Add ML dependencies to requirements.txt (scikit-learn, joblib, xgboost)
- [x] 1.2 Create app/ml/ module structure with __init__.py
- [x] 1.3 Create app/ml/models/ directory for model storage
- [x] 1.4 Create app/ml/feature_extractor.py module
- [x] 1.5 Create app/ml/predictor.py module for model inference
- [x] 1.6 Create app/ml/trainer.py module for model training

## 2. Feature Extraction Implementation

- [x] 2.1 Implement statistical feature extraction (mean, std, min, max, percentiles)
- [x] 2.2 Implement histogram features (entropy, skewness, kurtosis)
- [x] 2.3 Implement texture features (LBP histogram with 10 bins)
- [x] 2.4 Implement GLCM features (contrast, homogeneity, energy, correlation)
- [x] 2.5 Implement edge features (Canny edge density, gradient magnitude)
- [x] 2.6 Implement shape features (circularity, compactness)
- [x] 2.7 Create feature vector normalization and scaling
- [x] 2.8 Add feature extraction performance optimization (<500ms target)
- [x] 2.9 Write unit tests for feature extraction functions

## 3. Synthetic Training Data Generation

- [x] 3.1 Create app/ml/data_generator.py for synthetic data generation
- [x] 3.2 Implement parameter variation logic for different image types
- [x] 3.3 Generate training samples with systematic parameter sweeps
- [x] 3.4 Evaluate segmentation quality (Dice/IoU scores) for each sample
- [x] 3.5 Create training dataset CSV with features and labels
- [x] 3.6 Generate ~1000 synthetic training samples
- [x] 3.7 Split data into train/validation/test sets

## 4. ML Model Training

- [x] 4.1 Implement RandomForest model training pipeline
- [x] 4.2 Train model to predict segmentation method (otsu_roi, region_grow, watershed)
- [x] 4.3 Train model to predict method-specific parameters
- [x] 4.4 Implement confidence score calculation
- [x] 4.5 Evaluate model performance on validation set
- [x] 4.6 Save trained model with joblib to app/ml/models/
- [x] 4.7 Create model metadata.json with version, training date, metrics
- [x] 4.8 Implement model loading and caching logic

## 5. ML API Endpoints

- [x] 5.1 Create POST /api/ml/predict-parameters endpoint
- [x] 5.2 Implement image upload and feature extraction in predict endpoint
- [x] 5.3 Add model inference and confidence score calculation
- [x] 5.4 Return predicted method, parameters, confidence, and features
- [x] 5.5 Create POST /api/ml/click-segment endpoint
- [x] 5.6 Implement click coordinate handling and ROI-aware segmentation
- [x] 5.7 Return segmentation mask and overlay as base64 images
- [x] 5.8 Create GET /api/ml/model-info endpoint
- [x] 5.9 Add error handling and logging for all ML endpoints
- [ ] 5.10 Write integration tests for ML API endpoints

## 6. Click-Based Segmentation

- [x] 6.1 Enhance region growing to accept click coordinates as seed point
- [x] 6.2 Implement local feature extraction around click point
- [x] 6.3 Use ML-predicted grow_T for click-based region growing
- [x] 6.4 Add support for multiple click points with result merging
- [x] 6.5 Optimize click segmentation for <1 second response time
- [x] 6.6 Add ROI-aware clicking (constrain to detected ROI if available)
- [ ] 6.7 Write unit tests for click segmentation logic

## 7. Frontend Mode Selector

- [x] 7.1 Add mode selector UI component (Manual/Smart/Click tabs)
- [x] 7.2 Implement mode switching logic in frontend
- [x] 7.3 Show/hide parameter controls based on selected mode
- [x] 7.4 Add CSS styling for mode selector
- [x] 7.5 Persist selected mode in browser localStorage

## 8. Smart Mode UI

- [x] 8.1 Add "Predict Parameters" button in Smart mode
- [x] 8.2 Implement API call to /api/ml/predict-parameters
- [x] 8.3 Display predicted method and parameters in UI
- [x] 8.4 Show confidence score with color-coded indicator (green >0.8, yellow 0.5-0.8, red <0.5)
- [x] 8.5 Allow manual adjustment of predicted parameters
- [x] 8.6 Add loading spinner during prediction
- [x] 8.7 Display error messages for prediction failures
- [x] 8.8 Pre-fill parameter controls with predicted values

## 9. Click Mode UI

- [x] 9.1 Create canvas overlay component for click interaction
- [x] 9.2 Implement click event handling on image canvas
- [x] 9.3 Display click markers at user-selected points
- [x] 9.4 Call /api/ml/click-segment on each click
- [x] 9.5 Show real-time segmentation preview with transparency overlay
- [x] 9.6 Add support for multiple clicks with combined results
- [x] 9.7 Implement undo/clear functionality for click points
- [x] 9.8 Add loading indicator during segmentation
- [x] 9.9 Display segmentation result with overlay

## 10. Training Data Collection

- [ ] 10.1 Create POST /api/ml/save-training-data endpoint
- [ ] 10.2 Implement opt-in UI for training data collection (checkbox)
- [ ] 10.3 Store training samples in app/ml/models/training_data/
- [ ] 10.4 Add thumbs up/down rating buttons for results
- [ ] 10.5 Track parameter adjustments made by users
- [ ] 10.6 Calculate and store quality metrics (Dice score if ground truth available)
- [ ] 10.7 Implement data export to CSV functionality
- [ ] 10.8 Create retraining script for model updates
- [ ] 10.9 Add privacy notice about feature-only storage

## 11. Testing and Validation

- [ ] 11.1 Write unit tests for all ML modules (feature extraction, prediction, training)
- [ ] 11.2 Write integration tests for ML API endpoints
- [ ] 11.3 Create end-to-end tests for Smart mode workflow
- [ ] 11.4 Create end-to-end tests for Click mode workflow
- [ ] 11.5 Test with various image types (dermoscopy, X-ray, ultrasound)
- [ ] 11.6 Validate prediction accuracy on test dataset
- [ ] 11.7 Performance test feature extraction (<500ms)
- [ ] 11.8 Performance test click segmentation (<1s)
- [ ] 11.9 Test model versioning and rollback

## 12. Documentation and Deployment

- [ ] 12.1 Document ML feature extraction in code comments
- [ ] 12.2 Document model training process in README
- [ ] 12.3 Create user guide for Smart and Click modes
- [ ] 12.4 Document API endpoints in API documentation
- [ ] 12.5 Add model retraining instructions
- [ ] 12.6 Update main README with ML features
- [ ] 12.7 Create deployment checklist for model files
- [ ] 12.8 Add feature flags for ML functionality
