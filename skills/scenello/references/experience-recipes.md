# Reconstructing complete cinematic experiences

Use these independently written recipes to turn a prompt or an authorized reference into a functioning site. They describe mechanisms and user contracts, not reusable artwork or a universal visual theme. Choose the closest mechanism, then create fresh composition, copy, assets and timing for the new subject.

## Establish what is current

Inspect the active entry route and imports before trusting a README, screenshot, archived build or checkpoint. Later changes can replace both the renderer and the business flow while old files remain. Record the current interaction, separately from historical approval notes. Source inspection establishes implemented intent; it cannot establish appearance, perceptual fidelity, playback quality or final user acceptance.

For each scene write a compact contract: input owner, visible subject, entry condition, progress or elapsed-time range, transition destination, interruption behavior and usable fallback. Keep three clocks distinct:

| Clock | Appropriate use | Required behavior |
|---|---|---|
| Native scroll position | Spatial travel, product handoff, restoration montage | Seekable, reversible and stable on a stationary hold |
| Elapsed active time | Brief opening, cooking action, dancer performance | Explicit pause; exclude hidden intervals; deliberate replay |
| Finite passage followed by periodic ambience | Arrival, cruising, environmental movement | Clamp travel at destination; continue a seam-safe environmental phase |

Use the existing project stack. For new art direction consult the art-direction reference and relevant design skills. For scroll choreography consult motion and the appropriate animation-library skill. Use spatial production when the required view genuinely needs geometry, rigging or offline compositing. Asset-generation tools need authorized inputs; a visual reference never grants upload or redistribution rights. Component MCPs can inform accessible control semantics without dictating the whole visual design. Read security and reference-intake guidance before using a supplied pack.

## Sculptural product collection

**Experience.** An optional, interruptible material close-up resolves into a held product stage. Several variants pass horizontally through it; the last variant hands its detail image into an editorial material section, then a selectable collection cabinet. A local bag supplies the functional destination.

**Architecture.** Keep backdrop, product, optical accents and copy as separate layers. One scroll playhead derives each variant's entry, exit and held pose. Products travel farther than copy; departing copy clears before incoming copy becomes readable. A separate macro layer can bridge the last stage into the next section by interpolating measured destination bounds. Refresh those bounds on resize rather than hard-coding a desktop rectangle.

**Assets.** Create a consistent product model or approved photographic set, several genuine yaw views per variant, high-quality resting views, detail crops and complete-object bag images. Blending neighboring rendered angles creates a bounded turn; a CSS tilt of one photograph cannot reveal a missing side. Decode the necessary incoming views before revealing them. Hold a usable prior state and expose a retry or browse alternative on failure.

**Interaction.** The showcase chapter counter may be informational. Put actual selection controls in the collection, with selected state, named description, price and a single unambiguous Add action. Add snapshots the selected product. Validate persisted quantities, handle storage failure, support removal/subtotal, and return focus when the bag closes. State clearly whether the bag is local or connected to checkout.

**Check.** Reverse at every handoff; jump rapidly past unloaded variants; interrupt the opening; use a direct collection link; resize during the macro bridge; test multiple variants and a reopened bag. Reduced motion uses readable held poses and no travelling or rotating copy. Pre-rendered turns are not real-time volumetric rendering. Dense view sets need an explicit decoded-memory budget.

## Vessel inspection and arrival

**Experience.** An exterior approach, onboard inspection and sheltered arrival form three real chapters. Scroll changes the editorial layout; each visible film runs on its own elapsed-time clock. Returning resumes the retained playhead. The user can inspect materials and prepare a local interest summary.

**Architecture.** Give every scene one playback owner. Combine active-chapter eligibility, actual media visibility, page visibility, shared pause/still preference and media readiness before playing. Keep the exact first-frame poster visible until a decoded video frame can replace it. Handle autoplay rejection with a deliberate Play control. Finite approach films hand off to periodic ambience; inspection may loop directly. Replay alone resets the passage.

**Assets.** Use distinct authored views for bow approach, low tracking, foredeck, material detail and rear-quarter arrival. Produce water/contact/reflection layers with the same hull pose. Water may move around rigid fittings; furniture, architecture and horizon should not deform. A separately authored angle avoids inventing the hidden geometry of a flat vessel image. Match the last travel pose to the ambient start, and make environmental phases periodic. Arrival wake decays independently of gentle water motion.

**Interaction.** Detail tabs decode before commit, ignore stale requests, preserve focus and expose load failure. Material stills have no misleading film controls. A local drawer preserves scroll and playback; interest choices and note become a copyable summary with a selectable-text fallback. A preview must not imply that an enquiry has been sent.

**Check.** Enter a chapter slowly and by a large scroll jump; leave before readiness; return after pause; hide the tab; reject playback; fail a source; replay after arrival; change a detail rapidly; open/close the drawer during a handoff. On narrow screens use natural-flow chapters and intentionally compose media framing. Inspect every later CSS override: an earlier promise of a full panoramic frame does not prove the final crop preserves it. A film may be appropriate for environmental movement, while scroll remains the owner of site navigation.

## Photographic restoration journey

**Experience.** An asymmetric editorial opening leads into the same building through neglect, cleaning, painting, restored daylight and evening. Service disclosures and a contact-review flow finish the website.

**Architecture.** Use registered photographs in one shared coordinate space. Scroll controls a bounded camera path and dissolves between stages; stopping freezes all work-related movement. Clamp camera centers to prevent exposed image edges. Decode layers before visibility. Keep typography outside the transformation frame. Show service labels only while their corresponding work is present.

**Assets.** Preserve camera, architecture, windows, door, perspective and lighting continuity across edits. Workers must already have coherent hand/tool contact and grounded feet. When subtle local motion is useful, restrict it to narrow forearm/tool supports that move together; keep glazing, wall and the rest of the person rigid. Provide the underlying photograph when the small GPU patch cannot initialize or loses its context. This technique is photographic motion, not full-body filmed labor.

**Interaction.** A short opening settles into the measured final hero frame and skips immediately on user input, resize or a deep link. Native service disclosures remain operable. A frontend contact form uses labels, required validation, service choice, review and edit with preserved values; no invented successful submission. Reduced motion can show the completed evening state directly and keep the rest of the site readable.

**Failure lesson.** Detached animated tools, floating cut-out people and broad rubber-like image warps undermine physical credibility. If a photographic montage replaces an earlier process renderer, stop teaching obsolete paint progress controls or comparisons unless they remain imported by the final route. Preserve a specifically requested ending even when the production method changes.

**Check.** Compare fixed architectural landmarks across dissolves; inspect the full worker at intermediate progress; hold and reverse around every service transition; resize during the close-up; disable GPU support; check the contact review/edit round trip. Never use a fast callback sample as proof that worker motion looks convincing.

## Food assembly, cooking and local loyalty

**Experience.** A stacked food object briefly lifts and separates, returns to a readable stack, transitions into a cooking action, then arrives with its serving surface beside recipe and quantity controls. A tray can continue into a loyalty-card interaction and a clearly identified payment preview.

**Architecture.** Register transparent ingredient layers against a common stack anchor. Give each a timed vertical path and, where suitable, bounded perspective spins. Compute lift clearance from the crown to navigation, particularly on short screens. Stage the headline after the object clears it. Keep the opening interruptible and restore every position, scale and rotation channel to a valid stack after selection or resize. Use scroll for scene composition and a separate short action timeline for spatula launch, airborne flip and catch. An alternative shared-viewport handoff is a deliberate variant, not an accidental route difference.

**Assets.** Prepare transparent ingredient and recipe sheets with consistent size, lighting, edge cleanup and shadow direction. A spatula and patty need a shared support/contact coordinate system. Burger and serving paper move as one serving unit. Perspective sprites are a 2.5D illusion; do not describe them as a volumetric food simulation.

**Interaction.** Track requested and committed recipes separately. Decode before commit; discard stale async results; recover the current stack on failure. Add takes an immutable snapshot of committed recipe, integer-unit price and quantity. Combine identical tray lines, allow edits/removal and calculate totals from integer currency units. The local loyalty flow has ready, reading and result states, back navigation and a readable numeric saving. Payment preview shows the final receipt without collecting payment.

**Limit.** A demonstration that accepts any nonempty code and applies a percentage discount is a simulated reader, not verified membership or fraud protection. Label it honestly. Opening the tray anew may reset its loyalty step; choose and test whether that is intended. Never infer a five-second peripheral flight from an old direction document when current source implements a shorter vertical toss.

**Check.** Interrupt at ascent and landing; choose recipes rapidly; fail the requested image; add during loading; change quantity and remove the final item; return between loyalty and tray; change code; pause mid-action; close with Escape and verify focus return. Reduced motion starts assembled and shortens incidental reader transitions.

## Sound sculpture into an instrument corridor

**Experience.** A procedural woven object forms, then unwinds onto an axis that continues into a curved corridor of linked instrument cards. Each card opens a real workbench with parameters, deliberate audio playback and a downloadable sound file.

**Architecture.** Separate visual motion from audio synthesis. A low-cost layered line drawing can suggest a sculptural surface without a mesh. Sample a shared centerline once per frame, then derive filaments. Scroll transforms that object toward the same axis used by the next section. In the corridor, project a world-space route using a camera position and look-ahead tangent. Project both ribbon edges from compatible samples so neighboring bands share seams. Cards bank beside the route and converge into a readable selected state.

**Interaction.** Give each card a real destination and provide an always usable station index. Near-plane clipping and opacity must not leave hidden cards keyboard-focusable; moving to a station should focus its corresponding visible link. Reduced motion becomes an ordinary readable library. On the workbench expose labeled pitch/body controls, Play/Stop, error feedback and export. A user gesture resumes the audio context; changing parameters stops stale playback. Disconnect audio nodes and revoke exported object URLs.

**Assets and checks.** Procedural visuals still require a coherent palette, lighting field and typography. Audio can be synthesized locally, but assess its quality with an appropriate listening tool before describing its sound. This guide does not attest to listening. Check corridor entry and exit, reverse travel, station focus, all detail routes, parameter bounds, cancelled playback and downloaded-file structure. Gate offscreen drawings, cap pixel ratio and avoid redrawing idle card artwork continuously.

## Rotating packaged drinks

**Experience.** One hero package enters, the opening composition resolves into a depth-ordered flavor orbit, and the selected flavor links to an individual product page with return/next navigation.

**Architecture.** Map scroll into an introductory composition and then a carousel angle. Derive horizontal position, depth, size, brightness, roll and stacking order from that angle; keep the selected label stable and readable. A cylindrical label shader can wrap an authorized flat label around an approximate can surface while retaining a rendered silhouette and metal highlights. It is an analytic surface illusion rather than a full mechanical model.

**Assets and interaction.** Supply a clean transparent package poster and matching wrap per variant; preserve the poster when GPU support or textures fail. Every package remains a genuine product link. Derive detail routes from stable identifiers, not current animation index alone. Reduced motion uses discrete readable selections or a static collection.

**Check.** Test front/back crossover, selected text/link agreement, details and next/return routes, short mobile viewports, texture failure and context loss. A minimal shader prototype may lack context restoration and disposal; implement them for a long-lived application. Several independent canvases multiply decoded and GPU memory even if drawings are event-driven.

## Department deck and template archive

**Experience.** The full opening scene contracts and flips into a department card. Subsequent cards rotate through a readable central position. The archive expands into a forward-moving field of linked template previews with smaller distant companions. Department pages supply a simpler secondary route.

**Architecture.** Measure the destination card bounds and make the opening scene share its transform origin. Control flip, shrink and card entrance from the same scroll playhead. Suppress backfaces. Compute each card's transform, opacity and stacking order from distance to the selected position. For the archive use a depth function with bounded scale and near-plane culling; companion previews establish distance without blocking the primary links.

**Interaction.** Keep department selection distinct from opening a template. All visible cards have real links, descriptive names and usable hit regions. Disable interaction with hidden/back-facing objects. Mobile needs its own fan arc and archive handoff, not uniform desktop scaling. Reduced motion is a normal grid/list with every destination available.

**Check.** Follow each department and template route, use browser Back, tab through entry and exit, inspect near-plane clipping, and verify the final archive release. Reuse the spatial mechanism with fresh categories, preview images and detail content; do not ship bundled private site builds as teaching assets.

## Specimen field and responsive portrait

**Specimen field.** A translucent focal organism leads into a wider constellation of individually linked specimens. Scroll reduces the dominant image into a labeled observation field while current lines explain the spatial change. Use separate normalized desktop/phone positions and inverse label scaling so labels retain legibility. A brief canvas deformation can suggest bell contraction and tail drag, but keep it bounded, interruptible and removable when offscreen or motion is reduced. Provide a conventional species index and detail routes. Illustrative deformation is not a biological simulation; factual claims need their own sources.

**Portrait.** A point cloud assembles into an indexed surface with restrained material shading. Pointer position turns the head; projected eye hit regions trigger a limited eye-opening effect and hold the pose. Keyboard arrows turn it and Enter supplies an equivalent eye action. Derive hit targets from the same pose and projection used for the render. Stop rendering when stable/offscreen and cap pixel ratio. Supply a deliberate fallback and loading/error state for missing geometry, GPU failure or binary-fetch failure. Painted shader eyes are not anatomical eyelid rigging; validate plausibility at every permitted angle.

## Rigged performance and class programme

**Experience.** A rigged performer introduces a studio. In the class programme, a persistent stage accompanies readable class information. Scroll selects the demonstrated class while time drives the performance. A local membership dialog supplies a tangible action without implying payment or enrollment in a real service.

**Architecture.** Use a compatible skeletal model and actual joint/root motion. Resample or retarget recordings into a known rig; validate bone order and clip lengths. Interpolate quaternions between frames and blend outgoing/incoming clips with independent retained entry times. Wardrobe changes must follow the skinned surface. A single renderer can move between hero and programme mounts; resize and camera framing must follow its active container. Contact shadows derive from actual hand/foot world positions near the floor.

**Assets and limits.** Need a licensed rig, compatible motion, material/garment mappings and explicit provenance per class. An adapted movement study is not proof of cultural or technical authenticity. A custom extension, a borrowed phrase and recorded choreography require distinct attribution. Do not invent motion-capture origin or credentials.

**Check.** Play/pause each stage; change class both slowly and rapidly; inspect floor contacts, root drift, limb intersections, garment deformation, headspins and transitions; stop and resume after a hidden tab. Cap delta time and discard hidden elapsed time. Verify reduced-motion still poses and direct class navigation. Missing model/clip handling and GPU cleanup are required before production even if an observed prototype omitted them. Test local subscription confirmation, removal, reopen and storage failure; distinguish the local preview from a real subscription.

## Editorial engineering portfolio

**Experience.** Two authored hand layers, one human and one mechanical, approach a shared fingertip contact, then hand the first actual project into a diagonal card wheel. Follow the chosen project order: computer vision and machine learning first, reliable systems next, then any remaining discipline. Continue into a selectable experience chapter, a capabilities field guide and a biography spread with an authorized portrait and readable text. The portfolio content is the destination, not a reward for waiting through the opening.

**Reconstruction boundary.** Active imports establish the current opening; an earlier particle/pinch contract is a separate historical variant. The inspected implementation uses layered hand artwork and native scroll-driven contact, rather than the removed particle worker. It does not establish the appearance or timing of that historical opening. If a brief explicitly requests the particle/pinch variant, obtain its authorized reference states or source and record any missing evidence. Do not call the active hand composition abandoned, or the historical version shipped, without supporting evidence.

**Handoff.** Register each fingertip in source coordinates and map it to the viewport with the same transform as its hand. Use restrained wrist-led movement around plausible fixed anatomy, a small local contact impulse, then carry the first project card into the browsing composition. Preserve the same card element, image identity, direction and velocity through release, gathering and final placement. Avoid a second entrance, a pause at contact or a brief backwards drift. One seekable scroll playhead owns the current approach and release. If reconstructing a particle/pinch variant, particles must resolve into its own credible gesture and share the same handoff contract. Prepare the application and critical image before contact; do not load the entire interface at the dramatic instant.

**Diagonal catalogue.** Derive each card's sweep, depth, bank, yaw, scale and opacity from distance along one tilted wheel. A tangent-continuous bridge connects the rotating group to the browsing strip. Adjust portrait lanes and safe bounds around the lead image rather than shrinking the full desktop layout. At the vision-to-systems boundary, coordinate the outgoing edge-on turn with the incoming face opening. Keep the taxonomy in one content manifest so section shortcuts, visible cards, selected metadata and case navigation agree. Provide project-index buttons, arrow/Home/End navigation and actual case-study links; a drag must not accidentally open a case. Preserve scroll and focus on browser Back and provide a direct-route fallback when no gallery origin exists.

**Supporting chapters.** An experience selector keeps image, employer/role, period and summary in one active state. Scroll can select the nearest stop, while thumbnail buttons and Up/Down/Home/End offer direct control. Capabilities pair concrete disciplines with related work and inspectable process steps; desktop can share a persistent exhibit, while narrow screens put each exhibit beside its own text. Manual stage selection takes precedence over a short automatic explanation. The biography keeps portrait, introductory paragraph, longer account and education distinct; reveal effects must not erase the portrait or delay access to the prose. Use fresh, authorized content rather than transferring another person's credentials or project claims.

**Check.** Hold and reverse through approach, contact, release and the first browsing stop; skip early, fail the lead image, resize at contact and cross the discipline boundary repeatedly. For a particle variant also inspect resolution and pinch. Inspect diagonal cards for clipping and readable metadata on short portrait/landscape screens. Test experience buttons against scroll state, capability manual overrides, direct case URLs, modified-click links, route cancellation, browser Back, language changes, portrait alt text and biography reading order. Reduced motion supplies a static opening and directly navigable collection. A server-painted or plain index keeps projects, experience and contact reachable if enhanced startup fails. Validate this recipe in the browser before claiming the requested opening or its continuity has been reproduced.

## Acceptance and measurement

For a reconstruction, compare authorized reference keyframes with actual browser states at matched size and progress, then inspect continuous playback between them. For a prompt-only build, judge the visual contract and working destination. In either case capture actual interaction rather than substituting a staged recording.

Check at least narrow portrait, short landscape, tablet and desktop; resize at a difficult intermediate pose. Include forward/reverse/fast scroll, stopped holds, touch, keyboard, reduced motion, deep links, browser Back, asset failure and GPU/audio failure where applicable. Test the business flow as carefully as the hero.

Measure initial transfer/decode, input latency, drawing cost, long tasks, frame intervals and memory separately, under recorded conditions. Use representative low-powered hardware when available. Historic successful checks apply only to the version, browser and conditions they actually exercised. No source-only recipe proves visual fidelity, acceptance, cross-browser correctness or a universal frame rate. Keep uncertainties explicit and reproduce checks after changes.
