# Spatial cards without sacrificing navigation

The card is a real anchor or button with a title and destination. Put motion on a visual wrapper, not on a screenshot masquerading as UI. Keep hit targets aligned with rendered cards. Do not assign every card tabindex=-1 simply because it is offscreen: either retain a linear accessible alternative or reveal focused content deliberately.

## Diagonal orbit / fan handoff

1. Establish the lead card at the front with two or three visible neighbours.
2. Rotate the group around a normalized diagonal vector, e.g. (0.3,0.8,0.15), using rotate3d. Perspective belongs to one shared parent.
3. Begin individual separation before the group rotation ends. The same lead card keeps its identity as it approaches its reading position.
4. Outgoing cards travel behind the axis while the next card approaches. Use z-order based on depth; a numeric index is not a depth model.
5. Settle into a readable catalogue with links. Do not hide the entire collection behind a scroll-only theatre.

Use transform composition in a known order: camera perspective → group transform → card position → local orientation. Reversing these changes the implied pivot. Backface hiding prevents mirrored text but can also make a card unexpectedly disappear. Test the entire turn, not just endpoints.

## Mobile is a composition, not a smaller desktop

Use one legible foreground card and partial neighbours. Reserve a separate text zone. Reduce orbit radius and simultaneous overlap; preserve the turn mechanism. Keep the lead in focus throughout the handoff. Do not replace a requested spatial shuffle with a plain horizontal swipe just because the screen is narrow. Landscape may require a shallower turn and smaller sticky area.

## Inputs and semantics

Native scrolling owns navigation. Keyboard users must reach each sample and details. Touch must retain vertical scrolling and pinch zoom. If a modal is used, native dialog can supply modal behavior; label it, include a close control, return focus and support Escape. Deep-linkable inline detail sections are simpler and work without JS.

## Validation and performance

Capture group mid-turn and single-card entry at 320,390,768,1440 widths. Assert no horizontal document overflow and visible focus. Do not infer readability from bounds alone: inspect pixels. Animate transforms/opacity, not card width/left/top. Limit promoted surfaces and avoid high-resolution duplicated images. Original code demo and storyboard: `assets/examples/materials/`, `assets/storyboards/card-handoff.svg`. Neither contains third-party imagery.

Paths beginning `assets/` are relative to the Scenello skill directory, alongside SKILL.md.

## Shared-image route continuity

A shared View Transition name must be unique in both old and new captures. Clear the previous preview name inside the update callback before assigning the destination image. Await destination image decoding and observe ready rejection/fallback explicitly. A click completing does not prove the shared transition ran. Preserve gallery geometry while it is display:none on a detail route; recompute after unhide before calculating return progress. A hidden gallery measured as distance=1 causes a visible return jump. These are route-state/geometry checks, not reasons to add another animation engine.


For a moving card that becomes a functional layout item, measure and verify the actual border boxes immediately before and after ownership changes. The destination slot must retain the same aspect ratio as the moving artwork; a stale ratio can compress the print on the final frame even when scroll endpoints and links pass. Check both dimensions, center, identity and reading-zone clearance at a near-end progress value and at the exact dock, on desktop and mobile. Keep the real link/button, not an inaccessible visual duplicate. A heading merely entering the viewport is not proof that the card arrived at its destination.
