# Observable action evidence

Normal tasks may use a small opt-in local log: `python scripts/audit.py --directory <explicit-local-folder> --run <id> --event <type> --data <safe-json>`. Do not require this for a trivial card hover. Substantial evaluations need durable streamed tool events, file hashes/patches, decisions and browser evidence.

Record actions as they happen, with UTC time, sequence, actor, phase, source aliases, status and links. Never claim hidden-reasoning access. Do not collect environment values, credentials, cookies, raw private prompts or arbitrary transcripts. Redact before disk; capture scope must be disclosed. A local hash chain detects consistency changes, not authenticity against an attacker able to rewrite the log.

Use supported `codex exec --json` events or app-server item/turn streams. Hooks are project-scoped and opt-in; review current official support and respect exact-definition trust. Never bypass hook trust or install global hooks to obtain evidence. Hosted tools may not pass through local tool hooks. Keep known blind spots explicit.

A timeout must retain prior flushed events and file state, terminate only the supervised process tree and append a linked failure/recovery record. Resume a known run; do not silently replace it. Screenshot/video/diff filenames must be unique per attempt. If logging fails, stop consequential changes, repair the recorder and resume from the last checkpoint.

Browser traces can contain DOM/network data: use fictional/demo inputs and keep them private. Playwright context tracing does not itself capture test assertions; record those outcomes separately. An owner dashboard must be read-only, offline-capable and render log text safely. Retention/deletion is an explicit owner decision, never a hidden cleanup.


## Privacy boundary of streamed agent events

The repaired evaluation supervisor persists event/status/file-change metadata incrementally. Arbitrary shell payloads and aggregated outputs are digest-only because a tool command may contain a confidential inline brief even when no credential pattern matches. Canonical-skill mention is recorded as a boolean, not treated as proof that a successful read occurred. Trusted task-specific wrappers can record reviewed command summaries and redacted file patches separately. State this observation limit rather than silently claiming full tool-text capture. Diagnostic stderr is bounded/redacted; review it locally before sharing. A hash chain establishes local consistency, not provenance authenticity, access control or tamper resistance against a writer who can replace the whole log.

On Windows the supervisor owns a kill-on-close Job Object where permitted; on POSIX it owns a process session. If ownership cannot be established, record best-effort supervision and do not claim isolation. This is process cleanup, not a security sandbox. Authentication failures must remain explicit incomplete runs; never copy personal credentials to make a baseline execute.

Record the PID returned by a process you launch. Diagnose and clean up that owned tree; do not enumerate or persist unrelated applications’ command lines, which may contain credentials or private inline tasks. A failed broad diagnostic is still a failure to preserve and learn from, not a reason to repeat it with elevated access.

Redirect browser diagnostic logs into the owned private evidence directory through the child process environment. Do not weaken a release allowlist when an unexpected root debug log appears: preserve it privately, record the discovery and correct its producer. Raw browser diagnostics are not public skill assets.
