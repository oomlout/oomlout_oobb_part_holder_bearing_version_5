"""Optional animated preview of the actual generated bevel STL pair."""

from pathlib import Path
import subprocess
import tempfile

from PIL import Image

from action_make_corner import ROOT, OPENSCAD


def main(bearing_size="6810"):
    examples = ROOT / "examples" / f"corner_{bearing_size}"
    with tempfile.TemporaryDirectory(prefix="oobb_corner_frames_") as folder:
        temp = Path(folder)
        result = subprocess.run([OPENSCAD, "--backend=Manifold", "-o", str(temp / "frame.png"),
            "--animate=24", "--imgsize=720,600", "--viewall", "--autocenter",
            "--projection=o", "--render=true", str(examples / "bevel_mesh.scad")],
            capture_output=True, text=True, timeout=180)
        log = result.stdout + result.stderr
        if result.returncode or "WARNING:" in log or "ERROR:" in log:
            raise RuntimeError(log)
        paths = sorted(temp.glob("frame*.png"))
        if len(paths) != 24:
            raise RuntimeError(f"Expected 24 frames; got {len(paths)}")
        frames = [Image.open(p).convert("RGB") for p in paths]
        target = examples / "bevel_motion.gif"
        frames[0].save(target, save_all=True, append_images=frames[1:], duration=100, loop=0)
        print(target)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bearing", choices=["6810", "6704"], default="6810")
    main(parser.parse_args().bearing)
