# Performance evidence with correct units

Separate these questions:

1. Loading: FCP/LCP, transfer, decode, render blocking and CLS under cold versus warm cache.
2. Main-thread work: top-level task durations and per-frame occupied time from a trace, with nested spans counted once.
3. Pacing: requestAnimationFrame timestamp intervals, p50/p95/p99 and counts beyond 16.67/33.3/50 ms. rAF is supplementary, not proof of presented frames.
4. Input: event timing and input-to-next-paint where supported. A synthetic click timing is not field INP.
5. GPU/presentation: raster, compositor and presented-frame evidence when available. A headless trace may not establish physical display behavior.

A 60 Hz budget is approximately 16.67 ms; 120 Hz is tighter. Short JS callbacks do not imply short total frame work. Long Animation Frames expose frames over 50 ms where supported, so zero LoAF records cannot establish p99 under 16 ms. [MDN LoAF](https://developer.mozilla.org/en-US/docs/Web/API/Performance_API/Long_animation_frame_timing).

## Reproducible experiment

Record browser/build, OS, viewport, DPR, CPU/network throttle, visible/foreground status, cache state, refresh assumptions, tool versions and sample counts. Use at least ten repeats per practical profile; report per-run distributions as well as pooled percentiles. Nearest-rank percentile: sorted sample at ceil(p*n)-1. State excluded data and why. Keep diagnostics identical for comparisons. Use a functional static mode as a rendering baseline, not as evidence of a no-skill agent baseline.

Prefer native input gestures. Repeated evaluate(scrollTo) can inject forced layout and contaminate a scroll benchmark. Test the same content with motion on/off, and investigate traces rather than deleting essential content to win a number. Save compact trace evidence outside release assets. No default recording of user data.

## Optimization order

Profile initialization, hydration, asset decode and the actual animation separately. Preserve visible first-frame content. Precompute geometry outside hot loops; batch reads before writes; reuse storage; request a frame only when dirty. Avoid full-page blur, huge translucent layers, animating layout and per-frame React state. A few transformed layers still consume texture memory; use will-change sparingly. Lazy loading is not an excuse for a blank hero.

The included browser harness records repeated local-lab rAF pacing, trace top-level tasks, LoAF, CLS and lab LCP. It deliberately does not label task percentiles as per-frame workload or lab interactions as INP. No software test certifies a universal 16 ms target. Physical mobile/Firefox/WebKit testing remains separate when those devices or engines are unavailable.

## Concrete startup diagnosis from the demo refinement

A large initial Layout was not fixed by simplifying scroll math or switching system font names. Below-fold containment reduced the scope; two small preloaded, same-origin, OFL font faces removed the expensive platform font-resolution path in the tested Windows/Chromium profile. Explicit line metrics preserved baseline placement. This is a measured case, not a rule to replace every project font. Check first paint, fallback/loading failures, glyph coverage, font rights and actual layout similarity. Do not hide load samples or prewarm unreported work to improve a number.

## Preserve cinematic quality while optimizing

Before tuning, freeze a reviewed visual and motion baseline: asset identities and resolution, typography, composition, camera path, easing, scroll range, reveal order, contact anchors, and functional destinations. Compare deterministic poses across the full timeline and responsive layouts, not only the opening and final frames. Include reverse scroll and resize. A faster build fails if it flattens depth, changes camera composition, lowers artwork quality, removes layers, shortens the journey, speeds playback, postpones visible content or turns an interaction into a recording without the user's request.

Find the exact phase of each spike. Correlate interval endpoints with trace Layout, style, paint, decode, script and compositor work. Deferred work can simply relocate a stall to the moment a section becomes eligible for rendering. Chunk independent reading items, preserve intrinsic geometry, verify full-page scrolling and deep links, and use ResizeObserver for clean post-layout geometry when appropriate. Do not replace a startup stall with a blank frame or discard load samples. Performance wins require both measured improvement and visual/motion parity.

Stress the real experience: cold/warm load, immediate input during initialization, fast forward/reverse flings, full catalogue entry, actual links and filters, orientation, small/high-DPR viewports, heavier CPU throttling and idle recovery. Pair diagnostics on/off to estimate instrumentation effects. Compare per-phase and whole-run distributions; pooling a long idle segment must not conceal a transition failure. Keep reporting remaining outliers rather than promising universal 16 ms compliance. Prefer reducing avoidable layout and paint scope over simplifying the cinematic approach.

The full review repository (not a skill-only installation) includes `tests/cinematic_parity.py` (reviewed local baseline ZIP, 21 deterministic poses per viewport plus screenshots) and `tests/stress_check.py` (repeatable native-input stress). They use existing browser tooling and do not install it. In another project, adapt the same checks to its existing tools; do not assume those repository helpers were installed with the skill. [Native containment](https://web.dev/articles/content-visibility), [layout observation](https://developer.mozilla.org/en-US/docs/Web/API/ResizeObserver) and [animation rendering guidance](https://web.dev/articles/animations-guide) explain the mechanisms; actual browser evidence decides whether a change is retained.

Font delivery belongs in cinematic latency diagnosis. A same-origin preload can still lose a bandwidth race on a constrained connection, causing an expensive first layout with fallback fonts. Compare actual response completion, font decode, first layout and first paint rather than assuming a preload solved it. Where useful, subset licensed fonts to the site's actual text and dynamic strings; verify every retained glyph's outlines and advances, preserve line metrics, keep the original licensed source and a loading-failure fallback, then prove rendered parity. Rebuild subsets when content or languages change. Test no-JS and failed-font paths. Do not hide text with a different display policy merely to improve a frame metric. Subsetting and font-range composition are measured options, not universal defaults for every site.

A containment optimization can change paint/raster origin or intrinsic sizing even when outer rectangles match. Compare the complete reading sections too. The demo refinement rejected per-card visibility containment after its catalogue screenshots diverged, and retained verified-identical font subsets plus definite grid sizing instead. Treat source files and all intermediate measurements as evidence; do not turn a successful probe into a claim that every startup/rotation interval meets budget.

If traces show a first-use typography cost at a later section, a bounded idle measurement of the exact upcoming font styles may prepare shared font caches without changing the DOM. Compare enabled/disabled probes under the same instrumentation. Keep each slice small, stop when no idle budget is available, clean up on hiding/navigation, and include the preparation cost in load/whole-run statistics. Start a separate input stress test at actual first contentful paint so late low-priority resources cannot manufacture a warm-up advantage. This is optional evidence-driven preparation, not permission to delay the scene or hide typography.

## Startup reads and invisible scene content

A promise-valued browser API is not necessarily a layout-free read. In the demo traces, accessing document.fonts.ready during deferred script evaluation synchronously flushed style/layout, costing about 23 ms inside the font-helper script on a throttled mobile profile. Query readiness after the first natural rendering opportunity when it is only needed for optional background preparation. Geometry observation can similarly avoid a synchronous initial getBoundingClientRect/offsetHeight flush. Validate cleanup and direct-link initialization, and retain all load samples. [Font readiness semantics](https://developer.mozilla.org/en-US/docs/Web/API/FontFaceSet/ready).

Do not lay out an entirely zero-opacity scene group if its children are not yet interactive and their appearance can be restored at the exact existing activation threshold. Preserve the same DOM nodes, opacity functions, camera transforms, material detail, and interaction timing. Prepare its fonts if first activation would otherwise stutter. Test forward/reverse crossings immediately on both sides of that threshold, including input from first paint. This is not permission to omit visible content or move a startup stall into the reveal.

Quality comparisons should require identical rendered pixels and visible geometry. A fully zero-opacity node can legitimately have deferred geometry; still compare its opacity, content and interactivity, then require matching geometry as soon as it becomes visible. The repository trace audit checks for Layout nested inside initial scene/font-helper EvaluateScript spans, separately from native frame layout and total pacing; it must not be presented as proof that every frame meets budget.

### Preserve measurement integrity

Inspect the test harness inside startup traces. High-level browser evaluation or waiting can inject a large automation utility bundle and create a false site bottleneck. Prefer small native CDP calls during Chromium measurements; retain tracing, early rAF/PerformanceObserver sampling and the original input-start condition. Never move diagnostics after first paint to improve numbers. Repeat both baseline and candidate with the same corrected harness, preserve older evidence and disclose measurement corrections. Native style/font/layout misses still count. Reject changes that merely relocate stalls, hide first visible content, or weaken cinematic parity.


## Separate the measuring tool from the shipped page

During measured startup avoid automation helpers that inject large utility scripts into the page. Prefer small direct Chrome DevTools Protocol evaluations and native input, with an early bounded observer installed before navigation. A wait helper can add hundreds of kilobytes of harness code and manufacture a startup spike. Retain affected captures as instrumented failures, correct the harness, and repeat; never silently remove outliers.

For WebGL record the actual renderer/backend and parallel shader capability. A software renderer is not evidence of physical mobile performance. Attribute module setup, original texture generation, environment preparation, shader compile/link, synchronous status checks and first draw separately. Debug shader-status queries may synchronize the GPU/driver; a production-only debug toggle is acceptable only with unchanged imagery, preserved diagnostic mode and error/context-loss recovery. Identical precomputed texture bytes may remove startup work without changing visual quality. Validate decoded texel parity, responsive scene positions and actual input progression. Improved main-thread rAF after queuing GPU work is not proof that those frames were presented.

Never turn a single targeted improvement into a40-run pass. Mark the prior batch and the changed-runtime diagnostic separately; repeat acceptance samples on the frozen final source. Keep the old baseline even when its shader stalls are seconds long.


## Do not lose the work before the first callback

Record navigation-relative first rAF timestamp AND actual first callback execution time, plus FCP and the trace tasks before that callback. A short first inter-callback interval can follow hundreds of milliseconds of earlier blocked layout. Report the entire initialization window and every outlier, not only what fits inside an existing rAF interval. A candidate that makes the first interval shorter while relocating a large task earlier or later has not fixed startup.

For critical fonts, collect visible strings from HTML attributes as well as element text, JavaScript and CSS generated content. Placeholder ellipses, image alt text and encoded attributes can request an otherwise unused full font. Verify actual browser resource requests and coverage; a19KB subset file does not mean the page transferred19KB if the164KB source face still loads. Declare fallback coverage from its real cmap rather than promising glyphs the source never contained. Test outlines, metrics, variable instances and rendered poses. Inline delivery is a hypothesis to measure, not a guaranteed cure for native font/layout costs. Never remove glyphs, change typography or hide text to manufacture a latency pass.


For demand-rendered scenes, cache the visible render state (progress, viewport/buffer scale and mode) and avoid repeated GPU draws once progress is clamped outside the story. Keep DOM navigation, contrast and section-state updates running independently: an early return from the whole callback can break the ordinary website. Invalidate the GPU cache after a resize or context/buffer reset. Prove unchanged raw pixels and actual draw-command counts; a rAF counter alone is not GPU work. This removes redundant work without changing geometry or camera motion, but does not establish that shader startup is now fast.
