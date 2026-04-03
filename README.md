# Big Bro MCP

**Made and maintained by [The A-Tech Corporation PTY LTD](https://a-tech.com.au).**

## The Problem

You're building something. You hit a wall. The problem is too hard for your current model to solve alone.

Most developers would quit. Or ship a half-baked solution.

But you don't have to.

## The Solution

Big Bro MCP lets your AI call in backup. When stuck, it escalates to a more capable model — someone with deeper reasoning, more context, and better problem-solving.

Think of it like having a senior engineer on speed dial. Except the senior engineer is Claude Opus, GPT-4o, or whatever the best model is right now.

## What You Get

| Feature | Benefit |
|---------|---------|
| **3 Providers** | OpenAI, Anthropic, OpenRouter — pick the best tool for the job |
| **2 Escalation Modes** | Ask a question OR hand off the entire task |
| **Zero Friction** | Install, configure keys, done |

## Installation

**Step 1:** Install dependencies
```bash
pip install -r requirements.txt
```

**Step 2:** Configure API keys
```bash
cp .env.example .env
# Edit .env and add your key(s)
```

You only need ONE provider to work. But having options is better.

| Provider | Get Key From |
|----------|--------------|
| Anthropic | https://console.anthropic.com/settings/keys |
| OpenAI | https://platform.openai.com/api-keys |
| OpenRouter | https://openrouter.ai/keys |

## How To Use

### Run The Server

```bash
# For local MCP clients (Claude Code, etc.)
python big_bro_mcp.py

# For remote clients
python big_bro_mcp.py --transport http --host 0.0.0.0 --port 8000
```

### Add To Claude Code

Edit `~/.claude/settings.json`:

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

## The Tools

### `ask_big_bro` — When You're Stuck On Something Specific

Use this when you hit a problem that needs deeper reasoning.

**Example:**
> "I've been debugging this regex for 20 minutes. It's not matching the email format correctly. Here's what I've tried..."

**Parameters:**
- `question` — The problem. Be specific. Include what you've already tried.
- `provider` — Which model to use (default: anthropic)
- `model` — Specific model (optional — uses best default)
- `system_prompt` — Custom context (optional)

---

### `escalate_task` — When You Need To Hand Off The Whole Thing

Use this when the problem is too big for a simple question.

**Example:**
> "Task: Build a custom auth middleware from scratch. Context: I've tried Express middleware, Passport, and Auth0. Here's the error I'm getting..."

**Parameters:**
- `task_description` — What needs to be done
- `context` — Everything you've tried, current state, errors, constraints
- `provider` — Which model to use (default: anthropic)

---

### `get_available_providers` — Check Your Setup

Returns which providers are configured and their default models.

## Default Models

| Provider | Default Model |
|----------|---------------|
| Anthropic | claude-sonnet-4-6-20250929 |
| OpenAI | gpt-4o |
| OpenRouter | anthropic/claude-sonnet-4-6-20250929 |

## When To Use Big Bro

| Situation | Action |
|-----------|--------|
| Complex reasoning beyond your capabilities | `ask_big_bro` |
| Specialized domain knowledge needed | `ask_big_bro` |
| Need deeper analysis or longer context | `ask_big_bro` |
| Entire task is too big to handle | `escalate_task` |
| Want a fresh perspective from a stronger model | Either |

## The Point

Most people give up when they hit a wall.

Big Bro MCP removes the wall.

You don't have to be the smartest person in the room. You just need to know when to ask for help.

---

## License

MIT
