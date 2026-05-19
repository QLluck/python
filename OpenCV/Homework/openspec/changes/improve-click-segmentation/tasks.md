## 1. Core: Color-aware floodFill function

- [x] 1.1 Add `segment_region_grow_color()` function to `app/core/segment.py` that accepts a BGR image, converts to Lab, and runs multi-channel floodFill with per-channel thresholds (L=grow_T, a=grow_T*0.6, b=grow_T*0.6)
- [x] 1.2 Add `analyze_color_variance()` helper function that computes color_ratio from a local patch around the seed point and returns `("lab" | "grayscale", color_ratio)`
- [x] 1.3 Add enhanced morphological post-processing: close(5x5) → open(3x3) → contour-based hole filling for enclosed regions < 500px

## 2. API Integration

- [x] 2.1 Update `click_segment()` in `app/api/ml_routes.py` to call `analyze_color_variance()` on the original BGR image, then dispatch to either `segment_region_grow_color()` (Lab) or existing `segment_region_grow()` (grayscale)
- [x] 2.2 Add `color_mode` and `color_ratio` fields to the `debug_info` response

## 3. Threshold Prediction

- [x] 3.1 Update `_predict_region_grow_params()` in `app/ml/predictor.py` to include a `chroma_factor` parameter (default 0.6) used for a/b channel thresholds
- [x] 3.2 Update `predict_for_click()` to extract color features from the BGR image (not just grayscale) when available, feeding them into threshold prediction
