"""
Machine Learning module for intelligent segmentation.

This module provides ML-powered features including:
- Automatic parameter prediction from image features
- Click-based interactive segmentation
- Training data collection and model retraining
"""

from app.ml.feature_extractor import FeatureExtractor
from app.ml.predictor import Predictor

__all__ = ["FeatureExtractor", "Predictor"]
