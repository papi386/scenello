# Terrain passage and route continuity

Independent technical reconstruction from a locally inspected reference. Source media, platform identities, brands and frame captures remain private. Approximate times describe the recording, which may start mid-page or loop; they are not a specification of source code or easing.

## Creative objective
Let a landscape become a navigable journey rather than a decorative background.

## Visual description
A mountain overview alternates with closer terrain views and a visible route. The focal terrain persists while distance, elevation and information density change.

## Temporal sequence and key moments
0–3s: overview/working interface; 3–6s: large landscape title and darkened depth; 6–11s: camera-like approach toward terrain and route; 11–15s: closer relief and viewpoint changes; the final seconds repeat earlier material.

## Motion and camera
Camera elevation and target distance imply a route through space. The recorded monitor and changing UI do not prove the original renderer, projection, exact easing or scroll mapping.

## Implementation
Author a camera spline and a look-at target spline independently. Define terrain scale and an occlusion-safe corridor. If using 2.5D, limit the viewing cone so missing terrain surfaces never appear. Keep route details in linked DOM content and expose a readable route list.

## Interaction
Use normalized route progress and preserve native scrolling. Route stops should be real anchors/details; do not require a recorded camera flight to reach them.

## Responsive adaptation
On mobile reduce the field-of-view change, move annotations into a stable lower reading zone and prioritize the current stop over peripheral labels.

## Accessibility
Use a static route overview and ordinary linked stops for reduced motion. Test route names and controls without relying on colour or hover.

## Performance
Terrain meshes, oversized heightmaps and repeated texture upload can dominate GPU work. Limit texture resolution, reuse geometry and pause offscreen rendering.

## Validation
Check terrain occlusion, camera-ground clearance, reverse travel, direct stop links, resize and low-quality tiers. Diagram positions cannot establish geographic accuracy.

Original explanatory storyboard: `assets/storyboards/terrain-passage.svg`, relative to the skill root. The simple shapes explain the mechanism; they are not production assets claiming photographic fidelity. For tested independent examples see `assets/examples/`; reuse ideas, not a fixed page design.
