"""Build per-holder assembly manifests, BOMs and CAD diagrams without editing CAD.

Production print meshes are put back into assembly coordinates using the exact
inverse of working_scad.prepare_bearing_holder_print. Corner meshes already have
their own documented assembly transforms. Blender only renders these meshes.
"""
import argparse
from collections import Counter
import csv
import hashlib
import json
import math
from pathlib import Path
import subprocess

import numpy as np
import trimesh

import catalogue
from render_parts import find_blender, font, sha, valid_png, write_json

ROOT = Path(__file__).resolve().parent
WORKER = ROOT / 'presentation/scripts/render_assembly.py'
COLOURS = {'frame': '#00b1b7', 'hub': '#121212', 'gear': '#121212',
           'bearing': '#a8b2bb', 'screw': '#8b969f', 'nut': '#8b969f', 'insert': '#bd944a'}


def transform(mesh, translation=(0, 0, 0), axis=None, angle=0):
    mesh = mesh.copy()
    if axis is not None:
        mesh.apply_transform(trimesh.transformations.rotation_matrix(angle, axis))
    mesh.apply_translation(translation)
    return mesh


def restore_print_mesh(source, detail):
    """Return actual connected pieces, their roles, and explosion vectors."""
    import oobb
    import working_scad as cad
    cad.define_bearing_dimensions(**dict(detail, mode='3dpr'))
    span = detail['width'] * oobb.gv('osp')
    if detail.get('body') == 'cylinder':
        span = 2 * oobb.gv('holder_bearing_adapter_radius', '3dpr')
    distance = span + detail.get('print_gap', 10)
    depth = detail['depth']
    gap = max(14, detail['width'] * 4)
    radius = oobb.gv(f"holder_bearing_{detail['bearing_size']}_relief_id", '3dpr')
    centers = cad.get_bearing_centers(**detail)
    pieces = []
    original = trimesh.load_mesh(source)
    for mesh in original.split(only_watertight=False):
        upper = detail.get('split', True) and mesh.bounds[0, 0] > span / 2
        mesh = transform(mesh, (-distance if upper else 0, 0, -depth / 2))
        if upper:
            mesh = transform(mesh, axis=(1, 0, 0), angle=math.pi)
        is_hub = any(np.max(np.linalg.norm(mesh.vertices[:, :2] - [x, y], axis=1)) < radius + .15
                     for x, y in centers)
        role = 'hub' if is_hub else 'frame'
        shift = gap if upper else -gap
        if not detail.get('split', True):
            shift = gap  # one-piece hub slides into the bearing from above
        pieces.append((mesh, role, [0, 0, shift]))
    if not np.isclose(sum(m.volume for m, _, _ in pieces), original.volume, rtol=1e-8):
        raise ValueError(f'Assembly transform changed volume: {source}')
    return pieces


def nominal_bearing(detail):
    import oobb
    size = detail['bearing_size']
    if 'bearing_inner_diameter' in detail:
        return [detail['bearing_inner_diameter'], detail['bearing_outer_diameter'], detail['bearing_depth']]
    return [2 * oobb.gv(f'bearing_{size}_id', 'true'),
            2 * oobb.gv(f'bearing_{size}_od', 'true'),
            7 if str(size) == '6810' else oobb.gv(f'bearing_{size}_depth', 'true')]


def ring(inner, outer, height, sections=64):
    return trimesh.creation.annulus(r_min=inner, r_max=outer, height=height, sections=sections)


def screw_mesh(length, socket=False):
    # Simplified unthreaded M3 outline, with the top face at z=0.
    head_depth = 3 if socket else 1.7
    shaft = transform(trimesh.creation.cylinder(radius=1.5, height=length-head_depth, sections=24),
                      (0, 0, -(length+head_depth)/2))
    if socket:
        head = transform(trimesh.creation.cylinder(radius=2.75, height=head_depth, sections=32), (0, 0, -head_depth/2))
    else:
        head = trimesh.creation.revolve([[0, -head_depth], [1.5, -head_depth], [2.85, 0], [0, 0]], sections=32)
    return trimesh.util.concatenate([shaft, head])


def inventory(part, folder, root=ROOT):
    """Single source for the diagram, parts table and machine-readable manifest."""
    import working_scad as cad
    d = dict(part['oobb_details'], mode='3dpr')
    rows, objects, notes, dependencies = [], [], [], [folder/'3dpr.stl', folder/'working.yaml',
        root/'assembly.py', root/'working_scad.py', root/'render_parts.py',
        root/'presentation/scripts/render_assembly.py', root/'presentation/scripts/render_catalogue.py']

    def row(key, name, qty, kind, purpose):
        if qty:
            rows.append(dict(key=key, part=name, quantity=qty, kind=kind, purpose=purpose))

    def obj(mesh, role, shift):
        objects.append(dict(mesh=mesh, role=role, explode=shift))

    def joins(items, depth, gap, prefix='joining'):
        counts = Counter()
        for j in items:
            socket = j.get('inner_joining', False) and d.get('inner_joining_head') == 'socket_cap'
            face = -1 if j.get('screw_face', 0) == 180 else 1
            length = 12 if depth == 15 else (10 if depth == 9 else depth)
            # Socket lengths exclude the head; the recess here occupies 3 mm.
            if socket:
                length = 10 if depth == 12 else length
            counts[(length, socket)] += 1
            top = 6 if depth == 15 else depth/2
            mesh = screw_mesh(length + (3 if socket else 0), socket)
            if face < 0:
                mesh = transform(mesh, axis=(0, 1, 0), angle=math.pi)
            obj(transform(mesh, (j['screw_x'], j['screw_y'], face*top)), 'screw', [0, 0, face*(gap+length+7)])
            nut = ring(1.5, 3.175, 2.4, 6)
            obj(transform(nut, (j['screw_x'], j['screw_y'], -face*(top-1.2))), 'nut', [0, 0, -face*(gap+10)])
        for (length, socket), count in counts.items():
            row(f'{prefix}_{length}_{socket}', f'M3 × {length:g} mm {"socket-cap" if socket else "countersunk"} screws', count, 'Hardware', 'Join printed halves; follow the alternating head/nut faces')
        row(prefix+'_nuts', 'M3 hex nuts', len(items), 'Hardware', 'Opposite-face joining pockets')
        if depth == 9 or any(socket for _, socket in counts):
            notes.append('Joining screw length is a nominal stock selection; check protrusion against the recessed head and nut stack before tightening.')

    size = str(d['bearing_size'])
    if 'corner' in d:
        example = root/'examples'/f'corner_{size}'
        c = json.loads((example/'layout.json').read_text())
        dependencies.append(example/'layout.json')
        component = example/'components'
        def load(name):
            path = component/(name+'.stl'); dependencies.append(path)
            return trimesh.load_mesh(path)
        for positive in (False, True):
            obj(load('frame_positive' if positive else 'frame_negative'), 'frame', [0, 24 if positive else -24, 0])
        for second in (False, True):
            # Match examples/corner_*/assembly.scad, including gear B phase.
            def place(mesh, shift):
                if second:
                    matrix = trimesh.transformations.rotation_matrix(math.pi/2, [0, 1, 0]) @ trimesh.transformations.rotation_matrix(math.pi/c['gear_teeth'], [0, 0, 1])
                    mesh = mesh.copy(); mesh.apply_transform(matrix)
                    shift = (matrix[:3, :3] @ shift).tolist()
                return transform(mesh, [-c['distance'], 0, 0] if second else [0, 0, -c['distance']]), shift
            entries = [
                (transform(load('hub_outer'), [0, 0, -c['depth']/2]), 'hub', [0, 0, -24]),
                (transform(load('hub_gear'), [0, 0, c['depth']/2], [1, 0, 0], math.pi), 'hub', [0, 0, 24]),
                (load('bearing'), 'bearing', [0, 0, 0]),
                (transform(load('gear'), [0, 0, c['distance']-c['apex']]), 'gear', [0, 0, 55]),
            ]
            for mesh, role, shift in entries:
                mesh, shift = place(mesh, shift); obj(mesh, role, shift)
        row('frame', 'Printed connected corner halves', 2, 'Print', 'One of each complementary half')
        row('hub', 'Printed hub discs', 4, 'Print', 'Two outer discs and two gear-facing discs; supplied hub files each contain two copies')
        row('gear', f"Matching {c['gear_teeth']}-tooth backed bevel gears", 2, 'Print', f"Use examples/corner_{size}/components/gear.stl; retained companion {c['gear_id']}")
        row('bearing', f'{size} bearing', 2, 'Hardware', 'One on each perpendicular axis')
        row('seam', 'M3 × 25 mm socket-cap screws', 3, 'Hardware', 'Connected corner seam')
        row('seam_nuts', 'M3 hex nuts', 3, 'Hardware', 'Seam pockets')
        row('hub_screws', f"M3 × {10 if size == '6704' else 12} mm countersunk screws", 4, 'Hardware', 'Two joins per bearing hub')
        row('hub_nuts', 'M3 hex nuts' + (' — 2.4 mm thick' if size == '6704' else ''), 4, 'Hardware', 'Hub joins')
        thread, length = ('M3', 30) if size == '6704' else ('M6', 45)
        row('gear_screws', f'{thread} × {length} mm screws', 8, 'Hardware', 'Four per gear; suggested stack from the existing corner guide')
        row('gear_nuts', f'{thread} hex nuts', 8, 'Hardware', 'Gear connections')
        row('gear_washers', f'{thread} washers', 16, 'Hardware', 'One under each gear screw head and nut; check final protrusion')
        notes.append('Corner diagram shows printed parts and bearings. Seam, hub and gear fasteners are listed in the table; see the linked corner guide for their insertion paths and suggested lengths.')
        steps = ['Join each bearing between an outer hub disc and a gear-facing hub disc, with the stand-offs facing the gear.',
                 'Capture both bearing/hub units between the connected corner halves; fit the three seam screws and nuts.',
                 'Bolt on the matching gears, rotate the second hub and gear together to mesh, and check free movement.']
        guide = f'examples/corner_{size}/README.md'
    else:
        cad.define_bearing_dimensions(**d)
        layout = cad.get_mounting_layout(**d)
        pieces = restore_print_mesh(folder/'3dpr.stl', d)
        counts = Counter(role for _, role, _ in pieces)
        for mesh, role, shift in pieces:
            obj(mesh, role, shift)
        row('frame', 'Printed frame halves', counts['frame'], 'Print', 'Print all frame pieces in 3dpr.stl once')
        row('hub', 'Printed hub pieces', counts['hub'], 'Print', 'Print all hub pieces in 3dpr.stl once; preserve complementary faces')
        dims = nominal_bearing(d)
        centers = cad.get_bearing_centers(**d)
        for x, y in centers:
            obj(transform(ring(dims[0]/2, dims[1]/2, dims[2]), (x, y, 0)), 'bearing', [0, 0, 0])
        row('bearing', f"{size} bearing — {' × '.join(f'{v:g}' for v in dims)} mm", len(centers), 'Hardware', 'Bore × outside diameter × width')
        joining = list(layout['joining'])
        if d.get('holder_type') == 'holder_90_degree':
            for i in range(d['width']-1):
                joining.append(dict(screw_x=-(d['width']-2)*7.5+i*15, screw_y=-15, screw_face=(i%2)*180))
            row('extension_nuts', 'M6 hex nuts', d['width'], 'Hardware', 'Load extension pockets/slots before closing; mating bolts depend on the mounted part')
            notes.append('The extension M6 nuts and mating installation bolts are not shown in the diagram.')
        gap = max(14, d['width']*4)
        joins(joining, d['depth'], gap)
        for thread, count in Counter(n['radius_name'] for n in layout['nuts']).items():
            row('embedded_'+thread, thread.upper()+' hex nuts', count, 'Hardware', 'Captive mounting pockets at the split; additional to joining nuts')
        for n in layout['nuts']:
            dia = int(n['radius_name'][1:]); h = 2.4 if dia == 3 else 5
            obj(transform(ring(dia/2, 3.175 if dia == 3 else 5.774, h, 6), (n['x'], n['y'], d.get('split_z', 0))), 'nut', [0, 0, 0])
        if d.get('inside') == 'flange_coupler':
            row('coupler', '5 mm bore metal flange coupler', 1, 'Interface', '22 mm flange, four M3 holes on a 16 mm bolt circle; fits outside the hub')
            row('coupler_nuts', 'M3 hex nuts', d['coupler_mount_count'], 'Hardware', 'Load the four split-face coupler pockets before closing')
            row('coupler_screws', 'M3 coupler mounting screws', d['coupler_mount_count'], 'Interface', 'Select length for the actual flange, half-hub and captive nut stack')
            notes.append('The coupler and its four mounting screws/nuts are listed separately and are not shown in the diagram.')
        shaft = d.get('shaft', '')
        if shaft.startswith('motor_'):
            row('motor', shaft.removeprefix('motor_').replace('_', ' ')+' motor / mating shaft', 1, 'Interface', 'Use the specified shaft interface; motor and mounting hardware are not shown')
            row('inserts', 'M3 threaded inserts', 2*len(centers), 'Interface', 'CAD insert pockets: 4 mm diameter; choose compatible insert depth and fit')
            row('insert_screws', 'M3 insert mounting screws', 2*len(centers), 'Interface', 'Length depends on the mating component and selected insert; do not bottom out')
            if 'servo' in shaft:
                row('servo_center', ('M2' if 'micro' in shaft else 'M2.5')+' servo retaining screw', 1, 'Interface', 'Match the servo thread and required engagement; length is servo-specific')
            if shaft == 'motor_servo_standard_01':
                row('horn_screws', 'M2 self-tapping horn screws', 2, 'Interface', 'At y = ±7.375 mm; choose length for the actual horn and hub')
        if d.get('body') == 'cylinder':
            notes.append('This variant supplies the rotating adapter only. Provide a compatible stationary outer bearing support in the surrounding assembly.')
        if counts['hub'] and not any(j.get('inner_joining') for j in joining):
            notes.append('No separate hub joining screws are modelled. Retain the hub with the mating shaft/interface hardware.')
            if not shaft.startswith('motor_'):
                row('shaft_retention', 'M6 shaft / axle with hub retainers', len(centers), 'Interface', 'Required to retain the unjoined hub pieces; select length and retainers for the application')
        if d['depth'] == 15:
            notes.append('M3 × 12 mm countersunk joins sit 1.5 mm below each outside face of the 15 mm holder.')
        notes.append('Bearing rings and fasteners are simplified nominal illustrations; threads, drive sockets, inserts and motor/interface hardware are omitted. Installation bolts depend on the surrounding assembly.')
        if d.get('split', True):
            steps = ['Print one complete 3dpr.stl layout. Keep the complementary frame and hub pieces in their matching orientation.',
                     'Load any captive nuts, coupler nuts or inserts while their pockets are accessible. Seat each bearing between its matching hub and frame pieces.',
                     'Close the complementary pieces and fit the listed joining screws and nuts, following the alternating head and nut recesses.',
                     'Fit the specified shaft or motor interface. Check free rotation before fastening the holder to the surrounding structure.']
        else:
            steps = ['Print the single adapter and clear its shaft and insert openings.',
                     'Slide the adapter into the bearing from the open end. Fit the matching motor shaft and interface hardware.',
                     'Retain the outer bearing in a separate support and check that the adapter rotates freely.']
        guide = 'PROJECT_GUIDE.md'
    manifest = dict(schema=1, id=part['id'], title=f"{size} bearing holder · {d['width']} × {d['height']} · {d['depth']} mm",
                    variant=(d.get('extra') or 'standard M6 centre').replace('_', ' '),
                    roles=sorted({o['role'] for o in objects}),
                    scope='Quantities for one complete printed holder/adapter, plus its listed interface. Installation fasteners are application-specific.',
                    bom=rows, notes=notes, steps=steps, guide=guide,
                    sources={p.relative_to(root).as_posix(): sha(p) for p in dict.fromkeys(dependencies)})
    return manifest, objects


def markdown(manifest, folder, destination):
    rel = catalogue.relative
    parts = [manifest['scope'], '', '| Part | Quantity | Type | Use |', '| --- | ---: | --- | --- |']
    for r in manifest['bom']:
        parts.append('| '+' | '.join(catalogue.safe_text(r[k]) for k in ('part','quantity','kind','purpose'))+' |')
    parts += ['', f'[Machine-readable parts list]({rel(folder/"assembly.json", destination)}) · [CSV parts list]({rel(folder/"assembly_parts.csv", destination)})']
    assembly = [f'![AI-generated assembled and exploded CAD diagram]({rel(folder/"assembly.png", destination)})', '',
                *[f'{i}. {step}' for i, step in enumerate(manifest['steps'], 1)], '', *manifest['notes'], '',
                f'[Variant assembly notes]({rel(folder.parent.parent/manifest["guide"], destination)})']
    return '\n'.join(parts), '\n\n'.join(assembly)


def publish_sheet(manifest, directory, target):
    from PIL import Image, ImageDraw
    canvas = Image.new('RGB', (1800, 1200), '#f6f4ef')
    draw = ImageDraw.Draw(canvas)
    draw.text((44, 24), manifest['title'], font=font(36), fill='#243a3b')
    draw.text((45, 68), manifest['variant'].capitalize(), font=font(22), fill='#616966')
    for i, view in enumerate(('assembled','exploded')):
        with Image.open(directory/(view+'.png')) as raw:
            raw = raw.convert('RGBA')
            canvas.paste(raw, (25+900*i, 100), raw)
        draw.text((45+900*i, 92), 'Assembled' if i == 0 else 'Exploded along assembly axes', font=font(27), fill='#243a3b')
    # The key uses the same functional colours in both views.
    keys = [('frame','Printed frame'), ('hub','Rotating hub'), ('bearing','Bearing'), ('screw','Screws / nuts')]
    if any(r['key']=='gear' for r in manifest['bom']):
        keys.append(('gear','Companion gears'))
    keys = [(role, label) for role, label in keys if role in manifest['roles'] or (role == 'screw' and 'nut' in manifest['roles'])]
    for i, (role, label) in enumerate(keys):
        x = 45+i*345
        draw.rectangle((x, 985, x+24, 1009), fill=COLOURS[role])
        draw.text((x+34, 978), label, font=font(24), fill='#243a3b')
    hardware = [r for r in manifest['bom'] if r['kind'] == 'Hardware']
    import textwrap
    summary = ' · '.join(f"{r['quantity']} × {r['part']}" for r in hardware)
    for i, line in enumerate(textwrap.wrap(summary, width=132)[:3]):
        draw.text((45, 1030+i*29), line, font=font(23), fill='#3b4b4b')
    detail = 'Corner fasteners are listed, not shown.' if 'gear' in manifest['roles'] else 'Simplified hardware; see the parts table for interface and installation items.'
    draw.text((45, 1160), 'AI-generated CAD illustration. Errors possible. '+detail, font=font(21), fill='#616966')
    canvas.save(target, optimize=True)


def build(part_filter='', force=False, root=ROOT):
    root = Path(root).resolve()
    selected = [(s,p) for s,p in catalogue.records(root) if part_filter in p['id'] and p.get('oobb_details')]
    if not selected:
        raise ValueError(f'No holders match {part_filter!r}')
    executable = find_blender()
    version = subprocess.check_output([executable, '--version'], text=True).splitlines()[0]
    pending = []
    for folder, part in selected:
        manifest, objects = inventory(part, folder, root)
        key_data = dict(manifest=manifest, pipeline=sha(Path(__file__)), worker=sha(WORKER),
                        cad=sha(root/'working_scad.py'), blender=version)
        key = hashlib.sha256(json.dumps(key_data, sort_keys=True).encode()).hexdigest()
        manifest['build_key'] = key
        target = folder/'assembly.png'
        old = json.loads((folder/'assembly.json').read_text()) if (folder/'assembly.json').exists() else {}
        if not force and old.get('build_key') == key and valid_png(target, (1800,1200)) and old.get('image_sha256') == sha(target):
            continue
        directory = root/'build/assembly'/part['id']; directory.mkdir(parents=True, exist_ok=True)
        scene_objects = []
        for i, obj in enumerate(objects):
            path = directory/f'{i}.stl'; obj['mesh'].export(path)
            scene_objects.append(dict(source=str(path), role=obj['role'], explode=obj['explode']))
        job = dict(directory=str(directory), objects=scene_objects, colours=COLOURS)
        pending.append((folder, manifest, job))
    if pending:
        jobs = root/'build/assembly/jobs.json'
        write_json(jobs, [j for _,_,j in pending])
        log = jobs.with_suffix('.log')
        print(f'Rendering {len(pending)} assembly diagrams; log: {log}', flush=True)
        with log.open('w', encoding='utf-8') as stream:
            result = subprocess.run([executable, '--background', '--python-exit-code', '1', '--python', str(WORKER), '--', str(jobs)], stdout=stream, stderr=subprocess.STDOUT)
        if result.returncode:
            raise RuntimeError(f'Assembly renderer failed; see {log}')
    for folder, manifest, job in pending:
        directory = Path(job['directory'])
        for view in ('assembled','exploded'):
            if not valid_png(directory/(view+'.png'), (850,850)):
                raise ValueError(f'Missing assembly view: {directory}/{view}')
        publish_sheet(manifest, directory, folder/'assembly.png')
        manifest['image_sha256'] = sha(folder/'assembly.png')
        write_json(folder/'assembly.json', manifest)
        with (folder/'assembly_parts.csv').open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=['key','part','quantity','kind','purpose'])
            writer.writeheader(); writer.writerows(manifest['bom'])
    print(f'Assembly diagrams ready: {len(selected)} holders ({len(pending)} refreshed)', flush=True)


def verify(root=ROOT):
    count = 0
    for folder, part in catalogue.records(root):
        if not part.get('oobb_details'):
            continue
        path = folder/'assembly.json'
        data = json.loads(path.read_text())
        if data['id'] != part['id'] or not data['bom']:
            raise ValueError(f'Invalid assembly manifest: {path}')
        for source, digest in data['sources'].items():
            if sha(root/source) != digest:
                raise ValueError(f'Stale assembly source: {source}')
        if not valid_png(folder/'assembly.png', (1800,1200)) or sha(folder/'assembly.png') != data['image_sha256']:
            raise ValueError(f'Stale assembly image: {path}')
        with (folder/'assembly_parts.csv').open(encoding='utf-8', newline='') as stream:
            rows = list(csv.DictReader(stream))
        if rows != [{k:str(v) for k,v in r.items()} for r in data['bom']]:
            raise ValueError(f'BOM CSV mismatch: {path}')
        count += 1
    return count


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--filter', default='')
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()
    build(args.filter, args.force)
    catalogue.navigation()
