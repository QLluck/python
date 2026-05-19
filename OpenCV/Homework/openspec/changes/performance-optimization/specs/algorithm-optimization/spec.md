## ADDED Requirements

### Requirement: Optimized preprocessing algorithms

The system SHALL use optimized preprocessing algorithms that reduce computation time while maintaining output quality.

#### Scenario: Adaptive median kernel size
- **WHEN** image size > 1MP and performance_mode=balanced
- **THEN** median kernel is limited to 3x3
- **AND** processing time reduced by 4x compared to 5x5

#### Scenario: Bilateral filter optimization
- **WHEN** bilateral filter is enabled
- **THEN** uses optimized parameters (d=5, sigma=50)
- **AND** processing time < 100ms for 1280x1280 images

#### Scenario: CLAHE optimization
- **WHEN** CLAHE is applied
- **THEN** uses tile size 8x8 for balanced performance
- **AND** clip limit adjusted based on mode

### Requirement: Optimized detection algorithms

The system SHALL use optimized detection algorithms that reduce redundant computations.

#### Scenario: Single threshold computation
- **WHEN** detecting ROI
- **THEN** Otsu threshold computed once and reused
- **AND** avoids redundant threshold calculations

#### Scenario: Optimized connected components
- **WHEN** finding lesion candidates
- **THEN** uses 8-connectivity for faster processing
- **AND** filters components during iteration (not after)

#### Scenario: Early termination
- **WHEN** best candidate found with high confidence
- **THEN** stops searching remaining components
- **AND** reduces processing time by up to 30%

### Requirement: Optimized segmentation algorithms

The system SHALL provide fast segmentation algorithms as alternatives to slow methods.

#### Scenario: Fast Otsu segmentation
- **WHEN** segment_method=otsu_fast
- **THEN** uses simple Otsu + morphology
- **AND** completes in < 30ms (5x faster than watershed)

#### Scenario: Optimized watershed
- **WHEN** segment_method=watershed
- **THEN** uses reduced iterations and smaller kernels
- **AND** processing time reduced by 40%

#### Scenario: Region growing optimization
- **WHEN** segment_method=region_grow
- **THEN** uses optimized seed selection
- **AND** early stopping when region stable

### Requirement: Vectorized LBP computation

The system SHALL use vectorized NumPy operations for LBP feature extraction instead of loops.

#### Scenario: Vectorized LBP calculation
- **WHEN** LBP features are computed
- **THEN** uses NumPy array operations
- **AND** processing time < 30ms (3x faster than loop-based)

#### Scenario: Optimized neighborhood comparison
- **WHEN** computing LBP patterns
- **THEN** uses array slicing for all 8 neighbors
- **AND** single pass computation

### Requirement: Reduced image copying

The system SHALL minimize unnecessary image copying operations to reduce memory allocation overhead.

#### Scenario: In-place operations where safe
- **WHEN** image transformations are applied
- **THEN** uses in-place operations when possible
- **AND** reduces memory allocations by 30%

#### Scenario: View instead of copy
- **WHEN** extracting ROI
- **THEN** uses array views instead of copies
- **AND** saves 5-10ms per operation

#### Scenario: Necessary copies preserved
- **WHEN** original image must be preserved
- **THEN** creates copy only when required
- **AND** documents reason in code

### Requirement: Optimized color space conversions

The system SHALL minimize redundant color space conversions.

#### Scenario: Single grayscale conversion
- **WHEN** processing pipeline starts
- **THEN** converts to grayscale once
- **AND** reuses grayscale image throughout

#### Scenario: Avoid unnecessary conversions
- **WHEN** image already in target color space
- **THEN** skips conversion
- **AND** checks color space before converting

### Requirement: Algorithm performance targets

The system SHALL meet specific performance targets for each optimized algorithm.

#### Scenario: Preprocess performance target
- **WHEN** preprocessing 1280x1280 image
- **THEN** completes in < 100ms
- **AND** logs warning if exceeded

#### Scenario: Detection performance target
- **WHEN** detecting ROI in 1280x1280 image
- **THEN** completes in < 50ms
- **AND** finds valid candidates

#### Scenario: Segmentation performance target
- **WHEN** segmenting with otsu_fast
- **THEN** completes in < 30ms
- **AND** produces valid mask

#### Scenario: LBP performance target
- **WHEN** computing LBP features
- **THEN** completes in < 30ms
- **AND** generates valid feature map
