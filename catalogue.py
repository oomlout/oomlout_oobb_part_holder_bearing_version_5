"""Deterministic catalogue build, Markdown navigation and validation.

Project geometry remains in working_scad.py. Current parts_source records are the
authoritative catalogue; archives and legacy desktop automation are never scanned.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
from urllib.parse import quote, unquote

import yaml

ROOT = Path(__file__).resolve().parent
START = '<!-- oobb-presentation:start -->'
END = '<!-- oobb-presentation:end -->'
NOTICE = 'AI-generated images and instructions. Errors possible.'
ORIGIN = ('This is an entirely AI-generated coding project. The generated outputs are included and usually work, '
          'but the main purpose of publishing it is to give others a starting point for modifying the project with their own AI tools.')

def config(root=ROOT):
    return json.loads((root / 'catalogue.json').read_text(encoding='utf-8'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def records(root=ROOT):
    result = []
    for path in sorted((root / 'parts').glob('*/working.yaml')):
        if path.is_symlink() or path.parent.is_symlink():
            raise ValueError(f'Linked part is not supported: {path}')
        data = yaml.safe_load(path.read_text(encoding='utf-8'))
        if not isinstance(data, dict) or data.get('id', path.parent.name) != path.parent.name:
            raise ValueError(f'Invalid canonical part metadata: {path}')
        data['id'] = path.parent.name
        result.append((path.parent, data))
    if not result:
        raise ValueError('No active part metadata')
    return result

def relative(target, page):
    return quote(os.path.relpath(target, page.parent).replace('\\', '/'), safe='/.-_')

def safe_text(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')

def segment(value):
    value = str(value).replace('.', 'd')
    if value in ('', '.', '..') or re.search(r'[<>:"/\\|?*\x00-\x1f]', value) or value.endswith(' '):
        raise ValueError(f'Unsafe taxonomy: {value!r}')
    return value

def natural(path):
    return [int(x) if x.isdigit() else x for x in re.split(r'(\d+)', path.name)]

def generated(path, body):
    block = START + '\n' + body.rstrip() + '\n' + END + '\n'
    old = path.read_text(encoding='utf-8') if path.exists() else ''
    if START in old or END in old:
        if old.count(START) != 1 or old.count(END) != 1 or old.index(START) > old.index(END):
            raise ValueError(f'Malformed generation markers: {path}')
        return old[:old.index(START)] + block.rstrip('\n') + old[old.index(END)+len(END):]
    return block + ('\n' + old if old else '')

def page(part, source, destination, cfg):
    root = source.parent.parent
    detail = part.get('oobb_details') or {}
    purchased = not detail
    title = part.get('name_proper') or part['id'].replace('_', ' ').title()
    lines = [f'# {safe_text(title)}', '', NOTICE, '', '## Summary', '',
             ('Purchased hardware referenced by this project.' if purchased else cfg['summary']), '', ORIGIN, '']
    preview = source / '3dpr_presentation.png'
    if preview.exists():
        lines += [f'![CAD preview]({relative(preview, destination)})', '']
    lines += ['## Details', '', f"**Full OOMP ID:** `{part['id']}`", '',
              f'[Part folder]({relative(source, destination)}/) · [OOBB navigation]({relative(root / "navigation_oobb", destination)}/)', '',
              '| Field | Value |', '| --- | --- |']
    for key, value in detail.items():
        if not isinstance(value, (dict, list)) and key not in ('run_scad', 'run_solidcraft'):
            lines.append(f'| {safe_text(key.replace("_", " ").title())} | {safe_text(value)} |')
    taxonomy = [part.get(f'taxonomy_{i}') for i in range(1, 16) if part.get(f'taxonomy_{i}')]
    lines.append('| Taxonomy | ' + safe_text(' / '.join(map(str, taxonomy))) + ' |')
    metadata = yaml.safe_dump(part, sort_keys=False, allow_unicode=True).rstrip()
    fence = '`' * max(3, max((len(m[0])+1 for m in re.finditer(r'`+', metadata)), default=3))
    parts_text = 'Purchased hardware; no printable mesh is generated for this record.' if purchased else cfg['parts']
    assembly_text = 'Use the hardware specification above when sourcing this item.' if purchased else cfg['assembly']
    if cfg.get('assembly_pipeline') and not purchased:
        from assembly import markdown
        manifest = json.loads((source/'assembly.json').read_text(encoding='utf-8'))
        parts_text, assembly_text = markdown(manifest, source, destination)
    lines += ['', '<details>', '<summary>Full part details: all working.yaml fields</summary>', '', fence+'yaml', metadata, fence, '', '</details>', '',
              '## Parts', '', parts_text, '', '## Assembly', '', assembly_text, '']
    if (root/'PROJECT_GUIDE.md').exists() and not (cfg.get('assembly_pipeline') and not purchased):
        lines += [f'[Project guide and existing assembly notes]({relative(root / "PROJECT_GUIDE.md", destination)})', '']
    return '\n'.join(lines)

def navigation(root=ROOT):
    root = Path(root).resolve(); cfg = config(root); nav = root/'navigation_oobb'
    if nav.is_symlink() or (hasattr(nav,'is_junction') and nav.is_junction()):
        raise ValueError('Navigation must be an ordinary directory')
    if nav.exists():
        for p in nav.rglob('*'):
            if p.is_symlink() or (hasattr(p,'is_junction') and p.is_junction()):raise ValueError(f'Linked navigation: {p}')
            if p.is_file() and p.name not in ('README.md','oomp_id.txt'):
                raise ValueError('Archive legacy navigation before adopting the text-only generator: '+str(p))
    leaves={}; dirs={Path('.')}; pages={}
    active=records(root)
    taxonomy_paths={part['id']:Path(*[segment(part[f'taxonomy_{i}']) for i in range(1,16) if part.get(f'taxonomy_{i}') not in (None,'','default')]) for _,part in active}
    prefix_ids={identity for identity,path in taxonomy_paths.items() if any(path != other and path in other.parents for other in taxonomy_paths.values())}
    for source, part in active:
        pieces = [segment(part[f'taxonomy_{i}']) for i in range(1,16) if part.get(f'taxonomy_{i}') not in (None,'','default')]
        # Full IDs live in the two leaf files; repeating them in deep directory
        # names exceeded Windows path limits in bearing/electronics catalogues.
        leaf=Path(*pieces) if pieces else Path(part['id'])
        if part['id'] in prefix_ids:leaf=leaf/'_part'
        if leaf in leaves:raise ValueError('Duplicate navigation identity')
        leaves[leaf]=(source,part); dirs.add(leaf); dirs.update(leaf.parents)
        target=nav/leaf/'README.md'
        pages[target]=generated(target,page(part,source,target,cfg))
        pages[nav/leaf/'oomp_id.txt']=part['id']+'\n'
        canonical=source/'README.md';pages[canonical]=generated(canonical,page(part,source,canonical,cfg))
    if any(a != b and a in b.parents for a in leaves for b in leaves):
        raise ValueError('A part taxonomy cannot also be a category')
    def collapse(child):
        while child not in leaves:
            children=[p for p in dirs if p!=Path('.') and p.parent==child]
            if len(children)!=1:break
            child=children[0]
        return leaves[child][0] if child in leaves else nav/child
    for d in sorted(dirs,key=str):
        if d in leaves:continue
        dest=nav/d/'README.md'
        lines=['# '+('OOBB navigation' if d==Path('.') else d.name.replace('_',' ')), '',f'[Canonical parts]({relative(root/"parts",dest)}/)', '']
        if d!=Path('.'):lines+=['[Parent category](../)', '']
        for child in sorted((p for p in dirs if p!=Path('.') and p.parent==d),key=natural):
            lines.append(f'- [{safe_text(child.name)}]({relative(collapse(child),dest)}/)')
        pages[dest]=generated(dest,'\n'.join(lines))
    dest=root/'README.md';discovery=collapse(Path('.'))
    hero=[]
    for source, part in sorted(leaves.values(),key=lambda item:item[1]['id'] != cfg.get('example_id')):
        image = source/cfg.get('example_image', '3dpr_presentation.png')
        if image.exists():
            label = '7 × 5 6810 holder — 15 mm depth' if part['id'] == cfg.get('example_id') else 'Example part'
            hero=[f'![AI-generated example CAD diagram]({relative(image,dest)})', '',f'[{label}]({relative(source,dest)}/)', ''];break
    lines=['# '+cfg['title'],'',NOTICE,'','## Summary','',cfg['summary'],'',ORIGIN,'',*hero,'## Details','',
           f'This catalogue contains **{len(leaves)} records**. [Browse OOBB navigation]({relative(discovery,dest)}/).','',
           'Each part has one canonical folder, its full OOMP ID and complete metadata. Navigation links open folders; use GitHub’s file pane to browse the available files.','',
           '[Build and maintenance guide](CATALOGUE_BUILD.md)','',
           '## Parts','',cfg['parts'],'','## Assembly','',cfg['assembly'],'']
    if (root/'PROJECT_GUIDE.md').exists():lines+=['[Project guide and existing assembly notes](PROJECT_GUIDE.md)','']
    pages[dest]=generated(dest,'\n'.join(lines))
    # Compute and validate every page before replacing anything.
    for p,content in pages.items():
        p.parent.mkdir(parents=True,exist_ok=True)
        tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(content,encoding='utf-8')
        for attempt in range(20):
            try:
                os.replace(tmp,p)
                break
            except PermissionError:
                if attempt==19:raise
                time.sleep(0.1)
    if nav.exists():
        for p in nav.rglob('*'):
            if p.is_file() and p not in pages:
                old=p.read_text(encoding='utf-8')
                if p.name=='README.md' and (START not in old or old.split(START)[0].strip() or old.split(END)[-1].strip()):
                    raise ValueError(f'Preserve manual notes before retiring navigation: {p}')
                p.unlink()
        for p in sorted((x for x in nav.rglob('*') if x.is_dir()),key=lambda x:len(x.parts),reverse=True):
            if not any(p.iterdir()):p.rmdir()
    return {'records':len(leaves),'navigation_files':sum(p.is_file() for p in nav.rglob('*'))}

def sources(root=ROOT, part_filter=''):
    result=[]
    for source,part in records(root):
        if part_filter not in part['id'] or not part.get('oobb_details'):continue
        preferred=config(root).get('native_primary',False)
        main=source/('3dpr_solidcraft.stl' if preferred else '3dpr.stl')
        if not main.exists():raise ValueError(f'Missing production mesh: {main}')
        result.append((source,part,'3dpr',main))
        nominal=source/('true_solidcraft.stl' if preferred else 'true.stl')
        if nominal.exists():result.append((source,part,'true',nominal))
    return result

def sync_sources(root=ROOT, part_filter=''):
    # Merge deterministic metadata directly, without launching queued GUI jobs.
    paths=sorted((root/'parts_source').glob('*/working.yaml'))
    if not paths:raise ValueError('Missing parts_source catalogue')
    for p in paths:
        if part_filter not in p.parent.name:continue
        data=yaml.safe_load(p.read_text(encoding='utf-8'))
        if not isinstance(data,dict):raise ValueError(f'Invalid source: {p}')
        if data.get('id',p.parent.name)!=p.parent.name:raise ValueError(f'Source ID mismatch: {p}')
        target=root/'parts'/p.parent.name/'working.yaml';target.parent.mkdir(parents=True,exist_ok=True)
        existing=yaml.safe_load(target.read_text(encoding='utf-8')) if target.exists() else {}
        existing.update(data);existing['id']=p.parent.name
        existing.setdefault('name_proper',p.parent.name.replace('_',' ').title())
        target.write_text(yaml.safe_dump(existing,sort_keys=False,allow_unicode=True),encoding='utf-8')

def openscad():
    exe=os.environ.get('OPENSCAD_EXE') or shutil.which('openscad.com') or shutil.which('openscad')
    if not exe:raise FileNotFoundError('Set OPENSCAD_EXE or add OpenSCAD to PATH')
    return exe

def build(part_filter='', workers=2, native=False, legacy_actions=False, populate=False):
    root=ROOT
    os.chdir(root)
    if populate:
        import working_oomp_populate
        working_oomp_populate.main(filter=part_filter)
    sync_sources(root,part_filter)
    import working_scad
    modes=config(root).get('modes',['3dpr'])
    working_scad.main(filter=part_filter,typ='fast',save_type='none',navigation=False,overwrite=True,modes=modes,oomp_run=False,generate_stl=False)
    if native or config(root).get('native_primary'):
        import working_solidcraft
        context={'part_filter':part_filter,'modes':['3dpr','true'],'export_stl':True,'export_extras':True,'verify_solidcraft':False}
        if config(root).get('native_recipe'):context['recipe_source']=config(root)['native_recipe']
        working_solidcraft.main(solidcraft_context=context)
    exe=openscad();jobs=[]
    for source,part in records(root):
        if part_filter not in part['id'] or not part.get('oobb_details'):continue
        if config(root).get('native_primary'):continue
        for mode in modes:
            scad=source/(mode+'.scad')
            if not scad.exists():raise ValueError(f'CAD generation failed to produce {scad}')
            jobs.append(scad)
    logs=root/'build/catalogue';logs.mkdir(parents=True,exist_ok=True)
    def export(scad):
        output=scad.with_suffix('.stl');temporary=scad.with_name(scad.stem+'.building.stl')
        log=logs/(scad.parent.name+'_'+scad.stem+'.log')
        with log.open('w',encoding='utf-8') as stream:
            result=subprocess.run([exe,'--hardwarnings','--export-format','binstl','-o',str(temporary),str(scad)],stdout=stream,stderr=subprocess.STDOUT)
        diagnostics=log.read_text(encoding='utf-8',errors='replace')
        if result.returncode or 'ERROR:' in diagnostics or 'WARNING:' in diagnostics or not temporary.exists() or temporary.stat().st_size<84:
            raise RuntimeError(f'OpenSCAD export failed: {scad}; see {log}')
        from render_parts import dimensions
        dimensions(temporary)
        os.replace(temporary,output)
        print('Exported '+str(output.relative_to(root)),flush=True)
    with ThreadPoolExecutor(max_workers=max(1,min(workers,4))) as pool:list(pool.map(export,jobs))
    if legacy_actions:
        import working_action
        working_action.main(filter=part_filter)
    import render_parts
    render_parts.main(part_filter=part_filter,workers=min(workers,2))
    if config(root).get('assembly_pipeline'):
        import assembly
        assembly.build(part_filter, root=root)
    navigation(root)
    return verify(root)

def verify(root=ROOT):
    root=Path(root).resolve();parts=records(root);expected={p['id'] for _,p in parts}
    txt=list((root/'navigation_oobb').rglob('oomp_id.txt'))
    if len(txt)!=len(expected) or {p.read_text().strip() for p in txt}!=expected:raise ValueError('Navigation coverage mismatch')
    for p in (root/'navigation_oobb').rglob('*'):
        if p.is_file() and p.name not in ('README.md','oomp_id.txt'):raise ValueError('Navigation contains assets')
    manifest=json.loads((root/'presentation/catalogue.json').read_text())
    rendered={r['id'] for r in manifest['renders'] if r['variant']=='3dpr'}
    printable={p['id'] for _,p in parts if p.get('oobb_details')}
    if rendered!=printable:raise ValueError(f'Render coverage mismatch: {printable-rendered}, {rendered-printable}')
    from render_parts import valid_png
    for r in manifest['renders']:
        for pathkey,hashkey in [('source','source_sha256'),('image','image_sha256')]:
            if sha(root/r[pathkey])!=r[hashkey]:raise ValueError('Stale artifact: '+r[pathkey])
        if not valid_png(root/r['image'],(1600,1000)):raise ValueError('Invalid PNG')
    pages=[root/'README.md',*(s/'README.md' for s,_ in parts),*(root/'navigation_oobb').rglob('README.md')]
    links=0
    for p in pages:
        content=p.read_text(encoding='utf-8')
        block=content.split(START,1)[-1].split(END,1)[0]
        # YAML metadata can contain arbitrary Markdown-like strings; it is not navigation.
        block=re.sub(r'<details>.*?</details>','',block,flags=re.S)
        for match in re.finditer(r'!?\[[^\]]*\]\(([^)]+)\)',block):
            url=unquote(match[1]).split('#',1)[0]
            if not url or '://' in url:continue
            target=(p.parent/url).resolve()
            if not target.is_relative_to(root) or not target.exists():raise ValueError(f'Broken link: {p}: {url}')
            links+=1
    result={'records':len(parts),'printable_parts':len(printable),'render_sheets':len(manifest['renders']),'navigation_files':sum(p.is_file() for p in (root/'navigation_oobb').rglob('*')),'checked_links':links}
    if config(root).get('assembly_pipeline'):
        import assembly
        result['assembly_diagrams'] = assembly.verify(root)
    (root/'presentation/validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)
    return result

def cli():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['build','docs','render','assembly','verify'],nargs='?',default='build')
    parser.add_argument('--filter',default='')
    parser.add_argument('--workers',type=int,default=2,choices=[1,2,3,4])
    parser.add_argument('--native',action='store_true')
    parser.add_argument('--legacy-actions',action='store_true')
    parser.add_argument('--populate',action='store_true',help='Explicitly rerun the catalogue definition before building')
    a=parser.parse_args()
    if a.command=='build':build(a.filter,a.workers,a.native,a.legacy_actions,a.populate)
    elif a.command=='docs':navigation()
    elif a.command=='verify':verify()
    elif a.command=='assembly':
        import assembly
        assembly.build(a.filter);navigation();verify()
    else:
        import render_parts
        render_parts.main(part_filter=a.filter,workers=min(a.workers,2))
        if config().get('assembly_pipeline'):
            import assembly
            assembly.build(a.filter)
        navigation();verify()

if __name__=='__main__':cli()
