# Scenello UI demo fonts

Renamed derivative of Microsoft's open-source Selawik (a Segoe UI replacement), licensed under SIL OFL 1.1. Full copyright and license: LICENSE.txt. This font software is not MIT and is not an official Microsoft product.

Source: https://github.com/microsoft/Selawik — reviewed Regular/Bold UFO sources. Modifications: cubic-to-quadratic conversion, decomposed outlines, small original geometric navigation symbols, deterministic metadata and renamed family. No proprietary Windows font is redistributed. CSS metric overrides preserve the former Segoe UI baseline; outlines are compatible in direction, not asserted pixel-identical.

The two approximately 19 KB WOFF files are preloaded from the same origin to avoid costly platform font resolution during initial layout. Existing type scale, composition, palette and motion remain. Fallback uses the original system stack if loading fails. These files cover the demos' text, not every script/language.

Optional rebuild: tools/build_demo_fonts.py at repository root, with reviewed UFO source and FontTools 4.68.0 available. The core skill does not depend on FontTools, and no downloads/installations occur at runtime. Source ZIP/hash and build provenance are retained privately; asset-manifest.json records production file hashes.

## Critical subsets (0.3.0)

The critical regular/bold WOFF files retain the same glyph outlines and advances for the two English-language demos. Each is about 8 KB. The optional FontTools build in tools/build_critical_fonts.py verifies retained glyph coordinates and horizontal metrics against the complete local source faces, then writes matching CSS and preload links. It does not install or download tools. The full faces remain adjacent and are the URL-loading failure fallback; no third-party font service is used. The motion bootstrap remains ordinary code, without encoded font payloads.

These are content-specific subsets, not a universal multilingual typeface. Regenerate them for changed text, dynamic labels or another language; do not silently replace new characters with missing-glyph boxes. Critical provenance lists the exact codepoints and file hashes. OFL-1.1 covers the subset files too, under the same bundled license; the reserved upstream family name is not used.
