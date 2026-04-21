"""LLM provider abstraction. Uses OpenAI-compatible API (works with Ollama, OpenAI, etc.)."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field

from openai import AsyncOpenAI

from .config import LLMConfig

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """Structured response from an LLM call."""

    content: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    latency_ms: float
    raw_response: dict = field(default_factory=dict)


class LLMProvider:
    """Async LLM provider using OpenAI-compatible API.

    Works with:
    - Ollama (localhost:11434/v1)
    - OpenAI API
    - Any OpenAI-compatible endpoint (llama.cpp server, vLLM, etc.)
    """

    def __init__(self, config: LLMConfig) -> None:
        self.config = config
        self.client = AsyncOpenAI(
            base_url=config.base_url,
            api_key=config.api_key,
        )
        self._call_count = 0
        self._total_tokens = 0

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        """Generate a completion from the LLM.

        Args:
            prompt: The user message.
            system_prompt: Optional system message.
            temperature: Override default temperature.
            max_tokens: Override default max tokens.

        Returns:
            Structured LLM response with content and metadata.
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        temp = temperature if temperature is not None else self.config.temperature
        tokens = max_tokens if max_tokens is not None else self.config.max_tokens

        start = time.perf_counter()
        response = await self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=temp,
            max_tokens=tokens,
        )
        latency_ms = (time.perf_counter() - start) * 1000

        self._call_count += 1
        usage = response.usage
        prompt_tokens = usage.prompt_tokens if usage else 0
        completion_tokens = usage.completion_tokens if usage else 0
        total_tokens = usage.total_tokens if usage else 0
        self._total_tokens += total_tokens

        content = response.choices[0].message.content or ""

        logger.debug(
            "LLM call #%d: model=%s tokens=%d latency=%.0fms",
            self._call_count,
            self.config.model,
            total_tokens,
            latency_ms,
        )

        return LLMResponse(
            content=content,
            model=self.config.model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            latency_ms=latency_ms,
        )

    @property
    def call_count(self) -> int:
        return self._call_count

    @property
    def total_tokens_used(self) -> int:
        return self._total_tokens

    async def check_connection(self) -> bool:
        """Verify the LLM endpoint is reachable."""
        try:
            response = await self.generate("Say 'ok'.", max_tokens=5)
            return len(response.content) > 0
        except Exception as e:
            logger.error("LLM connection check failed: %s", e)
            return False
