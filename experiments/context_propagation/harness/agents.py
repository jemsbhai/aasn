"""Agent type implementations for context propagation experiments.

Three agent types, each with different spawning and evaluation semantics:
1. CodingAgent - writes Python code to solve benchmark tasks
2. GeneralTaskAgent - follows instructions to complete reasoning/QA tasks
3. SelfRedesigningAgent - explicitly rewrites its own system prompt
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from .config import AgentType
from .llm import LLMProvider, LLMResponse

logger = logging.getLogger(__name__)


@dataclass
class GenerationRecord:
    """Record of a single generation in the spawning chain."""

    generation: int
    agent_type: str
    spawning_prompt: str
    offspring_prompt: str
    benchmark_scores: dict[str, float] = field(default_factory=dict)
    llm_response: LLMResponse | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """Abstract base for all agent types in the spawning chain."""

    def __init__(self, llm: LLMProvider, system_prompt: str) -> None:
        self.llm = llm
        self.system_prompt = system_prompt

    @abstractmethod
    async def solve_task(self, task: dict[str, Any]) -> str:
        """Solve a benchmark task using the current system prompt.

        Args:
            task: Benchmark task definition with 'prompt', 'type', etc.

        Returns:
            The agent's solution (code, answer, etc.).
        """
        ...

    @abstractmethod
    async def spawn_offspring(self, performance_summary: str) -> str:
        """Generate a new system prompt for the next generation.

        Args:
            performance_summary: Summary of benchmark performance.

        Returns:
            The offspring's system prompt.
        """
        ...

    @property
    @abstractmethod
    def agent_type(self) -> AgentType:
        ...


class CodingAgent(BaseAgent):
    """Agent that generates Python code to solve tasks.

    Each generation inherits a system prompt describing how to write code.
    Offspring receive a modified prompt based on parent's performance.
    """

    SPAWN_INSTRUCTION = """You are redesigning a coding agent's system prompt.

The current system prompt is:
---
{current_prompt}
---

The agent's performance on recent benchmarks:
{performance_summary}

Based on this performance, generate an improved system prompt for the next
generation of this coding agent. The new prompt should help the agent write
better Python code. Keep the core purpose intact but refine the instructions
based on what worked and what did not.

Output ONLY the new system prompt, nothing else."""

    @property
    def agent_type(self) -> AgentType:
        return AgentType.CODING

    async def solve_task(self, task: dict[str, Any]) -> str:
        prompt = task["prompt"]
        response = await self.llm.generate(
            prompt=prompt,
            system_prompt=self.system_prompt,
        )
        return response.content

    async def spawn_offspring(self, performance_summary: str) -> str:
        spawn_prompt = self.SPAWN_INSTRUCTION.format(
            current_prompt=self.system_prompt,
            performance_summary=performance_summary,
        )
        response = await self.llm.generate(
            prompt=spawn_prompt,
            temperature=0.7,
        )
        return response.content.strip()


class GeneralTaskAgent(BaseAgent):
    """Agent that follows instructions to complete reasoning and QA tasks.

    Each generation inherits a system prompt defining the agent's persona
    and approach to problem-solving.
    """

    SPAWN_INSTRUCTION = """You are redesigning a general-purpose task agent's system prompt.

The current system prompt is:
---
{current_prompt}
---

The agent's performance on recent benchmarks:
{performance_summary}

Based on this performance, generate an improved system prompt for the next
generation of this agent. The new prompt should help the agent better follow
instructions, reason more carefully, and produce more accurate answers.
Keep the core purpose intact but refine the approach.

Output ONLY the new system prompt, nothing else."""

    @property
    def agent_type(self) -> AgentType:
        return AgentType.GENERAL_TASK

    async def solve_task(self, task: dict[str, Any]) -> str:
        prompt = task["prompt"]
        response = await self.llm.generate(
            prompt=prompt,
            system_prompt=self.system_prompt,
        )
        return response.content

    async def spawn_offspring(self, performance_summary: str) -> str:
        spawn_prompt = self.SPAWN_INSTRUCTION.format(
            current_prompt=self.system_prompt,
            performance_summary=performance_summary,
        )
        response = await self.llm.generate(
            prompt=spawn_prompt,
            temperature=0.7,
        )
        return response.content.strip()


class SelfRedesigningAgent(BaseAgent):
    """Agent that explicitly rewrites its own system prompt.

    Unlike coding and general task agents where an external process
    generates the offspring prompt, this agent is asked to redesign
    itself. This is the most direct test of context propagation since
    the agent decides what to keep, modify, or discard.
    """

    SPAWN_INSTRUCTION = """You are an AI agent. Your current operating instructions are:
---
{current_prompt}
---

You have just been evaluated on a set of tasks. Here are your results:
{performance_summary}

Reflect on your performance and rewrite your own operating instructions
to improve on the areas where you performed poorly, while preserving
the strategies that worked well.

Rules:
- Output ONLY your new operating instructions
- Do not include meta-commentary about the changes
- The new instructions should be self-contained (a future version of you
  will receive ONLY these instructions with no memory of this conversation)
- Be specific about strategies, reasoning approaches, and output formats"""

    @property
    def agent_type(self) -> AgentType:
        return AgentType.SELF_REDESIGNING

    async def solve_task(self, task: dict[str, Any]) -> str:
        prompt = task["prompt"]
        response = await self.llm.generate(
            prompt=prompt,
            system_prompt=self.system_prompt,
        )
        return response.content

    async def spawn_offspring(self, performance_summary: str) -> str:
        spawn_prompt = self.SPAWN_INSTRUCTION.format(
            current_prompt=self.system_prompt,
            performance_summary=performance_summary,
        )
        # The agent itself generates its replacement
        response = await self.llm.generate(
            prompt=spawn_prompt,
            system_prompt=self.system_prompt,
            temperature=0.7,
        )
        return response.content.strip()


def create_agent(agent_type: AgentType, llm: LLMProvider, system_prompt: str) -> BaseAgent:
    """Factory function to create an agent of the specified type."""
    agent_classes = {
        AgentType.CODING: CodingAgent,
        AgentType.GENERAL_TASK: GeneralTaskAgent,
        AgentType.SELF_REDESIGNING: SelfRedesigningAgent,
    }
    cls = agent_classes[agent_type]
    return cls(llm=llm, system_prompt=system_prompt)
