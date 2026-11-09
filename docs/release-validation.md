# 0.5.0-rc2 focused validation

Executed 2026-11-09 on Windows, Python 3.14, existing Node and Codex CLI 0.167.0-alpha.3.2. No dependencies installed and no new website/performance campaign.

- PASS: 56 Python unit tests in 25.952 seconds. Covers source routing, archive risks, audit redaction/timeout retention, fonts, installation non-overwrite, unexpected ZIP members, checksums and extracted verification without Git.
- PASS: 2 geometry tests (`node --test tests/geometry.test.mjs`).
- PASS: source privacy/provenance and manifest checks, including all canonical guide links.
- PASS: actual Codex app-server discovery of one enabled Scenello skill, zero parse errors.
- Explicit workflow use: canonical skill read in this assisted session. Independent model invocation, implicit and negative host selection remain UNVERIFIED; previous isolated authentication failures retained. Lexical routing negative tests passed and are not model activation tests.
- Claude: executable unavailable, NOT TESTED. No universal host support claim.
- No executable uninstaller exists. Documented uninstall only removes the checked project-local skill folder. Installer tests verify non-overwrite and preservation of unrelated project content; no global configuration mutations.
- CI workflow is present. Local checks passed; remote CI/branch protection NOT TESTED and nothing pushed.
- Current source Git history had zero revisions before the authorized initial review commit. Allowlisted staged paths must match the scanned payload before committing.

The package scanner is heuristic, not security certification. Original code/guides/diagrams are MIT; bundled font derivatives are OFL-1.1 with notices and verified asset hashes. No third-party runtime library, MCP server, lifecycle hook, telemetry or private source media is bundled. Existing optional host/build tools are outside the payload; no comprehensive vulnerability claim about those external tools is made.

One reporting error occurred after geometry tests passed: the Windows console could not print a Unicode checkmark. The audit retained the test result; only remaining checks were resumed. A generated browser log was preserved under ignored private artifacts, without weakening the source allowlist.

Official plugin structure and desktop metadata were checked against the linked official sources in release.md. Portal validation, publisher verification, support/privacy listing details and owner approval remain pending. Historical demo evidence is not new artistic approval.
