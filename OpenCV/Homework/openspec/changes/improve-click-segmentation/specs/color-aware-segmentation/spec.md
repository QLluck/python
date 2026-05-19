## ADDED Requirements

### Requirement: Color-aware floodFill segmentation
The click-segment endpoint SHALL support multi-channel floodFill in Lab color space when processing color images. The system SHALL convert the input BGR image to Lab color space and run `cv2.floodFill` on the 3-channel Lab image with per-channel thresholds.

#### Scenario: Color image with visible lesion
- **WHEN** user clicks on a colored medical image (e.g., skin lesion with red/purple tones)
- **THEN** the system SHALL use Lab-space floodFill and produce a mask that captures the color-distinct lesion region

#### Scenario: Grayscale or near-grayscale image
- **WHEN** the color variance around the click point is low (color_ratio <= 0.3)
- **THEN** the system SHALL fall back to grayscale floodFill (current behavior)

### Requirement: Automatic color-space decision
The system SHALL analyze a local patch (120x120 pixels) around the click point to compute color variance. The decision metric SHALL be `color_ratio = (std_a + std_b) / (std_L + 1)` where std_a, std_b, std_L are standard deviations of the Lab channels in the local patch.

#### Scenario: High color variance region
- **WHEN** `color_ratio > 0.3` in the local patch around the click point
- **THEN** the system SHALL use Lab multi-channel floodFill

#### Scenario: Low color variance region
- **WHEN** `color_ratio <= 0.3` in the local patch around the click point
- **THEN** the system SHALL use grayscale floodFill

### Requirement: Per-channel threshold adaptation
When using Lab multi-channel floodFill, the system SHALL apply asymmetric thresholds: L channel uses `grow_T`, a and b channels use `grow_T * 0.6`.

#### Scenario: Threshold values for Lab floodFill
- **WHEN** Lab mode is selected and grow_T is predicted as 30
- **THEN** floodFill loDiff and upDiff SHALL be `(30, 18, 18)` for the (L, a, b) channels respectively

### Requirement: Enhanced morphological post-processing
After floodFill, the system SHALL apply enhanced morphological operations: close with 5x5 elliptical kernel, open with 3x3 elliptical kernel, and contour-based hole filling for enclosed regions.

#### Scenario: Lesion with internal texture holes
- **WHEN** floodFill produces a mask with small internal holes (< 500 pixels each)
- **THEN** the morphological post-processing SHALL fill those holes to produce a solid lesion mask

### Requirement: Debug info includes color mode
The API response `debug_info` SHALL include a `color_mode` field indicating whether `"lab"` or `"grayscale"` was used, and the computed `color_ratio` value.

#### Scenario: Response includes color mode info
- **WHEN** click-segment returns successfully
- **THEN** `debug_info.color_mode` SHALL be `"lab"` or `"grayscale"` and `debug_info.color_ratio` SHALL be a float value
