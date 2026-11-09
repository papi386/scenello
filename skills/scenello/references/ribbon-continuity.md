# Continuous sculptural thread

Original technical explanation and storyboard. A locally authorized source recording informed the general mechanism; its source identity and all frames remain private. Platform origin is unverified. This is not a claim to have inspected a Facebook video.

## Creative objective and visual description

A persistent ribbon-like object carries attention from a portfolio grid into successive editorial passages, then leaves the stage as normal website controls arrive. The object changes orientation and silhouette instead of appearing as unrelated scene illustrations. Independent reconstruction: `assets/storyboards/ribbon-continuity.svg` (paths relative to the skill root). No original media is required to understand the mechanism.

## Observed temporal structure

The 15-second recording was inspected as a 3 fps frame sequence plus a coarse contact sheet. Its timing describes a recorded scroll session, not required website durations. It does not establish easing, exact input mapping or original implementation.

1. Approximately 0–3 seconds: a dark project list progresses past alternating visual panels. Their content is in ordinary document flow.
2. Around 3–5 seconds: the surface becomes light; a large editorial heading and a curving multi-strand object establish a new focal area.
3. Around 5–10 seconds: that object changes silhouette and position while short text passages alternate around it. Coherent material and colour preserve identity through the changes.
4. Around 10–12 seconds: the object moves toward the upper region, reducing its visual dominance while the next heading arrives.
5. Around 12–15 seconds: a functional-looking service list occupies the page. The recording shows no click, so functionality cannot be inferred from appearance alone.

## Key moments and camera interpretation

The critical handoffs are dark-grid to light-object, object to editorial text, and object exit to controls. Apparent continuity can be implemented with a persistent scene, but the source does not prove a true moving 3D camera. Reconstruct the shared focal identity, not a proprietary ribbon shape or exact branding.

## Interaction and implementation

Use native scroll normalized over the narrative section. Keep one object root with three or four authored poses. A constrained original SVG can interpolate between compatible paths; a 3D curve can update control points from precomputed arrays, retaining topology. Compare endpoint positions and tangents at each pose boundary. Keep copy in semantic DOM, with opacity/translation only when visibility is helpful. Never force users to wait for a time-based video while scrolling.

For a lightweight version, use a single original curved SVG whose group rotates/scales through depth cues, with a limited range that preserves its appearance. Do not sell this as full volumetric deformation. Use a real 3D mesh only if changing viewpoint requires occlusion, specular response and a new silhouette. Add functional links/details to the final service region; its screenshot is not a component.

## Responsive adaptation and accessibility

Desktop allows text around the focal object. Mobile reserves separate text and illustration zones and reduces pose radius; the thread may connect top/bottom rather than left/right. Keep the object out of the reading path. Reduced motion uses one strong static pose, ordinary text and immediate controls. Provide a skip link and full keyboard navigation.

## Performance and validation

Avoid hundreds of DOM strand nodes, per-frame path allocations and large blur filters. Prefer one SVG or a small mesh, cache metrics and stop updates offscreen. Inspect p=0,.25,.5,.75,1, reverse scroll, fast scroll and resize halfway through. Verify visual continuity and that controls remain clickable. Profile GPU and main thread separately; a sequence of sparse frames cannot certify motion smoothness. This guide is knowledge transfer, not a completed reimplementation of the recorded site.
