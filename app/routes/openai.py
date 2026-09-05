from fastapi import APIRouter, Depends, HTTPException, Header, Request
from pydantic import BaseModel
from typing import Optional
import os
import time

from app.openai_client import OpenAIClient
from app.db import get_db_session
from app.models.usage import UsageEvent

router = APIRouter()

# Simple API key check (placeholder). In production wire to tenant store.
async def get_api_key(x_api_key: Optional[str] = Header(None)):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing API key")
    # TODO: validate API key against DB
    return x_api_key

class ChatRequest(BaseModel):
    messages: list
    model: Optional[str] = None

class CodeAssistRequest(BaseModel):
    prompt: str
    model: Optional[str] = None
    max_tokens: Optional[int] = 1024

@router.post('/api/v1/chat')
async def chat_endpoint(req: ChatRequest, api_key: str = Depends(get_api_key)):
    client = OpenAIClient()
    start = time.time()
    resp = await client.chat(req.messages, model=req.model)
    duration = time.time() - start

    # record usage in DB if session present
    usage = resp.get('usage', {})
    total_tokens = usage.get('total_tokens')

    async with get_db_session() as session:
        ev = UsageEvent(api_key=api_key, endpoint='chat', request_tokens=0, response_tokens=usage.get('completion_tokens', 0) or 0, total_tokens=total_tokens or 0)
        session.add(ev)
        await session.commit()

    return {"result": resp, "latency": duration}

@router.post('/api/v1/code-assist')
async def code_assist(req: CodeAssistRequest, api_key: str = Depends(get_api_key)):
    client = OpenAIClient()
    # Optionally run moderation
    try:
        mod = await client.moderation(req.prompt)
        if mod.get('results') and mod['results'][0].get('flagged'):
            raise HTTPException(status_code=400, detail="Prompt content flagged by moderation")
    except Exception:
        # On moderation failure, continue but log in production
        pass

    start = time.time()
    resp = await client.code_assist(req.prompt, model=req.model, max_tokens=req.max_tokens)
    duration = time.time() - start

    usage = resp.get('usage', {})
    total_tokens = usage.get('total_tokens')

    async with get_db_session() as session:
        ev = UsageEvent(api_key=api_key, endpoint='code-assist', request_tokens=0, response_tokens=usage.get('completion_tokens', 0) or 0, total_tokens=total_tokens or 0)
        session.add(ev)
        await session.commit()

    return {"result": resp, "latency": duration}
