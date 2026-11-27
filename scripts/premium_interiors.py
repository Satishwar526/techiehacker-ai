"""Style generated interior pages only; preserve homepage, archives and original assets."""
from pathlib import Path
import html, re, json, hashlib, urllib.parse
E=lambda s:html.escape(str(s),quote=True)
NAV=[('Home',''),('AI News','news'),('Trending','trending'),('AI Academy','academy'),('Tools','tools'),('Research','research'),('Developer Hub','developers'),('Blogs','blogs'),('Tutorials','tutorials'),('Courses','courses'),('Prompt Library','prompts'),('Media','media')]
EXTRA=[('Methodologies','methodologies'),('Interactive Labs','experience'),('Resource Library','library'),('Technical Insights','insights'),('Learning Resources','learn'),('Meet the Founder','about')]
LABEL={p:n for n,p in NAV+EXTRA}
LABEL.update({'discover':'Search','search':'Search','reference-resources':'Learning resources','photo-credits':'Photography credits','lab':'AI Lab'})
DESC={'news':'Source-linked reporting and analysis • explore the stories shaping AI.','blogs':'Technical perspectives • practical experiments • balanced insights.','tutorials':'Learn by doing • practical exercises • official documentation.','courses':'Structured learning paths • build skills at your own pace.','academy':'Your learning journey • from fundamentals to applied AI.','media':'Original publisher films • technology demonstrations • ambient listening.','experience':'Hands-on AI concepts • experiment safely in your browser.','research':'Explore the evidence, papers and ideas behind AI.','tools':'Explore AI tools and find the right resource for your workflow.','about':'The voice behind TechieHacker • curiosity, learning and practical technology.'}
def category(text):
 t=text.lower()
 for key,terms in [('health',('medical','health','biotech','medicine','drug','protein')),('robotics',('robot','manufactur','autonomous')),('earth',('earth','space','climate','satellite','astronom','agricultur')),('servers',('gpu','cloud','hardware','server','infrastructure','deploy','model serving')),('studio',('video','media','creativ','image generat','film','podcast'))]:
  if any(x in t for x in terms):return key
 return 'developer'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def render(root,out):
 root,out=Path(root),Path(out); home=out/'index.html'; before=digest(home)
 def exists(p):return (out/p/'index.html').is_file()
 nav=[(n,p) for n,p in NAV if exists(p)]; extra=[(n,p) for n,p in EXTRA if exists(p)]
 search='discover' if exists('discover') else 'search' if exists('search') else None
 manifest=json.loads((out/'natural/photos.json').read_text())
 def photo(p,rel):
  f=p['file'].replace(' ','_'); h=hashlib.md5(f.encode()).hexdigest(); q=urllib.parse.quote(f)
  original=f'https://upload.wikimedia.org/wikipedia/commons/{h[0]}/{h[:2]}/{q}'
  thumb=f'https://upload.wikimedia.org/wikipedia/commons/thumb/{h[0]}/{h[:2]}/{q}/960px-{q}'
  local=next((out/'natural'/f'{p["id"]}-{w}.webp' for w in (1280,640,3840) if (out/'natural'/f'{p["id"]}-{w}.webp').is_file()),None)
  return {'src':rel+str(local.relative_to(out)) if local else thumb,'fallback':original if not local else '', 'alt':p['alt'],'credit':p['credit'],'license':p['license'],'source':'https://commons.wikimedia.org/wiki/File:'+q}
 def href(p,rel):return rel+(p+'/' if p else '')
 def links(items,rel,active=''):return ''.join(f'<a href="{E(href(p,rel))}"'+(' aria-current="page"' if p==active else '')+f'>{E(n)}</a>' for n,p in items)
 count=0; details=0
 for path in sorted(out.rglob('*.html')):
  if path==home:continue
  s=path.read_text(encoding='utf-8'); assert 'data-th-interior="1"' not in s, f'Already themed: {path}'
  if not re.search(r'<body\b',s,re.I) or not re.search(r'</head\s*>',s,re.I):continue
  route=path.parent.relative_to(out).parts; group=route[0] if route else ''; rel='../'*len(route) or './'; detail=len(route)>1 and group in ('blogs','news','tutorials','courses','methodologies','prompts','experience'); titlematch=re.search(r'<title[^>]*>(.*?)</title>',s,re.I|re.S)
  title=html.unescape(re.sub('<[^>]+>','',titlematch.group(1))).split(' | TechieHacker')[0] if titlematch else LABEL.get(group,group.title())
  label=LABEL.get(group,group.replace('-',' ').title() or 'Explore')
  selected=category(group+' '+title); photo_map={p['id']:photo(p,rel) for p in manifest}; img=photo_map.get(selected,photo_map.get('developer'))
  # Body class is additive, preserve all original attributes and script selectors.
  def body(m):
   tag=m.group(0)
   if re.search(r'\bclass\s*=\s*["\']',tag,re.I):tag=re.sub(r'(\bclass\s*=\s*)(["\'])(.*?)\2',lambda x:x[1]+x[2]+x[3]+' th-interior'+x[2],tag,count=1,flags=re.I)
   else:tag=tag[:-1]+' class="th-interior">'
   return tag[:-1]+' data-th-interior="1" data-th-detail="'+('1' if detail else '0')+'">'
  s=re.sub(r'<body\b[^>]*>',body,s,count=1,flags=re.I)
  # Keep legacy controls and navigation available and original JS IDs intact.
  old=re.search(r'<header\b[^>]*>.*?</header\s*>',s,re.I|re.S)
  if old:s=s[:old.start()]+'<details class="th-legacy-controls"><summary>Original page controls</summary>'+old.group(0)+'</details>'+s[old.end():]
  form=f'<form class="th-search" action="{E(href(search,rel))}" method="get"><input type="search" name="q" aria-label="Search TechieHacker" placeholder="Search AI resources"><button type="submit">Search</button></form>' if search else ''
  mast=f'''<div class="th-mast"><div class="th-navrow"><a class="th-brand" href="{rel}"><b>TH</b><span>TECHIE<span>HACKER</span></span></a><nav class="th-desktop" aria-label="Primary navigation">{links(nav,rel,group)}</nav><details class="th-mobile"><summary>Explore menu</summary><nav aria-label="Mobile navigation">{links(nav+extra,rel,group)}</nav></details></div><div class="th-subrow"><nav aria-label="Learning destinations">{links(extra,rel,group)}</nav>{form}</div></div>'''
  crumb=f'<a href="{rel}">Home</a><span aria-hidden="true">/</span><a href="{E(href(group,rel))}">{E(label)}</a>' if group and exists(group) else f'<a href="{rel}">Home</a>'
  if detail:crumb+='<span aria-hidden="true">/</span><span aria-current="page">'+E(title)+'</span>'
  pic=''
  if img and group not in ('about','photo-credits'):
   pic=f'<figure class="th-banner-photo"><img src="{E(img["src"])}" data-th-fallback="{E(img["fallback"])}" alt="{E(img["alt"])}" decoding="async"><figcaption><a href="{E(img["source"])}">File photo · {E(img["credit"])} · {E(img["license"])}</a></figcaption></figure>'
  intro=f'<div class="th-intro"><div class="th-crumb" aria-label="Breadcrumb">{crumb}</div><div class="th-banner"><div><div class="th-kicker">TECHIEHACKER / {E(label.upper())}</div><strong>{E(label)}<span>.</span></strong><p>{E(DESC.get(group,"Explore. Learn. Build. Practical resources for the AI community."))}</p></div>{pic}</div><div class="th-actions"><button type="button" data-th-save aria-pressed="false">☆ Save page</button><button type="button" data-th-focus aria-pressed="false">Focus mode</button><button type="button" data-th-share>Copy page link</button><details class="th-reading-menu"><summary>Reading list</summary><div class="th-reading-pop"><div class="th-kicker">YOUR SAVED PAGES</div><p>Saved in this browser only.</p><div data-th-saved></div></div></details><span data-th-message role="status"></span></div></div>'
  rail=f'<aside class="th-rail" aria-label="Page tools"><div class="th-sidebox" data-th-toc hidden><div class="th-kicker">ON THIS PAGE</div><nav aria-label="Article sections"></nav></div><div class="th-sidebox"><div class="th-kicker">CONTINUE EXPLORING</div><nav aria-label="Recommended destinations">{links([(n,p) for n,p in extra+nav if p and p!=group][:8],rel)}</nav></div><div class="th-sidebox"><div class="th-kicker">YOUR READING LIST</div><p>Saved locally on this browser.</p><div data-th-saved></div></div></aside>'
  # Wrap existing main rather than regenerating any article, exercise or tool markup.
  main=re.search(r'<main\b[^>]*>.*?</main\s*>',s,re.I|re.S)
  if main:
   content=main.group(0); wrap='<div class="th-layout">'+content+(rail if detail else '')+'</div>'
   s=s[:main.start()]+wrap+s[main.end():]
  else:
   # Older plain HTML pages are preserved; give them the same shell.
   a=re.search(r'<body\b[^>]*>',s,re.I).end();b=re.search(r'</body\s*>',s,re.I).start();s=s[:a]+'<div class="th-layout"><main>'+s[a:b]+'</main>'+(rail if detail else '')+'</div>'+s[b:]
  footerbrand='' if re.search(r'<footer\b',s,re.I) else f'<a class="th-brand" href="{rel}"><b>TH</b><span>TECHIE<span>HACKER</span></span></a><p>Explore. Learn. Innovate.</p>'
  endnav=f'<div class="th-footer">{footerbrand}<nav aria-label="More resources">{links(nav[1:]+extra,rel)}</nav>'+ (f'<a href="{rel}photo-credits/">Photography credits</a>' if exists('photo-credits') else '')+'</div>'
  s=re.sub(r'(<body\b[^>]*>)',lambda m:m[0]+'<a class="th-skip" href="#th-content">Skip to content</a><div class="th-progress" aria-hidden="true"></div>'+mast+intro+'<div id="th-content" tabindex="-1"></div>',s,count=1,flags=re.I)
  # Map is data, not executable JS; escaping '<' avoids script element termination.
  photo_json=json.dumps(photo_map,ensure_ascii=False).replace('<','\\u003c')
  s=re.sub(r'</head\s*>',lambda m:f'<link rel="stylesheet" href="{rel}premium/interior.css"><script defer src="{rel}premium/interior.js"></script>'+m[0],s,count=1,flags=re.I)
  s=re.sub(r'</body\s*>',lambda m:endnav+f'<script type="application/json" id="th-photo-data">{photo_json}</script>'+m[0],s,count=1,flags=re.I)
  path.write_text(s,encoding='utf-8');count+=1;details+=detail
 assert digest(home)==before,'Homepage changed unexpectedly'
 print(f'Premium Interiors: {count} internal HTML pages themed ({details} detail pages); homepage SHA-256 unchanged: {before}')
