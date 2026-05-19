## 1. HTML Structure

- [x] 1.1 Add debug panel HTML structure to index.html above the tabs section
- [x] 1.2 Add debug panel header with title "调试日志" and icon
- [x] 1.3 Add clear button with trash icon to debug panel header
- [x] 1.4 Add collapse/expand button with chevron icon to debug panel header
- [x] 1.5 Add debug content container div with id="debugLog"

## 2. CSS Styling

- [x] 2.1 Add .debug-panel base styles with glass-card aesthetic
- [x] 2.2 Add .debug-header styles with flex layout for title and controls
- [x] 2.3 Add .debug-title styles with icon and text layout
- [x] 2.4 Add .debug-actions styles for button container
- [x] 2.5 Add .btn-icon-sm styles for small icon buttons with hover effects
- [x] 2.6 Add .chevron-icon rotation animation for collapse/expand
- [x] 2.7 Add .debug-panel.collapsed styles to hide content
- [x] 2.8 Add .debug-content styles with max-height, scrolling, and monospace font
- [x] 2.9 Add .debug-entry styles for individual log entries with flex layout
- [x] 2.10 Add .debug-time styles for timestamp display
- [x] 2.11 Add .debug-level styles with color variants (info, success, warning, error)
- [x] 2.12 Add .debug-message styles for main message text
- [x] 2.13 Add .debug-detail styles for indented detail text

## 3. Logger Core Implementation

- [x] 3.1 Add debugLogs array and maxLogs property to state object
- [x] 3.2 Create Logger object with log() base method
- [x] 3.3 Implement Logger.info() method
- [x] 3.4 Implement Logger.success() method
- [x] 3.5 Implement Logger.warning() method
- [x] 3.6 Implement Logger.error() method
- [x] 3.7 Implement Logger.render() method to create and append log entry DOM elements
- [x] 3.8 Implement Logger.clear() method to remove all log entries
- [x] 3.9 Add console output integration (console.log/warn/error) in log() method
- [x] 3.10 Add auto-scroll to bottom when new log entry is added
- [x] 3.11 Add 100-entry limit with FIFO removal in log() method

## 4. Panel Controls

- [x] 4.1 Add event listener for collapse/expand button to toggle .collapsed class
- [x] 4.2 Add event listener for clear button to call Logger.clear()
- [x] 4.3 Add event listener for debug header click to toggle collapse (excluding actions area)

## 5. File Selection Logging

- [x] 5.1 Add Logger.info() call in fileInput change event with filename and file size
- [x] 5.2 Add Logger.info() call in drag-and-drop event with filename and file size

## 6. Parameter Validation Logging

- [x] 6.1 Add Logger.info() call after successful validation in collectFormData()
- [x] 6.2 Add Logger.error() call in validation error catch block with error details

## 7. API Request Logging

- [x] 7.1 Add Logger.info() call at start of runBtn click handler ("开始处理图像...")
- [x] 7.2 Add Logger.info() call before fetch request ("发送 API 请求...")
- [x] 7.3 Add Logger.success() call after successful API response with elapsed time
- [x] 7.4 Add Logger.error() call for HTTP error responses with status code
- [x] 7.5 Add Logger.error() call for network errors in catch block

## 8. Data Reception Logging

- [x] 8.1 Add Logger.info() call when overlay_png_b64 data is received with size in KB
- [x] 8.2 Add Logger.info() call when mask_png_b64 data is received with size in KB
- [x] 8.3 Add Logger.info() call when roi_preview_png_b64 data is received with size in KB
- [x] 8.4 Add Logger.info() call when preprocess_png_b64 data is received with size in KB
- [x] 8.5 Add Logger.info() call when lbp_png_b64 data is received with size in KB

## 9. Tab Switching Logging

- [x] 9.1 Add Logger.info() call in tab click event handler with tab name

## 10. Image Rendering Logging

- [x] 10.1 Add Logger.info() call at start of renderActiveTab() when b64Data exists with tab name and data size
- [x] 10.2 Add Logger.success() call in img.onload handler with tab name
- [x] 10.3 Add Logger.error() call in img.onerror handler with tab name and reason
- [x] 10.4 Add Logger.warning() call when b64Data is null with tab name and reason

## 11. Testing and Verification

- [x] 11.1 Test panel collapse/expand functionality
- [x] 11.2 Test clear logs button
- [x] 11.3 Test file selection logging with different file sizes
- [x] 11.4 Test parameter validation logging (both success and error cases)
- [x] 11.5 Test API request logging through full workflow
- [x] 11.6 Test data reception logging for all image types
- [x] 11.7 Test tab switching logging
- [x] 11.8 Test image rendering logging (success, failure, and missing data cases)
- [x] 11.9 Verify console output matches UI logs
- [x] 11.10 Verify 100-entry limit works correctly
- [x] 11.11 Verify auto-scroll to newest entry works
- [x] 11.12 Verify color coding for all severity levels
