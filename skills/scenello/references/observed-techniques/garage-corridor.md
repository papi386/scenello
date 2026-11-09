# Showroom corridor into a catalogue

Independent technical reconstruction from a locally inspected reference. Source media, platform identities, brands and frame captures remain private. Approximate times describe the recording, which may start mid-page or loop; they are not a specification of source code or easing.

## Creative objective
Connect an immersive environment to an ordinary selectable inventory.

## Visual description
A vehicle catalogue alternates with reflective showroom corridors and closer vehicle views. Editorial trust content and inventory cards coexist with the cinematic passage.

## Temporal sequence and key moments
0–4s: editorial/inventory sections; 4–8s: vehicle details and showroom approach; 8–13s: darker vehicle corridor and inspection; 13–18s: doorway/vehicle reveal; final seconds revisit inventory and earlier content.

## Motion and camera
Converging ground lines, repeated lights and object scale imply camera translation. Reflections and environment geometry need to remain consistent during any reconstructed move.

## Implementation
Build an actual camera path with wheel-ground contact and material highlights in world space. Use original licensed assets. A 2.5D version needs separate foreground, floor and distant plates; translating a whole photograph cannot reproduce a long corridor traversal.

## Interaction
Use scroll for the transition, then real linked inventory items with readable availability/specifications. Do not use a screenshot of inventory as the interactive end state.

## Responsive adaptation
On mobile reduce visible inventory neighbours and keep one vehicle silhouette clear. Put filters and specifications outside the animated overlap zone.

## Accessibility
Provide a bypass link and static inventory when motion is reduced or the renderer fails. Keep keyboard focus on usable DOM targets.

## Performance
Limit dynamic lights/reflection passes, instanced repeated fixtures and expensive transparent surfaces. Test fill rate as well as JS cost.

## Validation
Inspect scene seams, wall/ground scale, camera clipping, live card links, reverse scroll and changing viewport aspect ratios.

Original explanatory storyboard: `assets/storyboards/garage-corridor.svg`, relative to the skill root. The simple shapes explain the mechanism; they are not production assets claiming photographic fidelity. For tested independent examples see `assets/examples/`; reuse ideas, not a fixed page design.
