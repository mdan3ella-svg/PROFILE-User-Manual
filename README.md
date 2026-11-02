# PROFILE | MOTION ENGINE · Engineering Evaluation Release

Contains the patched source HTML, original supplied humanoid/scorpion GLBs, operator manual and a reproducible **fully offline single-file builder**. The supplied `index.html` is a hosted evaluation and **still requires internet** for Three.js until the offline build is run. The offline build is not included precompiled because npm dependencies could not be retrieved in this environment.

## Run hosted evaluation
Upload `index.html`, `operator-manual.html`, `.nojekyll`, and the `assets/` directory together to GitHub Pages. Or run `python -m http.server 8000` and visit http://localhost:8000.

## Generate the genuinely offline single HTML
On a computer with Node.js 20+, connect to the internet once to install **pinned** toolchain packages, then run:

```
npm install
npm run check
npm run build:offline
```

The output `offline/PROFILE_MOTION_ENGINE_OFFLINE.html` embeds the original 16 MB humanoid GLB, 15 MB scorpion GLB, the operator manual, and the bundled Three.js engine/addons. It requires no CDN, no server and no network after building. It can be opened using `file://`. The resulting HTML can be larger than GitHub's per-file limits; for GitHub Pages use the split assets layout instead.

## Scope / qualification
Syntax and GLB container integrity are mechanically checked. Six-leg IK controls, body-part weight mappings, animated GLB round trip and ergonomics require hands-on browser QA with imported models and target-engine testing. This is **not a certified product** and makes no claim of 5A+ industrial certification. The original `operator-manual.html` describes a workflow, not proof of functional compliance.

## Known limitations
- Generated rig joint locations are estimated using geometry heuristics; rigid scorpion shell paint groups exist but exact pivots cannot be inferred reliably from named meshes alone.
- A single tail mesh still requires authored mechanical splits for true rigid segments.
- Generic FBX skin adoption is incomplete. Imported GLB animation compatibility should be tested in each target engine.
- The single-file build's base64 decoding has a transient memory cost proportional to the 31 MB of assets. For constrained devices, use the hosted multi-file edition.


## 2026-11-02 rigid binding patch
The scorpion GLB contains nine named nodes, no skin, and no animation. Rigid bind now maps each named body/leg part to exactly one bone and groups tail vertices by indexed triangle connectivity before assigning one bone per island. Continuous welded tail shells cannot articulate without deformation; such shells are locked rigidly to a single bone and reported. This is a geometry-safety correction, not calibrated mechanical pivot validation. Other rig presets retain the existing skinning logic; no claim of comprehensive dynamic certification is made. Run `npm run check` and check joint rotation, FK/IK, motion and GLB exports in a browser before production use.


## Blender / open metarig interchange
Select a metarig in Blender and execute `blender_export_metarig.py` from its Scripting workspace. Load `profile-metarig-guide.json` in the application's Rig panel. The importer matches compatible bone names, supports proportional model-bounds placement or absolute coordinates, reports unmatched joints, supports optional L/R mirroring and explicit rebinding. This is an interoperable **landmark guide**, not an embedded Rigify engine; full Rigify control rig, constraints, drivers, and native Blender modifiers do not run in browser. Rigify GPL code is not bundled. Results require manual inspection and calibration. The browser app still depends on CDN Three.js unless built using the separate offline build process.

## Motion Studio expansion (November 2026)

Use **MOTION STUDIO** in the timeline header to open the dedicated animation workspace. It adds additive/override per-bone position, quaternion rotation and scale layers (static pose offsets applied after animation evaluation); a six-preset locomotion driver linked to the existing gait system; basic look-at relationships and a connection to existing IK chain targets; named snapshot takes and JSON compilation; keyed channel visualization; camera review; PNG capture and a frame contact sheet. It also includes basic rig/animation state checks.

**Scope limits:** These layers are static weighted offsets, not yet independently keyframed or blended NLA tracks. The take compiler saves/loads timeline snapshots and exports JSON rather than compiling all takes into one multi-clip GLB. Camera captures use the active WebGL canvas; reliable captures on all browsers and continuous video recording need runtime verification. Bone look-at does not enforce joint limits; IK reach depends on an existing valid IK chain. No claims of offline operation, Blender-equivalent animation NLA, professional certification, anatomical accuracy or universal GLB export compatibility are made.

The hosted HTML still imports Three.js over the network. Preserve the existing `assets/humanoid.glb` and `assets/scorpion.glb` in the GitHub Pages repository. This lightweight delivery excludes 3D assets.


## Motion Studio extended animation update (November 2026)
- Per-frame keyed transform layers (bone rotation SLERP, translation, scale); additive/override mode, mute and bake-to-timeline. The compositor is procedural per frame rather than a complete nonlinear animation editor.
- Saved timeline takes can be compiled as multiple named clips into a single GLB. Confirm target importers correctly recognize all animation clips.
- Per-bone angular deviation limit relative to rest, tracking / reach, and experimental foot stabilization (not a full constraint graph, robust contact IK or physically modeled stance).
- Keyframed perspective camera interpolation, optional live WebM capture, PNG snapshots and contact sheets. Recording codec/permission support varies by browser.
- The `npm run build:offline` script requires one-time internet access to install pinned `three` and `esbuild` dependencies (`npm install`), then bundles local JavaScript and any assets in `assets/`. There is no already-certified single-file HTML in this source release.
- Automated checks verify JavaScript syntax and controls only. Full physical rigs, export round-trip and browser interoperability remain unverified; do not represent this as certified production software.

## Advanced nonlinear editing update (November 2026)

The Motion Studio panel now includes modules 08–12:
- **NLA strips:** add saved takes as time-positioned strips; choose start, duration, speed including reverse, fade-in/out, blend weight, override or additive blending. Restrict each strip to selected bone channels through an editable bone mask. The strip preview is evaluated during playback. These are pose-channel masks; not a full transform-axis-specific mixer.
- **Ordered constraints:** add per-bone angular limits, rotation copy, or aim-to-bone targets; reorder or remove constraints. A dependency check rejects cycles. These evaluation constraints are separate from the original IK stack.
- **Character root motion path:** author XYZ waypoints at explicit frames, interpolate world-space root position and display a path line.
- **Shot sequencer:** capture camera poses as independently timed shots; support cuts and overlaps with configurable crossfade. Existing video recording captures the active rendered output.

**Known limitations:** These are in-memory authoring tools. The standalone NLA strip stack, path/shot edits, and ordered constraints are not currently serialized by native project saves or baked automatically into GLB exports. Use the existing timeline bake and multi-clip export for ordinary keyed animation; output from NLA and paths requires an additional integration/baking pass for interoperable GLB delivery. Foot contact still uses experimental heuristics rather than a validated multi-contact solver. A CDN-hosted Three.js build remains online-only. The provided offline build workflow requires local npm dependencies, and no independently confirmed fully offline artifact is included. Static checks do not constitute a browser regression test or certification.


## Priority composition export and project persistence patch (2026-11-02)
- Version 2 project JSON includes Motion Studio layer key maps, takes, angular limits, camera keys, NLA strips, ordered constraints, waypoints, camera shot sequencing and active editor toggles. Older version 1 projects remain readable.
- Composed NLA/constraints/path/foot IK are sampled into a separate `Composed_NLA_Constraints_Path` glTF animation clip (up to 3,600 samples) alongside available original takes. This is dense sampling, not an editable nonlinear graph in glTF.
- Root waypoints have editable time-keyed cubic Hermite interpolation, with optional travel-direction alignment; line preview samples the curve.
- Contact assist adds planted-anchor hysteresis and uses available enabled foot IK chains rather than translating the whole rig as a fallback. This is **not** a force-based dynamics solver; no force, friction, mass or ground collision model is implemented and results are not physically validated.
- The hosted HTML still imports Three.js from CDN. `npm install && npm run build:offline` is required to produce an offline artifact on a machine with npm dependencies.
- JS module syntax check passed. Browser runtime and exported GLB round-trip tests have not passed in this execution environment.

## 2026-11-02 — Motion Studio visual workflow correction

The Motion Studio overlay now includes a persistent 10-module navigation ribbon with functional jumps to Animation Layers, Locomotion, Target Relationships, Review Viewer, Clips/Curves, NLA Strips, Bone Masks, Constraints, Character Paths and Cameras. Each module is discipline-color-coded (purple/orange/cyan/green), with matching fieldset accents, selected-module descriptions and focus outlines. The navigation is UI-only and preserves the existing animation engine and data model. Static source/syntax verification passed. Automated Chromium navigation was blocked by the environment (`ERR_BLOCKED_BY_ADMINISTRATOR`), so visual and workflow browser QA still needs confirmation after deployment.

## Live Motion Studio 3D viewport repair (November 2026)
The Motion Studio preview now renders the same active scene with its own Three.js WebGL renderer and a synchronized copy of the active camera, instead of copying pixels from the main renderer before its draw call. Open Main Rigging App, import the model, and click MOTION STUDIO: the live viewer reflects rig poses and animation. The status line below the viewer reports model/bone/frame information or a rendering failure. Existing GLB assets remain in `assets/`. The hosted HTML still requires CDN access for Three.js. Source syntax checks do not establish GPU/browser runtime compatibility.

## Color workflow / VIS / tutorials refresh (2026-11-02)

The splash screen now distinguishes rig and skin (lime), animation/NLA (purple), locomotion/path (orange), constraints (cyan), camera review (green), and live VIS (blue). The built-in About dialog has Color Workflow, VIS Telemetry, and QA / Limitations chapters. The VIS dock includes a shortcut to the live Motion Studio and an About workflow guide. Existing FPS, joint rotation and sampled weight statistics remain scene-derived; advanced editor counters show `—` unless corresponding editor rows are exposed, rather than displaying fabricated metrics. This is a user-interface/documentation enhancement, **not** an additional validated simulation system. The hosted Three.js CDN dependency remains.


## Release gate — 2026-11-02 (not certified)

The hosted `index.html` still depends on CDN Three.js. A self-contained, offline file must be **built**, not merely renamed:

1. Put original `humanoid.glb` and `scorpion.glb` in `assets/`.
2. With internet available once on your build computer, run `npm ci` (if lockfile present) or `npm install`.
3. Run `npm run check`, then `npm run verify:glb -- assets/humanoid.glb assets/scorpion.glb`.
4. Run `npm run build:offline`, then `npm run verify:offline`.
5. Open `offline/PROFILE_MOTION_ENGINE_OFFLINE.html` with network disabled. Import models, move bones, scrub all animation presets, save/reopen a project and export/reimport GLB in a browser and in Blender.

The offline builder now fails if either demo asset is missing. `verify:offline` rejects remote script tags, an importmap, unresolved Three.js imports, or absent embedded demo assets. Passing this check establishes packaging conditions, **not** full runtime functionality.

### What the new validation does and does not prove

- `verify:glb` checks GLB v2 headers, chunks, JSON, skin joint references, animation sampler references, and presence of weight attributes. It cannot prove accuracy of weight values, hinge placement, exported clip interpolation, or compatibility with Blender.
- Source model audit: `humanoid.glb` has 1 unskinned mesh and 0 clips; `scorpion.glb` has 9 unskinned meshes and 0 clips. Both therefore require PROFILE-generated rigs.
- Foot-contact support remains kinematic foot anchoring, not a physical contact-force, friction, inverse-dynamics, or certified stability solver. Do not advertise force-based gait simulation.
- Constraints are evaluated in the application; their mathematical correctness and cross-runtime export fidelity have not passed an independent compliance suite.
- Required before any professional certification: automated real-browser rig regression, runtime assertion checks across presets, synthetic contact tests for multiple slopes and velocities, GLB round trips in a second engine, performance and stability testing on target browsers/devices, and independent reviewer signoff.
