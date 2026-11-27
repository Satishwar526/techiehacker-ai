from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'dist'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.themed=False;self.added=[];self.stack=[];self.scope=0
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='body':self.themed=a.get('data-th-interior')=='1'
  # Check premium links through a separate parsed pass below; existing validator checks original homepage and author content.
  for k in ('href','src','action'):
   if a.get(k):self.added.append(a[k])
 def handle_startendtag(self,t,a):self.handle_starttag(t,a)
def parse(p):a=Page();a.feed(p.read_text(encoding='utf-8'));return a
home=OUT/'index.html';assert not parse(home).themed,'Homepage unexpectedly themed'
assert 'premium/interior.css' not in home.read_text(encoding='utf-8')
count=0;checked=0;missing=[]
for p in OUT.rglob('*.html'):
 if p==home:continue
 a=parse(p);assert a.themed,f'Unthemed internal page: {p.relative_to(OUT)}';count+=1
 for u in a.added:
  v=urlsplit(u)
  if v.scheme or v.netloc or not v.path:continue
  target=(OUT/unquote(v.path.lstrip('/'))) if v.path.startswith('/') else (p.parent/unquote(v.path))
  target=target.resolve();target=target/'index.html' if target.is_dir() else target;checked+=1
  if not target.is_file() or not target.is_relative_to(OUT.resolve()):missing.append((str(p.relative_to(OUT)),u))
assert count>0
print(f'{count} themed interior pages; {checked} local href/src/action references; {len(missing)} missing; homepage excluded.')
if missing:raise SystemExit('\n'.join(map(str,missing)))
