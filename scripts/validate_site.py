"""Verify generated internal references using only Python standard library."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
ROOT=Path(__file__).resolve().parents[1]/'dist'
class Links(HTMLParser):
    def __init__(self):super().__init__();self.urls=[]
    def handle_starttag(self,tag,attrs):
        if tag in ('a','link','script','img'):
            d=dict(attrs);u=d.get('href') or d.get('src')
            if u:self.urls.append(u)
missing=[]; count=0; pages=list(ROOT.rglob('index.html'))
for p in pages:
    parser=Links();parser.feed(p.read_text())
    for u in parser.urls:
        parts=urlsplit(u)
        if parts.scheme or parts.netloc or not parts.path:continue
        target=(ROOT/parts.path.lstrip('/') if parts.path.startswith('/') else p.parent/unquote(parts.path)).resolve()
        if target.is_dir():target=target/'index.html'
        count+=1
        if not target.is_file() or not target.is_relative_to(ROOT.resolve()):missing.append(f'{p.relative_to(ROOT)}: {u}')
for path in ('news','academy','insights','library','lab','search','blogs','about'):
    assert (ROOT/path/'index.html').is_file(),path
idx=json.loads((ROOT/'search-index.json').read_text())
for record in idx:
    u=urlsplit(record['url'])
    if not u.scheme and not u.netloc:
        target=(ROOT/'search'/unquote(u.path)).resolve()
        if target.is_dir():target=target/'index.html'
        if not target.is_file():missing.append('search-index: '+record['url'])
print(f'{len(pages)} pages; {count} local references; {len(idx)} search records; {len(missing)} missing targets')
if missing:raise SystemExit('\n'.join(missing))

blogs=json.loads((ROOT.parent/"blogs.json").read_text())
assert len(blogs)>=200 and len({b["slug"] for b in blogs})==len(blogs)
for b in blogs:
    text=(ROOT/"blogs"/b["slug"]/"index.html").read_text()
    assert "Author: Satishwar Mallekedi" in text and "Where we need caution" in text,b["slug"]
print(f"{len(blogs)} authored blog pages verified")
