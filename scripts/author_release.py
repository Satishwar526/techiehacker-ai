"""Preserve approved artwork, overlay untouched original author photographs, and link actual resources.
Run after the existing Natural Edition and (if present) Reference Lock hooks.
"""
from pathlib import Path
import html, json, re, shutil, hashlib, base64, urllib.parse, xml.etree.ElementTree as ET
E=lambda v:html.escape(str(v),quote=True)
BASE='https://www.techiehacker.com/'
PHOTOS=[('IMG_6094.jpg','Portrait at IIT Madras'),('IMG_6090.jpg','Technical learning session at IIT Madras'),('IMG_6201.jpg','At the IIT Madras lectern — photograph 1'),('IMG_6204.jpg','At the IIT Madras lectern — photograph 2'),('IMG_6206.jpg','At the IIT Madras lectern — photograph 3'),('IMG_6308.jpg','At IIT Madras, holding a folder in traditional attire')]
W,H=1254,669 # proportional coordinate grid measured on the approved cropped artwork
HOT=[]
def add(t,u,x,y,X,Y):HOT.append((t,u,x,y,X,Y))
for t,u,x,X in [('TechieHacker','index.html',18,208),('Home','index.html',293,350),('AI News','news/',359,406),('Trending','trending/',415,468),('AI Academy','academy/',477,550),('Tools','tools/',558,591),('Research','research/',603,657),('Developer Hub','developers/',669,745),('Blogs','blogs/',757,797),('Tutorials','tutorials/',806,860),('Courses','courses/',868,921),('Prompt Library','prompts/',928,1009),('Podcast and media','media/',1020,1085),('Search','discover/',1133,1165),('News updates','news/',1173,1202),('About the author','about/',1205,1236)]:add(t,u,x,2,X,29)
add('Explore AI World','experience/',280,160,411,191);add('Join AI Academy','academy/',420,160,561,191)
add('Meet the founder — original photograph','about/',0,32,274,204)
for t,u,x,y,X,Y in [('Robotics learning and original videos','reference-resources/#robotics',596,39,808,116),('NVIDIA GPU and accelerated computing','reference-resources/#gpu',812,39,1020,116),('Building AI apps','courses/coding/',1025,39,1236,116),('AI in healthcare','reference-resources/#health',596,120,808,198),('Earth and satellite intelligence','reference-resources/#earth',812,120,1020,198),('AI tools for creators','courses/creative/',1025,120,1236,198)]:add(t,u,x,y,X,Y)
for t,u,x,X in [('Agentic AI','courses/agents/',670,743),('AI Agents','methodologies/agents/',747,813),('RAG','methodologies/rag/',817,870),('LangChain','tutorials/langchain/',874,948),('MCP','tutorials/mcp/',952,1003),('AI Security','tutorials/ai-security/',1008,1080),('Automation','tutorials/n8n/',1085,1158),('Deployment','methodologies/llmops/',1163,1240)]:add(t,u,x,207,X,228)
add('Meet the Founder','about/',15,236,302,327)
for t,u,x,X in [('Technical blogs','blogs/',311,365),('Reader figures — design note','#reference-note',371,427),('Content views — design note','#reference-note',433,488),('Courses','courses/',493,549),('Research','research/',554,613)]:add(t,u,x,240,X,321)
add('About TechieHacker','about/',624,236,975,326);add('Watch available publisher videos','media/',985,236,1241,326)
for t,u,x,X in [('Latest AI Intelligence','news/',15,133),('AI Academy','academy/',140,254),('Tools and resources','library/',260,377),('Research','research/',382,501),('Developer Hub','developers/',508,627),('Interactive Labs','experience/',633,751),('Podcast and media','media/',756,879),('Technical blogs','blogs/',883,1002),('Tutorials','tutorials/',1008,1119),('Courses','courses/',1125,1241)]:add(t,u,x,333,X,383)
add('Latest AI Intelligence — live archive','news/',15,389,530,408)
for t,u,x,X in [('AI chips and infrastructure','reference-resources/#gpu',24,150),('OpenAI and language models','methodologies/llm/',158,279),('AI in drug discovery and research','reference-resources/#health',285,405),('AI-powered coding','tutorials/cursor/',412,524)]:add(t,u,x,410,X,511)
add('Build real-world AI agents','courses/agents/',541,389,871,514);add('All AI tools','tutorials/',881,389,1241,408)
for t,u,x,X in [('ChatGPT','tutorials/chatgpt/',891,958),('Claude','tutorials/claude/',963,1027),('Gemini','tutorials/gemini/',1030,1093),('Cursor','tutorials/cursor/',1096,1162),('Midjourney','tutorials/midjourney/',1167,1235)]:add(t,u,x,411,X,507)
for t,u,x,X in [('AI Tools Directory','tools/',15,217),('Learning Paths','courses/',225,417),('Certification resources','reference-resources/#certification',425,634),('Community / Newsletter','reference-resources/#community',640,858),('Case studies','reference-resources/#cases',865,1033),('Featured courses','courses/',1041,1240)]:add(t,u,x,522,X,562)
add('Tutorials and learning pages','tutorials/',16,568,722,585)
for i,(t,u) in enumerate([('ChatGPT','tutorials/chatgpt/'),('Claude','tutorials/claude/'),('Gemini','tutorials/gemini/'),('Cursor','tutorials/cursor/'),('Midjourney','tutorials/midjourney/'),('GitHub Copilot','tutorials/github-copilot/'),('MCP','tutorials/mcp/'),('RAG','methodologies/rag/'),('AI Agents','methodologies/agents/'),('Prompt Engineering','methodologies/prompt-engineering/'),('Automation','tutorials/n8n/'),('Deployment','methodologies/llmops/')]):add(t+' learning guide',u,23+i*57.85,586,77+i*57.85,614)
for t,u,x,X in [('Technical blogs','blogs/',733,832),('Readers — design note','#reference-note',836,936),('AI tools','tools/',940,1036),('Courses','courses/',1041,1133),('Research','research/',1137,1236)]:add(t,u,x,567,X,616)
for t,u,x,y,X,Y in [('Home','index.html',15,625,213,666),('AI news','news/',231,642,269,653),('Trending','trending/',270,642,311,653),('Blogs','blogs/',313,642,339,653),('Research','research/',341,642,383,653),('AI Academy','academy/',231,654,289,666),('Tools','tools/',292,654,316,666),('Developer Hub','developers/',318,654,382,666),('Tutorials','tutorials/',394,642,436,653),('Courses','courses/',438,642,478,653),('Learning paths','courses/',480,642,533,653),('Certification','reference-resources/#certification',394,654,451,666),('Interactive labs','experience/',454,654,532,666),('AI tools directory','tools/',557,642,626,653),('Prompt library','prompts/',629,642,685,653),('Case studies','reference-resources/#cases',557,654,610,666),('Downloads and learning resources','library/',613,654,683,666),('Community / Newsletter','reference-resources/#community',698,641,823,653),('YouTube / Podcast resources','media/',698,654,823,666),('About TechieHacker','about/',844,641,924,653),('Meet the founder','about/',925,641,1005,653),('Our journey','about/#author-gallery',844,654,912,666),('Contact information','reference-resources/#community',914,654,1003,666),('Newsletter information','reference-resources/#community',1009,636,1120,660),('Media — YouTube resources','media/',1134,635,1155,662),('LinkedIn information','reference-resources/#community',1160,635,1179,662),('X information','reference-resources/#community',1182,635,1200,662),('GitHub project','reference-resources/#community',1205,635,1223,662),('Podcast resources','media/',1226,635,1242,662)]:add(t,u,x,y,X,Y)

def rect(x,y,X,Y):return f'left:{100*x/W:.7f}%;top:{100*y/H:.7f}%;width:{100*(X-x)/W:.7f}%;height:{100*(Y-y)/H:.7f}%'
CSS='''*{box-sizing:border-box}html{background:#0b1216;color:#e8e9e9;font:15px/1.5 system-ui,sans-serif}body{margin:0}a{color:#f0d297}.viewport{overflow-x:auto}.design{position:relative;width:100%;min-width:1000px;aspect-ratio:1672/892;isolation:isolate}.art{width:100%;height:100%;display:block;user-select:none}.original-slot{position:absolute;background:#101619;display:flex;justify-content:center;align-items:flex-start;overflow:hidden;pointer-events:none}.original-slot img{width:100%;height:100%;object-fit:contain;object-position:center top;display:block}.hero-original{clip-path:polygon(0 0,100% 0,100% 85%,88.35% 85%,88.35% 100%,0 100%)}.founder-original{border-radius:8px 0 0 8px;align-items:center}.founder-original img{object-position:center}.hotspot{position:absolute;display:block;border-radius:5px;text-decoration:none;outline:none}.hotspot:focus-visible{outline:3px solid #ffdc8b;outline-offset:1px;background:#fff1}.search-overlay{position:absolute;display:flex;gap:0}.search-overlay input{width:84%;min-width:0;border:0;background:transparent;color:transparent;font:inherit;padding:0 5px;outline:none;caret-color:white}.search-overlay input:focus,.search-overlay input:not(:placeholder-shown){background:#20262a;color:white;border:1px solid #d8b36b;border-radius:5px}.search-overlay button{width:16%;border:0;background:transparent;color:transparent;cursor:pointer}.search-overlay button:focus-visible{outline:3px solid #ffdc8b}.sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}.note{padding:16px 24px;border-top:1px solid #364147;max-width:1200px;margin:auto;color:#c5cbd0;font-size:13px}.note p{margin:7px 0}.note nav{line-height:2}.skip{position:absolute;left:-9999px}.skip:focus{position:fixed;left:12px;top:12px;z-index:5;background:#111;color:white;padding:10px}'''

def home(root,preview=False):
 def dest(u):return BASE+('' if u=='index.html' else u) if preview and not u.startswith('#') else u
 def asset(rel):
  if not preview:return rel
  mime='image/png' if rel.endswith('.png') else 'image/jpeg'
  return 'data:'+mime+';base64,'+base64.b64encode((root/'site'/rel).read_bytes()).decode()
 def overlay(name,cls,x,y,X,Y,alt):return f'<div class="original-slot {cls}" style="{rect(x,y,X,Y)}"><img src="{asset("original-author/"+name)}" alt="{E(alt)}"></div>'
 links=''.join(f'<a class="hotspot" href="{E(dest(u))}" aria-label="{E(t)}" title="{E(t)}" style="{rect(x,y,X,Y)}"><span class="sr">{E(t)}</span></a>' for t,u,x,y,X,Y in HOT)
 search=f'<form class="search-overlay" action="{E(dest("discover/"))}" method="get" style="{rect(245,205,645,230)}"><input name="q" placeholder=" " type="search" aria-label="Search AI news, tutorials and courses"><button type="submit" aria-label="Search">Search</button></form>'
 nav=' · '.join(f'<a href="{E(dest(u))}">{E(t)}</a>' for t,u in [('AI news','news/'),('AI Academy','academy/'),('Tools','tools/'),('Blogs','blogs/'),('Tutorials','tutorials/'),('Courses','courses/'),('Media and music','media/'),('Interactive labs','experience/'),('About','about/'),('Resource guide','reference-resources/')])
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TechieHacker — Tomorrow’s Intelligence. Today.</title><meta name="description" content="AI news, academy, tools, research and technical blogs by Satishwar Mallekedi."><style>{CSS}</style></head><body><a class="skip" href="#reference-note">Skip to accessible navigation</a><main><h1 class="sr">TechieHacker — Tomorrow’s Intelligence. Today.</h1><div class="viewport"><div class="design"><img class="art" src="{asset('reference/homepage.png')}" width="1672" height="892" alt="Approved TechieHacker design with AI media, learning, news and tools.">{overlay('IMG_6204.jpg','founder-original',15,236,98,326,'Full original photograph at the IIT Madras lectern')}{links}{search}</div></div></main><footer class="note" id="reference-note"><p><strong>Design reference:</strong> The approved artwork is preserved except for the founder-card photograph, which shows the full unmodified supplied JPEG. The pictured readership, view counts, headlines, course totals, video titles and durations are illustrative. Tiles lead to relevant real learning resources and available publisher videos, not necessarily the exact pictured clip or headline. No social account or newsletter subscription is claimed; community information is linked. On narrow screens, scroll horizontally to preserve the desktop composition.</p>{'<p>Standalone visual preview: links point to the production domain, and newly added routes work after deployment.</p>' if preview else ''}<nav aria-label="Accessible navigation">{nav}</nav></footer></body></html>'''

RESOURCE_SECTIONS=[('robotics','Robotics and physical AI','Explore real robot engineering and its underlying learning concepts.',[('Boston Dynamics Atlas','https://bostondynamics.com/products/atlas/'),('Publisher video collection','../media/'),('AI agent foundations','../methodologies/agents/')]),('gpu','GPU infrastructure and accelerated computing','Learn how accelerated computing supports AI training and inference.',[('NVIDIA Deep Learning Institute','https://www.nvidia.com/en-us/training/'),('Production AI and LLMOps','../methodologies/llmops/'),('Local models and ML course','../courses/models/')]),('health','AI in healthcare and scientific research','Start with trustworthy research and responsible applications.',[('WHO: artificial intelligence','https://www.who.int/health-topics/artificial-intelligence'),('Health and medicine technical perspectives','../discover/?q=healthcare'),('Research resources','../research/')]),('earth','Earth and satellite intelligence','Explore Earth observation and related scientific data.',[('NASA Earth science','https://science.nasa.gov/earth/'),('Publisher films','../media/'),('Environmental AI perspectives','../discover/?q=climate')]),('certification','Learning and certification resources','TechieHacker tracks are independent self-paced learning, not accredited certificates. Check official providers for eligibility and fees.',[('NVIDIA training and certification','https://www.nvidia.com/en-us/training/'),('TechieHacker courses','../courses/'),('AI Academy','../academy/')]),('cases','Practical projects and case-study learning','Explore guided exercises and technical perspectives. These are not claims of verified commercial deployments.',[('Technical blogs','../blogs/'),('Tool tutorials','../tutorials/'),('Interactive labs','../experience/'),('Agent engineering course','../courses/agents/')]),('community','Community, newsletter and social links','No confirmed newsletter service or social profile has been supplied. Follow the public project, source-linked news and media library for now.',[('TechieHacker GitHub project','https://github.com/Satishwar526/techiehacker-ai'),('Latest AI news','../news/'),('Media and background music','../media/'),('About the founder','../about/')])]

def resource_page(out):
 sections=''.join(f'<section id="{s}"><h2>{E(t)}</h2><p>{E(d)}</p><ul>'+''.join(f'<li><a href="{E(u)}">{E(n)} →</a></li>' for n,u in links)+'</ul></section>' for s,t,d,links in RESOURCE_SECTIONS)
 path=out/'reference-resources';path.mkdir(exist_ok=True)
 (path/'index.html').write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Learning resources | TechieHacker</title><link rel="stylesheet" href="../natural/theme.css"><link rel="stylesheet" href="../original-author/author.css"></head><body class="natural"><header class="top"><a class="brand" href="../">TECHIEHACKER</a><nav><a href="../tutorials/">Tutorials</a> · <a href="../courses/">Courses</a> · <a href="../media/">Media</a></nav></header><main class="inner reading"><h1>Explore the original resources</h1><p>Relevant learning links behind the approved homepage tiles.</p>{sections}</main></body></html>',encoding='utf-8')


def inject_photo_pages(root,out):
 def img(name,caption,rel):return f'<img src="{rel}original-author/{name}" alt="{E(caption)}" loading="lazy" decoding="async">'
 def add_css(s,rel):return s.replace('</head>',f'<link rel="stylesheet" href="{rel}original-author/author.css"></head>',1)
 def replace_old(s,rel):
  # Only older generated author portraits, never unrelated article images.
  return re.sub(r'<img\b[^>]*(?:satishwar-[^"\s>]+|author-scene\.webp|cinematic/author\.webp|natural/portrait\.(?:webp|jpg))[^>]*>',img('IMG_6094.jpg',PHOTOS[0][1],rel),s,flags=re.I)
 p=out/'about/index.html';s=replace_old(p.read_text(encoding='utf-8'),'../');s=add_css(s,'../')
 gallery=''.join(f'<figure><a href="../original-author/{n}">{img(n,c,"../")}</a><figcaption>{E(c)} · Original photograph</figcaption></figure>' for n,c in PHOTOS)
 content=f'<section id="author-gallery" class="original-gallery"><h2>My journey in photographs</h2><p>Original photographs supplied by Satishwar Mallekedi, displayed without image editing. These document moments at IIT Madras and a technical learning session; they do not imply an institutional endorsement or a particular degree.</p><div class="original-grid">{gallery}</div></section>'
 if '</main>' in s:s=s.replace('</main>',content+'</main>',1)
 else:s=s.replace('</body>',content+'</body>',1)
 p.write_text(s,encoding='utf-8')
 archive=json.loads((root/'blogs.json').read_text(encoding='utf-8'));assert isinstance(archive,list) and len(archive)>=200,'Expected existing 200+ blog archive; no articles will be invented.'
 for i,b in enumerate(archive):
  slug=b['slug'];assert re.fullmatch(r'[A-Za-z0-9_-]+',slug),slug
  p=out/'blogs'/slug/'index.html';assert p.is_file(),f'Existing blog page missing: {slug}'
  s=add_css(replace_old(p.read_text(encoding='utf-8'),'../../'),'../../');n,c=PHOTOS[i%len(PHOTOS)]
  block=f'<aside class="original-author-card"><a href="../../about/#author-gallery">{img(n,c,"../../")}</a><div><strong>Author: Satishwar Mallekedi</strong><p>Tech Blogger · AI Enthusiast · Founder</p><small>{E(c)} · Original author photograph, not evidence of the article’s technical claims.</small><p><a href="../../about/#author-gallery">About the author and photo gallery →</a></p></div></aside>'
  # After the main heading, without modifying the article body.
  if re.search(r'</h1\s*>',s,re.I):s=re.sub(r'</h1\s*>',lambda m:m.group(0)+block,s,count=1,flags=re.I)
  elif '<body>' in s:s=s.replace('<body>','<body>'+block,1)
  else:s=s.replace('</body>',block+'</body>',1)
  p.write_text(s,encoding='utf-8')
 return len(archive)


def render(root,out):
 root,out=Path(root),Path(out)
 for d in ('reference','original-author'):shutil.copytree(root/'site'/d,out/d,dirs_exist_ok=True)
 hashes=json.loads((root/'site/original-author/originals.json').read_text())
 for n,h in hashes.items():assert hashlib.sha256((out/'original-author'/n).read_bytes()).hexdigest()==h,n
 ref=json.loads((root/'site/reference/reference.json').read_text());assert hashlib.sha256((out/'reference/homepage.png').read_bytes()).hexdigest()==ref['asset_sha256']
 resource_page(out);count=inject_photo_pages(root,out)
 (out/'index.html').write_text(home(root),encoding='utf-8')
 # Add new resource page to search and sitemap, retaining existing data.
 index=out/'search-index.json';records=json.loads(index.read_text()) if index.exists() else []
 if isinstance(records,list):
  records=[r for r in records if r.get('url')!='../reference-resources/'];records.append(dict(title='Original learning resources',summary='Robotics GPU NVIDIA healthcare Earth certification community case studies',category='Learning',url='../reference-resources/'));index.write_text(json.dumps(records,ensure_ascii=False),encoding='utf-8')
 sitemap=out/'sitemap.xml'
 if sitemap.exists():
  tree=ET.parse(sitemap);sr=tree.getroot();ns=sr.tag.split('}')[0]+'}' if '}' in sr.tag else '';u=BASE+'reference-resources/'
  if u not in {x.text for x in sr.iter(ns+'loc')}:ET.SubElement(ET.SubElement(sr,ns+'url'),ns+'loc').text=u
  if ns:ET.register_namespace('',ns[1:-1])
  tree.write(sitemap,encoding='utf-8',xml_declaration=True)
 print(f'Original Photo Edition: {len(HOT)} homepage links; {count} authored blog pages; {len(hashes)} byte-identical originals.')
