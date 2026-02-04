## Context

Building a 0-1 problem diagnosis system to automate manual log analysis across 30+ modules (1.2M+ lines). Current process takes hours to days; target is <1 minute for 80% of cases. System must work offline (internal network) with custom OpenAI-compatible LLM endpoint. First version targets 2-3 week development cycle with P0 features only.

## Goals / Non-Goals

**Goals:**
- Automate log collection from SSH servers, local files, and manual uploads
- AI-powered root cause analysis with >80% accuracy
- Code understanding for 30+ modules across 4 languages (Java, Python, C++, Node.js)
- Auto-generate problem reports in <30 seconds
- Web UI for <2 second page loads, support 10+ concurrent users
- Role-based access control with audit logging

**Non-Goals:**
- Integration with existing log platforms (ELK, Splunk)
- Real-time log streaming or monitoring integration (P1 feature)
- Mobile applications
- Multi-tenancy or SaaS deployment
- Automated code fixes or deployments
- Third-party ticketing system integration (manual import only)

## Decisions

### D1: Architecture - Monolithic Backend + SPA Frontend

**Decision:** Single backend service (Python FastAPI) + React SPA frontend

**Rationale:**
- Simpler deployment for internal network environment
- Faster initial development (2-3 week timeline)
- Easier to maintain with small team
- All capabilities tightly coupled (log analysis needs code index, reports need both)

**Alternatives considered:**
- Microservices: Rejected due to complexity, deployment overhead, and tight coupling between capabilities
- Server-side rendering: Rejected as SPA provides better UX for interactive analysis workflows

### D2: Code Indexing - Tree-sitter + Vector Embeddings

**Decision:** Use tree-sitter for AST parsing, generate embeddings via LLM, store in vector DB (ChromaDB)

**Rationale:**
- Tree-sitter supports all 4 required languages with unified API
- Vector search enables semantic code search ("find authentication logic")
- ChromaDB is lightweight, embeddable, no separate service needed
- First index <10 minutes for 1.2M lines

**Alternatives considered:**
- Language-specific parsers: Rejected due to maintenance burden across 4 languages
- Full-text search only: Rejected as it can't handle semantic queries
- Graph database: Rejected as overkill for initial version, adds complexity

### D3: Log Storage - SQLite + File System

**Decision:** Structured log metadata in SQLite, raw logs on filesystem

**Rationale:**
- SQLite handles GB-scale data, no separate DB server needed
- Filesystem efficient for large raw log files
- Simple backup/restore strategy
- Query performance adequate for 10+ concurrent users

**Alternatives considered:**
- PostgreSQL: Rejected as overkill for single-server deployment
- All-in-database: Rejected due to BLOB storage inefficiency for GB files
- NoSQL (MongoDB): Rejected as adds deployment complexity

### D4: LLM Integration - OpenAI-compatible API Client

**Decision:** Use OpenAI Python SDK with custom base_url pointing to internal endpoint

**Rationale:**
- Customer already has OpenAI-compatible endpoint
- Standard interface, easy to swap models later
- Streaming support for long analyses
- Well-documented, stable SDK

**Alternatives considered:**
- Direct HTTP calls: Rejected as reinvents wheel, no streaming helpers
- LangChain: Rejected as too heavy, adds unnecessary abstractions

### D5: SSH Credential Storage - Encrypted at Rest with Fernet

**Decision:** Encrypt SSH passwords with Fernet (symmetric encryption), store key in environment variable

**Rationale:**
- Fernet provides authenticated encryption
- Simple key management for single-server deployment
- Meets security requirement for encrypted storage
- Python cryptography library is well-maintained

**Alternatives considered:**
- HashiCorp Vault: Rejected as too complex for initial version, separate service
- User enters password each time: Rejected as poor UX for repeated log collection
- SSH keys only: Rejected as many servers use password auth

### D6: Report Generation - Markdown + Pandoc for PDF

**Decision:** Generate reports in Markdown, use Pandoc to convert to PDF

**Rationale:**
- Markdown easy to template and generate programmatically
- Pandoc handles PDF conversion with good formatting
- Both formats required by spec
- Can include Mermaid diagrams for visualizations

**Alternatives considered:**
- HTML + headless browser: Rejected as heavier dependency, slower
- LaTeX: Rejected as complex templating, steep learning curve
- Python PDF libraries (ReportLab): Rejected as low-level, time-consuming

## Risks / Trade-offs

**[R1] LLM accuracy depends on model quality** → Mitigation: Design prompts with clear structure, include examples, allow manual override of AI suggestions

**[R2] Code indexing time scales with codebase size** → Mitigation: Implement incremental indexing for future versions, first version does full reindex

**[R3] SSH connections may timeout or fail** → Mitigation: Implement retry logic with exponential backoff, clear error messages, allow manual log upload as fallback

**[R4] SQLite concurrent write limitations** → Mitigation: Use WAL mode, queue writes if needed, acceptable for 10 users

**[R5] Fernet key compromise exposes all SSH credentials** → Mitigation: Restrict file permissions, audit log access, rotate keys periodically, document key management procedures

**[R6] Large log files (>1GB) may cause memory issues** → Mitigation: Stream file processing, chunk large files, set upload size limits with clear messaging

**[R7] Vector search quality depends on embedding model** → Mitigation: Use same LLM for embeddings and analysis for consistency, tune chunk sizes

## Migration Plan

**Initial Deployment:**
1. Deploy backend service on internal server
2. Deploy frontend static files to web server or serve from backend
3. Configure LLM endpoint URL in environment variables
4. Set up Fernet encryption key
5. Initialize SQLite database with schema
6. Run initial code indexing (10 minutes)
7. Create admin user account
8. Verify SSH connectivity to target servers

**Rollback Strategy:**
- System is new, no migration needed
- If critical issues found, disable service and revert to manual process
- Data loss acceptable in first version (no production data yet)

**Future Migrations:**
- V1.1: Add knowledge base tables to SQLite schema
- V1.2: Add monitoring integration tables

## Open Questions

**Q1: Which specific LLM model/endpoint will be used?**
- Need endpoint URL, API key, model name
- Need to test prompt performance and latency
- Affects prompt engineering approach

**Q2: What are the SSH server connection details?**
- How many servers? (spec says 5+)
- Authentication method per server (password vs key)?
- Log file locations and naming conventions?

**Q3: Code repository access method?**
- Git clone? Direct filesystem access?
- Update frequency for reindexing?
- Which repositories/modules to index?

**Q4: Audit log retention policy?**
- How long to keep audit logs?
- Storage limits?
- Compliance requirements?

**Q5: User authentication mechanism?**
- LDAP/AD integration or local users?
- Password policy requirements?
- Session timeout configuration (spec says 30 min)?
