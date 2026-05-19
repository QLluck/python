"""
Feature extraction for ML-based segmentation parameter prediction.

Extracts statistical, texture, edge, and shape features from medical images
to enable ML models to predict optimal segmentation parameters.
"""

from __future__ import annotations

import time
from typing import Dict, Optional

import cv2
import numpy as np
from scipy import stats
from skimage.feature import graycomatrix, graycoprops

from app.core.lbp import uniform_lbp_image


class FeatureExtractor:
    """
    Extract features from medical images for ML prediction.
    
    Features extracted:
    - Statistical: mean, std, min, max, percentiles (5 features)
    - Histogram: entropy, skewness, kurtosis (3 features)
    - Texture: LBP histogram (10 bins), GLCM metrics (4 features)
    - Edge: Canny edge density, gradient magnitude (2 features)
    - Shape: circularity, compactness (2 features) - optional, requires mask
    
    Total: 26 features (24 without shape features)
    
    Target performance: <500ms for images up to 2048x2048
    """
    
    def __init__(self):
        """Initialize feature extractor."""
        self.feature_names = self._get_feature_names()
    
    def _get_feature_names(self) -> list[str]:
        """Get ordered list of feature names."""
        names = []
        
        # Statistical features (5)
        names.extend(['mean', 'std', 'min', 'max', 'median'])
        
        # Histogram features (3)
        names.extend(['entropy', 'skewness', 'kurtosis'])
        
        # Texture features - LBP (10)
        names.extend([f'lbp_bin_{i}' for i in range(10)])
        
        # Texture features - GLCM (4)
        names.extend(['glcm_contrast', 'glcm_homogeneity', 'glcm_energy', 'glcm_correlation'])
        
        # Edge features (2)
        names.extend(['edge_density', 'gradient_magnitude'])
        
        # Shape features (2) - optional
        names.extend(['circularity', 'compactness'])
        
        return names
    
    def extract(
        self,
        image: np.ndarray,
        mask: Optional[np.ndarray] = None,
        include_shape: bool = False
    ) -> Dict[str, float]:
        """
        Extract all features from an image.
        
        Args:
            image: Grayscale image (H, W) or RGB image (H, W, 3)
            mask: Optional binary mask for shape feature extraction
            include_shape: Whether to include shape features (requires mask)
        
        Returns:
            Dictionary mapping feature names to values
        
        Raises:
            ValueError: If image is invalid or shape features requested without mask
        """
        start_time = time.time()
        
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image.copy()
        
        # Validate image
        if gray.size == 0:
            raise ValueError("Image is empty")
        
        features = {}
        
        # Extract statistical features
        features.update(self._extract_statistical(gray))
        
        # Extract histogram features
        features.update(self._extract_histogram(gray))
        
        # Extract texture features
        features.update(self._extract_texture(gray))
        
        # Extract edge features
        features.update(self._extract_edge(gray))
        
        # Extract shape features if requested
        if include_shape:
            if mask is None:
                raise ValueError("Shape features require a mask")
            features.update(self._extract_shape(mask))
        else:
            # Add default values for shape features
            features['circularity'] = 0.0
            features['compactness'] = 0.0
        
        elapsed = time.time() - start_time
        
        # Log warning if extraction is slow
        if elapsed > 0.5:
            print(f"Warning: Feature extraction took {elapsed:.3f}s (target: <0.5s)")
        
        return features
    
    def extract_vector(
        self,
        image: np.ndarray,
        mask: Optional[np.ndarray] = None,
        include_shape: bool = False
    ) -> np.ndarray:
        """
        Extract features as a numpy array (for ML model input).
        
        Args:
            image: Grayscale or RGB image
            mask: Optional binary mask for shape features
            include_shape: Whether to include shape features
        
        Returns:
            1D numpy array of feature values in consistent order
        """
        features = self.extract(image, mask, include_shape)
        return np.array([features[name] for name in self.feature_names])
    
    def _extract_statistical(self, gray: np.ndarray) -> Dict[str, float]:
        """Extract statistical features: mean, std, min, max, median."""
        return {
            'mean': float(np.mean(gray)),
            'std': float(np.std(gray)),
            'min': float(np.min(gray)),
            'max': float(np.max(gray)),
            'median': float(np.median(gray)),
        }
    
    def _extract_histogram(self, gray: np.ndarray) -> Dict[str, float]:
        """Extract histogram features: entropy, skewness, kurtosis."""
        # Calculate histogram
        hist, _ = np.histogram(gray.ravel(), bins=256, range=(0, 256))
        
        # Normalize histogram to get probability distribution
        hist = hist.astype(float) / hist.sum()
        
        # Calculate entropy: -sum(p * log2(p))
        # Add small epsilon to avoid log(0)
        hist_nonzero = hist[hist > 0]
        entropy = -np.sum(hist_nonzero * np.log2(hist_nonzero))
        
        # Calculate skewness and kurtosis from pixel values
        flat = gray.ravel()
        skewness = float(stats.skew(flat))
        kurtosis = float(stats.kurtosis(flat))
        
        return {
            'entropy': float(entropy),
            'skewness': skewness,
            'kurtosis': kurtosis,
        }
    
    def _extract_texture(self, gray: np.ndarray) -> Dict[str, float]:
        """Extract texture features: LBP histogram and GLCM metrics."""
        features = {}
        
        # LBP features
        lbp = uniform_lbp_image(gray, radius=1, neighbors=8)
        
        # Create histogram with 10 bins (reduce from 256 for efficiency)
        hist, _ = np.histogram(lbp.ravel(), bins=10, range=(0, 256))
        hist = hist.astype(float) / hist.sum()  # Normalize
        
        for i, val in enumerate(hist):
            features[f'lbp_bin_{i}'] = float(val)
        
        # GLCM features
        # Downsample image for faster GLCM computation
        if gray.shape[0] > 512 or gray.shape[1] > 512:
            scale = min(512 / gray.shape[0], 512 / gray.shape[1])
            gray_small = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        else:
            gray_small = gray
        
        # Quantize to 64 levels for faster GLCM computation
        gray_quantized = (gray_small // 4).astype(np.uint8)
        
        # Compute GLCM with distance=1, angles=[0, 45, 90, 135]
        glcm = graycomatrix(
            gray_quantized,
            distances=[1],
            angles=[0, np.pi/4, np.pi/2, 3*np.pi/4],
            levels=64,
            symmetric=True,
            normed=True
        )
        
        # Extract GLCM properties (average over all angles)
        features['glcm_contrast'] = float(graycoprops(glcm, 'contrast').mean())
        features['glcm_homogeneity'] = float(graycoprops(glcm, 'homogeneity').mean())
        features['glcm_energy'] = float(graycoprops(glcm, 'energy').mean())
        features['glcm_correlation'] = float(graycoprops(glcm, 'correlation').mean())
        
        return features
    
    def _extract_edge(self, gray: np.ndarray) -> Dict[str, float]:
        """Extract edge features: Canny edge density and gradient magnitude."""
        # Canny edge detection
        edges = cv2.Canny(gray, threshold1=50, threshold2=150)
        edge_density = float(np.sum(edges > 0) / edges.size)
        
        # Gradient magnitude using Sobel
        grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        gradient_mag = np.sqrt(grad_x**2 + grad_y**2)
        avg_gradient = float(np.mean(gradient_mag))
        
        return {
            'edge_density': edge_density,
            'gradient_magnitude': avg_gradient,
        }
    
    def _extract_shape(self, mask: np.ndarray) -> Dict[str, float]:
        """Extract shape features: circularity and compactness."""
        # Find contours
        contours, _ = cv2.findContours(
            mask.astype(np.uint8),
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        if not contours:
            return {
                'circularity': 0.0,
                'compactness': 0.0,
            }
        
        # Use largest contour
        contour = max(contours, key=cv2.contourArea)
        
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, closed=True)
        
        # Avoid division by zero
        if perimeter == 0 or area == 0:
            return {
                'circularity': 0.0,
                'compactness': 0.0,
            }
        
        # Circularity: 4π * area / perimeter^2
        # Perfect circle = 1.0, irregular shape < 1.0
        circularity = 4 * np.pi * area / (perimeter ** 2)
        
        # Compactness: perimeter^2 / area
        # Lower values = more compact
        compactness = (perimeter ** 2) / area
        
        return {
            'circularity': float(circularity),
            'compactness': float(compactness),
        }
