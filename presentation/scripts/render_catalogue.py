"""Blender worker: render unchanged STL geometry in millimetres, two views per mesh."""
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


def linear(v):
    return v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4


def material(name, colour, roughness=.4):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    shader = m.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = (*[linear(v / 255) for v in colour], 1)
    shader.inputs['Roughness'].default_value = roughness
    return m


def aim(obj, point):
    obj.rotation_euler = (Vector(point) - obj.location).to_track_quat('-Z', 'Y').to_euler()


def render(job):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 24
    scene.cycles.use_denoising = True
    prefs = bpy.context.preferences.addons['cycles'].preferences
    try:
        prefs.compute_device_type = 'OPTIX'
        prefs.get_devices()
        for d in prefs.devices:
            d.use = d.type == 'OPTIX'
        if any(d.use for d in prefs.devices):
            scene.cycles.device = 'GPU'
            # Keep the same studio style; denoise on the GPU during large batches.
            scene.cycles.denoising_use_gpu = True
    except Exception:
        pass
    scene.render.resolution_x = 1000
    scene.render.resolution_y = 1000
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.film_transparent = True
    scene.view_settings.view_transform = 'AgX'
    scene.world = bpy.data.worlds.new('Studio')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs[0].default_value = (.8, .8, .8, 1)
    scene.world.node_tree.nodes['Background'].inputs[1].default_value = .35
    bpy.ops.wm.stl_import(filepath=job['source'])
    part = bpy.context.object
    # STL is in millimetres. Preserve geometry; translate to the floor and centre.
    part.scale = (.001,) * 3
    bpy.context.view_layer.update()
    corners = [part.matrix_world @ Vector(v) for v in part.bound_box]
    lo = Vector([min(v[i] for v in corners) for i in range(3)])
    hi = Vector([max(v[i] for v in corners) for i in range(3)])
    part.location -= Vector(((lo.x + hi.x) / 2, (lo.y + hi.y) / 2, lo.z))
    size = hi - lo
    part.data.materials.append(material('Satin teal PLA', (0, 177, 183)))
    # No remeshing, bevel modifier or smoothing of real holes and sharp edges.
    # An open background keeps through-holes legible; floor shadows can resemble hardware.
    span = max(size)
    for name, pos, energy, radius in [
        ('Key', (-2, -3, 5), 22, 4), ('Fill', (3, -1, 3), 12, 3),
        ('Rim', (0, 4, 4), 18, 3),
    ]:
        data = bpy.data.lights.new(name, 'AREA')
        data.energy = energy * .07 * (span / .1) ** 2
        data.shape = 'DISK'
        data.size = span * radius
        light = bpy.data.objects.new(name, data)
        scene.collection.objects.link(light)
        light.location = Vector(pos) * span
        aim(light, (0, 0, 0))
    data = bpy.data.cameras.new('Camera')
    data.type = 'ORTHO'
    cam = bpy.data.objects.new('Camera', data)
    scene.collection.objects.link(cam)
    scene.camera = cam
    for view, pos in [('angle', (1.15, -1.45, 1.65)), ('top', (0, 0, 3))]:
        cam.location = Vector(pos) * span
        aim(cam, (0, 0, size.z / 2))
        bpy.context.view_layer.update()
        bounds = [cam.matrix_world.inverted() @ (part.matrix_world @ Vector(v)) for v in part.bound_box]
        extent = max(max(v[i] for v in bounds) - min(v[i] for v in bounds) for i in (0, 1))
        data.ortho_scale = extent * 1.23
        data.clip_start = .0001
        scene.render.filepath = str(Path(job['directory']) / (view + '.png'))
        bpy.ops.render.render(write_still=True)
    print('OOBB rendered ' + job['key'], flush=True)


if __name__ == '__main__':
    jobs = json.loads(Path(sys.argv[sys.argv.index('--') + 1]).read_text())
    for job in jobs:
        render(job)
