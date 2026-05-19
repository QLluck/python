"""Central defaults for pipeline parameters — optimized for dermoscopy melanoma detection."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MEDSEG_", extra="ignore")

    # --- 解码 ---
    max_side: int = 1280

    # --- 预处理 (针对皮肤镜黑色素瘤优化) ---
    median_ksize: int = 5
    use_bilateral: bool = True                     # 双边滤波：保边去噪，去除毛发纹理
    bilateral_d: int = 7                            # 稍大空间核，黑素瘤面积较大
    bilateral_sigma_color: float = 75.0             # 更强颜色平滑
    bilateral_sigma_space: float = 50.0
    clahe_clip: float = 3.0                         # 更强对比度增强，黑素瘤常很暗
    clahe_tile: int = 8
    use_tophat: bool = True                         # 顶帽变换：增强比周围暗的区域
    tophat_kernel: int = 21                         # 大核，黑素瘤通常较大
    use_blackhat: bool = False
    blackhat_kernel: int = 15

    # --- ROI 检测 ---
    detect_threshold: str = "adaptive"              # 自适应阈值：应对皮肤镜光照不均
    adaptive_block_size: int = 45                   # 大块适应光照渐变
    adaptive_c: int = 4                            # 更宽松常数
    min_component_area: int = 30                    # 不过滤早期小病灶
    max_component_area_ratio: float = 0.90
    roi_margin_ratio: float = 0.15                  # 更大边距：黑素瘤边界不规则
    color_fusion: str = "or"                        # OR融合：包含所有颜色线索

    # --- 分割 ---
    segment_method: str = "dual"                    # 双路对比自动选优
    threshold_in_segment: str = "otsu"
    morph_kernel_segment: int = 5                   # 稍大核平滑不规则边界
    min_post_area: int = 30                         # 保留更多碎片
    grow_T: int = 20                                # 更大容差：黑素瘤边界渐变模糊
    grow_G: float = 0.0
    use_gradient_gate: bool = False
    seed_strategy: str = "dark"                     # 黑素瘤通常暗于周围皮肤

    # --- 分水岭参数 (非默认方法) ---
    watershed_fg_erosion_iters: int = 2
    watershed_bg_dilation_iters: int = 3

    # --- 日志 ---
    runs_log_csv: str = "runs_log.csv"


settings = Settings()
