## ADDED Requirements

### Requirement: Predict segmentation method
The system SHALL predict the optimal segmentation method (otsu_roi, region_grow, or watershed) based on image features.

#### Scenario: Predict method for simple lesion
- **WHEN** image has high contrast and simple shape
- **THEN** system predicts otsu_roi method with high confidence

#### Scenario: Predict method for complex lesion
- **WHEN** image has irregular boundaries
- **THEN** system predicts region_grow or watershed method

### Requirement: Predict segmentation parameters
The system SHALL predict optimal parameter values for the selected segmentation method.

#### Scenario: Predict threshold values
- **WHEN** method requires thresholding
- **THEN** system predicts optimal threshold value

#### Scenario: Predict region growing parameters
- **WHEN** region_grow method is selected
- **THEN** system predicts grow_T, seed_strategy, and other parameters

### Requirement: Return confidence scores
The system SHALL return confidence scores for all predictions.

#### Scenario: High confidence prediction
- **WHEN** image features match training data well
- **THEN** system returns confidence > 0.8

#### Scenario: Low confidence prediction
- **WHEN** image features are unusual
- **THEN** system returns confidence < 0.5 and suggests manual tuning

### Requirement: Model versioning
The system SHALL support multiple model versions and allow version selection.

#### Scenario: Load specific model version
- **WHEN** API request specifies model version
- **THEN** system loads and uses that version

#### Scenario: Default to latest model
- **WHEN** no version specified
- **THEN** system uses latest stable model

### Requirement: Fast prediction
The system SHALL complete parameter prediction within 1 second including feature extraction.

#### Scenario: Quick prediction
- **WHEN** prediction is requested
- **THEN** system returns results within 1 second
