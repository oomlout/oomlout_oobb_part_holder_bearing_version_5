"""Blender worker for assembly.py: actual meshes, orthographic studio views."""
import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_catalogue import aim, material


def render(job):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 20
    scene.cycles.use_denoising = True
    prefs = bpy.context.preferences.addons['cycles'].preferences
    try:
        prefs.compute_device_type = 'OPTIX'
        prefs.get_devices()
        for device in prefs.devices:
            device.use = device.type == 'OPTIX'
        if any(d.use for d in prefs.devices):
            scene.cycles.device = 'GPU'
            scene.cycles.denoising_use_gpu = True
    except Exception:
        pass
    scene.render.resolution_x = scene.render.resolution_y = 850
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.film_transparent = True
    scene.view_settings.view_transform = 'AgX'
    scene.world = bpy.data.worlds.new('Studio')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs[0].default_value = (.8,.8,.8,1)
    scene.world.node_tree.nodes['Background'].inputs[1].default_value = .4
    materials = {}
    for role, colour in job['colours'].items():
        m = material(role, tuple(int(colour[i:i+2],16) for i in (1,3,5)))
        if role in ('bearing','nut','screw','insert'):
            m.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value = .65
        materials[role] = m
    objects = []
    for entry in job['objects']:
        bpy.ops.wm.stl_import(filepath=entry['source'])
        obj = bpy.context.object
        obj.scale = (.001,)*3
        obj.data.materials.append(materials[entry['role']])
        objects.append((obj, Vector(entry['explode'])*.001))
    data = bpy.data.cameras.new('Camera'); data.type = 'ORTHO'; data.clip_start = .0001
    camera = bpy.data.objects.new('Camera', data); scene.collection.objects.link(camera); scene.camera = camera
    lights = []
    for name, position, energy in [('Key',(-2,-3,5),22),('Fill',(3,-1,3),12),('Rim',(0,4,4),18)]:
        lamp = bpy.data.lights.new(name, 'AREA'); lamp.shape = 'DISK'
        obj = bpy.data.objects.new(name, lamp); scene.collection.objects.link(obj)
        lights.append((obj, Vector(position), energy))
    for view in ('assembled','exploded'):
        for obj, delta in objects:
            obj.location = delta if view == 'exploded' else (0,0,0)
        bpy.context.view_layer.update()
        bounds = [obj.matrix_world @ Vector(v) for obj,_ in objects for v in obj.bound_box]
        low = Vector([min(v[i] for v in bounds) for i in range(3)])
        high = Vector([max(v[i] for v in bounds) for i in range(3)])
        centre = (low+high)/2; span = max(high-low)
        for lamp, position, energy in lights:
            lamp.location = centre+position*span
            lamp.data.energy = energy*.07*(span/.1)**2
            lamp.data.size = span*3
            aim(lamp, centre)
        camera.location = centre+Vector((1.15,-1.6,1.2))*span
        aim(camera, centre)
        bpy.context.view_layer.update()
        projected = [camera.matrix_world.inverted() @ v for v in bounds]
        data.ortho_scale = max(max(v[i] for v in projected)-min(v[i] for v in projected) for i in (0,1))*1.15
        scene.render.filepath = str(Path(job['directory'])/(view+'.png'))
        bpy.ops.render.render(write_still=True)
    print('Assembly rendered: '+Path(job['directory']).name, flush=True)


if __name__ == '__main__':
    # Blender does not always put the script directory on sys.path.
    for job in json.loads(Path(sys.argv[sys.argv.index('--')+1]).read_text()):
        render(job)
