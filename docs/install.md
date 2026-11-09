# Installation and host status

## Codex: project-scoped copy

Run the root README's installer from a reviewed checkout. Default dry run; `--apply` writes only to the explicitly selected project's `.agents/skills/scenello`. Existing folders cause failure. The entire canonical folder, including examples, references and its MIT license, is copied. No symlink or global configuration is created.

Current official [skill discovery](https://learn.chatgpt.com/docs/build-skills) describes `.agents/skills` from working directory to repository root. Invoke `$scenello` in Codex. If changes are not discovered, restart the host; inspect the skills selector before claiming success. Avoid installing duplicate same-name copies. Installed-path tests exercise file integrity and refusal to overwrite. An isolated Codex app-server discovery run found the skill enabled with zero parse errors and correct UI metadata. The independent forward task explicitly read it; implicit model activation remains unverified.

## Update

Review a new release diff and checksums. Archive your old `scenello` folder outside discovery locations, then run the installer again. Do not overwrite local changes blindly. The tool deliberately does not implement destructive update or uninstall commands.

## Uninstall

Close sessions using the skill and remove only the project-local `scenello` folder you installed, after checking its resolved path and preserving local modifications. No MCP connections, global settings, remote files or project website files need changing.

## Claude Code: prepared, untested adapter

The same canonical folder can be copied with `--agent claude --apply` into `.claude/skills/scenello`. Official [Claude Code skills](https://code.claude.com/docs/en/skills) describe this directory and `/scenello` invocation. Its permission/tool model remains the host's. No duplicated knowledge library or Claude-specific preapproved tools are bundled. Claude CLI was unavailable here, so discovery, execution and behavioral compatibility are **untested**. Do not label this supported until an independent install/activation/task/cleanup run succeeds.

Other agents: open-standard format only, untested. No implicit claim that all Agent Skills hosts behave identically.

## Plugin distribution

Root `plugin.json` uses portable Agent Plugins 1.0.0; `skills/` is discovered automatically. OpenAI presentation is namespaced under `extensions.com.openai`. A verified publisher and human review are still required for directory publication. No account is connected by local installation. See release.md; do not confuse an API skill upload with a local Codex install.
