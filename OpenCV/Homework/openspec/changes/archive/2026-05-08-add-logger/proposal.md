## Why

The frontend currently lacks visibility into runtime behavior and errors. When users encounter issues (like image loading failures), there's no easy way to diagnose what went wrong without opening browser DevTools. A lightweight, visual debug logging system will help users and developers quickly identify problems during image processing workflows.

## What Changes

- Add a collapsible debug log panel to the frontend UI
- Implement a JavaScript logging system that captures key events (file selection, API requests, image rendering, errors)
- Display logs with timestamps, severity levels (INFO, SUCCESS, WARNING, ERROR), and contextual details
- Provide log management features (clear logs, expand/collapse panel)
- Integrate logging throughout the existing workflow (file upload, parameter validation, API calls, tab switching, image loading)

## Capabilities

### New Capabilities
- `frontend-debug-logger`: Visual debug logging system for the web frontend that displays real-time operational logs with severity levels, timestamps, and contextual information

### Modified Capabilities
<!-- No existing capabilities are being modified - this is a pure addition -->

## Impact

**Affected Files:**
- `static/index.html` - Add debug panel HTML structure
- `static/style.css` - Add debug panel styling
- `static/app.js` - Add Logger object and integrate logging calls throughout existing event handlers

**User Experience:**
- Improved debugging experience for users encountering issues
- Better visibility into what the application is doing during processing
- No impact on existing functionality - purely additive feature

**Performance:**
- Minimal impact - logs are rendered incrementally and capped at 100 entries
- Panel is collapsible to reduce visual clutter
