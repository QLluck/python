## Context

The click-segment endpoint (`/api/ml/click-segment`) currently:
1. Decodes the uploaded image as BGR
2. Converts to grayscale via `preprocess_gray()`
3. Runs `floodFill` on the grayscale image with a single threshold (`grow_T`)
4. Returns mask + overlay

For colored medical pathology images (skin diseases, herpes, tissue samples), grayscale conversion collapses the most discriminative feature — color — into a single channel where lesion/background contrast is often minimal.

## Goals / Non-Goals

**Goals:**
- Improve segmentation accuracy on colored medical images by leveraging color information
- Automatically detect whether color-based or grayscale segmentation is more appropriate
- Maintain backward compatibility — grayscale images should work as before
- Keep response time under 1 second for typical images

**Non-Goals:**
- Deep learning-based segmentation (out of scope for this OpenCV-based project)
- Changing the manual-mode pipeline (`/api/process`) — only the click-segment path is affected
- UI changes — the API contract stays the same

## Decisions

### 1. Use Lab color space for multi-channel floodFill

**Decision:** Convert BGR → Lab and run `cv2.floodFill` on the 3-channel Lab image.

**Why Lab over HSV/RGB:**
- Lab is perceptually uniform — equal distances in Lab correspond to equal perceived color differences
- The L channel separates lightness from chromaticity (a, b), allowing independent threshold control
- HSV's H channel wraps around (0°=360°=red), causing discontinuities near red — problematic for skin lesion images where red is common
- RGB channels are correlated, making threshold tuning unpredictable

**Alternatives considered:**
- HSV: Rejected due to hue wraparound issue with red tones common in medical images
- RGB: Rejected due to channel correlation making thresholds hard to tune
- Grayscale only (current): Insufficient for color-dominant features

### 2. Automatic color-vs-grayscale decision

**Decision:** Analyze a local patch around the click point. If color variance (in a/b channels) is high relative to luminance variance, use color-aware segmentation; otherwise fall back to grayscale.

**Metric:** `color_ratio = (std_a + std_b) / (std_L + 1)`. If `color_ratio > 0.3`, use Lab multi-channel; otherwise use grayscale (current behavior).

**Why:** Some medical images (X-rays, ultrasound) are naturally grayscale. Forcing Lab on them adds no benefit and may cause unpredictable results.

### 3. Per-channel threshold strategy

**Decision:** Use asymmetric thresholds for L, a, b channels:
- L channel: `grow_T` (same as current grayscale threshold)
- a channel: `grow_T * 0.6` (tighter — chromaticity changes are more semantically meaningful)
- b channel: `grow_T * 0.6`

**Why:** A large threshold on chromaticity channels would cause the flood to spill across color boundaries. The 0.6 factor was chosen empirically — chromaticity channels in Lab have smaller dynamic range than L.

### 4. Enhanced morphological post-processing

**Decision:** After floodFill, apply:
1. Close operation (fill small holes within lesions) — kernel size 5x5
2. Open operation (remove small noise) — kernel size 3x3
3. Contour-based hole filling (fill enclosed holes in the mask)

**Why:** Medical lesion masks often have internal holes due to texture variation. The current 3x3 morphology is insufficient.

## Risks / Trade-offs

- **[Risk] Lab conversion adds ~5-10ms per image** → Acceptable within the 1s budget. Lab conversion is a single O(n) pass.
- **[Risk] Color threshold ratio (0.6) may not be optimal for all image types** → The threshold is exposed via the predictor, which can be refined with training data.
- **[Risk] Auto-detection heuristic may misclassify some images** → Fallback to grayscale is safe (current behavior). Only color-mode is new.
- **[Trade-off] Slightly larger mask areas due to more aggressive hole filling** → Acceptable for medical images where under-segmentation is worse than mild over-segmentation.
