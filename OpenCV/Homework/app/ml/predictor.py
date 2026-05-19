"""
ML model predictor for segmentation parameter prediction.

Loads trained models and predicts optimal segmentation method and parameters
based on extracted image features.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Dict, Optional, Tuple

import cv2
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

from app.ml.feature_extractor import FeatureExtractor


class Predictor:
    """
    ML predictor for segmentation parameters.
    
    Predicts:
    - Segmentation method (otsu_roi, region_grow, watershed)
    - Method-specific parameters
    - Confidence scores for predictions
    """
    
    def __init__(self, model_dir: Optional[Path] = None, version: str = "1.0.0"):
        """
        Initialize predictor with trained models.
        
        Args:
            model_dir: Directory containing model files (default: app/ml/models/)
            version: Model version to load (default: "1.0.0")
        """
        if model_dir is None:
            model_dir = Path(__file__).parent / "models"
        
        self.model_dir = Path(model_dir)
        self.version = version
        self.feature_extractor = FeatureExtractor()
        
        # Model components (loaded lazily)
        self._method_classifier: Optional[RandomForestClassifier] = None
        self._param_regressor: Optional[Dict] = None
        self._scaler: Optional[StandardScaler] = None
        self._metadata: Optional[Dict] = None
        
        # Cache for loaded models
        self._models_loaded = False
        
        # 性能优化：特征缓存
        # 缓存最近计算的特征，避免重复计算
        self._feature_cache: Dict[str, Dict] = {}
        self._cache_max_size = 50  # 最多缓存 50 个图像的特征
        self._metadata: Optional[Dict] = None
        
        # Cache for loaded models
        self._models_loaded = False
    
    def load_models(self) -> None:
        """Load trained models from disk."""
        if self._models_loaded:
            return
        
        # Load method classifier
        method_model_path = self.model_dir / f"rf_v{self.version}.joblib"
        if method_model_path.exists():
            self._method_classifier = joblib.load(method_model_path)
        else:
            raise FileNotFoundError(
                f"Method classifier not found at {method_model_path}. "
                "Please train the model first."
            )
        
        # Load feature scaler
        scaler_path = self.model_dir / f"scaler_v{self.version}.joblib"
        if scaler_path.exists():
            self._scaler = joblib.load(scaler_path)
        else:
            raise FileNotFoundError(
                f"Feature scaler not found at {scaler_path}. "
                "Please train the model first."
            )
        
        # Load metadata
        metadata_path = self.model_dir / "metadata.json"
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                self._metadata = json.load(f)
        else:
            self._metadata = {
                "version": self.version,
                "trained_date": "unknown",
                "accuracy": 0.0,
                "feature_count": len(self.feature_extractor.feature_names)
            }
        
        self._models_loaded = True
    
    def predict(
        self,
        image: np.ndarray,
        mask: Optional[np.ndarray] = None
    ) -> Dict:
        """
        Predict optimal segmentation method and parameters.
        
        Args:
            image: Input image (grayscale or RGB)
            mask: Optional mask for shape features
        
        Returns:
            Dictionary containing:
            - method: Predicted segmentation method
            - parameters: Predicted parameter values
            - confidence: Confidence score (0-1)
            - features: Extracted features (for debugging)
        """
        # Ensure models are loaded
        self.load_models()
        
        # Extract features
        features = self.feature_extractor.extract(image, mask, include_shape=False)
        feature_vector = np.array([features[name] for name in self.feature_extractor.feature_names])
        feature_vector = feature_vector.reshape(1, -1)
        
        # Scale features
        if self._scaler is not None:
            feature_vector_scaled = self._scaler.transform(feature_vector)
        else:
            feature_vector_scaled = feature_vector
        
        # Predict method
        if self._method_classifier is not None:
            method_pred = self._method_classifier.predict(feature_vector_scaled)[0]
            method_proba = self._method_classifier.predict_proba(feature_vector_scaled)[0]
            confidence = float(np.max(method_proba))
        else:
            # Fallback to default method
            method_pred = "region_grow"
            confidence = 0.5
        
        # Predict parameters based on method
        parameters = self._predict_parameters(method_pred, feature_vector_scaled, features)
        
        return {
            "method": method_pred,
            "parameters": parameters,
            "confidence": confidence,
            "features": features,
        }
    
    def _predict_parameters(
        self,
        method: str,
        feature_vector: np.ndarray,
        features: Dict[str, float]
    ) -> Dict:
        """
        Predict method-specific parameters.
        
        Args:
            method: Predicted segmentation method
            feature_vector: Scaled feature vector
            features: Raw feature dictionary
        
        Returns:
            Dictionary of parameter names and values
        """
        # For now, use heuristic-based parameter prediction
        # TODO: Replace with trained regression models in future iterations
        
        if method == "otsu_roi":
            return self._predict_otsu_params(features)
        elif method == "region_grow":
            return self._predict_region_grow_params(features)
        elif method == "watershed":
            return self._predict_watershed_params(features)
        else:
            return {}
    
    def _predict_otsu_params(self, features: Dict[str, float]) -> Dict:
        """Predict parameters for otsu_roi method."""
        # Use image statistics to predict parameters
        contrast = features['std'] / (features['mean'] + 1e-6)
        
        return {
            "otsu_scale": 1.0 if contrast > 0.3 else 0.8,
            "morph_open_k": 3 if features['edge_density'] > 0.1 else 5,
            "morph_close_k": 5,
        }
    
    def _predict_region_grow_params(self, features: Dict[str, float]) -> Dict:
        """
        Predict parameters for region_grow method.
        
        改进的参数预测策略（v4 - 更宽松的阈值）：
        1. 增大阈值范围，减少保守性
        2. 考虑局部对比度
        3. 根据种子点位置自适应
        """
        edge_density = features['edge_density']
        std = features['std']
        mean = features['mean']
        
        # 获取种子点信息（如果有）
        seed_value = features.get('seed_value', mean)
        seed_relative = features.get('seed_relative', 0)
        
        # 计算对比度
        contrast_ratio = std / (mean + 1e-6)
        
        # ============================================================
        # 智能阈值预测 v4 - 更宽松的策略
        # ============================================================
        
        # 基础策略：根据局部标准差决定阈值
        # 使用更大的基础阈值和系数，减少保守性
        
        if std < 10:
            # 非常均匀的区域（如纯色背景）
            base_T = 12      # 从 8 增加到 12
            std_factor = 0.8  # 从 0.5 增加到 0.8
        elif std < 20:
            # 较均匀的区域
            base_T = 15      # 从 10 增加到 15
            std_factor = 0.7  # 从 0.4 增加到 0.7
        elif std < 30:
            # 中等纹理
            base_T = 18      # 从 12 增加到 18
            std_factor = 0.6  # 从 0.35 增加到 0.6
        else:
            # 复杂纹理
            base_T = 22      # 从 15 增加到 22
            std_factor = 0.5  # 从 0.3 增加到 0.5
        
        # 根据边缘密度调整（更宽松）
        if edge_density > 0.15:
            # 边界清晰，但仍然使用合理的阈值
            edge_factor = 0.9  # 从 0.8 增加到 0.9
        elif edge_density > 0.08:
            edge_factor = 1.0  # 从 0.9 增加到 1.0
        else:
            # 边界模糊，需要更大阈值
            edge_factor = 1.1  # 从 1.0 增加到 1.1
        
        # 计算阈值
        grow_T = base_T * edge_factor + std * std_factor
        
        # 根据种子点位置微调
        # 如果点击在极端值（很暗或很亮），可能需要更大阈值
        if abs(seed_relative) > 0.8:
            # 极端区域
            grow_T *= 1.2   # 从 1.15 增加到 1.2
        elif abs(seed_relative) > 0.5:
            # 偏离中心
            grow_T *= 1.1   # 从 1.08 增加到 1.1
        
        # 限制阈值范围（更宽松的范围）
        grow_T = float(np.clip(grow_T, 12, 50))
        
        # chroma_factor for Lab a/b channel thresholds
        # Lower value = tighter color matching, higher = more permissive
        color_std = features.get('color_std_ab', 0)
        if color_std > 15:
            chroma_factor = 0.7
        elif color_std > 8:
            chroma_factor = 0.6
        else:
            chroma_factor = 0.5
        
        return {
            "grow_T": grow_T,
            "chroma_factor": chroma_factor,
            "seed_strategy": "center",
            "connectivity": 8,
        }
    
    def _predict_watershed_params(self, features: Dict[str, float]) -> Dict:
        """Predict parameters for watershed method."""
        # Use gradient and texture features
        gradient = features['gradient_magnitude']
        
        return {
            "ws_min_distance": 10 if gradient > 30 else 20,
            "ws_compactness": 0.5,
        }
    
    def get_model_info(self) -> Dict:
        """
        Get information about loaded models.
        
        Returns:
            Dictionary with model version, training date, and metrics
        """
        self.load_models()
        return self._metadata.copy() if self._metadata else {}
    
    def predict_for_click(
        self,
        image: np.ndarray,
        click_x: int,
        click_y: int,
        roi: Optional[Tuple[int, int, int, int]] = None,
        bgr_image: Optional[np.ndarray] = None,
    ) -> Dict:
        """
        Predict parameters optimized for click-based segmentation.
        
        Args:
            image: Grayscale input image
            click_x: X coordinate of click
            click_y: Y coordinate of click
            roi: Optional ROI (x, y, w, h) to constrain segmentation
            bgr_image: Optional BGR color image for color feature extraction
        
        Returns:
            Dictionary with method and parameters optimized for region growing
        """
        cache_key = self._generate_cache_key(image, click_x, click_y)
        
        if cache_key in self._feature_cache:
            cached_features = self._feature_cache[cache_key]
            params = self._predict_region_grow_params(cached_features)
        else:
            h, w = image.shape[:2]
            
            window_size = 60
            x1 = max(0, click_x - window_size // 2)
            y1 = max(0, click_y - window_size // 2)
            x2 = min(w, click_x + window_size // 2)
            y2 = min(h, click_y + window_size // 2)
            
            local_region = image[y1:y2, x1:x2]
            
            seed_value = float(image[click_y, click_x])
            
            features = self.feature_extractor.extract(local_region, mask=None, include_shape=False)
            
            features['seed_value'] = seed_value
            features['seed_relative'] = (seed_value - features['mean']) / (features['std'] + 1e-6)
            
            # Extract color features from BGR image if available
            if bgr_image is not None and len(bgr_image.shape) == 3:
                bgr_patch = bgr_image[y1:y2, x1:x2]
                lab_patch = cv2.cvtColor(bgr_patch, cv2.COLOR_BGR2Lab)
                features['color_std_ab'] = float(
                    np.std(lab_patch[:, :, 1]) + np.std(lab_patch[:, :, 2])
                ) / 2.0
            else:
                features['color_std_ab'] = 0.0
            
            self._cache_features(cache_key, features)
            
            params = self._predict_region_grow_params(features)
        
        # Add click coordinates
        params['seed_x'] = click_x
        params['seed_y'] = click_y
        
        if roi is not None:
            params['roi'] = roi
        
        return {
            "method": "region_grow",
            "parameters": params,
            "confidence": 0.8,  # High confidence for click-based
        }
    
    def _generate_cache_key(self, image: np.ndarray, click_x: int, click_y: int) -> str:
        """
        生成缓存键，基于图像内容哈希和点击位置。
        
        Args:
            image: 输入图像
            click_x, click_y: 点击坐标
        
        Returns:
            缓存键字符串
        """
        # 使用图像的一小部分来生成哈希（避免对整个图像计算哈希）
        h, w = image.shape[:2]
        
        # 采样策略：取图像的几个关键点
        sample_points = [
            image[0, 0],  # 左上角
            image[h-1, w-1],  # 右下角
            image[h//2, w//2],  # 中心
            image[click_y, click_x],  # 点击位置
        ]
        
        # 组合图像尺寸、采样点和点击位置
        key_data = f"{w}x{h}_{sample_points}_{click_x}_{click_y}"
        
        # 生成哈希
        return hashlib.md5(key_data.encode()).hexdigest()[:16]
    
    def _cache_features(self, key: str, features: Dict) -> None:
        """
        缓存特征，使用 LRU 策略。
        
        Args:
            key: 缓存键
            features: 特征字典
        """
        # 如果缓存已满，删除最旧的条目
        if len(self._feature_cache) >= self._cache_max_size:
            # 删除第一个条目（最旧的）
            oldest_key = next(iter(self._feature_cache))
            del self._feature_cache[oldest_key]
        
        # 添加新条目
        self._feature_cache[key] = features.copy()
    
    def clear_cache(self) -> None:
        """清除特征缓存。"""
        self._feature_cache.clear()
