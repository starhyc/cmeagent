## Why

Problem diagnosis currently relies entirely on manual processes, requiring hours to days to locate issues across 30+ modules with 40K+ lines each. New employees need months of training to become effective. This system automates log collection, analysis, and reporting to reduce diagnosis time to under 1 minute for 80% of cases.

## What Changes

- Add automated log aggregation from multiple sources (SSH, local files, customer uploads)
- Add AI-powered log analysis to identify errors, anomalies, and root causes
- Add code understanding system with indexing and AI explanations for 30+ modules
- Add automated problem report generation with PDF/Markdown export
- Add web UI for log upload, analysis visualization, and report management
- Add role-based access control with admin and user roles

## Capabilities

### New Capabilities

- `log-aggregation`: Collect and normalize logs from SSH servers, local files, and manual uploads; support JSON, text, and structured formats; correlate logs across modules by timestamp and request ID
- `log-analysis`: Detect errors and exceptions; analyze cross-module call chains; identify root causes using AI; generate ranked list of probable issues
- `code-understanding`: Index codebase (Java, Python, C++, Node.js); provide AI code explanations; generate business flow diagrams; recommend relevant code locations based on errors
- `report-generation`: Generate problem reports with overview, symptoms, root cause, and solutions; export to PDF and Markdown; include visualizations (timelines, call graphs, flow diagrams)
- `web-interface`: Provide UI for log upload/configuration, analysis result visualization, timeline views, call chain graphs, code display with syntax highlighting
- `access-control`: Implement admin and user roles; control access to sensitive code and servers; maintain audit logs of all operations

### Modified Capabilities

None - this is a new system with no existing capabilities to modify.

## Impact

- New standalone web application with backend API and frontend UI
- Requires integration with custom OpenAI-compatible LLM endpoint
- Requires SSH access configuration for remote log collection
- Requires code repository access for indexing
- Storage requirements for logs (GB-scale), code index, and generated reports
- Security considerations: SSH credential storage, code access control, audit logging
