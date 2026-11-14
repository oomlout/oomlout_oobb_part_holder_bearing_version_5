# OOBB bearing holders, version 5

The catalogue is in [working_populate.py](working_populate.py). Drawings are in
[working_scad.py](working_scad.py), using multiline dictionaries, `**kwargs`,
OOBB primitives and component groups. There is no handwritten SCAD, imported
legacy geometry, or dependency on the old generator at build time.

`working_oomp_populate.py` is the compatibility entry point used by `working.py`.
The `parts_source` and `parts` folders are generated from the catalogue.

The [6810 bevel corner](examples/corner_6810/README.md) and
[6704 corner for the 3-wide bevel gear](examples/corner_6704/README.md) have two
connected corner halves with a vertical split, four whole hub discs, the full
fitting M6/M3 grid and extra outward mounting rows, printable STLs, and assembled / exploded / animated
meshing examples. Build either with `python action_make_corner.py --bearing 6704`
or `--bearing 6810`, and check it with the same argument to `validate_corner.py`.

## Catalogue

Taxonomy:

```text
oobb, part, holder, bearing, {bearing_size}_bearing_size,
{width}_width, {height}_height, {depth}_depth, {extra}
```

The two former jack variants use `holder_90_degree` instead of `holder`, and
`basic` distinguishes the open nut-loading-slot version. Width and height are
nominal grid units; depth is the assembled thickness in mm, not half thickness.
Motor adapters retain their original nominal grid designation even when the
saved geometry is cylindrical.

All source names below have the prefix `oobb_bearing_plate_` and refer to
`C:/gh/oomlout_oobb_version_3/things`. Each generated record retains its complete
`legacy_id` and `legacy_source`.

| Source suffix | Bearing | Width | Height | Depth | New extra / family |
| --- | --- | --- | --- | --- | --- |
| `03_03_12_606` | 606 | 3 | 3 | 12 | standard holder |
| `03_03_12_6704` | 6704 | 3 | 3 | 12 | standard holder |
| `03_03_12_6803` | 6803 | 3 | 3 | 12 | standard holder |
| `03_03_12_6804` | 6804 | 3 | 3 | 12 | standard holder |
| `05_05_12_6808` | 6808 | 5 | 5 | 12 | standard holder |
| `07_05_12_6810` | 6810 | 7 | 5 | 12 | standard holder |
| `03_03_12_6704_sh_motor_gearmotor_01` | 6704 | 3 | 3 | 12 | `motor_gearmotor_01` |
| `03_03_12_6704_sh_motor_servo_micro_01` | 6704 | 3 | 3 | 12 | `motor_servo_micro_01` |
| `03_03_12_6704_ex_horn_adapter_printed_sh_motor_servo_standard_01` | 6704 | 3 | 3 | 12 | `motor_servo_standard_01_horn_adapter_printed` |
| `03_03_12_6704_ex_horn_adapter_screws_sh_motor_servo_standard_01` | 6704 | 3 | 3 | 12 | `motor_servo_standard_01_horn_adapter_screws` |
| `03_03_12_6704_sh_motor_building_block_large_01` | 6704 | 3 | 3 | 12 | `motor_building_block_large_01` |
| `03_03_12_6704_sh_motor_n20` | 6704 | 3 | 3 | 12 | `motor_n20` |
| `jack_03_03_12_606` | 606 | 3 | 3 | 12 | `holder_90_degree`, no extra |
| `jack_basic_03_03_12_606` | 606 | 3 | 3 | 12 | `holder_90_degree`, `basic` |

The catalogue now contains **41 variants**: the 14 migrations above, seven
6705 equivalents, two smaller embedded-nut variants, ten 6709 variants,
one standard 608, two 6810 captive-nut variants, a 6810 centre with a 30 mm bore,
a 9 mm single 6704, a 9 mm double 6704, and two-bearing 6810 and 6704 bevel corners.
The new designs do not claim a
legacy source. Both 6704 and 6705 have these eight choices of `extra`:

- empty: standard M6 centre bore and complete fitting M6/M3 grid
- `motor_gearmotor_01`
- `motor_servo_micro_01`
- `motor_servo_standard_01_horn_adapter_printed`
- `motor_servo_standard_01_horn_adapter_screws`
- `motor_building_block_large_01`
- `motor_n20`
- `inside_embedded_m3_nuts`

The double 6704 uses an **8 x 3 OOBB plate with 9 mm assembled depth** (`extra: double`). Its
`bearing_positions: [[3, 2], [6, 2]]` are one-based OOBB grid coordinates:
centres at (-22.5, 0) and (22.5, 0) mm, 45 mm (three pitches) apart. Each
bearing has its own M6 centre bore, annular seat, relief and diagonal hub joins.
The shared frame uses the fitting OOBB mounting grid and splits into two
4.5 mm halves for printing. The single 6704 also has a 9 mm depth option.

The other 6704/6705 options use 3 x 3 grid units and 12 mm assembled depth. The 6705 bearing
seat uses the named OOBB dimensions (25 mm inner diameter, 32 mm nominal outer
diameter, 4 mm nominal thickness). Its round adapter bodies increase from
12 to 14.5 mm radius to reach the larger inner race. Motor interfaces, the
offset screw-horn split and the unsplit building-block option remain as on 6704.

The **6709 5 x 5 x 12** family includes all eight choices above, plus
`inside_embedded_m6_nuts` and the existing
`inside_mechanical_coupler_flange_name_5_mm_bore` option. Square bodies are
75 x 75 mm. Round motor-adapter bodies have a 24.5 mm radius, sized for the
larger inner race. Shaft interfaces and their mounting patterns stay the same;
the 6709 hub's joining screws remain on 45-degree diagonals, now at
(+/-13, -/+13) mm. Gearmotor and micro-servo variants use all four diagonals
in print mode. The complete fitting M6/M3 grid covers the frame and hub.
The screw-horn adapter retains its z=0.5 split, and the building-block adapter
remains a single piece, just like the smaller versions.

### Complete mounting patterns and captive nuts

The frame and rotating inside now consider every position on the **15 mm M6
grid** and the intervening **7.5 mm M3 grid**. Where a main-grid M6 hole is too
large for the bearing seat or body, a plain M3 hole is used if it fits.
The centre remains the specified shaft interface, with no captive nut.
Motor inserts, servo connections, and OOMP coupler connections retain their
required sizes and positions.

`get_mounting_layout(**kwargs)` checks the most restrictive bearing/fastener
clearances across the three export modes. `mounting_minimum_web`, default
**0.3 mm**, is the minimum CAD material between new features. Nut checks use
hexagonal outlines and try additional rotations. Holes cannot cut into the
bearing recess, through a body edge, or into another connection's head or nut.
The narrowest new webs still need a practical print/strength check.

On captive-nut versions, requested nut positions take priority; additional
inside holes receive matching nuts wherever the pocket can fit. Where the
hole fits but a pocket cannot, the hole remains plain. Outer-frame holes do
not receive captive nuts. M3 captive variants keep M3 bores at their inner
main-grid positions so the M3 nuts remain retained.

| Inside variant | Fitted pockets | Plain-hole behaviour |
| --- | --- | --- |
| 6704, M3 | None at the standard grid spacing | Four M3 holes at (+/-7.5, 0), (0, +/-7.5); replaces the earlier experimental 13 mm nut spacing |
| 6705, M3 | 4 M3 | Standard 15 mm spacing |
| 6709, M3 | 20 M3 | Includes the newly usable half-grid positions |
| 6709, M6 | 4 M6 + 4 M3 | Additional fitting holes without pockets remain open |
| 6810, M3 | 22 M3 | Includes cardinal, corner and half-grid positions |
| 6810, M6 | 4 M6 + 2 M3 | Four additional plain M6 holes at (+/-15, +/-15); M6 nuts do not fit at these corners |

`embedded_nut_positions` supplies preferred pockets; the drawing fits further
pockets automatically. `embedded_nut_rotation`, `embedded_nut_rotation_radial`
and `mounting_minimum_web` remain editable. All pockets use named `oobb_nut`
primitives at the split, with named `oobb_hole` bolt bores. `prepare_print=True`
exposes both pocket halves; `False` shows the assembled sandwich.

The companion `shim_02_6704` is deferred, as agreed in the plan: it has no
legacy grid width/height and needs its own taxonomy decision. Bearing wheels,
circles and standalone hardware are outside this catalogue.

### 608 and 6810 additions

The **608 standard holder** is 3 x 3 x 12 mm-depth (45 x 45 x 12 mm assembled).
The bearing is 8 x 22 x 7 mm according to the [SKF catalogue](https://www.emarketplace.in.skf.com/industrial/bearings?search=608-RSH).
Its fit dimensions are explicit in `working_populate.py` because 608 is absent
from the shared OOBB variable table. Print mode starts with 0.2 mm radial outer
clearance (22.4 mm recess diameter) and a 7 mm seat depth. A central M6 hole
retains approximately 0.74 mm of plastic at the narrowest inner-race seat;
physical fit remains untested. There are no special inside options for 608.

The **6810 captive-nut holders** use the existing 7 x 5 x 12 mm-depth envelope
(105 x 75 x 12 mm assembled) and bearing fit, with the expanded mounting grid. The
existing standard 6810 remains available. These special insides are available:

- `inside_embedded_m3_nuts`
- `inside_embedded_m6_nuts`
- `inside_hole_30_mm`

The complete grid and captive-pocket counts are described above. Both 608 and
6810 retain `prepare_print` and the two-half layout.

### 6810 centre with a 30 mm bore

`extra="inside_hole_30_mm"` adds a centre ring with a **30 mm diameter
through-hole**, drawn using `oobb_hole` and a project-specific named radius.
The four **M6 holes at (+/-15, +/-15) mm** are the corners of the standard
3 x 3 OOBB grid. Two plain M3 holes remain at (+/-22.5, 0); the
Y-axis joining pair is at (0, +/-21), moved 1.5 mm inward for full-depth nuts. There are no
sandwich mounting-nut pockets in this option.

The nominal bore is 30 mm in every mode, without an added fit allowance.
`centre_hole_diameter` is editable in its catalogue block. The surrounding
6810 holder remains 7 x 5 x 12 mm, with the existing bearing fit. Two M3
countersunk joining screws at (0, +/-21) mm sit 1.5 mm radially inward from
the M3 half-grid positions, leaving the bore and all four M6 corners clear.
Their full-depth opposite-face M3 nut recesses fit inside the bearing's inner
surface, so the nuts sit flush rather than proud.
Both screw and nut primitives use `overhang=True`. `prepare_print` still
produces the two sandwich halves.

### Joining screws

Outer joining screws move between grid rows, beyond the outermost grid
column, freeing usable perimeter midpoints. On 3 x 3 frames their positions
are rotations of (18.5, 8) mm; on 5 x 5 frames, rotations of (33.5, 22.5) mm.
The 7 x 5 frame uses (+/-48.5, +/-22.5) mm. The 90-degree variants retain their
extension hardware and use two frame joins plus two extension joins.

The 6808 standard centre and the standard/captive 6810 centres use M3
joining holes at (-7.5, 7.5) and (7.5, -7.5) mm on the half-grid. The
30 mm bore option moves its pair inward to (0, +/-21) mm for flush nuts. Each uses named countersunk screw
and opposite-face nut primitives with `overhang=True` in all modes.
Other existing inner joining arrangements are retained. Small hubs retain their 7.5 mm joining radius.
The 6709 uses (+/-13, -/+13) mm, making room for additional half-grid holes.
Edit `inner_joining_positions` for these grid joins, or
`inner_joining_radius` / `inner_joining_rotation` for the existing radial joins. Motor/servo connection holes stay in place.
Screw-horn and unsplit building-block exceptions retain their arrangements.

The 6704 captive-labelled option retains M3 socket-cap joining screws; other
printed joins use M3 countersunk screws. Existing radial laser inner joins
retain their head and nut recesses; the 6808/6810 grid joins use the countersunk
primitive in every mode. Outer joins retain their
standoffs. Mounting holes are excluded only where the head, nut, bearing seat
or fixed connection leaves insufficient material.

### 6709 middle piece for a 5 mm flange coupler

The 5 x 5 x 12 mm-depth variant has
`extra="inside_mechanical_coupler_flange_name_5_mm_bore"`. Its middle piece
mounts OOMP **`mechanical_coupler_flange_name_5_mm_bore`**. Here "5 mm" is the
coupler's shaft bore; its mounting screws are M3.

- Bearing: 6709, 45 mm bore x 55 mm outside diameter x 6 mm thickness.
- Holder: 75 x 75 x 12 mm assembled, split into two 6 mm halves.
- Coupler: 22 mm flange diameter, 2 mm flange thickness, 10 mm barrel diameter.
- Four M3 through-holes on a **16 mm bolt circle**, at (8, 0), (0, 8),
  (-8, 0), (0, -8) mm. This is not a 16 mm square pattern.
- Four captive M3 nut pockets at the split, plus a central M5 clearance hole.
- Separate hub joining screws at (-13, 13) and (13, -13) mm
  clamp both hub halves, at 45 degrees to the OOBB grid.

Place the nuts in the split face, assemble the hub around the bearing, and
fasten its two halves together. Bolt the metal flange flat against an outside
hub face with its barrel pointing away from the holder. The shaft passes through
the centre hole; the barrel and grub screws remain accessible outside the
plastic. The coupler hardware is not included in the printable solids.

Dimensions are copied from the OOMP project's `source_file/dimension/flange/dimension.csv`;
its drawing confirms that the 16 mm dimension is the bolt-circle diameter.
[The local reference snapshot](source_file/coupler_flange_5_mm_reference.yaml)
records the full OOMP ID, source paths and dimensions. Editable drawing values
live in the `working_populate.py` option block, so builds do not depend on the
OneDrive folder being available.

The shared OOBB library does not yet define 6709. Its nominal dimensions are
recorded in the catalogue from the [bearing manufacturer's table](https://www.cxnjs.com/content/150.html)
and resolved into project-specific named radii. The initial print allowance is
0.2 mm radially on the outside recess, giving a 55.4 mm recess diameter;
bearing-seat depth remains 6 mm. No shared library variables are changed.
Physical bearing/coupler fit remains untested.

## Building and editing

Use the local Python environment with the v5 `oobb`, `opsc`, OOMP and helper
modules available. OpenSCAD is needed to render STLs or PNG previews.

Regenerate catalogue metadata and all SCAD modes, without running unrelated
artwork actions:

```powershell
python -c "import working; working.main(run_action=False, modes=['3dpr','true','laser'], navigation=False)"
```

`3dpr.scad` defaults to the bed layout; `true.scad` is the nominal assembled
design. `laser.scad` and `laser_flat.scad` retain the assembled/sandwich layout.
To inspect assembled geometry with the **printing fit dimensions**, toggle:

```powershell
python -c "import working_scad; working_scad.main(prepare_print=False, modes=['3dpr'], navigation=False)"
```

That overwrites `3dpr.scad`. Restore the bed layout with:

```powershell
python -c "import working_scad; working_scad.main(prepare_print=True, modes=['3dpr'], navigation=False)"
```

The override is per build; the catalogue's default stays unchanged. Use
`filter='6804_bearing_size'` (or any part-ID substring) to regenerate one family.
Use `generate_stl=True` on `working.main` for the existing full export pipeline.

To add a variant, copy an `option` block in `working_populate.py`. Give it a
distinct `extra`. For an extra interior pattern, for example:

```python
option["extra"] = "interior_four_m3_holes"
option["interior_radius_name"] = "m3"
option["interior_hole_positions"] = [
    [-7.5, -7.5],
    [-7.5, 7.5],
    [7.5, -7.5],
    [7.5, 7.5],
]
```

Positions in that list are millimetres. Existing bearing and fastening patterns
remain present; check clearance before adding new holes. `print_gap`, `split_z`
and `split` can also be set in an individual option block.

## Drawing layout

`get_bearing_holder` composes the body, annular bearing recess and relief,
perimeter and interior holes, joining fasteners, and shaft interface.
`get_mounting_layout` selects fitting holes and pockets; `get_joining_positions`
keeps the editable screw coordinates together.
`get_bearing_holder_90_degree` uses those same features and adds the extension.
Small helpers keep the editable dimensions next to each feature.

`prepare_bearing_holder_print` clips two independent copies of the **complete**
assembled geometry using `oobb_slice`, flips the upper half, and places both
outer faces on z=0. Spacing follows the actual body width plus `print_gap`.
The inner hubs are separate solids by design; do not merge them into the frame.

Exceptions retained from the saved source:

- Screw-horn adapter: split at z=0.5, giving 6.5 and 5.5 mm sections.
- Building-block adapter: single piece, positioned on the bed without splitting.
- Basic 90-degree holder: complementary halves now share the same clipping
  routine, replacing its old ad hoc shifted/overlapping print layout.

## Migration details

The project now lives in `C:/gh/oomlout_oobb_part_holder_bearing_version_5`.
Current part IDs and navigation use `holder` and `holder_90_degree`; drawing
entry points and project-specific named dimensions use holder names too.
`body="plate"` and `oobb_plate` still describe the OOBB body primitive.
Historical `legacy_id` and `legacy_source` values retain their original v3
plate names so they continue to identify the saved source parts.

- Saved `things` SCAD/metadata are the reference. The current v3 generator has
  drifted and would change some rectangular plates into cylinders.
- Standard envelopes are 45, 75 and 105 mm, using `oobb_plate(extra_mm=True)`.
  The 6804 laser outline remains 47.75 mm.
- Bearing seats use project-specific named radii derived from OOBB variables.
  Saved 606 and 6810 fit differences are explicit in `define_bearing_dimensions`.
  The 606 print outer radius is 8.55 mm; the 6810 inner radius and seat depth are
  25 and 7 mm. The mode-dependent 6704 seat depth remains 3.6 mm for printing.
- Saved nut rotations include a double rotation in v3. The standard 90-degree
  extension retains its downward hex pockets explicitly. The basic version
  has open loading slots. The two versions are not collapsed into one shape.
- N20's saved SCAD uses radius 0.95 mm and an invalid negative-depth D flat.
  Its resulting circular opening is preserved using the v5 D-shaft primitive
  with `shaft_cut_depth=0`. Both shaft parameters are editable in the catalogue.
  This migration does not assert that this legacy opening fits a real N20 shaft.
- V5 screw/nut primitives supply support geometry and current fastener profiles;
  these are not byte-for-byte copies of the legacy generated meshes.

The current `oobb_cylinder` expands all modes and reuses the first radius,
so project aliases are resolved per enclosing mode before primitive expansion.
Standard OOBB variables and shared library files are untouched. All drawing
geometry uses OOBB primitives; there is no bespoke SCAD.

The flange-coupler variant records its full OOMP ID and uses that record's
dimensions with named `oobb_hole` and `oobb_nut` primitives. The fixed pattern
and M8 centre hole in `oobb_coupler_flanged` are not used for this 5 mm coupler.

## Verification

```powershell
python -m pytest tests/test_bearing_holders.py -q
```

Requires pytest, numpy, trimesh and OpenSCAD on PATH. The tests render all
37 assembled/print pairs and check watertightness, bed height, separation,
reassembly bounds, volume, centre of mass and inertia. Rendered sections probe
every planned mounting bore at three heights, the material around each opening,
and every captive pocket's enclosed sides and retaining faces in all modes.
Other tests cover taxonomy, runtime print overrides, positioning, bearing
seats, shaft and OOMP coupler interfaces, and diagonal joining screws.

The complete grid intentionally changes the old v3 volumes. The latest mesh
measurements and actual hole/nut layouts are recorded in
`source_file/migration_validation.json` for all 37 variants and all three modes.
Physical bearing, nut and shaft fit remains untested.
