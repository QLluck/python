## Context

The medical image processing frontend currently provides visual feedback through toast notifications, but lacks detailed operational logging. When issues occur (e.g., image loading failures, API errors), users have no visibility into what happened without opening browser DevTools. This makes debugging difficult for both users and developers.

The existing codebase has:
- Toast notification system for user-facing messages
- Event handlers for file upload, API calls, tab switching, and image rendering
- State management for image data (base64 strings)

We need a lightweight logging system that integrates seamlessly without disrupting the existing UI/UX.

## Goals / Non-Goals

**Goals:**
- Provide visual debug logging in the UI for operational transparency
- Log key events: file selection, validation, API requests, data reception, tab switching, image rendering
- Support multiple severity levels (INFO, SUCCESS, WARNING, ERROR) with color coding
- Keep logs manageable (limit history, collapsible panel)
- Dual output to both UI and browser console
- Zero impact on existing functionality

**Non-Goals:**
- Server-side logging or log aggregation
- Log persistence across page reloads
- Advanced filtering or search capabilities
- Log export functionality
- Performance profiling or metrics collection

## Decisions

### Decision 1: In-page debug panel vs. browser console only

**Choice:** Add visual debug panel in the UI

**Rationale:**
- Browser console requires DevTools knowledge and is intimidating for non-technical users
- Visual panel provides immediate feedback without context switching
- Can still output to console for developers who prefer it
- Collapsible design minimizes visual clutter

**Alternatives considered:**
- Console-only: Rejected because it's not accessible to all users
- Modal/overlay: Rejected because it would interrupt workflow
- Separate debug page: Rejected because it requires navigation away from main UI

### Decision 2: Panel placement

**Choice:** Place debug panel above the result tabs in the results section

**Rationale:**
- Keeps logs close to the results they describe
- Doesn't interfere with input controls on the left
- Natural reading flow: see logs, then see results
- Results section already has vertical space

**Alternatives considered:**
- Bottom of page: Rejected because it requires scrolling
- Floating panel: Rejected because it could obscure content
- Left sidebar: Rejected because input panel already occupies left side

### Decision 3: Log entry structure

**Choice:** Timestamp + Level + Message + Optional Detail

**Rationale:**
- Timestamp enables temporal correlation of events
- Level enables quick visual scanning by severity
- Message provides human-readable description
- Detail provides additional context without cluttering main message
- Indented detail (with └─ prefix) shows hierarchical relationship

**Alternatives considered:**
- Flat structure: Rejected because it's harder to scan
- JSON format: Rejected because it's not user-friendly
- Expandable entries: Rejected as over-engineering for current needs

### Decision 4: Log history limit

**Choice:** Cap at 100 entries, remove oldest when exceeded

**Rationale:**
- 100 entries covers typical debugging sessions
- Prevents memory issues during long sessions
- FIFO removal keeps recent (most relevant) logs
- Users can clear manually if needed

**Alternatives considered:**
- Unlimited: Rejected due to memory concerns
- 50 entries: Rejected as potentially too limiting
- Time-based expiry: Rejected as more complex with minimal benefit

### Decision 5: Event binding approach for image loading

**Choice:** Bind onload/onerror handlers BEFORE setting img.src

**Rationale:**
- Prevents race condition where image loads before handlers are attached
- Ensures all load events are captured
- Clears old handlers to prevent memory leaks
- Consistent with best practices for dynamic image loading

**Alternatives considered:**
- Set src first: Rejected due to race condition (the original bug)
- Use Image() constructor: Rejected as unnecessary complexity for base64 data URIs

### Decision 6: Styling approach

**Choice:** Use existing glass-card aesthetic with monospace font for logs

**Rationale:**
- Consistent with existing UI design language
- Monospace font improves readability for technical logs
- Semi-transparent background maintains visual hierarchy
- Color-coded severity levels leverage existing color palette

## Risks / Trade-offs

**[Risk]** Log panel adds visual clutter to the UI  
→ **Mitigation:** Panel is collapsible and defaults to expanded but can be easily hidden

**[Risk]** Excessive logging could impact performance  
→ **Mitigation:** 100-entry cap, incremental rendering, no complex operations in log path

**[Risk]** Users might rely on logs instead of proper error messages  
→ **Mitigation:** Keep toast notifications for critical user-facing errors; logs are supplementary

**[Risk]** Base64 data size calculations could be inaccurate  
→ **Mitigation:** Use string length / 1024 for KB estimate; exact size not critical for debugging

**[Trade-off]** Adding logging calls throughout codebase increases maintenance surface  
→ **Accepted:** The debugging benefit outweighs the maintenance cost; logging is non-invasive

**[Trade-off]** Logs don't persist across page reloads  
→ **Accepted:** Session-based logging is sufficient for current debugging needs; persistence would add complexity

## Open Questions

None - design is straightforward and well-scoped.
