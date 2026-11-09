# Review and publication checklist

1. Run the fast unit, geometry and privacy/conformance checks in the README.
2. Review the allowlisted file list and source licenses. Do not stage artifacts, private references, browser logs or recordings.
3. Build a new named ZIP with `python tools/release.py --package dist/my-review.zip`. Existing files are refused.
4. Run `python tools/verify_package.py dist/my-review.zip`. Extracted consumer verification requires no Git. Compare the external SHA-256 before installation.
5. Obtain owner approval. Confirm publisher identity, support information and published privacy policy before public listing.
6. Push only the approved feature branch, review a PR and separately authorize merging/publication. Local preparation does not publish anything.

The root portable Agent Plugins 1.0.0 manifest uses `skills/` and `extensions.com.openai`. This repository-oriented skill sets `requires_local_executor: true`, per [desktop-only guidance](https://developers.openai.com/plugins/deploy/desktop-only). No MCP server or lifecycle hook is bundled.

[Official package format](https://developers.openai.com/plugins/build/plugins), [skills](https://developers.openai.com/plugins/build/skills), [submission](https://developers.openai.com/plugins/deploy/submission) and [guidelines](https://developers.openai.com/plugins/plugin-guidelines) were checked for this pass. Skills-only packages do not need MCP review cases. Local format checks are not portal validation, approval or publisher verification. The public author attribution is recorded in plugin.json; official publisher verification remains a separate step. Owner contact and URLs must not be invented.

The 8 MiB content and 2 MiB member limits are project safeguards, not asserted portal limits. Keep the submission dashboard's current requirements authoritative. A privacy policy must accurately describe the published distribution and any selected external tools.
