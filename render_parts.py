"""Render project production mesh variants using the OOBB catalogue studio style."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import yaml

ROOT = Path(__file__).resolve().parent
WORKER = ROOT / "presentation/scripts/render_catalogue.py"
VARIANTS = (("3dpr", "Print-adjusted"), ("true", "Nominal"))
SHEET_VERSION = 1


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def dimensions(source):
    """Accept binary and ASCII STL without changing mesh geometry."""
    import trimesh
    mesh = trimesh.load_mesh(source, process=False)
    if len(mesh.vertices) == 0 or not np.isfinite(mesh.vertices).all():
        raise ValueError(f"Invalid or empty STL: {source}")
    return [round(float(v), 3) for v in mesh.extents]


def valid_png(path, size):
    try:
        with Image.open(path) as image:
            if image.size != size:
                return False
            image.verify()
        return True
    except (OSError, ValueError):
        return False


def font(size):
    for path in (Path("C:/Windows/Fonts/segoeui.ttf"), Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")):
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default(size=size)


def sheet(cache, destination, label, size):
    canvas = Image.new("RGB", (1600, 1000), "#f6f4ef")
    for i, view in enumerate(("angle", "top")):
        with Image.open(cache / (view + ".png")) as source:
            image = source.convert("RGBA").resize((720, 720), Image.Resampling.LANCZOS)
        canvas.paste(image, (40 + 800 * i, 105), image)
    draw = ImageDraw.Draw(canvas)
    import textwrap
    for i, line in enumerate(textwrap.wrap(label, width=95)):
        draw.text((48, 18 + 34*i), line, fill="#243a3b", font=font(28))
    draw.text((48, 850), "Angled view", fill="#3b4b4b", font=font(26))
    draw.text((848, 850), "Top view", fill="#3b4b4b", font=font(26))
    extent = " × ".join(f"{v:g}" for v in size)
    draw.text((48, 904), f"Mesh envelope  {extent} mm", fill="#243a3b", font=font(26))
    draw.text((48, 955), "AI-generated CAD illustration. Errors possible.", fill="#616966", font=font(21))
    temporary = destination.with_suffix(".tmp")
    canvas.save(temporary, format="PNG", optimize=True)
    os.replace(temporary, destination)


def find_blender(value=None):
    executable = value or os.environ.get("BLENDER_EXE") or shutil.which("blender")
    if executable:
        return executable
    candidates = sorted(Path("C:/Program Files/Blender Foundation").glob("Blender */blender.exe"), reverse=True)
    if candidates:
        return str(candidates[0])
    raise FileNotFoundError("Blender is required; set BLENDER_EXE or add Blender to PATH")


def reusable(record, previous, root):
    return (previous is not None and previous.get("key") == record["key"]
            and previous.get("sheet_version") == SHEET_VERSION
            and valid_png(root / record["image"], (1600, 1000))
            and previous.get("image_sha256") == sha(root / record["image"]))


def main(part_filter="", force=False, blender=None, root=ROOT, workers=2):
    root = Path(root).resolve()
    executable = find_blender(blender)
    version = subprocess.check_output([executable, "--version"], text=True).splitlines()[0]
    worker_hash = sha(WORKER)
    manifest_path = root / "presentation/catalogue.json"
    previous = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    old = {r["source"]: r for r in previous.get("renders", [])}
    cache = root / "build/presentation"
    cache.mkdir(parents=True, exist_ok=True)
    records, pending, jobs = [], [], {}
    sources = sorted((root / "parts").glob("*/working.yaml"))
    selected = [p for p in sources if part_filter in p.parent.name]
    if not selected:
        raise ValueError(f"No parts match {part_filter!r}")
    import catalogue
    for folder, part, mode, source in catalogue.sources(root, part_filter):
        source_hash = sha(source)
        variant = "Print layout" if mode == "3dpr" else "Nominal / assembly"
        label = part.get("name_proper", part["id"].replace("_", " ")) + " — " + variant
        label = label.removeprefix("Oobb Part ").removeprefix("Oobb Tool ")
        key = hashlib.sha256((source_hash + worker_hash + version + label + str(SHEET_VERSION) + sha(Path(__file__))).encode()).hexdigest()[:24]
        destination = folder / f"{mode}_presentation.png"
        record = dict(id=part["id"], variant=mode, source=source.relative_to(root).as_posix(),
                      source_sha256=source_hash, image=destination.relative_to(root).as_posix(),
                      dimensions_mm=dimensions(source), key=key, sheet_version=SHEET_VERSION,
                      renderer_sha256=worker_hash, blender=version, label=label)
        if not force and reusable(record, old.get(record["source"]), root):
            record["image_sha256"] = old[record["source"]]["image_sha256"]
        else:
            directory = cache / key
            directory.mkdir(exist_ok=True)
            if force or not all(valid_png(directory / f"{v}.png", (1000, 1000)) for v in ("angle", "top")):
                jobs[key] = dict(source=str(source), directory=str(directory), key=key)
            pending.append((record, directory, destination, label))
        records.append(record)
    print(f"Presentation: {len(selected)} parts, {len(records)} sheets, {len(jobs)} meshes need rendering", flush=True)
    if jobs:
        count = max(1, min(int(workers), 2, len(jobs)))
        def run_batch(index):
            jobs_path = cache / f"jobs-{index}.json"
            write_json(jobs_path, list(jobs.values())[index::count])
            log_path = cache / f"blender-{index}.log"
            with log_path.open("w", encoding="utf-8") as log:
                result = subprocess.run([executable, "--background", "--python-exit-code", "1",
                                         "--python", str(WORKER), "--", str(jobs_path)],
                                        stdout=log, stderr=subprocess.STDOUT)
            if result.returncode:
                raise RuntimeError(f"Blender failed ({result.returncode}); see {log_path}")
        with ThreadPoolExecutor(max_workers=count) as pool:
            list(pool.map(run_batch, range(count)))
    for index, (record, directory, destination, label) in enumerate(pending, 1):
        if not all(valid_png(directory / f"{v}.png", (1000, 1000)) for v in ("angle", "top")):
            raise ValueError(f"Incomplete rendered views: {directory}")
        sheet(directory, destination, label, record["dimensions_mm"])
        record["image_sha256"] = sha(destination)
        if index % 20 == 0:
            print(f"Published {index}/{len(pending)} sheets", flush=True)
    # Keep unrelated records during filtered builds; remove stale records on full builds.
    if part_filter:
        replaced = {r["source"] for r in records}
        records += [r for r in old.values() if r["source"] not in replaced]
    write_json(manifest_path, dict(schema=1, renders=sorted(records, key=lambda r: r["source"])))
    print(f"Presentation complete: {len(selected)} parts", flush=True)
    return records


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--filter", default="", help="Part ID substring; default all active parts")
    parser.add_argument("--force", action="store_true", help="Refresh even unchanged renders")
    parser.add_argument("--blender")
    parser.add_argument("--workers", type=int, choices=(1, 2), default=2)
    args = parser.parse_args()
    main(part_filter=args.filter, force=args.force, blender=args.blender, workers=args.workers)
    import catalogue
    if catalogue.config().get('assembly_pipeline'):
        import assembly
        assembly.build(args.filter)
    import working_navigation
    working_navigation.generate_navigation(ROOT / "parts")
