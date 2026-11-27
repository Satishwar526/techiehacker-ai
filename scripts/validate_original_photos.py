from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'dist'
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set();self.hotspots=0;self.photos=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs);self.hotspots+=int(tag=='a' and d.get('class')=='hotspot');self.links.extend(d[k] for k in ('href','src','action') if d.get(k));self.ids.add(d.get('id',''))
  if tag=='img' and 'original-author/' in d.get('src',''):self.photos.append(d['src'])
def parse(p):
 a=Parser();a.feed(p.read_text(encoding='utf-8'));return a
hashes=json.loads((ROOT/'site/original-author/originals.json').read_text())
for f,h in hashes.items():
 for folder in ('site','dist'):assert hashlib.sha256((ROOT/folder/'original-author'/f).read_bytes()).hexdigest()==h,(folder,f)
assert hashlib.sha256((OUT/'reference/homepage.png').read_bytes()).hexdigest()==json.loads((ROOT/'site/reference/reference.json').read_text())['asset_sha256']
blogs=json.loads((ROOT/'blogs.json').read_text());assert len(blogs)>=200
home=parse(OUT/'index.html');assert home.hotspots>=79 and home.photos==["original-author/IMG_6204.jpg"]
about=parse(OUT/'about/index.html');assert len(about.photos)>=6
paths=[OUT/'index.html',OUT/'about/index.html',OUT/'reference-resources/index.html']+[OUT/'blogs'/b['slug']/'index.html' for b in blogs]
missing=[];count=0;used=set()
for p in paths:
 a=parse(p)
 if p.parent.parent==OUT/'blogs':
  assert a.photos and 'Author: Satishwar Mallekedi' in p.read_text(),p
  used.update(Path(x).name for x in a.photos)
 for u in a.links:
  v=urlsplit(u)
  if v.scheme or v.netloc:continue
  q=(p.parent/unquote(v.path)).resolve() if v.path else p
  if q.is_dir():q=q/'index.html'
  count+=1
  if not q.is_file() or not q.is_relative_to(OUT.resolve()):missing.append((p.relative_to(OUT),u));continue
  if v.fragment and q.suffix=='.html' and unquote(v.fragment) not in parse(q).ids:missing.append((p.relative_to(OUT),u+' (anchor missing)'))
assert used==set(hashes),used
print(f'{home.hotspots} homepage hotspots; {count} local link/asset/anchor checks; {len(missing)} missing; {len(blogs)} authored blogs; {len(hashes)} byte-identical JPEGs; original reference checksum passed.')
if missing:raise SystemExit('\n'.join(map(str,missing)))
