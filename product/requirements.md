# Chat

In-process chat with LLM chatbots. A TUI is the first consumer. Other in-process UIs may be added later; they import the chat port (they are not a second deployable).

## Current slice

**0 — authorities.** Modules exist at the paths in `axes.yaml`, with first members/variants only: OpenRouter, OpenAI-compat, env credentials, text parts, tool-call ADT, in-memory history, model as string, TUI command/stat/presentation placeholders. No `cache` module.

**Next — runnable TUI** that streams from OpenRouter. Still no second provider/protocol/UI, keyring, file history, cache, catalog search, model enum, non-streaming path.

## Frozen

- Product category: chat with LLMs; a TUI exists.
- Always streaming — no `if stream`.
- Model ids are strings the user supplies — no enum of all models.
- Second UI, if any, is in-process against the same Python chat port.

OpenRouter is the first **member** of `providers`, not its own axis. The TUI is the first **use** of `chat-contract`, not a representation of the consumer set.
