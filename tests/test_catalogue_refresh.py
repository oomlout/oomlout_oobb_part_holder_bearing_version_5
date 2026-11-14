"""Regression checks for catalogue safety, filtering and presentation contracts."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import yaml
import catalogue

class CatalogueTests(unittest.TestCase):
    def setUp(self):
        self.temporary=tempfile.TemporaryDirectory()
        self.root=Path(self.temporary.name)
        self.cfg=dict(title='Test catalogue',summary='Summary',parts='Parts',assembly='Assembly')
        (self.root/'catalogue.json').write_text(json.dumps(self.cfg))
        (self.root/'CATALOGUE_BUILD.md').write_text('Build guide')
        for name,width in [('sample_2',2),('sample_10',10)]:
            part=self.root/'parts'/name;part.mkdir(parents=True)
            (part/'working.yaml').write_text(yaml.safe_dump(dict(id=name,taxonomy_1='oobb',taxonomy_2='part',taxonomy_3=f'{width}_width',oobb_details=dict(width=width))))
    def tearDown(self):self.temporary.cleanup()
    def test_navigation_is_text_and_links_to_folders(self):
        catalogue.navigation(self.root)
        nav=self.root/'navigation_oobb'
        self.assertEqual(len(list(nav.rglob('oomp_id.txt'))),2)
        self.assertEqual({p.name for p in nav.rglob('*') if p.is_file()},{'README.md','oomp_id.txt'})
        discovery=(nav/'oobb/part/README.md').read_text()
        self.assertLess(discovery.index('2_width'),discovery.index('10_width'))
        self.assertIn('parts/sample_2/',discovery)
        self.assertNotIn('sample_2/README.md',discovery)
        self.assertIn('navigation_oobb/oobb/part/',(self.root/'README.md').read_text())
        for p in nav.rglob('oomp_id.txt'):
            self.assertIn(p.read_text().strip(),p.with_name('README.md').read_text())
    def test_manual_notes_survive_repeated_generation(self):
        path=self.root/'parts/sample_2/README.md';path.write_text('Manual fit note\n')
        catalogue.navigation(self.root);first=path.read_text();catalogue.navigation(self.root)
        self.assertEqual(first,path.read_text());self.assertIn('Manual fit note',first)
    def test_default_part_can_share_a_taxonomy_prefix_with_angle_variants(self):
        path=self.root/'parts/sample_10/working.yaml'
        part=yaml.safe_load(path.read_text());part.update(taxonomy_3='2_width',taxonomy_4='45_angle')
        path.write_text(yaml.safe_dump(part))
        catalogue.navigation(self.root)
        self.assertTrue((self.root/'navigation_oobb/oobb/part/2_width/_part/oomp_id.txt').exists())
        self.assertEqual(len(list((self.root/'navigation_oobb').rglob('oomp_id.txt'))),2)
    def test_legacy_assets_are_not_silently_deleted(self):
        nav=self.root/'navigation_oobb';nav.mkdir();asset=nav/'unique.stl';asset.write_bytes(b'keep')
        with self.assertRaises(ValueError):catalogue.navigation(self.root)
        self.assertEqual(asset.read_bytes(),b'keep')
    def test_invalid_markers_do_not_overwrite_manual_content(self):
        path=self.root/'parts/sample_2/README.md';original=catalogue.START+'\nunfinished';path.write_text(original)
        with self.assertRaises(ValueError):catalogue.navigation(self.root)
        self.assertEqual(path.read_text(),original)
    def test_filtered_metadata_merge_keeps_other_parts(self):
        for name in ('sample_2','sample_10'):
            p=self.root/'parts_source'/name;p.mkdir(parents=True)
            (p/'working.yaml').write_text(yaml.safe_dump(dict(id=name,oobb_details=dict(width=99))))
        catalogue.sync_sources(self.root,'sample_2')
        rows={p['id']:p for _,p in catalogue.records(self.root)}
        self.assertEqual(rows['sample_2']['oobb_details']['width'],99)
        self.assertEqual(rows['sample_10']['oobb_details']['width'],10)
    def test_missing_printable_geometry_is_an_error(self):
        with self.assertRaisesRegex(ValueError,'Missing production mesh'):catalogue.sources(self.root)
    def test_purchased_hardware_needs_no_invented_mesh(self):
        for source,part in catalogue.records(self.root):
            part.pop('oobb_details');(source/'working.yaml').write_text(yaml.safe_dump(part))
        self.assertEqual(catalogue.sources(self.root),[])
        catalogue.navigation(self.root)
        self.assertIn('Purchased hardware',(self.root/'parts/sample_2/README.md').read_text())
    def test_ascii_and_binary_mesh_measurements_match(self):
        import trimesh
        from render_parts import dimensions
        mesh=trimesh.creation.box(extents=[3,5,7])
        a=self.root/'ascii.stl';b=self.root/'binary.stl'
        a.write_text(trimesh.exchange.stl.export_stl_ascii(mesh));b.write_bytes(trimesh.exchange.stl.export_stl(mesh))
        self.assertEqual(dimensions(a),[3,5,7]);self.assertEqual(dimensions(a),dimensions(b))

if __name__=='__main__':unittest.main()
