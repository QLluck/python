## Context

Current system requires users to manually tune 20+ parameters to achieve good segmentation results. This creates a high barrier to entry and leads to suboptimal results. Users spend significant time experimenting with different parameter combinations without understanding which parameters matter most for their specific image.

The system already has:
- Complete image processing pipeline (preprocess, detect, segment)
- Multiple segmentation algorithms (otsu, region_grow, watershed)
- Comprehensive parameter set
- Web-based UI with parameter controls

We need to add intelligence to automatically predict optimal parameters and provide interactive segmentation for quick adjustments.

## Goals / Non-Goals

**Goals:**
- Predict optimal segmentation parameters from image features using ML
- Enable click-based interactive segmentation for quick results
- Maintain backward compatibility with manual parameter tuning
- Collect training data from successful segmentations
- Provide confidence scores for predictions
- Reduce time-to-result from minutes to seconds

**Non-Goals:**
- Deep learning models (too heavy, requires GPU)
- Real-time video segmentation
- 3D medical image support
- Automatic diagnosis or medical advice
- Cloud-based model training
- Multi-user collaboration features

## Decisions

### Decision 1: ML Model Choice - RandomForest vs XGBoost vs Neural Networks

**Choice:** Start with RandomForest, add XGBoost as optional upgrade

**Rationale:**
- RandomForest: Fast inference, interpretable, works with small datasets
- XGBoost: Better accuracy but slower, more complex
- Neural Networks: Overkill for tabular data, requires more training data
- Can train both and A/B test

**Alternatives considered:**
- Deep learning: Rejected due to complexity and resource requirements
- Simple heuristics: Rejected as not adaptive to different image types
- Ensemble of all three: Rejected as too complex for v1

### Decision 2: Feature Set - Comprehensive vs Minimal

**Choice:** Start with 20-30 key features, expand based on importance analysis

**Features to extract:**
- Statistical: mean, std, min, max, percentiles (5 features)
- Histogram: entropy, skewness, kurtosis (3 features)
- Texture: LBP histogram (10 bins), GLCM metrics (4 features)
- Edge: Canny edge density, gradient magnitude (2 features)
- Shape: circularity, compactness after initial detection (2 features)
- Color (dermoscopy only): LAB channel statistics (3 features)

**Rationale:**
- Balance between information and computation time
- All features computable in <500ms
- Feature importance analysis will guide future additions

**Alternatives considered:**
- Deep features from CNN: Rejected as too slow
- 100+ features: Rejected as overfitting risk with limited data
- Only statistical features: Rejected as insufficient information

### Decision 3: Training Data Strategy - Synthetic vs Real vs Hybrid

**Choice:** Hybrid approach - start with synthetic, augment with real user data

**Phase 1 (MVP):**
- Generate synthetic training data from existing test images
- Vary parameters systematically and evaluate results
- Use Dice/IoU scores as ground truth labels
- ~1000 synthetic samples

**Phase 2 (Production):**
- Collect real user adjustments
- Store: image features + final parameters + user satisfaction
- Retrain monthly with new data
- Target: 500+ real samples

**Rationale:**
- Can launch without waiting for real data
- Synthetic data provides baseline performance
- Real data improves accuracy over time

**Alternatives considered:**
- Wait for real data: Rejected as delays launch
- Only synthetic: Rejected as may not match real usage
- Crowdsourced labeling: Rejected as expensive

### Decision 4: Click Interaction - Region Growing vs GrabCut vs SAM

**Choice:** Enhanced region growing with adaptive thresholds

**Rationale:**
- Region growing: Already implemented, fast, predictable
- GrabCut: Slower, requires more user input (rectangle)
- SAM (Segment Anything): Too heavy, requires model download
- Can enhance region growing with ML-predicted parameters

**Implementation:**
- User clicks → extract local features around click
- Predict optimal grow_T for that region
- Run region growing from click point
- Return result in <1 second

**Alternatives considered:**
- GrabCut: Rejected as slower and less intuitive
- Watershed from markers: Rejected as requires multiple clicks
- SAM integration: Rejected as too heavy for web deployment

### Decision 5: Frontend Architecture - Separate Mode vs Integrated

**Choice:** Integrated with mode toggle (Manual / Smart / Click)

**Rationale:**
- Users can switch between modes seamlessly
- Smart mode pre-fills parameters (user can still adjust)
- Click mode bypasses parameters entirely
- Maintains existing workflow for power users

**UI Changes:**
- Add mode selector at top: [Manual] [Smart] [Click]
- Smart mode: "Predict Parameters" button + confidence display
- Click mode: Canvas overlay for clicking + real-time preview
- All modes share same result display

**Alternatives considered:**
- Separate page for ML features: Rejected as breaks workflow
- Replace manual mode: Rejected as removes power user features
- Modal dialog: Rejected as interrupts flow

### Decision 6: Model Storage and Versioning

**Choice:** Store models in `app/ml/models/` with version metadata

**Structure:**
```
app/ml/models/
├── rf_v1.0.0.joblib          # RandomForest model
├── xgb_v1.0.0.joblib         # XGBoost model (optional)
├── scaler_v1.0.0.joblib      # Feature scaler
├── metadata.json             # Model info, training date, metrics
└── training_data/
    ├── synthetic_v1.csv
    └── real_user_data.csv
```

**Versioning:**
- Semantic versioning (major.minor.patch)
- API returns model version in response
- Can A/B test different versions
- Rollback by changing loaded model

**Rationale:**
- Simple file-based storage (no database needed)
- Easy to version control
- Fast loading with joblib
- Can ship pre-trained model with code

### Decision 7: API Design - Separate Endpoints vs Unified

**Choice:** Separate endpoints for different ML features

**Endpoints:**
```
POST /api/ml/predict-parameters
  Input: image (multipart/form-data)
  Output: {method, parameters, confidence, features}

POST /api/ml/click-segment
  Input: image, click_x, click_y, (optional) roi
  Output: {mask_b64, overlay_b64, parameters_used}

POST /api/ml/save-training-data
  Input: image_features, parameters, dice_score, user_rating
  Output: {saved: true, sample_id}

GET /api/ml/model-info
  Output: {version, trained_date, accuracy, feature_count}
```

**Rationale:**
- Clear separation of concerns
- Can call predict-parameters without running full pipeline
- Click-segment is fast path (no parameter UI)
- Training data collection is opt-in

**Alternatives considered:**
- Add ML flag to existing /api/process: Rejected as too complex
- Single /api/ml endpoint with action parameter: Rejected as less RESTful

### Decision 8: Feature Extraction - Inline vs Cached

**Choice:** Inline extraction with optional caching for training

**Rationale:**
- Feature extraction is fast (<500ms)
- Caching adds complexity
- Images change with different preprocessing
- For training: can cache features with image hash

**Implementation:**
- Extract features on-demand for prediction
- For training data collection: cache features with image hash
- Cache stored in memory (LRU cache, max 100 entries)

## Risks / Trade-offs

**[Risk]** ML model accuracy may be poor initially  
→ **Mitigation:** Start with synthetic data for baseline, collect real data quickly, show confidence scores to users

**[Risk]** Feature extraction adds latency  
→ **Mitigation:** Optimize feature extraction (<500ms target), run in parallel with preprocessing, cache for repeated requests

**[Risk]** Model may not generalize to new image types  
→ **Mitigation:** Collect diverse training data, show confidence scores, allow manual override, retrain regularly

**[Risk]** Click segmentation may be inaccurate  
→ **Mitigation:** Use ML-predicted parameters for region growing, allow multiple clicks for refinement, show real-time preview

**[Risk]** Training data collection may have privacy concerns  
→ **Mitigation:** Only store features (not images), make opt-in, add data export/deletion, document in privacy policy

**[Risk]** Model files increase deployment size  
→ **Mitigation:** Models are small (<10MB), use joblib compression, optional download for advanced features

**[Trade-off]** Synthetic training data vs waiting for real data  
→ **Accepted:** Launch with synthetic data for baseline, improve with real data over time

**[Trade-off]** RandomForest (fast) vs XGBoost (accurate)  
→ **Accepted:** Start with RandomForest, add XGBoost as optional upgrade based on user feedback

**[Trade-off]** Simple region growing vs advanced methods (GrabCut, SAM)  
→ **Accepted:** Use existing region growing for speed and simplicity, can upgrade later if needed

## Migration Plan

**Phase 1: Core ML Infrastructure (Week 1-2)**
1. Add ML dependencies to requirements.txt
2. Create app/ml/ module structure
3. Implement feature extraction
4. Generate synthetic training data
5. Train initial RandomForest model
6. Add model loading and inference

**Phase 2: API Integration (Week 3)**
1. Create ML API endpoints
2. Integrate with existing pipeline
3. Add error handling and logging
4. Write unit tests for ML components
5. Test with various image types

**Phase 3: Frontend Integration (Week 4)**
1. Add mode selector UI
2. Implement Smart mode (predict parameters)
3. Add confidence display
4. Integrate with existing parameter controls
5. Add loading states and error handling

**Phase 4: Click Interaction (Week 5)**
1. Add canvas overlay for clicking
2. Implement click-to-segment logic
3. Add real-time preview
4. Support multiple clicks
5. Add undo/redo functionality

**Phase 5: Training Data Collection (Week 6)**
1. Add training data collection endpoint
2. Implement opt-in UI
3. Add data export functionality
4. Create retraining script
5. Document training process

**Rollback Strategy:**
- ML features are opt-in (manual mode still works)
- Can disable ML endpoints via feature flag
- Can rollback to previous model version
- No database migrations needed

**Testing Strategy:**
- Unit tests for feature extraction
- Integration tests for ML endpoints
- End-to-end tests for UI workflows
- Performance tests for latency
- Accuracy tests with validation dataset

## Open Questions

**Q: Should we support multiple ML models simultaneously?**  
A: Start with one, add A/B testing later if needed

**Q: How to handle model updates without downtime?**  
A: Load new model in background, atomic swap, keep old model for rollback

**Q: Should click segmentation work on original or preprocessed image?**  
A: Preprocessed image (more consistent), but store original for display

**Q: How to collect user feedback on ML predictions?**  
A: Add thumbs up/down buttons, track parameter adjustments, measure Dice score improvement

**Q: Should we expose feature importance to users?**  
A: Not in v1, but log for debugging and model improvement
