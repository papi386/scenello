# A continuous journey has one spatial contract

Define a normalized scene with x/y in [0,1], a depth unit relative to the scene width, and explicit focal anchors. Establish what is fixed: camera, object or screen plane. Avoid independently animated layers that imply contradictory camera moves.

## Sequence and ownership

Use one progress source and a deterministic `render(progress, metrics)` function or one library timeline. Example normalized beats: 0–.18 establish; .18–.5 anticipation/approach; .5–.65 contact or reconfiguration; .65–1 inherit the focal object into the next section. These are starting points, not mandatory timings. Scroll must remain reversible and tolerate a single large scroll jump. Do not chain setTimeout calls or add wheel-event blocking to create suspense.

Read geometry on initialization/resize, then write transforms in one requested frame. A passive scroll listener schedules one rAF, not a perpetual loop. Stop offscreen rendering; visibility changes must not advance a hidden simulation. Do not add smoothing that leaves the viewport lagging behind fast touch input.

CSS scroll timelines can avoid JS ownership but require actual feature checks and a useful static fallback. Existing GSAP ScrollTrigger can own pinning and responsive cleanup; do not install GSAP merely for two transforms. In React use scoped lifecycle cleanup and account for Strict Mode's repeated setup.

## Shared-element handoff

Keep the focal object alive through both stages. Let scale, position and orientation converge onto its destination at the same progress where neighbouring objects separate. Compare positions and finite-difference velocity on either side of a stage boundary: no discontinuity, dead plateau or velocity reversal unless intentional. Avoid opacity-swapping unrelated screenshots and calling it a camera move.

For a contact gesture, each layer has an authored anchor (ax,ay) in its asset coordinates. For the intended contact C, use translation T = C − M·anchor, with M the layer's scale/rotation matrix. Derive the transform, do not adjust random viewport pixel offsets. At reveal, verify both rendered anchors and inspect the anatomy; matching markers cannot prove fingertips match a badly annotated asset.

`assets/contact-anchor.mjs` is an optional original pure helper. Pass the untransformed displayed image size in scene pixels, its normalized fingertip anchor, the target contact in the same parent scene, and rotation/scale. Apply the returned CSS matrix with `transform-origin: 0 0`. Recompute metrics on resize, not every frame. If an image uses object-fit cropping, first map the asset anchor through that crop; do not pass source dimensions as displayed dimensions. The helper tests mathematical alignment, not photographic annotation accuracy or realistic articulation.

## Hero to functioning content

Progressive enhancement leaves headings, links and details in document flow without script. Add pinning only after initialization succeeds. Keep skip navigation outside animated layers. A hero may zoom into a catalogue, but the catalogue remains semantic links, not a canvas recording. Original optical demo uses a ring's expansion to frame a DOM research list; the material demo turns a card fan into selectable samples.

## Failure cases to capture

At p=0,.2,.5,.7,1 inspect overflow, focal point, intermediate readability and stacking. Resize at .5; reverse to .2; jump to 1; navigate back. A seek API in test builds should control the same renderer, never a separate fake screenshot implementation.

Paths beginning `assets/` are relative to the Scenello skill directory, alongside SKILL.md.

## Entrance readiness and the visible handoff

Give each transform one owner. Wait for the protagonist image to decode or for the first usable 3D render before starting its timed entrance; render a readable poster while waiting. A second shutter, CSS animation or resize handler can conceal or cancel the primary movement. Test a fresh context from navigation, then reload, deep link and back. Start timing from actual readiness, not module import. Any session suppression needs a documented rationale and an appropriate replay path; it must not suppress the entrance for every ordinary visit.

For an architectural reveal, a close detail can pull back into a framed image that becomes a real project link. For a product, move a camera rig along a meaningful material landmark before handing local rotation to the visitor. For a spatial journey, preserve a filament or object across both chapter boundaries. For a graphic interface, transform the actual poster into its program slot. These are mechanism choices, not mandatory layouts.

Scroll-driven means position determines state: stopping holds it, reverse restores it, and a large delta lands correctly. A one-shot IntersectionObserver tween is only a supporting reveal. Use GSAP scrub/pin with matchMedia and refresh when already appropriate, or a single request-driven renderer with cached geometry. Never let a drag controller and scroll controller overwrite the same rotation. Separate camera rig and local object rotation, or make ownership explicit.

Verify initial, quarter, midpoint, three-quarter and final states through the same live timeline, plus normal wheel/touch playback. Generic opacity changes alone do not satisfy a requested cinematic transformation. Keep reading zones outside the moving image footprint.
