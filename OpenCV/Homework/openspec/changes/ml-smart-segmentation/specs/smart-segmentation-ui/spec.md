## ADDED Requirements

### Requirement: Mode selector
The system SHALL provide UI to switch between Manual, Smart, and Click segmentation modes.

#### Scenario: Switch to Smart mode
- **WHEN** user selects Smart mode
- **THEN** UI shows "Predict Parameters" button and hides manual controls

#### Scenario: Switch to Click mode
- **WHEN** user selects Click mode
- **THEN** UI shows canvas overlay for clicking and hides parameter controls

### Requirement: Smart parameter prediction UI
The system SHALL display predicted parameters with confidence scores.

#### Scenario: Show predicted parameters
- **WHEN** Smart mode prediction completes
- **THEN** UI displays predicted method and parameters with confidence percentage

#### Scenario: Allow parameter adjustment
- **WHEN** predicted parameters are shown
- **THEN** user can manually adjust any parameter before running

### Requirement: Click interaction canvas
The system SHALL provide interactive canvas for click-based segmentation.

#### Scenario: Display click points
- **WHEN** user clicks on image
- **THEN** UI shows click marker at that location

#### Scenario: Show segmentation preview
- **WHEN** segmentation completes
- **THEN** UI overlays segmentation mask on image with transparency

### Requirement: Confidence visualization
The system SHALL visualize prediction confidence with color coding.

#### Scenario: High confidence display
- **WHEN** confidence > 0.8
- **THEN** UI shows green indicator

#### Scenario: Low confidence warning
- **WHEN** confidence < 0.5
- **THEN** UI shows yellow/red warning and suggests manual review
