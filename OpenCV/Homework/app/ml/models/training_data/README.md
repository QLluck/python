# Training Data

This directory stores training datasets for model training and retraining.

## Files

- `synthetic_v1.csv` - Synthetic training data generated from test images
- `real_user_data.csv` - Real user data collected from production usage
- `*.csv` - Additional training datasets

## Data Format

CSV files contain:
- Image features (statistical, texture, edge, shape)
- Target labels (segmentation method and parameters)
- Quality metrics (Dice/IoU scores)
- Metadata (timestamp, user rating, etc.)

## Privacy

Only extracted features are stored, never original images or patient data.
