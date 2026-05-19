## 1. Core Algorithm Modules - Preprocess

- [ ] 1.1 Add file-level documentation to preprocess.py explaining preprocessing purpose and algorithms
- [ ] 1.2 Add detailed docstring to preprocess_gray() function with algorithm steps
- [ ] 1.3 Add detailed docstring to apply_clahe() function with CLAHE explanation
- [ ] 1.4 Add detailed docstring to apply_morphology() function with morphology explanation
- [ ] 1.5 Add inline comments explaining median filter usage and parameters
- [ ] 1.6 Add inline comments explaining bilateral filter and when to use it
- [ ] 1.7 Add inline comments explaining CLAHE parameters (clip_limit, tile_size)
- [ ] 1.8 Add inline comments explaining top-hat operation and use cases
- [ ] 1.9 Add inline comments explaining black-hat operation and use cases
- [ ] 1.10 Add usage examples to preprocess.py docstrings

## 2. Core Algorithm Modules - Detect

- [ ] 2.1 Add file-level documentation to detect.py explaining detection purpose and algorithms
- [ ] 2.2 Add detailed docstring to detect_roi() function with detection workflow
- [ ] 2.3 Add detailed docstring to _binary_from_gray() function with thresholding explanation
- [ ] 2.4 Add inline comments explaining Otsu thresholding algorithm
- [ ] 2.5 Add inline comments explaining adaptive thresholding and parameters
- [ ] 2.6 Add inline comments explaining connected components analysis
- [ ] 2.7 Add inline comments explaining component filtering (area, ratio)
- [ ] 2.8 Add inline comments explaining ROI extraction and margin calculation
- [ ] 2.9 Add inline comments explaining color fusion strategies (and/or)
- [ ] 2.10 Add usage examples to detect.py docstrings

## 3. Core Algorithm Modules - Segment

- [ ] 3.1 Add file-level documentation to segment.py explaining segmentation purpose and algorithms
- [ ] 3.2 Add detailed docstring to segment_roi() function with method selection
- [ ] 3.3 Add detailed docstring to segment_otsu_triangle() function
- [ ] 3.4 Add detailed docstring to segment_region_grow() function with algorithm steps
- [ ] 3.5 Add detailed docstring to segment_watershed() function with algorithm steps
- [ ] 3.6 Add inline comments explaining region growing seed selection strategies
- [ ] 3.7 Add inline comments explaining region growing threshold (T) and gradient (G)
- [ ] 3.8 Add inline comments explaining watershed markers and distance transform
- [ ] 3.9 Add inline comments explaining morphology post-processing
- [ ] 3.10 Add usage examples to segment.py docstrings

## 4. Core Algorithm Modules - Pipeline

- [ ] 4.1 Add file-level documentation to pipeline.py explaining overall workflow
- [ ] 4.2 Add detailed docstring to run() function with stage-by-stage explanation
- [ ] 4.3 Add inline comments explaining stage flow (meta_only, preprocess_only, detect_only, full)
- [ ] 4.4 Add inline comments explaining data flow between stages
- [ ] 4.5 Add inline comments explaining timing measurements
- [ ] 4.6 Add inline comments explaining error handling and logging
- [ ] 4.7 Add inline comments explaining output format and base64 encoding
- [ ] 4.8 Add inline comments explaining metrics calculation (Dice, IoU)
- [ ] 4.9 Add workflow diagram in file-level documentation
- [ ] 4.10 Add usage examples to pipeline.py docstrings

## 5. Core Algorithm Modules - LBP

- [x] 5.1 File-level documentation already complete
- [x] 5.2 Function-level documentation already complete
- [x] 5.3 Inline comments already complete
- [x] 5.4 Usage examples already complete

## 6. Supporting Modules - Visualization

- [ ] 6.1 Add file-level documentation to viz.py explaining visualization purpose
- [ ] 6.2 Add detailed docstring to overlay_mask() function
- [ ] 6.3 Add detailed docstring to draw_contours() function
- [ ] 6.4 Add detailed docstring to draw_roi() function
- [ ] 6.5 Add detailed docstring to bgr_to_png_rgb_b64() function with base64 explanation
- [ ] 6.6 Add inline comments explaining alpha blending in overlay
- [ ] 6.7 Add inline comments explaining contour detection and drawing
- [ ] 6.8 Add inline comments explaining BGR to RGB conversion
- [ ] 6.9 Add usage examples to viz.py docstrings

## 7. Supporting Modules - Postprocess

- [ ] 7.1 Add file-level documentation to postprocess.py explaining postprocessing purpose
- [ ] 7.2 Add detailed docstring to fill_holes() function with algorithm explanation
- [ ] 7.3 Add detailed docstring to remove_small_components() function
- [ ] 7.4 Add detailed docstring to postprocess_mask() function
- [ ] 7.5 Add inline comments explaining binary fill holes algorithm
- [ ] 7.6 Add inline comments explaining connected components filtering
- [ ] 7.7 Add usage examples to postprocess.py docstrings

## 8. Supporting Modules - Metrics

- [ ] 8.1 Add file-level documentation to metrics.py explaining evaluation metrics
- [ ] 8.2 Add detailed docstring to dice_iou() function with formula explanation
- [ ] 8.3 Add detailed docstring to decode_mask_bytes() function
- [ ] 8.4 Add detailed docstring to resize_mask_to() function
- [ ] 8.5 Add inline comments explaining Dice coefficient calculation
- [ ] 8.6 Add inline comments explaining IoU calculation
- [ ] 8.7 Add inline comments explaining when to use Dice vs IoU
- [ ] 8.8 Add usage examples to metrics.py docstrings

## 9. Supporting Modules - Decode

- [ ] 9.1 Add file-level documentation to decode.py explaining image loading
- [ ] 9.2 Add detailed docstring to decode_image_bytes() function
- [ ] 9.3 Add detailed docstring to scale_longest_side() function
- [ ] 9.4 Add inline comments explaining image decoding with OpenCV
- [ ] 9.5 Add inline comments explaining aspect ratio preservation
- [ ] 9.6 Add inline comments explaining BGRA to BGR conversion
- [ ] 9.7 Add usage examples to decode.py docstrings

## 10. Supporting Modules - Validators

- [ ] 10.1 Add file-level documentation to validators.py
- [ ] 10.2 Add detailed docstrings to validation functions
- [ ] 10.3 Add inline comments explaining validation logic
- [ ] 10.4 Add usage examples to validators.py docstrings

## 11. Supporting Modules - Exceptions

- [ ] 11.1 Add file-level documentation to exceptions.py
- [ ] 11.2 Add detailed docstrings to exception classes
- [ ] 11.3 Add usage examples for exception handling

## 12. API and Main

- [ ] 12.1 Add file-level documentation to routes.py explaining API endpoints
- [ ] 12.2 Add detailed docstrings to route handlers
- [ ] 12.3 Add inline comments explaining request parsing
- [ ] 12.4 Add file-level documentation to main.py explaining application setup
- [ ] 12.5 Add inline comments explaining middleware and CORS

## 13. Supporting Documentation - TUTORIAL.md

- [ ] 13.1 Create TUTORIAL.md with quick start section
- [ ] 13.2 Add "Understanding the Pipeline" section with workflow diagram
- [ ] 13.3 Add "Module Deep Dive" section for each core module
- [ ] 13.4 Add "Parameter Tuning Guide" section
- [ ] 13.5 Add "Common Tasks" section (batch processing, custom parameters)
- [ ] 13.6 Add "Troubleshooting" section with common issues
- [ ] 13.7 Add "Learning Path" section for beginners

## 14. Supporting Documentation - EXAMPLES.md

- [ ] 14.1 Create EXAMPLES.md with basic usage example
- [ ] 14.2 Add example: Processing a single image with default parameters
- [ ] 14.3 Add example: Adjusting preprocessing parameters
- [ ] 14.4 Add example: Trying different segmentation methods
- [ ] 14.5 Add example: Batch processing multiple images
- [ ] 14.6 Add example: Using ground truth masks for evaluation
- [ ] 14.7 Add example: Extracting and visualizing LBP features
- [ ] 14.8 Add example: Debugging with intermediate outputs

## 15. Documentation Quality Review

- [ ] 15.1 Review all file-level documentation for accuracy and completeness
- [ ] 15.2 Review all function-level documentation for accuracy and completeness
- [ ] 15.3 Review all inline comments for clarity and usefulness
- [ ] 15.4 Check consistency of terminology across all modules
- [ ] 15.5 Verify all code examples are runnable
- [ ] 15.6 Check that all technical terms are explained or referenced in CONCEPTS.md
- [ ] 15.7 Verify documentation follows templates and quality standards
- [ ] 15.8 Get feedback from a beginner to test comprehensibility
- [ ] 15.9 Update COMMENT_PLAN.md progress tracker
- [ ] 15.10 Create summary document of completed work
