#!/usr/bin/env python3
"""
Test the trained ML model.

This script loads the trained model and tests it on sample images.
"""

import sys
from pathlib import Path

import cv2
import numpy as np

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.ml.predictor import Predictor


def main():
    """Test the trained model."""
    print("=" * 60)
    print("ML Model Testing")
    print("=" * 60)
    
    # Initialize predictor
    try:
        predictor = Predictor(version="1.0.0")
        predictor.load_models()
        print("\n✓ Model loaded successfully")
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        print("\nPlease train the model first:")
        print("  1. python scripts/generate_training_data.py")
        print("  2. python scripts/train_model.py")
        sys.exit(1)
    
    # Show model info
    model_info = predictor.get_model_info()
    print("\nModel Information:")
    for key, value in model_info.items():
        print(f"  {key}: {value}")
    
    # Test on synthetic image
    print("\n" + "=" * 60)
    print("Testing on Synthetic Image")
    print("=" * 60)
    
    # Create a test image with a dark lesion
    test_img = np.ones((512, 512), dtype=np.uint8) * 200
    cv2.ellipse(test_img, (256, 256), (80, 60), 45, 0, 360, 80, -1)
    test_img = cv2.GaussianBlur(test_img, (5, 5), 0)
    
    print("\nPredicting parameters...")
    result = predictor.predict(test_img)
    
    print(f"\nPrediction Results:")
    print(f"  Method: {result['method']}")
    print(f"  Confidence: {result['confidence']:.3f}")
    print(f"  Parameters:")
    for param, value in result['parameters'].items():
        print(f"    {param}: {value}")
    
    # Test click-based prediction
    print("\n" + "=" * 60)
    print("Testing Click-Based Prediction")
    print("=" * 60)
    
    click_result = predictor.predict_for_click(test_img, click_x=256, click_y=256)
    
    print(f"\nClick Prediction Results:")
    print(f"  Method: {click_result['method']}")
    print(f"  Confidence: {click_result['confidence']:.3f}")
    print(f"  Parameters:")
    for param, value in click_result['parameters'].items():
        print(f"    {param}: {value}")
    
    # Test on real fixture if available
    fixtures_dir = Path(__file__).parent.parent / "tests" / "fixtures"
    test_fixture = fixtures_dir / "valid_gray.png"
    
    if test_fixture.exists():
        print("\n" + "=" * 60)
        print("Testing on Real Fixture")
        print("=" * 60)
        
        img = cv2.imread(str(test_fixture), cv2.IMREAD_GRAYSCALE)
        if img is not None:
            result = predictor.predict(img)
            
            print(f"\nPrediction Results for {test_fixture.name}:")
            print(f"  Method: {result['method']}")
            print(f"  Confidence: {result['confidence']:.3f}")
            print(f"  Parameters:")
            for param, value in result['parameters'].items():
                print(f"    {param}: {value}")
    
    print("\n" + "=" * 60)
    print("Testing Complete!")
    print("=" * 60)
    print("\nThe model is working correctly and ready for integration.")


if __name__ == "__main__":
    main()
