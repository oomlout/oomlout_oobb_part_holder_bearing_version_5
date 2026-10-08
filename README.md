# OOBB bearing plates, version 5

The catalogue is in [working_populate.py](working_populate.py). Drawings are in
[working_scad.py](working_scad.py), using multiline dictionaries, `**kwargs`,
OOBB primitives and component groups. There is no handwritten SCAD, imported
legacy geometry, or dependency on the old generator at build time.

`working_oomp_populate.py` is the compatibility entry point used by `working.py`.
The `parts_source` and `parts` folders are generated from the catalogue.

## Catalogue

Taxonomy:

```text
oobb, part, plate, bearing, {bearing_size}_bearing_size,
{width}_width, {height}_height, {depth}_depth, {extra}
```

The two former jack variants use `plate_90_degree` instead of `plate`, and
`basic` distinguishes the open nut-loading-slot version. Width and height are
nominal grid units; depth is the assembled thickness in mm, not half thickness.
Motor adapters retain their original nominal grid designation even when the
saved geometry is cylindrical.

All source names below have the prefix `oobb_bearing_plate_` and refer to
`C:/gh/oomlout_oobb_version_3/things`. Each generated record retains its complete
`legacy_id` and `legacy_source`.

| Source suffix | Bearing | Width | Height | Depth | New extra / family |
| --- | --- | --- | --- | --- | --- |
| `03_03_12_606` | 606 | 3 | 3 | 12 | standard plate |
| `03_03_12_6704` | 6704 | 3 | 3 | 12 | standard plate |
| `03_03_12_6803` | 6803 | 3 | 3 | 12 | standard plate |
| `03_03_12_6804` | 6804 | 3 | 3 | 12 | standard plate |
| `05_05_12_6808` | 6808 | 5 | 5 | 12 | standard plate |
| `07_05_12_6810` | 6810 | 7 | 5 | 12 | standard plate |
| `03_03_12_6704_sh_motor_gearmotor_01` | 6704 | 3 | 3 | 12 | `motor_gearmotor_01` |
| `03_03_12_6704_sh_motor_servo_micro_01` | 6704 | 3 | 3 | 12 | `motor_servo_micro_01` |
| `03_03_12_6704_ex_horn_adapter_printed_sh_motor_servo_standard_01` | 6704 | 3 | 3 | 12 | `motor_servo_standard_01_horn_adapter_printed` |
| `03_03_12_6704_ex_horn_adapter_screws_sh_motor_servo_standard_01` | 6704 | 3 | 3 | 12 | `motor_servo_standard_01_horn_adapter_screws` |
| `03_03_12_6704_sh_motor_building_block_large_01` | 6704 | 3 | 3 | 12 | `motor_building_block_large_01` |
| `03_03_12_6704_sh_motor_n20` | 6704 | 3 | 3 | 12 | `motor_n20` |
| `jack_03_03_12_606` | 606 | 3 | 3 | 12 | `plate_90_degree`, no extra |
| `jack_basic_03_03_12_606` | 606 | 3 | 3 | 12 | `plate_90_degree`, `basic` |

The catalogue now contains **36 variants**: the 14 migrations above, seven
6705 equivalents, two smaller embedded-nut variants, ten 6709 variants,
one standard 608 and two 6810 captive-nut variants. The new designs do not claim a
legacy source. Both 6704 and 6705 have these eight choices of `extra`:

- empty: standard M6 centre bore and interior M3 slots
- `motor_gearmotor_01`
- `motor_servo_micro_01`
- `motor_servo_standard_01_horn_adapter_printed`
- `motor_servo_standard_01_horn_adapter_screws`
- `motor_building_block_large_01`
- `motor_n20`
- `inside_embedded_m3_nuts`

The 6704/6705 options use 3 x 3 grid units and 12 mm assembled depth. The 6705 bearing
seat uses the named OOBB dimensions (25 mm inner diameter, 32 mm nominal outer
diameter, 4 mm nominal thickness). Its round adapter bodies increase from
12 to 14.5 mm radius to reach the larger inner race. Motor interfaces, the
offset screw-horn split and the unsplit building-block option remain as on 6704.

The **6709 5 x 5 x 12** family includes all eight choices above, plus
`inside_embedded_m6_nuts` and the existing
`inside_mechanical_coupler_flange_name_5_mm_bore` option. Square bodies are
75 x 75 mm. Round motor-adapter bodies have a 24.5 mm radius, sized for the
larger inner race. Shaft interfaces and their mounting patterns stay the same;
the larger hub's joining screws are rotated 45 degrees, on a 15 mm radius.
The usual pair is at approximately (-10.607, 10.607) and (10.607, -10.607) mm.
Gearmotor and micro-servo variants use all four diagonals for their additional
joining screws, keeping the original motor insert holes separate.
The standard plate now has the four cardinal OOBB holes at (+/-15, 0) and
(0, +/-15) mm. Outer-frame screws and mounting holes retain their positions.
The screw-horn adapter retains its z=0.5 split, and the building-block adapter
remains a single piece, just like the smaller versions.

### Embedded nuts

`inside_embedded_m3_nuts` replaces the interior slots with M3 bolt holes
and hex pockets centred on the sandwich split: four on 6704, 6705 and 6709,
and eight on 6810 (cardinal positions plus corners). The central M6 bore and the
separate hub joining screws remain. Place the nuts in the open split face and
close the other half over them. `prepare_print=True` exposes both pocket halves
upward; `False` shows the assembled, enclosed pockets.

Pockets use `oobb_nut(radius_name="m3")`, including OOBB's mode-specific nut
depth and clearance. Pockets have flats facing the centre bore. On 6709 the
rotation follows each position radially on every captive-nut variant.
Edit `embedded_nut_positions` and `embedded_nut_rotation` in the option blocks.

| Bearing | Nut centres | Bolt spacing | Print clearance assessment |
| --- | --- | --- | --- |
| 6705 | (+/-7.5, 0), (0, +/-7.5) mm | 15 mm across opposite holes | At least 1.25 mm to the centre bore; about 1.83 mm to the faceted bearing seat |
| 6704 | (+/-6.5, 0), (0, +/-6.5) mm | 13 mm across opposite holes | Experimental: about 0.25 mm to the centre bore and 0.33 mm to the faceted bearing seat |
| 6709, M3 | (+/-15, 0), (0, +/-15) mm | 30 mm across opposite holes | More than 8.7 mm to the centre bore and 4.3 mm to the bearing seat |
| 6709, M6 | (+/-15, 0), (0, +/-15) mm | 30 mm across opposite holes | More than 6.6 mm to the centre bore and 2.1 mm to the faceted bearing seat |
| 6810, M3 | Cardinal positions and (+/-15, +/-15) mm corners | 15 mm grid | Corner pockets leave about 0.68 mm to the faceted bearing seat |
| 6810, M6 | (+/-15, 0), (0, +/-15) mm | 30 mm across opposite holes | Corner M6 pockets do not fit; cardinal pockets leave over 4.6 mm to the bearing seat |

`inside_embedded_m6_nuts` provides four named M6 bolt holes
and M6 hex pockets, retaining the central M6 bore and the two M3 hub joining
screws. Pockets are centred on the split and rotated 30 degrees. OOBB's print
nut depth is 5.5 mm, leaving 3.25 mm of retaining plastic on each outside face
of the 12 mm assembly. Edit `embedded_nut_radius_name`,
`embedded_nut_positions`, `embedded_nut_rotation` and
`embedded_nut_rotation_radial` in the catalogue block.

There is deliberately **no captive nut in the centre hole** and none in the
stationary outer plate. On 6709 the four cardinal positions are all the standard
OOBB grid positions that fit enclosed nut pockets; the corners extend too close
to the bearing seat. The larger 6810 accommodates M3 corner pockets as well.
On the large hubs the diagonal joining screws clear the four M6 nut envelopes
by over 1.9 mm.

M6 captive-nut patterns are offered for 6709 and 6810. They cannot fit radially between
the central M6 bore and the 6704 or 6705 bearing seat, even before allowing wall
thickness. The flange-coupler mounting nuts remain M3 because that hardware's
four holes are specified for M3 screws; enlarging those would not match it.

The 6704 pockets do not fit at 15 mm spacing even after rotation. Moving them
inwards to 13 mm spacing gives enclosed CAD pockets, but the remaining webs are
thinner than a typical extrusion width and may disappear during slicing or
break during assembly. This is a trial variant, not a strength- or fit-validated
part. Its bolt spacing differs from the 6705 version. Neither has been physically
printed or fitted with nuts yet.

The companion `shim_02_6704` is deferred, as agreed in the plan: it has no
legacy grid width/height and needs its own taxonomy decision. Bearing wheels,
circles and standalone hardware are outside this catalogue.

### 608 and 6810 additions

The **608 standard plate** is 3 x 3 x 12 mm-depth (45 x 45 x 12 mm assembled).
The bearing is 8 x 22 x 7 mm according to the [SKF catalogue](https://www.emarketplace.in.skf.com/industrial/bearings?search=608-RSH).
Its fit dimensions are explicit in `working_populate.py` because 608 is absent
from the shared OOBB variable table. Print mode starts with 0.2 mm radial outer
clearance (22.4 mm recess diameter) and a 7 mm seat depth. A central M6 hole
retains approximately 0.74 mm of plastic at the narrowest inner-race seat;
physical fit remains untested. There are no special inside options for 608.

The **6810 captive-nut plates** use the existing 7 x 5 x 12 mm-depth envelope
(105 x 75 x 12 mm assembled), bearing fit and outer fastening pattern. The
existing standard 6810 remains available. Only these special insides are added:

- `inside_embedded_m3_nuts`
- `inside_embedded_m6_nuts`

Both use the four cardinal inner grid positions: (+/-15, 0) and
(0, +/-15) mm. The M3 version also uses the four (+/-15, +/-15) corners.
Each has a captive nut at the split, radially aligned hex flats,
an unchanged plain centre hole, and separate M3 joining screws rotated 45
degrees on a 15 mm radius. There are no motor or coupler variants for 6810.
The default M6 grid cutouts are suppressed for the M3 captive variant, so each
M3 pocket retains its correctly sized bolt hole and retaining material.
Both 608 and the new 6810 options retain `prepare_print` and the two-half layout.

### Diagonal joining screws across families

Every family with existing screw-joined inner halves now uses a 45-degree
joining pattern: 6704, 6705, 6804, 6709 and the captive-nut 6810 variants.
The small hubs use a 7.5 mm joining radius (x/y approximately +/-5.303 mm);
the large hubs use 15 mm (x/y approximately +/-10.607 mm). This is the same in
print, nominal and laser modes. Outer-frame screws and shaft/motor connection
patterns remain in their original positions. Designs with no inner joining
screws, including the unsplit and screw-horn exceptions, keep that arrangement.

The experimental **6704 captive-nut variant uses M3 socket-cap joining screws**
with named counterbores. Its previous wide countersinks would leave almost no
wall alongside the extra nut through-holes. The other printed variants retain
M3 countersunk joining screws. The thin centre-bore webs on 6704 remain a trial
fit and are not strength validated.

Laser inner joining holes now use an M3 through-bolt with a recessed head and
nut in the outer faces, rather than a long central hex standoff. That keeps the
middle of the sandwich clear for the captive nuts. Outer-frame standoff
geometry remains unchanged. All these features use OOBB named primitives.

### 6709 middle piece for a 5 mm flange coupler

The 5 x 5 x 12 mm-depth variant has
`extra="inside_mechanical_coupler_flange_name_5_mm_bore"`. Its middle piece
mounts OOMP **`mechanical_coupler_flange_name_5_mm_bore`**. Here "5 mm" is the
coupler's shaft bore; its mounting screws are M3.

- Bearing: 6709, 45 mm bore x 55 mm outside diameter x 6 mm thickness.
- Plate: 75 x 75 x 12 mm assembled, split into two 6 mm halves.
- Coupler: 22 mm flange diameter, 2 mm flange thickness, 10 mm barrel diameter.
- Four M3 through-holes on a **16 mm bolt circle**, at (8, 0), (0, 8),
  (-8, 0), (0, -8) mm. This is not a 16 mm square pattern.
- Four captive M3 nut pockets at the split, plus a central M5 clearance hole.
- Separate hub joining screws at (-10.607, 10.607) and (10.607, -10.607) mm
  clamp both hub halves, at 45 degrees to the OOBB grid.

Place the nuts in the split face, assemble the hub around the bearing, and
fasten its two halves together. Bolt the metal flange flat against an outside
hub face with its barrel pointing away from the plate. The shaft passes through
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

`get_bearing_plate` composes the body, annular bearing recess and relief,
perimeter and interior holes, joining fasteners, and shaft interface.
`get_bearing_plate_90_degree` uses those same features and adds the extension.
Small helpers keep the editable dimensions next to each feature.

`prepare_bearing_plate_print` clips two independent copies of the **complete**
assembled geometry using `oobb_slice`, flips the upper half, and places both
outer faces on z=0. Spacing follows the actual body width plus `print_gap`.
The inner hubs are separate solids by design; do not merge them into the frame.

Exceptions retained from the saved source:

- Screw-horn adapter: split at z=0.5, giving 6.5 and 5.5 mm sections.
- Building-block adapter: single piece, positioned on the bed without splitting.
- Basic 90-degree plate: complementary halves now share the same clipping
  routine, replacing its old ad hoc shifted/overlapping print layout.

## Migration details

- Saved `things` SCAD/metadata are the reference. The current v3 generator has
  drifted and would change some rectangular plates into cylinders.
- Standard envelopes are 45, 75 and 105 mm, using `oobb_plate(extra_mm=True)`.
  The 6804 laser outline remains 47.75 mm.
- Bearing seats use project-specific named radii derived from OOBB variables.
  Saved 606 and 6810 fit differences are explicit in `define_bearing_dimensions`.
  The 606 print outer radius is 8.55 mm; the 6810 inner radius and seat depth are
  25 and 7 mm. The mode-dependent 6704 seat depth remains 3.6 mm for printing.
- The 6804 printed perimeter joining screws move outward by 0.01 mm to avoid
  the exact M3/bearing tangency that otherwise creates a non-manifold edge.
  This is exposed as `joining_tangent_clearance`; bearing fit is unchanged.
- Saved nut rotations include a double rotation in v3. The standard 90-degree
  extension retains its downward hex pockets explicitly. The basic version
  has open loading slots. The two versions are not collapsed into one shape.
- N20's saved SCAD uses radius 0.95 mm and an invalid negative-depth D flat.
  Its resulting circular opening is preserved using the v5 D-shaft primitive
  with `shaft_cut_depth=0`. Both shaft parameters are editable in the catalogue.
  This migration does not assert that this legacy opening fits a real N20 shaft.
- V5 screw/nut primitives supply support geometry and current fastener profiles;
  these are not byte-for-byte copies of the legacy generated meshes.

Two local primitive workarounds are explained beside their code. The current
`oobb_cylinder` expands all modes and reuses the first radius, so project aliases
are resolved per enclosing mode before primitive expansion. Standard OOBB
variables are untouched. The named-radius branch of `oobb_slot` references an
undefined variable, so short slots use a hull of two named OOBB holes instead.
No shared library files were changed.

The flange-coupler variant records its full OOMP ID and uses that record's
dimensions with named `oobb_hole` and `oobb_nut` primitives. The fixed pattern
and M8 centre hole in `oobb_coupler_flanged` are not used for this 5 mm coupler.

## Verification

```powershell
python -m pytest tests/test_bearing_plates.py -q
```

Requires pytest, numpy, trimesh and OpenSCAD on PATH. The tests render real
meshes, check all 36 assembled/print pairs for watertightness, bed height and
separation, then reassemble the halves and compare volume, bounds, centre of
mass and inertia. Saved standard-part lower-half volumes provide an additional
migration check. Other checks cover taxonomy, runtime overrides, non-print
modes, named bearing dimensions, through-holes and whole-part positioning.
Embedded-nut checks section the actual rendered meshes in all three modes to
check access at the split, retaining material above and below, and the small
remaining web to the centre bore. They also check nut-to-bearing clearance.
Coupler checks also verify the OOMP dimensions, mounting circle, central shaft
hole, captive pockets, independent hub fasteners and 6709 bearing retaining lip.
M6 checks verify full-size bolt holes, pocket depth, retaining material,
clearance to the bearing seat and centre bore, and omission from smaller hubs.
Additional checks cover every captive-nut position, omission of the centre nut,
and diagonal joining-screw clearance. Rendered sections check the material
between nut pockets and joining bores, and between mounting holes and recessed
joining heads, including the small hubs and the 6810 corner pockets.
Checks also cover the 608 seat and retaining lips, and both 6810 captive-nut
patterns, including the clear diagonal joining positions.
The full suite has 103 checks. `source_file/migration_validation.json` records
the exported meshes for all 36 variants in all three modes.

Mesh validation does not replace a physical bearing/shaft fit check.
