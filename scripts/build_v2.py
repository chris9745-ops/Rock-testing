"""Build the v2 shared view (site/v2/) from the v2 tracker.

usage: python3 scripts/build_v2.py <export_dir>

<export_dir> holds one folder per tracker collection (meta, areas, cases, testdata,
results, defects, activity), each with one <doc_id>.json per document, as saved by an
export of the tracker's shared store. The page itself comes from v2/tracker.html, the
same file the Claude artifact is published from; on Netlify it has no live store, so it
reads data.json and renders read-only.
"""
import json, glob, os, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHELL = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
         '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
         '<style>:root{box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
         'body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style></head><body>\n%s\n</body></html>\n')


def load(exp, col):
    out = []
    for f in sorted(glob.glob(os.path.join(exp, col, '*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        if set(d) <= {'id', 'data', 'version', 'updatedAt'} and isinstance(d.get('data'), dict):
            d = d['data']  # an export wrapped as {id, data, version}
        d['_id'] = os.path.basename(f)[:-5]
        out.append(d)
    return out


def main(exp):
    meta = {d['_id']: d for d in load(exp, 'meta')}.get('tracker', {})
    meta.pop('_id', None)
    results = {}
    for r in load(exp, 'results'):
        results[r.pop('_id')] = r
    data = {
        'generated': int(time.time() * 1000),
        'meta': meta,
        'areas': load(exp, 'areas'),
        'cases': load(exp, 'cases'),
        'testdata': load(exp, 'testdata'),
        'results': results,
        'defects': load(exp, 'defects'),
        'activity': sorted(load(exp, 'activity'), key=lambda a: -(a.get('at') or 0))[:500],
    }
    os.makedirs(os.path.join(ROOT, 'site', 'v2'), exist_ok=True)
    json.dump(data, open(os.path.join(ROOT, 'site', 'v2', 'data.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    page = open(os.path.join(ROOT, 'v2', 'tracker.html'), encoding='utf-8').read()
    open(os.path.join(ROOT, 'site', 'v2', 'index.html'), 'w', encoding='utf-8').write(SHELL.replace("%s", page.strip()))
    print(len(data['cases']), 'cases', len(results), 'results', len(data['defects']), 'defects', len(data['activity']), 'activity')


if __name__ == '__main__':
    main(sys.argv[1])
