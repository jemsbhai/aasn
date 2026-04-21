# AASN: Autonomous Agent Synthesis Network

A unified framework for automated multi-agent generation, semantic discovery, and cross-protocol coordination.

## Overview

AASN synthesizes Anthropic's Model Context Protocol (MCP), Google's Agent-to-Agent (A2A) protocol, and Google's Agent Development Kit (ADK) into a cohesive framework enabling:

- **Automated agent generation** from natural language task specifications
- **Semantic agent discovery** scaling to millions of agents
- **Cross-protocol interoperability** bridging MCP, A2A, and ADK ecosystems
- **Continual agent evolution** via modular skill transfer

## Project Structure

```
aasn/
├── src/aasn/          # SDK package
│   ├── core/          # Base agent, capability, workflow abstractions
│   ├── dna/           # Agent DNA representation
│   ├── registry/      # Discovery and registration
│   ├── compiler/      # Task-to-agent compilation
│   ├── adapters/      # MCP, A2A, ADK protocol adapters
│   ├── evolution/     # Evolution engine
│   ├── plugins/       # Plugin system
│   ├── testing/       # Test utilities
│   └── observability/ # Tracing, metrics
├── experiments/       # Research experiments
├── papers/            # Conference and journal papers
├── tests/             # Test suite
├── examples/          # Reference implementations
└── docs/              # Documentation
```

## Installation

```bash
pip install aasn-sdk
```

With optional dependencies:

```bash
pip install aasn-sdk[mcp]           # MCP adapter
pip install aasn-sdk[a2a]           # A2A adapter
pip install aasn-sdk[adk]           # ADK adapter
pip install aasn-sdk[observability] # OpenTelemetry, Prometheus
pip install aasn-sdk[all]           # Everything
```

## Quick Start

```python
from aasn import Agent, capability

@Agent(name="research_assistant", model="gemini-2.0-flash")
class ResearchAgent:
    @capability(description="Search academic papers on arXiv")
    async def search_papers(self, query: str, max_results: int = 10):
        return await self.mcp.search_arxiv(query, limit=max_results)
```

## Development Setup

```powershell
# Clone the repo
git clone https://github.com/jemsbhai/aasn.git
cd aasn

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install in development mode
pip install -e ".[dev,all]"

# Run tests
pytest tests/ -v
```

## Status

**Pre-alpha.** Under active development. See `CHANGELOG.md` for progress.

## License

Apache 2.0. See `LICENSE` for details.
