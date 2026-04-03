"""
Big Bro MCP Server

Allows LLMs to call upon larger models (OpenAI, Anthropic, OpenRouter) when stuck on tasks.
"""

import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from typing import Literal

# Import official SDKs
from anthropic import AsyncAnthropic
from openai import AsyncOpenAI

# Load environment variables from .env file (override existing)
load_dotenv(override=True)

# Initialize the MCP server
mcp = FastMCP(
    name="Big Bro",
    instructions="Escalate complex tasks to more capable AI models when needed."
)


def _get_api_key(provider: Literal["openai", "anthropic", "openrouter"]) -> str:
    """Get API key for the specified provider."""
    key_map = {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "openrouter": "OPENROUTER_API_KEY",
    }
    env_var = key_map.get(provider)
    if not env_var:
        raise ValueError(f"Unknown provider: {provider}")

    api_key = os.getenv(env_var)
    if not api_key:
        raise ValueError(
            f"{env_var} not set. Please set this environment variable "
            f"before using the {provider} provider."
        )
    return api_key


def _get_default_model(provider: Literal["openai", "anthropic", "openrouter"]) -> str:
    """Get default model for the specified provider."""
    if provider == "anthropic":
        return "claude-sonnet-4-6-20250929"
    elif provider == "openai":
        return "gpt-4o"
    elif provider == "openrouter":
        return "qwen/qwen3.6-plus:free"
    raise ValueError(f"Unknown provider: {provider}")


@mcp.tool
async def ask_big_bro(
    question: str,
    provider: Literal["openai", "anthropic", "openrouter"] = "anthropic",
    model: str | None = None,
    system_prompt: str | None = None,
) -> dict:
    """
    Ask a more capable AI model for help when stuck on a complex task.

    Use this tool when you encounter a problem that requires deeper reasoning,
    specialized knowledge, or capabilities beyond your current scope.

    Args:
        question: The question or problem you need help with. Be specific and include
                  all relevant context about what you've tried and where you're stuck.
        provider: The AI provider to use. Options: openai, anthropic, openrouter.
                  Default is anthropic.
        model: Specific model to use. If not specified, uses default powerful model
               for each provider (claude-sonnet-4-6 for Anthropic, gpt-4o for OpenAI,
               or a top model on OpenRouter).
        system_prompt: Optional system prompt to set context for the response.

    Returns:
        A dictionary containing the model's response and metadata.
    """
    try:
        api_key = _get_api_key(provider)
        
        if model is None:
            model = _get_default_model(provider)

        if system_prompt is None:
            system_prompt = (
                "You are 'Big Bro' - a highly capable AI assistant helping another AI "
                "that has encountered a challenging problem. Provide clear, detailed, "
                "and actionable guidance. The requesting AI will use your response to "
                "complete their task."
            )

        if provider == "anthropic":
            client = AsyncAnthropic(api_key=api_key)
            response = await client.messages.create(
                model=model,
                max_tokens=4096,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": question}
                ]
            )
            answer = response.content[0].text if response.content else ""
            usage = {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            }

        elif provider == "openai":
            client = AsyncOpenAI(api_key=api_key)
            response = await client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                max_tokens=4096
            )
            answer = response.choices[0].message.content or ""
            usage = {
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens,
            }

        elif provider == "openrouter":
            # OpenRouter is compatible with OpenAI SDK
            client = AsyncOpenAI(
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1",
                default_headers={
                    "HTTP-Referer": "https://github.com/big-bro-mcp",
                    "X-Title": "Big Bro MCP",
                }
            )
            response = await client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                max_tokens=4096,
            )
            answer = response.choices[0].message.content or ""
            usage = {
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens,
            }
        else:
            raise ValueError(f"Unknown provider: {provider}")

        return {
            "provider": provider,
            "model": model,
            "answer": answer,
            "usage": usage,
        }
    except Exception as e:
        import traceback
        return {
            "error": True,
            "error_type": type(e).__name__,
            "error_message": str(e),
            "provider": provider,
            "model": model,
            "debug_api_key_length": len(api_key) if 'api_key' in dir() else 'api_key not set',
            "debug_api_key_prefix": api_key[:15] + '...' if 'api_key' in dir() and api_key else 'None',
            "debug_traceback": traceback.format_exc(),
        }


@mcp.tool
async def escalate_task(
    task_description: str,
    context: str,
    provider: Literal["openai", "anthropic", "openrouter"] = "anthropic",
) -> dict:
    """
    Escalate a complete task to a more capable AI model.

    Use this when you need to hand off an entire task rather than just asking
    a specific question. This provides the full context and lets the bigger
    model handle the complete implementation.

    Args:
        task_description: Clear description of what needs to be accomplished.
        context: All relevant context including what you've tried, current state,
                 code snippets, error messages, and any constraints.
        provider: The AI provider to use. Default is anthropic.

    Returns:
        A dictionary containing the model's complete response and metadata.
    """
    full_prompt = f"""TASK ESCALATION

Task: {task_description}

Context and Current State:
{context}

---
Please provide a complete solution to this task, including any necessary code,
explanations, and next steps. Be thorough and actionable."""

    result = await ask_big_bro(
        question=full_prompt,
        provider=provider,
        system_prompt=(
            "You are 'Big Bro' - a highly capable AI assistant. Another AI has "
            "escalated a complete task to you because it requires capabilities "
            "beyond their scope. Provide a comprehensive, complete solution with "
            "all necessary code, explanations, and clear next steps. Don't hold back - "
            "give the full implementation."
        )
    )
    
    # Add task metadata to result
    result["task_description"] = task_description
    return result


@mcp.tool
def get_available_providers() -> dict:
    """
    Get information about available AI providers and their default models.

    Returns:
        Dictionary with provider information and default model configurations.
    """
    return {
        "providers": {
            "anthropic": {
                "description": "Anthropic Claude models - excellent for reasoning and code",
                "default_model": "claude-sonnet-4-6-20250929",
                "env_var": "ANTHROPIC_API_KEY",
                "configured": bool(os.getenv("ANTHROPIC_API_KEY")),
            },
            "openai": {
                "description": "OpenAI GPT models - strong general capabilities",
                "default_model": "gpt-4o",
                "env_var": "OPENAI_API_KEY",
                "configured": bool(os.getenv("OPENAI_API_KEY")),
            },
            "openrouter": {
                "description": "OpenRouter - access to multiple providers through one API",
                "default_model": "anthropic/claude-sonnet-4-6-20250929",
                "env_var": "OPENROUTER_API_KEY",
                "configured": bool(os.getenv("OPENROUTER_API_KEY")),
            },
        }
    }


if __name__ == "__main__":
    mcp.run()
