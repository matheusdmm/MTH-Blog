# Agent Instructions

Keep this project as agent-agnostic as possible.

## Rule: Context Maintenance

At the end of every significant task or session, summarize the current state, architectural decisions made, and pending "todo" items into AGENTS.md. Always ensure this file reflects the "ground truth" of the project so future sessions can resume without friction. Use the writeFile tool to overwrite it so the next session starts with current state.

## Rule: Commits

- Always use conventional commits (e.g. `feat:`, `fix:`, `docs:`, `chore:`)
- Never add anything agent related (copilot, claude, etc.) to commit messages or co-authorship
- Committing directly to main is okay in this repo

## Rule: Environment

- Use `/usr/bin/open` (full path) to open files or URLs on macOS — never plain `open`

## Rule: Secrets

- Never commit secrets, config files, or database files

---

## Operational Rules

- **Analysis:** Read files once before writing. Never re-read unless changed. Internalize structure to avoid redundant reads or write-delete-rewrite cycles.
- **Precision:** Prefer targeted edits over full rewrites. No over-engineering.
- **Reasoning:** Thorough internally, concise in output. If uncertain, say so — never hallucinate paths, APIs, or data.
- **Validation:** Test before declaring done. One fix/verify cycle maximum.
- **Directives:** No fluff, openers, or closings. User instructions override all rules.
- **Constraints:** Max 50 tool calls. Single focused pass per task.

---

## Project State

> **Update this section at the end of every significant task or session.**

### Current State
_Describe what the project does and where it currently stands._

### Architecture
_Key architectural decisions, patterns, and structure._

### Pending
_Todo items, known issues, deferred decisions._
