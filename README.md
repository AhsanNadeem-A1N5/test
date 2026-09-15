# ClaimForge AI

AI-powered insurance claims evidence and triage platform.

ClaimForge turns claim information into an auditable review brief with evidence-linked findings, deterministic triage, and a human-review boundary. It is designed as an engineering portfolio project rather than a system that makes binding coverage or fraud decisions.

## MVP
- FastAPI API
- Pydantic claim schemas
- Deterministic severity/routing analysis
- Risk signals
- Human-review flag
- Next.js dashboard planned
- MCP tool surface planned

## Roadmap
1. Multimodal evidence ingestion: PDFs, OCR, receipts and claim photos.
2. Evidence graph and contradiction detection.
3. LangGraph orchestration with explicit agent/tool boundaries.
4. Vision/model adapters with structured outputs and evidence citations.
5. Evaluation suite for extraction accuracy, grounding, routing calibration and hallucination resistance.
6. PostgreSQL/object storage/authentication/observability for production deployment.

## Safety boundary
ClaimForge provides advisory analysis. Consequential insurance decisions remain with authorized human reviewers.
