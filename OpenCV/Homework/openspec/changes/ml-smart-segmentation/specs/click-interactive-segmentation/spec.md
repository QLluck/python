## ADDED Requirements

### Requirement: Click-based segmentation
The system SHALL perform segmentation from user-specified click coordinates.

#### Scenario: Single click segmentation
- **WHEN** user clicks on lesion location
- **THEN** system performs region growing from that point and returns mask

#### Scenario: Multiple click refinement
- **WHEN** user clicks multiple times
- **THEN** system combines results from all click points

### Requirement: Real-time preview
The system SHALL provide real-time preview of segmentation result as user clicks.

#### Scenario: Immediate feedback
- **WHEN** user clicks on image
- **THEN** system shows segmentation result within 500ms

### Requirement: Adaptive parameters
The system SHALL use ML-predicted parameters for click-based segmentation.

#### Scenario: Smart region growing
- **WHEN** user clicks for segmentation
- **THEN** system uses ML-predicted grow_T and other parameters

### Requirement: ROI-aware clicking
The system SHALL support clicking within detected ROI or on full image.

#### Scenario: Click within ROI
- **WHEN** ROI is detected and user clicks inside it
- **THEN** system performs segmentation within ROI bounds

#### Scenario: Click on full image
- **WHEN** no ROI specified
- **THEN** system performs segmentation on full image from click point
