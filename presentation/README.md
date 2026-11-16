# Bearing-holder assembly pipeline

AI-generated images and instructions. Errors possible.

The main example is the [7 × 5 6810 holder, 15 mm depth](../parts/oobb_part_holder_bearing_6810_bearing_size_7_width_5_height_15_depth/).
All 44 canonical holder pages and their navigation leaves use a per-holder
assembly manifest for the diagram, parts table and CSV. Quantities cover one
holder or adapter. Mating motors, shafts and application-specific mounting
hardware are identified separately where the CAD does not specify their length.

## Rebuild

Use the existing OOBB Python environment, `requirements-catalogue.txt` and Blender.
Set `BLENDER_EXE` if Blender is not discoverable. Run from any working directory:

```powershell
python C:/gh/oomlout_oobb_part_holder_bearing_version_5/catalogue.py assembly
python C:/gh/oomlout_oobb_part_holder_bearing_version_5/catalogue.py assembly --filter 15_depth
python C:/gh/oomlout_oobb_part_holder_bearing_version_5/catalogue.py verify
```

`assembly.py --force` bypasses the render cache. `catalogue.py build` first
regenerates production CAD; the assembly-only command reads existing production
meshes and never replaces them. Render failures stop documentation generation.
An invalid filter fails rather than selecting another holder.

The example is pinned by `example_id` and `example_image` in `catalogue.json`.
After rebuilding it, refresh only its OOBB base-project thumbnail:

```powershell
python C:/gh/oomlout_oobb_version_5/presentation/scripts/build_project_thumbnails.py --filter bearing-holders
```

## Geometry and inventory

1. `assembly.inventory` reads each canonical `working.yaml` and `3dpr.stl`.
   `restore_print_mesh` separates connected pieces and reverses the production
   print transform: subtract the bed translation and rotate the upper half back
   by 180° around X. The off-centre servo split, double-bearing centres and unsplit
   building-block adapter retain their actual geometry. Piece volume is conserved.
2. Frame/hub quantities come from the connected production pieces. Joining axes
   and captive-nut counts come from `working_scad.get_mounting_layout`, with the
   90-degree extension's additional joins included. Nominal bearing dimensions
   come from the local OOBB table or the variant's explicit dimensions.
3. The bevel corners use the retained component meshes and `layout.json` in their
   existing examples, with the exact transforms and gear phase in `assembly.scad`.
   Their six printed holder pieces and two companion gears are counted separately.
   Gear meshes remain the retained backed-tooth family; do not substitute a newer
   gear with the same historical ID.
4. `presentation/scripts/render_assembly.py` renders assembled and exploded views
   in Blender. The production vertices are unchanged. Teal identifies stationary
   frames, black identifies rotating hubs and companion gears, and grey identifies
   hardware. Yellow is reserved for small spot accents, never whole hubs or other
   substantial components. Views use orthographic cameras and soft lights.
5. `publish_sheet` labels both views and adds the hardware quantities and AI notice.
   `catalogue.page` inserts the same manifest's BOM and instructions into canonical
   and navigation READMEs, with paths relative to each page.

Every part folder receives `assembly.png`, `assembly.json` and
`assembly_parts.csv`. Navigation stays text-only and references canonical assets.
Temporary component STLs, raw views and logs stay in ignored `build/assembly`.
The cache includes source hashes, generator and renderer hashes, and Blender's
version. Validation checks source/image hashes, image dimensions, CSV parity and
all generated local links. Existing manual text outside generation markers stays.

## Hardware assumptions

The table is a dimensional inventory derived from this repository's CAD and
existing corner guides, not a supplier catalogue. No unverified OOMP hardware IDs
or purchasing links are generated. Printable parts are included because these
tables describe the necessary parts for each holder.

The 15 mm holder uses six M3 × 12 mm countersunk screws, with both ends inset
1.5 mm. A 9 mm countersunk stack uses a nominal M3 × 10 mm stock screw, consistent
with the existing 6704 corner guide; check protrusion. The socket-cap exception
uses a nominal M3 × 10 mm screw in its 12 mm stack, with a recessed 3 mm head.
These stock-length selections do not establish a physical fit.

Bearing rings have nominal envelopes; they do not model races or balls.
Illustrative joining screws omit threads and drive sockets. Captive-nut models
are simplified hexagonal rings. Corner fasteners, extension nuts, coupler
hardware and motor interfaces are listed but omitted from the render, as stated
on the affected pages. Corner gear washer quantities assume one under each head
and nut. Servo and coupler screw lengths depend on the mating hardware.

Hub-only motor adapters need an external stationary bearing support. Hubs without
their own joining holes require retention by the mating shaft/interface. The
6704 captive-labelled variant has no fitting captive mounting-nut pockets;
its joining nuts are still required. Physical fit and load capacity are untested.
