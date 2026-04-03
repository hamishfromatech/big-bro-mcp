# Big Bro MCP

An MCP server that allows LLMs to call upon larger, more capable models when they get stuck on complex tasks.

**Made and maintained by [The A-Tech Corporation PTY LTD](https://theatechcorporation.com).**

## Features

- **Three Provider Support**: OpenAI, Anthropic, and OpenRouter
- **Two Escalation Modes**:
  - `ask_big_bro`: Ask a specific question to a more capable model
  - `escalate_task`: Hand off an entire task with full context
- **Automatic Fallback**: If one provider isn't configured, use another

## Installation

1. Clone or navigate to this directory

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure API keys (at least one required):
   ```bash
   cp .env.example .env
   # Edit .env and add your API key(s)
   ```

## Configuration

Set the following environment variables (in `.env` or your shell):

| Variable | Provider | Get Key From |
|----------|----------|--------------|
| `ANTHROPIC_API_KEY` | Anthropic Claude | https://console.anthropic.com/settings/keys |
| `OPENAI_API_KEY` | OpenAI GPT | https://platform.openai.com/api-keys |
| `OPENROUTER_API_KEY` | OpenRouter (multi-provider) | https://openrouter.ai/keys |

## Usage

### Running the Server

```bash
# Stdio transport (for local MCP clients like Claude Code)
python big_bro_mcp.py

# HTTP transport (for remote clients)
python big_bro_mcp.py --transport http --host 0.0.0.0 --port 8000
```

### Configuring in Claude Code

Add to your `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "big-bro": {
      "command": "python",
      "args": ["/path/to/big-bro-mcp/big_bro_mcp.py"],
      "env": {
        "ANTHROPIC_API_KEY": "your-key-here",
        "OPENAI_API_KEY": "your-key-here",
        "OPENROUTER_API_KEY": "your-key-here"
      }
    }
  }
}
```

### Available Tools

#### `ask_big_bro`

Ask a more capable AI model for help when stuck on a complex task.

**Parameters:**
- `question` (string): The question or problem you need help with
- `provider` (string): Provider to use - "openai", "anthropic", or "openrouter" (default: "anthropic")
- `model` (string, optional): Specific model to use (uses provider default if not specified)
- `system_prompt` (string, optional): Custom system prompt for context

**Example:**
```
I'm stuck on this regex pattern. Can you help me understand why it's not matching?
[provides context]
```

#### `escalate_task`

Escalate a complete task to a more capable AI model.

**Parameters:**
- `task_description` (string): Clear description of what needs to be accomplished
- `context` (string): All relevant context including what you've tried, current state, code, errors
- `provider` (string): Provider to use (default: "anthropic")

**Example:**
```
Task: Implement a custom authentication middleware
Context: I've tried X, Y, Z but keep getting this error... [full details]
```

#### `get_available_providers`

Get information about configured providers and their default models.

## Default Models

| Provider | Default Model |
|----------|---------------|
| Anthropic | claude-sonnet-4-6-20250929 |
| OpenAI | gpt-4o |
| OpenRouter | anthropic/claude-sonnet-4-6-20250929 |

## When to Use

Use Big Bro when you encounter:
- Complex reasoning problems beyond your capabilities
- Tasks requiring specialized domain knowledge
- Problems that need deeper analysis or longer context windows
- Situations where a fresh perspective from a more capable model would help

## License

MIT
