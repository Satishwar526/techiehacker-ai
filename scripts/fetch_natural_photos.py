"""Optional: download original, licensed photographs and cache resized copies with Pillow.
No API credentials; network access and Pillow required. Run from repository root.
"""
from pathlib import Path
import json,hashlib,urllib.parse,urllib.request,io
from PIL import Image,ImageOps
root=Path(__file__).resolve().parents[1]/'site/natural'
for p in json.loads((root/'photos.json').read_text()):
 f=p['file'].replace(' ','_'); h=hashlib.md5(f.encode()).hexdigest();u=f'https://upload.wikimedia.org/wikipedia/commons/{h[0]}/{h[:2]}/{urllib.parse.quote(f)}'
 try:
  req=urllib.request.Request(u,headers={'User-Agent':'TechieHackerPhotoCache/1.0 (www.techiehacker.com; editorial image cache)'})
  with urllib.request.urlopen(req,timeout=35) as r: data=r.read(30_000_001)
  if len(data)>30_000_000:raise ValueError('Image exceeds size limit')
  im=ImageOps.exif_transpose(Image.open(io.BytesIO(data))).convert('RGB');print(p['id'],im.size)
  for w in (640,1280,3840):
   thumb=im.copy();thumb.thumbnail((w,round(w*im.height/im.width)));thumb.save(root/f'{p["id"]}-{w}.webp',quality=86,method=5)
 except Exception as e:print('Remote image retained for',p['id'],str(e))
