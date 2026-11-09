# Art-direct for the available space

Use content and focal anchors to choose breakpoints. Test 320,360,375,390,430,768,1024,1280,1440,1920,2560 widths, short landscape and tall portrait, zoom and multiple DPRs. A matrix should record what actually ran; an untested width is not a pass.

On mobile retain the essential movement and simplify decoration. Reframe the hero around its contact or lead object, reduce simultaneous cards and reserve a stable text zone. Do not clip the only link or let transformed imagery cover copy. Avoid huge negative margins and unexplained per-device offsets. For 2.5D, respect the photographed viewing cone rather than rotating into an unpainted side.

Use semantic headings, anchors and buttons. Native details, dialog and form elements may be better than custom controls. Ensure focus remains visible on transformed objects. If an offscreen scene receives focus, reveal its content or offer an equivalent static path. Touch layouts need usable targets, native scroll and pinch zoom; viewport emulation alone cannot prove gesture correctness.

For reduced motion show an intentional static composition and ordinary content immediately. Listen for preference changes and clean up existing animation ownership. Never require scroll completion to unlock essential content. No-JS, failed-assets and deep links should preserve the underlying site.

Use WCAG 2.2 AA as the target: text contrast normally 4.5:1 (3:1 for qualifying large text), visible focus and non-text contrast, keyboard access, reflow, understandable labels, target sizing and no seizure-triggering flashes. Minimum target-size rules include exceptions; prefer generous 44px controls where practical. Reduced motion is an important usability requirement, not by itself a complete AA audit. [WCAG 2.2](https://www.w3.org/TR/WCAG22/).

Test actual pixels and interactions, not just CSS declarations. Automated geometry checks do not prove readable contrast, visual hierarchy or a natural physical gesture. Human review and assistive-technology checks complement automation.
