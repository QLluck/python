#!/usr/bin/env python3
"""
Generate synthetic training data for ML model training.

This script creates synthetic medical-like images and generates training samples
by varying segmentation parameters and evaluating results.
"""

import sys
from pathlib import Path

import cv2
import numpy as np

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.ml.data_generator import SyntheticDataGenerator


def create_synthetic_images(output_dir: Path, num_images: int = 10) -> list[Path]:
    """
    Create synthetic medical-like images for training.
    
    Args:
        output_dir: Directory to save synthetic images
        num_images: Number of images to generate
    
    Returns:
        List of paths to generated images
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    image_paths = []
    
    print(f"Generating {num_images} synthetic medical-like images...")
    
    for i in range(num_images):
        # Create base image (512x512)
        img = np.ones((512, 512), dtype=np.uint8) * 200
        
        # Add Gaussian noise for texture
        noise = np.random.normal(0, 20, img.shape).astype(np.int16)
        img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        
        # Add a lesion-like dark region
        center_x = np.random.randint(150, 362)
        center_y = np.random.randint(150, 362)
        radius = np.random.randint(40, 100)
        
        # Create elliptical lesion
        axes = (radius, int(radius * np.random.uniform(0.7, 1.3)))
        angle = np.random.randint(0, 180)
        
        # Draw filled ellipse (darker region)
        lesion_intensity = np.random.randint(50, 120)
        cv2.ellipse(img, (center_x, center_y), axes, angle, 0, 360, lesion_intensity, -1)
        
        # Add some irregular boundaries
        for _ in range(5):
            offset_x = np.random.randint(-30, 30)
            offset_y = np.random.randint(-30, 30)
            small_radius = np.random.randint(10, 30)
            cv2.circle(img, (center_x + offset_x, center_y + offset_y), 
                      small_radius, lesion_intensity - 20, -1)
        
        # Apply Gaussian blur for smoothness
        img = cv2.GaussianBlur(img, (5, 5), 0)
        
        # Save image
        img_path = output_dir / f"synthetic_{i:03d}.png"
        cv2.imwrite(str(img_path), img)
        image_paths.append(img_path)
    
    print(f"Created {len(image_paths)} synthetic images in {output_dir}")
    return image_paths


def main():
    """Generate synthetic training data."""
    # Setup paths
    project_root = Path(__file__).parent.parent
    synthetic_images_dir = project_root / "app" / "ml" / "models" / "training_data" / "synthetic_images"
    output_csv = project_root / "app" / "ml" / "models" / "training_data" / "synthetic_v1.csv"
    
    print("=" * 60)
    print("Synthetic Training Data Generation")
    print("=" * 60)
    
    # Create synthetic images
    image_paths = create_synthetic_images(synthetic_images_dir, num_images=10)
    
    # Add test fixtures if they exist
    fixtures_dir = project_root / "tests" / "fixtures"
    for img_file in ["valid_gray.png", "valid_rgb.jpg"]:
        img_path = fixtures_dir / img_file
        if img_path.exists():
            image_paths.append(img_path)
    
    print(f"\nTotal images for training data generation: {len(image_paths)}")
    
    # Generate training data
    # With 12 images and 100 samples per image = 1200 samples
    generator = SyntheticDataGenerator()
    
    print("\nGenerating training samples...")
    print("This will take a few minutes...")
    
    generator.generate_from_images(
        image_paths=image_paths,
        output_csv=output_csv,
        samples_per_image=100,  # 100 parameter variations per image
        ground_truth_masks=None  # Using heuristic quality scores
    )
    
    print("\n" + "=" * 60)
    print("Training data generation complete!")
    print(f"Output: {output_csv}")
    print(f"Total samples: {len(generator.samples)}")
    print("=" * 60)
    
    # Show sample statistics
    if generator.samples:
        import pandas as pd
        df = pd.DataFrame(generator.samples)
        
        print("\nDataset Statistics:")
        print(f"  Methods: {df['method'].value_counts().to_dict()}")
        print(f"  Mean Dice score: {df['dice_score'].mean():.3f}")
        print(f"  Mean IoU score: {df['iou_score'].mean():.3f}")
        print(f"  Features: {len([c for c in df.columns if c not in ['method', 'dice_score', 'iou_score', 'grow_T', 'morph_kernel']])}")


if __name__ == "__main__":
    main()
