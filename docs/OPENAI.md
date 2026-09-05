# OpenAI integration and usage docs

This document explains how Patasi--bai--ai integrates with OpenAI/Codex and how to configure it for deployment.

Environment variables (required)
- OPENAI_API_KEY - your OpenAI API key (store in Kubernetes secret)
- OPENAI_MODEL - default model to use (e.g. gpt-4o-code or gpt-4o-mini)
- DATABASE_URL - asyncpg URL for Postgres, e.g. postgresql+asyncpg://user:pass@host:5432/db
- REDIS_URL - optional Redis URL for rate limiting/caching
- STRIPE_SECRET_KEY - Stripe secret key for billing webhooks

Endpoints added
- POST /api/v1/chat
  - body: {"messages": [{"role":"user","content":"..."}, ...]}
  - requires header x-api-key: <api_key>
- POST /api/v1/code-assist
  - body: {"prompt": "...", "max_tokens": 1024}
  - requires header x-api-key: <api_key>

Notes
- The app records usage events into Postgres (usage_events table). Run migrations or create the table before deploying.
- Moderation is run for code-assist prompts. If flagged, the request is rejected.
- Configure Helm/Secrets to inject OPENAI_API_KEY into the deployment.

Prompt engineering
- Use a system message to set behavior for code generation (see app/openai_client.py)

Cost control
- Token usage is recorded so you can map tokens to cost per model and implement billing.
- Set per-tenant quotas (not implemented in scaffold) to avoid runaway costs.
