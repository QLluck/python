## Why

The click-based segmentation currently converts color medical images to grayscale before running floodFill, discarding color information critical for identifying skin lesions, herpes, and tissue abnormalities. For example, a red lesion on skin may differ by only ~15 gray levels from surrounding tissue, but differ by 60+ in individual color channels. This causes under-segmentation (incomplete capture of lesions) or over-segmentation (bleeding into healthy tissue).

## What Changes

- Replace grayscale-only floodFill with adaptive multi-channel floodFill using Lab color space for perceptually uniform color distance
- Add automatic color-space analysis at the click point to determine whether grayscale or color-based segmentation is more appropriate
- Adjust threshold prediction (`grow_T`) to account for multi-channel color differences
- Add morphological refinement tuned for medical pathology images (filling small holes in lesion masks)

## Capabilities

### New Capabilities
- `color-aware-segmentation`: Multi-channel floodFill in Lab color space with automatic fallback to grayscale when color variance is low. Includes per-channel threshold adaptation and color-space analysis at seed point.

### Modified Capabilities
_(none — no existing specs)_

## Impact

- **Backend**: `app/api/ml_routes.py` (click-segment endpoint), `app/core/segment.py` (new color-aware floodFill function), `app/ml/predictor.py` (threshold prediction adjustments)
- **Frontend**: No changes required — the API contract remains the same
- **Dependencies**: No new dependencies (OpenCV and NumPy already support Lab conversion and multi-channel floodFill)
