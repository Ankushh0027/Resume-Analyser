"""
OpenAI LLM Provider Implementation
Handles server-side execution for OpenAI Chat Completions endpoint.
"""

import json
import urllib.request
import urllib.error
from src.config import config
from src.providers.base import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):
    """OpenAI GPT Provider."""

    def __init__(self, api_key: str | None = None) -> None:
        super().__init__(name="OpenAI GPT", default_model=config.OPENAI_MODEL)
        self.api_key = api_key or config.OPENAI_API_KEY

    def generate(self, prompt: str, system_prompt: str, model_name: str | None = None) -> str:
        """Executes prompt via OpenAI Chat Completions REST endpoint."""
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not configured on the server.")

        target_model = model_name or self.default_model
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": target_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=45) as response:
                resp_body = response.read().decode("utf-8")
                resp_json = json.loads(resp_body)
                return resp_json["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"OpenAI HTTP {e.code}: {err_body}") from e
        except Exception as e:
            raise RuntimeError(f"OpenAI request failed: {str(e)}") from e
