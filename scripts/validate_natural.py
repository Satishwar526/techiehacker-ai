from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json
root=Path(__file__).resolve().parents[1]; out=root/'dist'
class Check(HTMLParser):
 def __init__(self):super().__init__();self.urls=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  for k in ('href','src','action'):
   if d.get(k):self.urls.append(d[k])
errors=[];count=0;pages=[]
for p in out.rglob('index.html'):
 text=p.read_text();
 if 'natural/theme.css' not in text:continue
 pages.append(p); parser=Check();parser.feed(text)
 for u in parser.urls:
  v=urlsplit(u)
  if v.scheme or v.netloc or not v.path:continue
  target=(out/v.path.lstrip('/') if v.path.startswith('/') else p.parent/unquote(v.path)).resolve()
  if target.is_dir():target=target/'index.html'
  count+=1
  if not target.is_file():errors.append(str(p.relative_to(out))+': '+u)
for x in json.loads((out/'natural/tutorials.json').read_text()):
 if not (out/'tutorials'/x[0]/'index.html').exists():errors.append('Missing tutorial '+x[0])
h=(out/'index.html').read_text();assert h.count('src="natural/portrait.webp"')==1;assert 'Tomorrow’s' in h
print(f'{len(pages)} Natural Edition pages; {count} local references; {len(errors)} missing targets')
if errors:raise SystemExit('\n'.join(errors))
