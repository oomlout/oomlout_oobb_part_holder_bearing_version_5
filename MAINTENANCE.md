# Catalogue refresh — 14 November 2026

The refresh retains all **44 active part records**, including the existing local
source and geometry edits. Canonical files live under `parts/`. Root discovery
links begin at the first branching category; final selections open part folders.
Each navigation leaf contains only README.md and oomp_id.txt with the full OOMP ID.

The previous navigation occupied **420,223,584 bytes**.
The previous parts occupied **425,246,416 bytes**. The original Git
directory occupied **116,623,329 bytes**. These are logical file sizes.
Original files, including navigation-only variants and dirty work, were backed up
and SHA256 checked before replacement. Recovery data is outside this repository.

## Build changes

The make-all entry uses a synchronous catalogue pipeline. Metadata is merged from
`parts_source`, project CAD recipes are retained, caller filters/options are honoured,
export failures propagate, and render completion precedes README generation. Legacy
GUI label actions and source repopulation are explicit options. ASCII and binary
STL measurement are supported; exports use compact binary STL. Cache identity
includes labels, geometry, Blender and renderer/sheet code. Manual README text
outside generation markers survives regeneration.

The studio sheets show actual exported geometry in angled and top views. Source
and image SHA256 values are in `presentation/catalogue.json`; validation counts are
in `presentation/validation.json`. Regenerate with `python catalogue.py build`.
The shared regression suite covers folder links, taxonomy prefixes, metadata filters,
manual notes, legacy asset preservation, hardware-only records and STL formats.

## History and storage

The reviewed final tree is intended as a new parentless Git snapshot, following the
explicitly authorised one-time history reset. Subsequent changes use normal commits.
Publication checks include indexed artifact hashes and an independent full clone.
Raw render caches, build logs, dependency environments and recovery archives are
excluded. The final measured storage and publication results are recorded in the
external batch report; retained recovery data is not claimed as freed disk space.

The corner fixtures retain their reviewed 12 mm backed-tooth companion gears. A compatibility validator preserves their original apex and spacer geometry; regenerated assembly examples and rendered collision checks verify the retained fit contract. They are not interchangeable with the newer flat-top bevel family.
