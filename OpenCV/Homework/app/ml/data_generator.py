"""
Synthetic training data generator for ML model training.

Generates training samples by systematically varying segmentation parameters
and evaluating results on test images.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import cv2
import numpy as np
from tqdm import tqdm

from app.core.metrics import dice_iou
from app.core.preprocess import preprocess_image, PreprocessParams
from app.core.segment import segment_otsu_triangle, segment_region_grow, segment_watershed, SegmentParams
from app.ml.feature_extractor import FeatureExtractor


class SyntheticDataGenerator:
    """
    Generate synthetic training data for ML model training.
    
    Creates training samples by:
    1. Loading test images
    2. Systematically varying segmentation parameters
    3. Evaluating segmentation quality (Dice/IoU)
    4. Extracting features and storing results
    """
    
    def __init__(self, feature_extractor: Optional[FeatureExtractor] = None):
        """
        Initialize data generator.
        
        Args:
            feature_extractor: FeatureExtractor instance (creates new if None)
        """
        self.feature_extractor = feature_extractor or FeatureExtractor()
        self.samples: List[Dict] = []
    
    def generate_from_images(
        self,
        image_paths: List[Path],
        output_csv: Path,
        samples_per_image: int = 100,
        ground_truth_masks: Optional[Dict[Path, np.ndarray]] = None
    ) -> None:
        """
        Generate training data from a list of images.
        
        Args:
            image_paths: List of paths to test images
            output_csv: Path to save training data CSV
            samples_per_image: Number of parameter variations per image
            ground_truth_masks: Optional dict mapping image paths to ground truth masks
        """
        print(f"Generating synthetic training data from {len(image_paths)} images...")
        print(f"Target: {samples_per_image} samples per image = {len(image_paths) * samples_per_image} total")
        
        self.samples = []
        
        for img_path in tqdm(image_paths, desc="Processing images"):
            # Load image
            img = cv2.imread(str(img_path))
            if img is None:
                print(f"Warning: Could not load {img_path}, skipping")
                continue
            
            # Get ground truth mask if available
            gt_mask = ground_truth_masks.get(img_path) if ground_truth_masks else None
            
            # Generate samples for this image
            image_samples = self._generate_samples_for_image(
                img, samples_per_image, gt_mask
            )
            
            self.samples.extend(image_samples)
        
        # Save to CSV
        self._save_to_csv(output_csv)
        
        print(f"\nGenerated {len(self.samples)} training samples")
        print(f"Saved to {output_csv}")
    
    def _generate_samples_for_image(
        self,
        image: np.ndarray,
        num_samples: int,
        gt_mask: Optional[np.ndarray] = None
    ) -> List[Dict]:
        """
        Generate training samples for a single image.
        
        Args:
            image: Input image
            num_samples: Number of samples to generate
            gt_mask: Optional ground truth mask for quality evaluation
        
        Returns:
            List of sample dictionaries
        """
        samples = []
        
        # Preprocess image
        preprocess_params = PreprocessParams()
        preprocessed = preprocess_image(image, preprocess_params)
        gray = cv2.cvtColor(preprocessed, cv2.COLOR_RGB2GRAY)
        
        # Extract features once for this image
        features = self.feature_extractor.extract(gray, mask=None, include_shape=False)
        
        # Generate parameter variations
        param_sets = self._generate_parameter_variations(num_samples)
        
        for params in param_sets:
            # Run segmentation
            try:
                mask = self._run_segmentation(gray, params)
                
                # Evaluate quality
                if gt_mask is not None:
                    dice, iou = dice_iou(mask, gt_mask)
                else:
                    # Use heuristic quality score if no ground truth
                    dice, iou = self._heuristic_quality_score(mask, gray)
                
                # Create sample
                sample = {
                    'method': params.method,
                    **features,  # Add all extracted features
                    'dice_score': dice,
                    'iou_score': iou,
                    # Store parameters for regression (future use)
                    'grow_T': params.grow_T,
                    'morph_kernel': params.morph_kernel,
                }
                
                samples.append(sample)
                
            except Exception as e:
                # Skip failed segmentations
                continue
        
        return samples
    
    def _generate_parameter_variations(self, num_samples: int) -> List[SegmentParams]:
        """
        Generate systematic parameter variations.
        
        Args:
            num_samples: Number of parameter sets to generate
        
        Returns:
            List of SegmentParams with varied parameters
        """
        param_sets = []
        
        # Divide samples among methods
        samples_per_method = num_samples // 3
        
        # Otsu variations
        for i in range(samples_per_method):
            params = SegmentParams(
                method="otsu_roi",
                threshold_kind=np.random.choice(["otsu", "triangle"]),
                morph_kernel=np.random.choice([3, 5, 7, 9]),
            )
            param_sets.append(params)
        
        # Region growing variations
        for i in range(samples_per_method):
            params = SegmentParams(
                method="region_grow",
                grow_T=np.random.randint(5, 50),
                seed_strategy=np.random.choice(["dark", "bright", "dt_peak"]),
            )
            param_sets.append(params)
        
        # Watershed variations
        for i in range(samples_per_method):
            params = SegmentParams(
                method="watershed",
                watershed_fg_erosion_iters=np.random.randint(1, 5),
                watershed_bg_dilation_iters=np.random.randint(1, 5),
            )
            param_sets.append(params)
        
        return param_sets
    
    def _run_segmentation(self, gray: np.ndarray, params: SegmentParams) -> np.ndarray:
        """
        Run segmentation with given parameters.
        
        Args:
            gray: Grayscale image
            params: Segmentation parameters
        
        Returns:
            Binary segmentation mask
        """
        if params.method == "otsu_roi":
            return segment_otsu_triangle(gray, params)
        elif params.method == "region_grow":
            return segment_region_grow(gray, params)
        elif params.method == "watershed":
            mask, warnings = segment_watershed(gray, params)
            return mask
        else:
            raise ValueError(f"Unknown method: {params.method}")
    
    def _heuristic_quality_score(
        self,
        mask: np.ndarray,
        gray: np.ndarray
    ) -> Tuple[float, float]:
        """
        Estimate segmentation quality without ground truth.
        
        Uses heuristics:
        - Mask should cover reasonable area (5-50% of image)
        - Mask should be compact (not too fragmented)
        - Foreground should be darker than background (for lesions)
        
        Args:
            mask: Binary segmentation mask
            gray: Grayscale image
        
        Returns:
            Tuple of (dice_estimate, iou_estimate)
        """
        h, w = mask.shape
        total_pixels = h * w
        
        # Calculate mask area
        mask_area = np.sum(mask > 0)
        area_ratio = mask_area / total_pixels
        
        # Penalize if area is too small or too large
        if area_ratio < 0.05 or area_ratio > 0.5:
            return 0.3, 0.2
        
        # Calculate compactness
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return 0.2, 0.1
        
        largest_contour = max(contours, key=cv2.contourArea)
        largest_area = cv2.contourArea(largest_contour)
        compactness = largest_area / mask_area if mask_area > 0 else 0
        
        # Calculate intensity contrast
        fg_mean = np.mean(gray[mask > 0]) if mask_area > 0 else 128
        bg_mean = np.mean(gray[mask == 0]) if mask_area < total_pixels else 128
        contrast = abs(fg_mean - bg_mean) / 255.0
        
        # Combine heuristics into quality score
        quality = (
            0.4 * min(area_ratio / 0.2, 1.0) +  # Prefer ~20% area
            0.3 * compactness +  # Prefer compact masks
            0.3 * contrast  # Prefer high contrast
        )
        
        # Estimate dice and iou from quality
        dice_estimate = max(0.0, min(1.0, quality))
        iou_estimate = max(0.0, min(1.0, quality * 0.8))
        
        return dice_estimate, iou_estimate
    
    def _save_to_csv(self, output_path: Path) -> None:
        """
        Save training samples to CSV file.
        
        Args:
            output_path: Path to output CSV file
        """
        if not self.samples:
            print("Warning: No samples to save")
            return
        
        # Get all feature names
        fieldnames = list(self.samples[0].keys())
        
        # Write CSV
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.samples)


def generate_synthetic_data(
    image_dir: Path,
    output_csv: Path,
    samples_per_image: int = 100,
    max_images: Optional[int] = None
) -> None:
    """
    Convenience function to generate synthetic training data.
    
    Args:
        image_dir: Directory containing test images
        output_csv: Path to save training data CSV
        samples_per_image: Number of parameter variations per image
        max_images: Maximum number of images to process (None = all)
    """
    # Find all images
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    image_paths = []
    
    for ext in image_extensions:
        image_paths.extend(image_dir.glob(f'*{ext}'))
        image_paths.extend(image_dir.glob(f'*{ext.upper()}'))
    
    if max_images:
        image_paths = image_paths[:max_images]
    
    if not image_paths:
        print(f"No images found in {image_dir}")
        return
    
    # Generate data
    generator = SyntheticDataGenerator()
    generator.generate_from_images(
        image_paths=image_paths,
        output_csv=output_csv,
        samples_per_image=samples_per_image
    )


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python data_generator.py <image_dir> <output_csv> [samples_per_image]")
        sys.exit(1)
    
    image_dir = Path(sys.argv[1])
    output_csv = Path(sys.argv[2])
    samples_per_image = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    
    generate_synthetic_data(image_dir, output_csv, samples_per_image)
