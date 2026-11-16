"""Check inventory exceptions and the inverse production-print transform."""
from collections import Counter
from pathlib import Path

import numpy as np
import pytest
import trimesh

import assembly
import catalogue


ROOT = Path(__file__).resolve().parents[1]
PARTS = {p['id']: (s, p) for s, p in catalogue.records(ROOT)}


def record(suffix):
    return PARTS['oobb_part_holder_'+suffix]


def inventory(suffix):
    folder, part = record(suffix)
    manifest, objects = assembly.inventory(part, folder)
    return {r['key']: r for r in manifest['bom']}, objects, manifest


def test_6810_main_example_has_six_recessed_12_mm_joins():
    rows, objects, data = inventory('bearing_6810_bearing_size_7_width_5_height_15_depth')
    assert rows['frame']['quantity'] == rows['hub']['quantity'] == 2
    assert rows['bearing']['quantity'] == 1
    assert rows['joining_12_False']['quantity'] == rows['joining_nuts']['quantity'] == 6
    screws = [o['mesh'] for o in objects if o['role'] == 'screw']
    assert len(screws) == 6
    for mesh in screws:
        np.testing.assert_allclose(mesh.bounds[:, 2], [-6, 6], atol=1e-7)
    assert catalogue.config()['example_id'] == data['id']


@pytest.mark.parametrize('suffix', [
    'bearing_6810_bearing_size_7_width_5_height_15_depth',
    'bearing_6704_bearing_size_8_width_3_height_9_depth_double',
    'bearing_6705_bearing_size_3_width_3_height_12_depth_motor_servo_standard_01_horn_adapter_screws',
    'bearing_6709_bearing_size_5_width_5_height_12_depth_motor_building_block_large_01',
])
def test_inverse_transform_recovers_every_printed_triangle(suffix):
    folder, part = record(suffix)
    detail = part['oobb_details']
    original = trimesh.load_mesh(folder/'3dpr.stl')
    restored = assembly.restore_print_mesh(folder/'3dpr.stl', detail)
    assert sum(len(m.faces) for m, _, _ in restored) == len(original.faces)
    assert sum(m.volume for m, _, _ in restored) == pytest.approx(original.volume, rel=1e-8)
    combined = trimesh.util.concatenate([m for m, _, _ in restored])
    np.testing.assert_allclose(combined.bounds[:, 2], [-detail['depth']/2, detail['depth']/2], atol=1e-5)
    if detail.get('split', True):
        split_z = detail.get('split_z', 0)
        lower = [m for m,_,shift in restored if shift[2] < 0]
        upper = [m for m,_,shift in restored if shift[2] > 0]
        assert max(m.bounds[1,2] for m in lower) == pytest.approx(split_z, abs=1e-5)
        assert min(m.bounds[0,2] for m in upper) == pytest.approx(split_z, abs=1e-5)


def test_double_holder_has_two_bearings_and_four_hub_pieces():
    rows, _, _ = inventory('bearing_6704_bearing_size_8_width_3_height_9_depth_double')
    assert rows['bearing']['quantity'] == 2
    assert rows['hub']['quantity'] == 4
    assert rows['frame']['quantity'] == 2
    assert rows['joining_nuts']['quantity'] == 8


def test_captive_counts_come_from_fitted_pockets_not_variant_name():
    rows, _, _ = inventory('bearing_6704_bearing_size_3_width_3_height_12_depth_inside_embedded_m3_nuts')
    assert 'embedded_m3' not in rows
    assert rows['joining_nuts']['quantity'] == 6
    assert rows['joining_10_True']['quantity'] == 2
    rows, _, _ = inventory('bearing_6810_bearing_size_7_width_5_height_12_depth_inside_embedded_m6_nuts')
    assert rows['embedded_m6']['quantity'] == 4
    assert rows['embedded_m3']['quantity'] == 2


def test_extension_and_coupler_have_additional_hardware():
    rows, _, _ = inventory('90_degree_bearing_606_bearing_size_3_width_3_height_12_depth_basic')
    assert rows['joining_nuts']['quantity'] == 4
    assert rows['extension_nuts']['quantity'] == 3
    rows, _, _ = inventory('bearing_6709_bearing_size_5_width_5_height_12_depth_inside_mechanical_coupler_flange_name_5_mm_bore')
    assert rows['coupler_nuts']['quantity'] == rows['coupler_screws']['quantity'] == 4


def test_unsplit_motor_adapter_has_one_hub_and_no_invented_frame_or_joins():
    rows, objects, _ = inventory('bearing_6704_bearing_size_3_width_3_height_12_depth_motor_building_block_large_01')
    assert rows['hub']['quantity'] == 1
    assert 'frame' not in rows and 'joining_nuts' not in rows
    assert Counter(o['role'] for o in objects) == {'hub': 1, 'bearing': 1}


@pytest.mark.parametrize('size,width,height,depth,teeth', [('6810',7,5,12,50), ('6704',5,3,9,30)])
def test_corners_use_two_bearings_six_holder_pieces_and_two_gears(size,width,height,depth,teeth):
    rows, objects, _ = inventory(f'90_degree_bearing_{size}_bearing_size_{width}_width_{height}_height_{depth}_depth_corner_bevel_{teeth}_teeth')
    assert rows['frame']['quantity'] == rows['bearing']['quantity'] == rows['gear']['quantity'] == 2
    assert rows['hub']['quantity'] == 4
    assert Counter(o['role'] for o in objects) == {'frame':2, 'hub':4, 'bearing':2, 'gear':2}


def test_every_holder_manifest_has_exact_identity_and_source_mesh():
    for folder, part in PARTS.values():
        data = __import__('json').loads((folder/'assembly.json').read_text())
        assert data['id'] == part['id']
        assert data['sources'][f"parts/{part['id']}/3dpr.stl"] == catalogue.sha(folder/'3dpr.stl')
        assert all(isinstance(row['quantity'], int) and row['quantity'] > 0 for row in data['bom'])
        readme = (folder/'README.md').read_text(encoding='utf-8')
        assert '(assembly.png)' in readme
        assert '| Part | Quantity | Type | Use |' in readme
    leaves = list((ROOT/'navigation_oobb').rglob('oomp_id.txt'))
    assert len(leaves) == len(PARTS)
    for leaf in leaves:
        readme = leaf.with_name('README.md').read_text(encoding='utf-8')
        assert '/assembly.png)' in readme
        assert '| Part | Quantity | Type | Use |' in readme
