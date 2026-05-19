## ADDED Requirements

### Requirement: Collect successful parameters
The system SHALL collect and store parameters from successful segmentations.

#### Scenario: Save training sample
- **WHEN** user achieves good segmentation result
- **THEN** system saves image features and parameters as training sample

#### Scenario: Include quality metrics
- **WHEN** ground truth mask is available
- **THEN** system calculates and stores Dice/IoU scores

### Requirement: User feedback collection
The system SHALL allow users to rate segmentation results.

#### Scenario: Thumbs up/down feedback
- **WHEN** user rates result
- **THEN** system stores rating with training sample

### Requirement: Data export
The system SHALL export collected training data in standard format.

#### Scenario: Export to CSV
- **WHEN** admin requests data export
- **THEN** system generates CSV with features and labels

### Requirement: Model retraining
The system SHALL support retraining models with new data.

#### Scenario: Retrain with new samples
- **WHEN** sufficient new training data collected
- **THEN** system can retrain model and evaluate performance

### Requirement: Privacy compliance
The system SHALL only store features, not original images.

#### Scenario: Feature-only storage
- **WHEN** training data is saved
- **THEN** system stores only extracted features, not image pixels
