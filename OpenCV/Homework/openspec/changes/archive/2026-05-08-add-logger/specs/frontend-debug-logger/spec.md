## ADDED Requirements

### Requirement: Debug panel UI component
The system SHALL provide a collapsible debug panel in the frontend that displays operational logs with visual hierarchy and controls.

#### Scenario: Panel is visible by default
- **WHEN** user loads the application
- **THEN** debug panel is displayed in expanded state above the results tabs

#### Scenario: User can collapse panel
- **WHEN** user clicks the collapse button or panel header
- **THEN** panel collapses to show only the header with title and controls

#### Scenario: User can expand collapsed panel
- **WHEN** user clicks the header of a collapsed panel
- **THEN** panel expands to show all log entries

#### Scenario: Panel displays header with controls
- **WHEN** panel is rendered
- **THEN** header shows "调试日志" title, clear button, and collapse/expand button

### Requirement: Log entry structure
The system SHALL display each log entry with timestamp, severity level, message, and optional detail information.

#### Scenario: Log entry shows timestamp
- **WHEN** a log entry is created
- **THEN** entry displays current time in HH:MM:SS format

#### Scenario: Log entry shows severity level
- **WHEN** a log entry is created
- **THEN** entry displays severity level (INFO, SUCCESS, WARNING, ERROR) with distinct color coding

#### Scenario: Log entry shows message
- **WHEN** a log entry is created
- **THEN** entry displays the main message text

#### Scenario: Log entry shows optional detail
- **WHEN** a log entry is created with detail parameter
- **THEN** entry displays detail text indented below the main message with "└─" prefix

### Requirement: Severity level color coding
The system SHALL use distinct colors for each severity level to enable quick visual scanning.

#### Scenario: INFO level uses blue color
- **WHEN** log entry has INFO level
- **THEN** level badge displays in blue (#3b82f6)

#### Scenario: SUCCESS level uses green color
- **WHEN** log entry has SUCCESS level
- **THEN** level badge displays in green (#10b981)

#### Scenario: WARNING level uses orange color
- **WHEN** log entry has WARNING level
- **THEN** level badge displays in orange (#f59e0b)

#### Scenario: ERROR level uses red color
- **WHEN** log entry has ERROR level
- **THEN** level badge displays in red (#ef4444)

### Requirement: Logger API
The system SHALL provide a Logger object with methods for logging at different severity levels.

#### Scenario: Logger provides info method
- **WHEN** code calls Logger.info(message, detail)
- **THEN** system creates INFO level log entry with message and optional detail

#### Scenario: Logger provides success method
- **WHEN** code calls Logger.success(message, detail)
- **THEN** system creates SUCCESS level log entry with message and optional detail

#### Scenario: Logger provides warning method
- **WHEN** code calls Logger.warning(message, detail)
- **THEN** system creates WARNING level log entry with message and optional detail

#### Scenario: Logger provides error method
- **WHEN** code calls Logger.error(message, detail)
- **THEN** system creates ERROR level log entry with message and optional detail

### Requirement: Log management
The system SHALL provide controls for managing log entries including clearing and limiting log history.

#### Scenario: User can clear all logs
- **WHEN** user clicks the clear button
- **THEN** all log entries are removed and a "日志已清空" info message is logged

#### Scenario: Logs are limited to prevent memory issues
- **WHEN** number of log entries exceeds 100
- **THEN** oldest log entry is removed before adding new entry

#### Scenario: Panel auto-scrolls to newest entry
- **WHEN** new log entry is added
- **THEN** panel scrolls to bottom to show the newest entry

### Requirement: Console integration
The system SHALL output all log entries to browser console in addition to the visual panel.

#### Scenario: INFO logs output to console.log
- **WHEN** Logger.info() is called
- **THEN** message is output to console.log with [INFO] prefix

#### Scenario: SUCCESS logs output to console.log
- **WHEN** Logger.success() is called
- **THEN** message is output to console.log with [SUCCESS] prefix

#### Scenario: WARNING logs output to console.warn
- **WHEN** Logger.warning() is called
- **THEN** message is output to console.warn with [WARNING] prefix

#### Scenario: ERROR logs output to console.error
- **WHEN** Logger.error() is called
- **THEN** message is output to console.error with [ERROR] prefix

### Requirement: File selection logging
The system SHALL log file selection events with file metadata.

#### Scenario: Log when file is selected
- **WHEN** user selects an image file
- **THEN** system logs INFO message with filename and file size in KB

### Requirement: Parameter validation logging
The system SHALL log parameter validation results.

#### Scenario: Log successful validation
- **WHEN** form parameters pass validation
- **THEN** system logs INFO message "参数验证通过"

#### Scenario: Log validation errors
- **WHEN** form parameters fail validation
- **THEN** system logs ERROR message with validation error details

### Requirement: API request logging
The system SHALL log API request lifecycle events including start, success, and failure.

#### Scenario: Log API request start
- **WHEN** user clicks run button and validation passes
- **THEN** system logs INFO message "发送 API 请求..."

#### Scenario: Log API success with timing
- **WHEN** API request completes successfully
- **THEN** system logs SUCCESS message with elapsed time from response metadata

#### Scenario: Log API failure with status
- **WHEN** API request fails with HTTP error
- **THEN** system logs ERROR message with HTTP status code

#### Scenario: Log network errors
- **WHEN** API request fails due to network error
- **THEN** system logs ERROR message "网络错误" with error details

### Requirement: Data reception logging
The system SHALL log when image data is received from API with data size information.

#### Scenario: Log overlay data reception
- **WHEN** API response includes overlay_png_b64 data
- **THEN** system logs INFO message with data size in KB

#### Scenario: Log mask data reception
- **WHEN** API response includes mask_png_b64 data
- **THEN** system logs INFO message with data size in KB

#### Scenario: Log ROI data reception
- **WHEN** API response includes roi_preview_png_b64 data
- **THEN** system logs INFO message with data size in KB

#### Scenario: Log preprocess data reception
- **WHEN** API response includes preprocess_png_b64 data
- **THEN** system logs INFO message with data size in KB

#### Scenario: Log LBP data reception
- **WHEN** API response includes lbp_png_b64 data
- **THEN** system logs INFO message with data size in KB

### Requirement: Tab switching logging
The system SHALL log when user switches between result tabs.

#### Scenario: Log tab switch
- **WHEN** user clicks a result tab
- **THEN** system logs INFO message with tab name (overlay, mask, roi, pre, lbp)

### Requirement: Image rendering logging
The system SHALL log image rendering events including success and failure.

#### Scenario: Log image render start
- **WHEN** renderActiveTab() is called with valid data
- **THEN** system logs INFO message with tab name and data size

#### Scenario: Log successful image load
- **WHEN** image loads successfully
- **THEN** system logs SUCCESS message with tab name

#### Scenario: Log image load failure
- **WHEN** image fails to load
- **THEN** system logs ERROR message with tab name and reason "base64 数据可能损坏"

#### Scenario: Log missing data warning
- **WHEN** renderActiveTab() is called with null data
- **THEN** system logs WARNING message with tab name and reason "该阶段可能未返回图片"
