# Botanical product constellation

Independent technical reconstruction from a locally inspected reference. Source media, platform identities, brands and frame captures remain private. Approximate times describe the recording, which may start mid-page or loop; they are not a specification of source code or easing.

## Creative objective
Give a product collection a spatial identity through ingredients that participate in its transitions.

## Visual description
A mobile product page holds a bottle near the centre while botanical elements orbit or move around it. Successive product identities and headings enter as the page is scrolled.

## Temporal sequence and key moments
0–3s: initial product/title; 3–6s: first botanical composition; 6–9s: a different identity enters; 9–12s: further ingredient change and return toward the hero; final seconds revisit the sequence.

## Motion and camera
The product and surrounding botanicals share depth cues; the physical phone and finger are recording context, not assets to reproduce.

## Implementation
Author ingredient paths in a product-local coordinate system, with front/back depth and appropriate occlusion. Keep the bottle scale, cap, label and contact shadow coherent across states. A flat diagonal wipe is a different mechanism. Use well-lit licensed or original product assets; do not infer perfume material realism from a tiny source frame.

## Interaction
Use native scroll for product-to-product choreography. Each bottle remains a real product link, and a normal collection list provides a direct path.

## Responsive adaptation
Prioritize the label and bottle silhouette on mobile. Keep ingredients out of the heading/button zone and reduce simultaneous overlap.

## Accessibility
Reduced motion changes the displayed identity without surrounding orbit. Name the active product through normal text and accessible links.

## Performance
Cap simultaneous alpha layers and nearby asset preloads. Large cutout botanicals with blur can be more expensive than the bottle.

## Validation
Check labels, cap alignment, compositing edges, ingredient occlusion, active links, reverse scroll and touch input.

Original explanatory storyboard: `assets/storyboards/botanical-product.svg`, relative to the skill root. The simple shapes explain the mechanism; they are not production assets claiming photographic fidelity. For tested independent examples see `assets/examples/`; reuse ideas, not a fixed page design.
