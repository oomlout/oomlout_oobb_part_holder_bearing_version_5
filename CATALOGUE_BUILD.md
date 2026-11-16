# Catalogue build and maintenance

The canonical catalogue is `parts/`; each `parts_source/<OOMP ID>/working.yaml`
supplies its metadata and geometry parameters. The existing project geometry
functions remain in `working_scad.py`. The refresh preserves the active catalogue,
including local geometry changes, and never scans archived or legacy folders.

## Rebuild

Install `requirements-catalogue.txt` in the project's configured Python environment.
The existing OOBB library must also be importable. OpenSCAD and Blender are required;
use `OPENSCAD_EXE` and `BLENDER_EXE` when they are not on PATH. Native projects retain
their `solidcraft/config.json` helper and Python configuration.

Run `python catalogue.py build` (or the project's make-all entry). All active source
records are merged synchronously, CAD is generated using the project's recipes,
STLs are exported with checked subprocess results, previews are completed, and only
then are READMEs/navigation generated and validated. A failed export or render
fails the build. OpenSCAD STLs remain enabled where they are the production source.
The timing-belt storage adapter uses its native recipe and avoids duplicate STL export.

Use `--filter <OOMP-ID-substring>` for a focused build; unchanged parts stay in the
catalogue. Use `--populate` explicitly to regenerate the source catalogue definitions.
Use `--native` to additionally run an available native adapter. Legacy Roboclick/
CorelDraw actions are opt-in with `--legacy-actions`; make-all does not launch desktop
automation by default. Existing labels and specialised examples are preserved.

`python catalogue.py render` refreshes previews and docs. `python catalogue.py docs`
refreshes documentation alone; `python catalogue.py verify` checks coverage, artifact
hashes, PNGs and generated local links. `python working_navigation.py` is compatible
with older navigation callers and generates only text.

`python catalogue.py assembly` regenerates the per-holder assembled/exploded
diagrams, JSON manifests and CSV parts lists, then updates READMEs and validates
the catalogue. Use `--filter 15_depth` for the main 7 × 5 6810 example.
Both `build` and `render` include this assembly stage. `docs` consumes the existing
assembly outputs; run `assembly` first after changing geometry or assembly code.
See [assembly pipeline details](presentation/README.md).

## Documentation contract

Root READMEs contain Summary, Details, Parts and Assembly, one example and a link
to the first branching discovery category. They do not enumerate every part or
file. Every part page includes the full OOMP ID, complete YAML details, a preview
where printable geometry exists, and links to folders. Purchased hardware is labelled
explicitly and gets no invented mesh. Existing project instructions are retained in
`PROJECT_GUIDE.md` when present. Text outside generation markers is preserved.

Navigation categories contain README files; terminal records contain README.md and
oomp_id.txt only. Final selection links go directly to the canonical part folder.
The generator refuses to silently remove legacy copied assets: archive those first.

## Rendering and validation

The vendored Blender worker uses the OOBB satin-teal, warm-background studio style
on actual STL geometry, with angled/top views and a measured envelope. It does not
invent details, alter holes or smooth away geometry. Raw views and logs stay under
ignored `build/`; final 1600×1000 sheets and a SHA256 manifest are published.
Cache identity includes geometry, renderer, Blender version, label and sheet code.
Both ASCII and binary STL are accepted. Purchased hardware records are not rendered.

## Storage and Git history

The initial refresh was explicitly authorised to replace history after verification.
Verified worktree archives, hash manifests and original Git bundles are retained
outside this checkout under `C:/gh/_repository_recovery/catalogue_refresh_2026-11-14/`.
They preserve old navigation-only material and uncommitted work. Ignored build and
dependency caches are local and excluded from the published tree.

Normal future updates use ordinary commits. Do not reset history on each build.
Any future reset must preserve current files, all relevant refs, dirty/index changes
and remote-only work, then validate the final tree. Create a parentless commit from
that reviewed tree and publish only with an explicit old-remote-SHA lease. Verify an
independent full clone before expiring old local reflogs or collecting objects.
Do not claim GitHub server storage is reclaimed simply because its branch changed.

[Refresh record](MAINTENANCE.md)
