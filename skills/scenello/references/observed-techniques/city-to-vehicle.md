# Continuous city descent into vehicle follow

Independent technical reconstruction from a locally inspected reference. Source media, platform identities, brands and frame captures remain private. Approximate times describe the recording, which may start mid-page or loop; they are not a specification of source code or easing.

## Creative objective
Convert a city-scale establishing view into a close moving subject without a disconnected scene cut.

## Visual description
A nighttime skyline becomes a descending view along a tall building, then a street-level vehicle follow and showroom inventory. Typography alternates with the moving environment.

## Temporal sequence and key moments
The 28.5-second capture begins in later catalogue content. Around 7–11s a large title returns; approximately 11–16s the city/building descent reaches the street; 16–21s follows a vehicle toward close detail; 21–28s moves through illuminated vehicle catalogue scenes. A platform login overlay appears at the end.

## Motion and camera
The defining mechanism is one camera trajectory whose height decreases while its target transfers from building to vehicle. Exact lens, geometry and asset method are not observable from this recording.

## Implementation
Author a continuous camera spline with velocity and target-tangent continuity. Place car motion in world coordinates with wheel-ground contact. A 2.5D alternative needs photographic depth layers, occlusion masks, a limited reveal cone and a separate vehicle asset; a whole-image zoom cannot reproduce the reference. Authentic neighbourhood geometry requires real reference research, varied roofs, believable scale and occupied streets, not mirrored repeated blocks.

## Interaction
Scroll drives both camera and car from a shared progress state. Make inventory cards and booking/contact controls functional and independently accessible.

## Responsive adaptation
On mobile tighten the viewing cone, simplify peripheral environment and preserve vehicle framing; do not replace the entire spatial passage with a static swipe.

## Accessibility
Provide a static location/vehicle overview and ordinary inventory for reduced motion. Never require a long descent to access booking information.

## Performance
Large world geometry, shadow maps, reflective paint and crowds need explicit budgets. Use instancing selectively without obvious repeated silhouettes; pause hidden scenes.

## Validation
Inspect horizon/roof repetition, camera clipping, street occupancy, light moving across the car, tire contact, continuous forward/reverse movement and live destinations.

Original explanatory storyboard: `assets/storyboards/city-to-vehicle.svg`, relative to the skill root. The simple shapes explain the mechanism; they are not production assets claiming photographic fidelity. For tested independent examples see `assets/examples/`; reuse ideas, not a fixed page design.
