"""Build just the corner catalogue entry and its reproducible assembly examples."""

import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess

import oobb
from oomp_populate_helper import write_extras
import yaml

import scad_help
import working_corner as corner
import working_populate
import working_scad


ROOT = Path(__file__).resolve().parent
EXAMPLES = ROOT / "examples" / "corner_6810"
OPENSCAD = shutil.which("openscad.com") or shutil.which("openscad")


def render(path, output=None, extra=()):
    output = output or path.with_suffix(".stl")
    result = subprocess.run([OPENSCAD, "--backend=Manifold", "-o", str(output),
                             *extra, str(path)], capture_output=True, text=True, timeout=180)
    log = result.stdout + result.stderr
    if result.returncode or "ERROR:" in log or "WARNING:" in log:
        raise RuntimeError(log)
    return output


def save_component(name, thing, examples=EXAMPLES):
    path = examples / "components" / f"{name}.scad"
    path.parent.mkdir(parents=True, exist_ok=True)
    oobb.opsc_make_object(str(path), thing["components"], mode="3dpr", save_type="none")
    scad_help.cleanup_raw_scad_artifacts(str(path.parent))
    render(path)


def main(bearing_size="6810"):
    examples = ROOT / "examples" / f"corner_{bearing_size}"
    option = next(o for o in working_populate.get_options() if "corner" in o and o["bearing_size"] == str(bearing_size))
    write_extras([option])
    folder = ROOT / "parts" / option["id"]
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "working.yaml").write_text(yaml.safe_dump(option), encoding="utf-8")
    # Exercise the normal working_oomp -> parts -> working_scad dispatch route.
    part = next(p for p in working_scad.get_parts(
        {"modes": ["3dpr"], "save_type": "none", "overwrite": True}, "project")
                if p["id"] == option["id"])
    scad_help.make_scad_generic(part)
    render(folder / "3dpr.scad")
    kwargs = copy.deepcopy(option["oobb_details"])
    c = corner.layout(**kwargs)
    for name in ("frame_negative", "frame_positive", "hub_outer", "hub_gear"):
        t = corner.new_thing()
        working_scad.get_bearing_holder_corner(t, **dict(kwargs, corner_part=name))
        path = folder / f"print_{name}.scad"
        oobb.opsc_make_object(str(path), t["components"], mode="3dpr", save_type="none")
        render(path)
    for name, thing in [
        ("frame_negative", corner.corner_half(c)),
        ("frame_positive", corner.corner_half(c, True)),
        ("hub_outer", corner.hub_half(c)),
        ("hub_gear", corner.hub_half(c, True)),
        ("bearing", corner.bearing(c)),
    ]:
        save_component(name, thing, examples)
    gear_repo = (ROOT / c["gear_repo"]).resolve()
    matches = []
    for candidate in (gear_repo / "parts").glob("*bevel*/working.yaml"):
        metadata = yaml.safe_load(candidate.read_text(encoding="utf-8"))
        details = metadata.get("oobb_details", {})
        if (details.get("teeth"), details.get("module"), details.get("depth")) == (
                c["gear_teeth"], c["gear_module"], c["gear_depth"]):
            matches.append((candidate, metadata))
    if len(matches) > 1:
        raise ValueError("More than one companion bevel gear matches the corner")
    if not matches:
        # The current gear catalogue retired its 12 mm backed-tooth family.
        # Keep the reviewed local companion; never substitute a new profile.
        import hashlib
        previous = json.loads((examples / "layout.json").read_text())
        for key in ("gear_teeth", "gear_module", "gear_depth", "gear_face_width", "gear_backlash"):
            if previous[key] != c[key]:
                raise ValueError("Retained companion does not match " + key)
        mesh = examples / "components/gear.stl"
        report = json.loads((examples / "validation.json").read_text())
        expected = report["sha256"][mesh.relative_to(ROOT).as_posix()]
        if hashlib.sha256(mesh.read_bytes()).hexdigest() != expected:
            raise ValueError("Retained companion gear changed; review and validate it first")
        gear_id = previous["gear_id"]
        metadata_path = mesh.relative_to(ROOT).as_posix()
        c["gear_reference_retained"] = True
    else:
        metadata_path, gear_metadata = matches[0]
        gear_id = gear_metadata["id"]
        gear_kwargs = gear_metadata["oobb_details"]
        for name, expected in [("module", c["gear_module"]), ("teeth", c["gear_teeth"]),
                               ("depth", c["gear_depth"]), ("face_width", c["gear_face_width"]),
                               ("backlash", c["gear_backlash"])]:
            if gear_kwargs[name] != expected:
                raise ValueError(f"Companion gear {name} differs from the corner configuration")
        spec = importlib.util.spec_from_file_location("corner_companion_gears", gear_repo / "working_scad.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        t = corner.new_thing()
        module.get_gear_bevel_style(t, **gear_kwargs)
        save_component("gear", t, examples)
    (examples / "layout.json").write_text(json.dumps(dict(c, gear_id=gear_id,
        gear_source=str(metadata_path)), indent=2) + "\n", encoding="utf-8")
    write_examples(c, examples)
    for name in ("print_layout", "assembly", "exploded", "bevel_mesh"):
        path = examples / f"{name}.scad"
        if name == "print_layout":
            path.write_text(f'import("../../parts/{option["id"]}/3dpr.stl");\n', encoding="utf-8")
        render(path, path.with_suffix(".png"), ["--imgsize=1200,1000", "--viewall", "--autocenter",
                                               "--projection=o", "--render=true"])
    print(f"Corner parts: {folder}")
    print(f"Assembly examples: {examples}")


def write_examples(c, examples=EXAMPLES):
    common = f'''// Generated by action_make_corner.py. Dimensions and source: layout.json.
D={c["distance"]}; depth={c["depth"]}; apex={c["apex"]}; teeth={c["gear_teeth"]};
angle=360*$t;
explode=0;
show_frame=true;
show_gears=true;
show_bearings=true;
show_hubs=true;
check=0; // 1 gear/gear; 2 frame/rotors; 3 bearing/printed; 4 frame/frame; 5 rotor/rotor.
module frame_half(positive=false) {{
    translate([0,positive ? explode : -explode,0])
        if(positive) import("components/frame_positive.stl");
        else import("components/frame_negative.stl");
}}
module frame() {{ frame_half(); frame_half(true); }}
module bearing() {{ import("components/bearing.stl"); }}
module hub() {{
    translate([0,0,-depth/2-explode]) import("components/hub_outer.stl");
    translate([0,0,depth/2+explode]) rotate([180,0,0]) import("components/hub_gear.stl");
}}
module rotor(a=0, gear_only=false, gear_color="Goldenrod", explode_side=1) {{
    rotate([0,0,a]) {{
        if(show_hubs && !gear_only) color("DarkOrange") hub();
        if(show_gears) color(gear_color) translate([0,explode_side*3*explode,D-apex+2*explode])
            import("components/gear.stl");
    }}
}}
module first(a=angle, gear_only=false) {{ translate([0,0,-D]) rotor(a,gear_only); }}
// With the second axis on X, the contact generator is on the first gear's -X.
// Even tooth counts require the same half-tooth phase as the companion demo.
module second(a=angle, gear_only=false) {{
    translate([-D,0,0]) rotate([0,90,0]) rotor(-a+180/teeth,gear_only,"MediumSeaGreen",-1);
}}
module bearings() {{
    // Keep the tessellated nominal inner surface aligned with its fitted hub.
    // Real bearing inner races turn with the hub; the outer seats remain fixed.
    translate([0,0,-D]) rotate([0,0,angle]) bearing();
    translate([-D,0,0]) rotate([0,90,0]) rotate([0,0,-angle+180/teeth]) bearing();
}}
if(check==1) intersection() {{ first(gear_only=true); second(gear_only=true); }}
else if(check==2) intersection() {{ frame(); union() {{ first(); second(); }} }}
else if(check==3) intersection() {{ bearings(); union() {{ frame(); first(); second(); }} }}
else if(check==4) intersection() {{ frame_half(); frame_half(true); }}
else if(check==5) intersection() {{ first(); second(); }}
else {{
    if(show_frame) color("LightSlateGray") frame_half();
    if(show_frame) color("Silver") frame_half(true);
    if(show_bearings) color("SteelBlue") bearings();
    first(); second();
}}
'''
    (examples / "assembly.scad").write_text(common, encoding="utf-8")
    (examples / "exploded.scad").write_text(common.replace("explode=0;", "explode=18;"), encoding="utf-8")
    (examples / "bevel_mesh.scad").write_text(common.replace("show_frame=true;", "show_frame=false;")
        .replace("show_bearings=true;", "show_bearings=false;")
        .replace("show_hubs=true;", "show_hubs=false;"), encoding="utf-8")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bearing", choices=["6810", "6704", "all"], default="6810")
    args = parser.parse_args()
    for bearing_size in (["6810", "6704"] if args.bearing == "all" else [args.bearing]):
        main(bearing_size)
