# Choose fidelity before choosing 3D

| Method | Good at | Principal limitation | Fallback |
|---|---|---|---|
| CSS/SVG | Typography, panels, diagrams, shallow objects | Cannot invent realistic anatomy | Static semantic layout |
| Layered 2.5D | Short camera moves over authorized photographic plates | Reveals missing surfaces, fixed reflections | Reframed still |
| Controlled render/sequence | Realistic articulated motion, consistent light | Transfer/decode/seek cost; video isn't live interaction | Poster + links |
| Real-time glTF | True orbit, lighting, changing view | Geometry, textures, GPU, asset rights | Poster + DOM controls |

A photograph translated along one axis is not a physical camera descent. For 2.5D define depth planes, foreground occlusion, camera path and a limited reveal cone. Do not expose surfaces never photographed. Cars need consistent tire contact, shadows and reflections; avoid adding random moving people to conceal an empty scene. If the reference requires genuine parallax, obtain suitable plates or reconstruct a narrow view honestly.

## Real-time scene

Use a parent rig for camera motion and local motion for the focal object. Light moves relative to world surfaces, not as a flat highlight pasted onto the screen. Match camera focal length and material roughness before adding effects. DOM content and the renderer share progress, dimensions and anchors. Put labels in stable DOM zones; projected labels require occlusion and edge collision handling.

Budget geometry, draw calls and texture memory. A 4096² RGBA texture is about 64 MiB before mipmaps, regardless of compressed download size. Start with a capped DPR, reduce effects based on measured limits, avoid unnecessary postprocessing, stop inactive loops and dispose renderer resources. A quality tier is a visual decision, not a user-agent string guess.

## Optional Blender route

First inspect installed executable/version and the project's production permissions. Do not silently download binaries or run Python from an untrusted .blend. Inspect source rights; open only trusted files, with automatic Python execution disabled. Render an inexpensive low-resolution representative frame first, then lighting/material previews and a bounded frame range. Record Blender version, scene/camera settings, render engine, asset licenses, seed, output dimensions and optimization. Large renders need disk/time bounds. A successful .blend open is not proof that a rig or lighting works.

Prefer original code geometry for explanatory demonstrations. Photorealistic requirements need genuinely appropriate assets; do not market geometric placeholders as final commercial imagery. Scenello core has no Blender or WebGL runtime dependency. No Blender execution is required to use its text guidance.
