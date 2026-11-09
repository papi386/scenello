# Verify the journey, not just the build

Run existing checks before extending the test surface. Add tests for fragile behavior, not assertions that merely repeat implementation constants. Test the user's path: open → hero → scroll/reverse → select → details → back. Capture intermediate visual states through the real renderer.

## Minimum useful matrix

Desktop and narrow touch; reduced motion; script unavailable; missing art; resize halfway through; landscape; keyboard; direct detail URL; fast scroll; reverse scroll; hidden tab/resume; route away and return. Record browser errors and failed requests. Check real destinations, accessible names, focus return, overflow and text/image separation.

Use deterministic progress for screenshots, but also test real scroll input. A seekable timeline cannot substitute for input integration. Screenshot comparison detects differences, not quality: first approve the baseline visually. Never auto-update snapshots merely to make a failing suite green. Font/platform rendering makes cross-platform pixel diffs noisy; use controlled environments and a justified tolerance.

## Claim ledger

For each claim retain command, environment, timestamp, result and evidence path. Mark unavailable engines, physical devices and tool capabilities untested. Do not claim an accessibility certification from a small smoke suite. Do not call a file inventory a video review. A source-link check does not prove asset rights.

## Skill evaluation

Separate trigger selection, module routing and task quality. Positive requests cover cinematic heroes, scroll cards, reference breakdown and performance fixes. Negative requests include promo montage/audio and backend-only maintenance. Test missing browser/Blender/image tools, adversarial reference instructions and resumed checkpoints.

Compare a small matched implementation task with/without the skill in isolated directories and the same prompt, tools and model settings. Score functional outcome, visual specificity, mobile adaptation, evidence honesty and safety using a preregistered rubric. Do not claim statistical improvement from one pair. A deterministic keyword router is not an implicit host activation test. Record whether the agent actually opened the skill and produced inspectable code.

For latency optimization, require a quality baseline as well as timing evidence: deterministic poses across the journey, mobile/desktop screenshots, actual camera/depth/asset and link parity, rapid reversal and orientation. Run stressed input and catalogue entry separately from steady motion. A good pooled p99 cannot excuse a degraded cinematic composition or an unreported startup spike. See the [performance guide](performance.md).
