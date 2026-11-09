# Object inspection through camera scale

Independent technical reconstruction from a locally inspected reference. Source media, platform identities, brands and frame captures remain private. Approximate times describe the recording, which may start mid-page or loop; they are not a specification of source code or easing.

## Creative objective
Let a premium object reveal its function through coherent changes in viewing scale.

## Visual description
A vessel moves between open-water context, a side view, near-deck detail and editorial specifications. The hull silhouette connects the views even when the surrounding surface changes.

## Temporal sequence and key moments
0–3s: water/deck context; 3–6s: dark editorial content; 6–10s: isolated vessel grows toward a close view; 10–13s: pullback and deck-angle detail; final seconds revisit earlier positions.

## Motion and camera
A spatial orbit and dolly are plausible reconstruction choices. The monitor recording does not establish whether the source used video, rendered frames or a real-time model.

## Implementation
Choose a single camera rig and preserve hull proportion, horizon and lighting direction. A real model supports large orbits; layered plates support only a narrow cone. If one view is requested, change camera distance and object position within that view rather than inventing multiple angles.

## Interaction
Native scroll owns the inspection timeline. Put technical information and enquiry links in semantic DOM. Stop/deck links must remain useful without a cinematic renderer.

## Responsive adaptation
Mobile prioritizes the recognizable silhouette, limits offscreen bow/stern loss and separates specification text from the moving object.

## Accessibility
Reduced motion uses a strong hero still plus a normal specification list. Do not lock navigation until an orbit finishes.

## Performance
Water reflections, transparent surfaces, texture size and repeated postprocessing are major costs. Start with credible material roughness and simple lighting before effects.

## Validation
Check changing scale, deck/hull continuity, horizon, reverse scroll, details and target links. If asset quality is insufficient, change production strategy openly.

Original explanatory storyboard: `assets/storyboards/vessel-inspection.svg`, relative to the skill root. The simple shapes explain the mechanism; they are not production assets claiming photographic fidelity. For tested independent examples see `assets/examples/`; reuse ideas, not a fixed page design.
