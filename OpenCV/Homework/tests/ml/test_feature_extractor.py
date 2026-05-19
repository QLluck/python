"""Unit tests for ML feature extraction."""

import numpy as np
import pytest

from app.ml.feature_extractor import FeatureExtractor


class TestFeatureExtractor:
    """Test suite for FeatureExtractor class."""
    
    @pytest.fixture
    def extractor(self):
        """Create a FeatureExtractor instance."""
        return FeatureExtractor()
    
    @pytest.fixture
    def sample_image(self):
        """Create a sample grayscale image."""
        # Create a 100x100 image with gradient
        img = np.linspace(0, 255, 100*100).reshape(100, 100).astype(np.uint8)
        return img
    
    @pytest.fixture
    def sample_mask(self):
        """Create a sample binary mask."""
        mask = np.zeros((100, 100), dtype=np.uint8)
        # Create a circular mask
        center = (50, 50)
        radius = 30
        y, x = np.ogrid[:100, :100]
        mask_circle = (x - center[0])**2 + (y - center[1])**2 <= radius**2
        mask[mask_circle] = 255
        return mask
    
    def test_feature_names(self, extractor):
        """Test that feature names are correctly defined."""
        names = extractor.feature_names
        
        # Check total count (26 features)
        assert len(names) == 28  # 26 + 2 shape features
        
        # Check statistical features
        assert 'mean' in names
        assert 'std' in names
        assert 'min' in names
        assert 'max' in names
        assert 'median' in names
        
        # Check histogram features
        assert 'entropy' in names
        assert 'skewness' in names
        assert 'kurtosis' in names
        
        # Check LBP features
        for i in range(10):
            assert f'lbp_bin_{i}' in names
        
        # Check GLCM features
        assert 'glcm_contrast' in names
        assert 'glcm_homogeneity' in names
        assert 'glcm_energy' in names
        assert 'glcm_correlation' in names
        
        # Check edge features
        assert 'edge_density' in names
        assert 'gradient_magnitude' in names
        
        # Check shape features
        assert 'circularity' in names
        assert 'compactness' in names
    
    def test_extract_statistical_features(self, extractor, sample_image):
        """Test statistical feature extraction."""
        features = extractor._extract_statistical(sample_image)
        
        assert 'mean' in features
        assert 'std' in features
        assert 'min' in features
        assert 'max' in features
        assert 'median' in features
        
        # Check value ranges
        assert 0 <= features['mean'] <= 255
        assert features['std'] >= 0
        assert features['min'] == 0  # Our gradient starts at 0
        assert features['max'] == 255  # Our gradient ends at 255
        assert 0 <= features['median'] <= 255
    
    def test_extract_histogram_features(self, extractor, sample_image):
        """Test histogram feature extraction."""
        features = extractor._extract_histogram(sample_image)
        
        assert 'entropy' in features
        assert 'skewness' in features
        assert 'kurtosis' in features
        
        # Entropy should be positive
        assert features['entropy'] > 0
        
        # Skewness and kurtosis can be any value
        assert isinstance(features['skewness'], float)
        assert isinstance(features['kurtosis'], float)
    
    def test_extract_texture_features(self, extractor, sample_image):
        """Test texture feature extraction (LBP and GLCM)."""
        features = extractor._extract_texture(sample_image)
        
        # Check LBP features
        for i in range(10):
            assert f'lbp_bin_{i}' in features
            # LBP histogram values should be normalized (sum to 1)
            assert 0 <= features[f'lbp_bin_{i}'] <= 1
        
        # Check GLCM features
        assert 'glcm_contrast' in features
        assert 'glcm_homogeneity' in features
        assert 'glcm_energy' in features
        assert 'glcm_correlation' in features
        
        # GLCM values should be non-negative
        assert features['glcm_contrast'] >= 0
        assert 0 <= features['glcm_homogeneity'] <= 1
        assert 0 <= features['glcm_energy'] <= 1
        assert -1 <= features['glcm_correlation'] <= 1
    
    def test_extract_edge_features(self, extractor, sample_image):
        """Test edge feature extraction."""
        features = extractor._extract_edge(sample_image)
        
        assert 'edge_density' in features
        assert 'gradient_magnitude' in features
        
        # Edge density should be between 0 and 1
        assert 0 <= features['edge_density'] <= 1
        
        # Gradient magnitude should be non-negative
        assert features['gradient_magnitude'] >= 0
    
    def test_extract_shape_features(self, extractor, sample_mask):
        """Test shape feature extraction."""
        features = extractor._extract_shape(sample_mask)
        
        assert 'circularity' in features
        assert 'compactness' in features
        
        # Circularity should be between 0 and 1 (1 = perfect circle)
        assert 0 <= features['circularity'] <= 1
        
        # For our circular mask, circularity should be close to 1
        assert features['circularity'] > 0.8
        
        # Compactness should be positive
        assert features['compactness'] > 0
    
    def test_extract_all_features(self, extractor, sample_image):
        """Test extracting all features without shape."""
        features = extractor.extract(sample_image, mask=None, include_shape=False)
        
        # Should have all features
        assert len(features) == 28  # All features including default shape values
        
        # Shape features should be 0 when not included
        assert features['circularity'] == 0.0
        assert features['compactness'] == 0.0
    
    def test_extract_with_shape(self, extractor, sample_image, sample_mask):
        """Test extracting all features including shape."""
        features = extractor.extract(sample_image, mask=sample_mask, include_shape=True)
        
        # Should have all features
        assert len(features) == 28
        
        # Shape features should be computed
        assert features['circularity'] > 0
        assert features['compactness'] > 0
    
    def test_extract_vector(self, extractor, sample_image):
        """Test extracting features as a vector."""
        vector = extractor.extract_vector(sample_image)
        
        # Should be a 1D numpy array
        assert isinstance(vector, np.ndarray)
        assert vector.ndim == 1
        assert len(vector) == 28
        
        # All values should be numeric
        assert np.all(np.isfinite(vector))
    
    def test_rgb_image_conversion(self, extractor):
        """Test that RGB images are converted to grayscale."""
        # Create RGB image
        rgb_image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        
        # Should not raise error
        features = extractor.extract(rgb_image)
        
        assert len(features) == 28
    
    def test_empty_image_error(self, extractor):
        """Test that empty images raise an error."""
        empty_image = np.array([])
        
        with pytest.raises(ValueError, match="Image is empty"):
            extractor.extract(empty_image)
    
    def test_shape_without_mask_error(self, extractor, sample_image):
        """Test that requesting shape features without mask raises error."""
        with pytest.raises(ValueError, match="Shape features require a mask"):
            extractor.extract(sample_image, mask=None, include_shape=True)
    
    def test_performance(self, extractor, sample_image):
        """Test that feature extraction meets performance target (<500ms)."""
        import time
        
        # Test with a larger image (512x512)
        large_image = np.random.randint(0, 256, (512, 512), dtype=np.uint8)
        
        start = time.time()
        features = extractor.extract(large_image)
        elapsed = time.time() - start
        
        # Should complete in less than 500ms
        assert elapsed < 0.5, f"Feature extraction took {elapsed:.3f}s (target: <0.5s)"
    
    def test_consistent_feature_order(self, extractor, sample_image):
        """Test that feature vector order is consistent."""
        vector1 = extractor.extract_vector(sample_image)
        vector2 = extractor.extract_vector(sample_image)
        
        # Should be identical for same image
        np.testing.assert_array_equal(vector1, vector2)
    
    def test_different_images_different_features(self, extractor):
        """Test that different images produce different features."""
        # Create two different images
        img1 = np.zeros((100, 100), dtype=np.uint8)  # All black
        img2 = np.ones((100, 100), dtype=np.uint8) * 255  # All white
        
        vector1 = extractor.extract_vector(img1)
        vector2 = extractor.extract_vector(img2)
        
        # Vectors should be different
        assert not np.array_equal(vector1, vector2)
        
        # Mean should be different
        features1 = extractor.extract(img1)
        features2 = extractor.extract(img2)
        assert features1['mean'] != features2['mean']
