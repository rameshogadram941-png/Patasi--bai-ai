import os
import asyncio
import httpx
from typing import Any, Dict, Optional

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-code")

class OpenAIClient:
    def __init__(self, api_key: Optional[str] = None, client: Optional[httpx.AsyncClient] = None):
        self.api_key = api_key or OPENAI_API_KEY
        self.client = client or httpx.AsyncClient(timeout=30.0)

    async def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        url = f"{OPENAI_API_BASE}/{path.lstrip('/')}"
        resp = await self.client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()

    async def chat(self, messages: list, model: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        payload = {
            "model": model or OPENAI_MODEL,
            "messages": messages,
            **kwargs,
        }
        return await self._post("chat/completions", payload)

    async def code_assist(self, prompt: str, model: Optional[str] = None, max_tokens: int = 1024, **kwargs) -> Dict[str, Any]:
        # Use the chat API with a system prompt for code generation
        messages = [
            {"role": "system", "content": "You are a helpful code assistant. Return only code when appropriate."},
            {"role": "user", "content": prompt},
        ]
        payload = {
            "model": model or OPENAI_MODEL,
            "messages": messages,
            "max_tokens": max_tokens,
            **kwargs,
        }
        return await self._post("chat/completions", payload)

    async def moderation(self, input_text: str) -> Dict[str, Any]:
        payload = {"input": input_text}
        return await self._post("moderations", payload)

    async def close(self):
        await self.client.aclose()

# Example usage
# async def main():
#     client = OpenAIClient()
#     resp = await client.code_assist("Write a python function that returns fibonacci sequence up to n")
#     print(resp)

# if __name__ == '__main__':
#     asyncio.run(main())
