# Editorial image selector and spatial card world

Independent technical reconstruction from a locally inspected reference. Source media, platform identities, brands and frame captures remain private. Approximate times describe the recording, which may start mid-page or loop; they are not a specification of source code or easing.

## Creative objective
Use one coherent image world to move from attention to selectable content, rather than repeating the same project gallery twice.

## Visual description
The recording includes a row of portrait cards, a changing full-bleed editorial image selector, images spread around a central workspace and later cards turning into a readable row.

## Temporal sequence and key moments
0–2s: portrait cards; 2–5s: a workspace view and cards changing spatial arrangement; 5–7s: full-bleed image/theme selection; 7–10s: image-to-card transition and numbered card row; 10–12s: a larger image collage; remaining seconds revisit preceding material.

## Motion and camera
The footage alternates between a person filming a monitor and a demonstrated UI. Film edits are not proof that every apparent transition is a continuous website camera.

## Implementation
Keep a lead DOM card persistent through group rotation and individual separation, with a diagonal shared axis. A selector should serve real categories, services or professional experience, not a redundant theme toy. Use different meaningful images for biography/capabilities versus selected projects. On a portfolio, preserve factual content and actual project links.

## Interaction
Native scroll drives the card world; selecting a card opens details or a real route. Keep a static catalogue/experience list as an equivalent path. Do not gate essential navigation behind a visual orbit.

## Responsive adaptation
Use one foreground card, partial neighbours and a separate text zone. Maintain lead-card identity through the handoff; outgoing and incoming cards move simultaneously rather than pause at a stack.

## Accessibility
Reduced motion uses ordinary cards/experience content. Keyboard focus must remain visible and reach all destinations; a hidden offscreen card needs an equivalent visible path.

## Performance
Pool only necessary layers, avoid duplicating large project images and cache geometry. Do not add per-frame layout reads or a large 3D engine for a DOM fan.

## Validation
Check card identity, diagonal axis, text overlap, duplicate project imagery, actual selection, reverse/jump and mobile touch. Original fan demo and anchor helper are independent teaching assets.

Original explanatory storyboard: `assets/storyboards/editorial-card-world.svg`, relative to the skill root. The simple shapes explain the mechanism; they are not production assets claiming photographic fidelity. For tested independent examples see `assets/examples/`; reuse ideas, not a fixed page design.
