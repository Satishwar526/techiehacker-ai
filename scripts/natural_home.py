"""Final rendering overlay; source archives and deployment workflow are read-only."""
from pathlib import Path
from collections import Counter
import json,html,re,hashlib,urllib.parse,xml.etree.ElementTree as ET,shutil
E=lambda x:html.escape(str(x),quote=True)
BASE='https://www.techiehacker.com/'
VIDEOS=[('29ECwExc-_M','All New Atlas','Boston Dynamics','robotics'),('4lSQnrMC6nY','Gemini Robotics 2','Google DeepMind','developer'),('wQF61J0Yd54','Synthesis — Ultra HD visualization','NASA · 4K labeled','servers'),('d66Qv2WASqw','Earth Day 2026','NASA · 4K labeled','earth'),('bY8RDKoBwU0','AI filmmaking','Higgsfield AI','studio')]
COURSES=[('foundations','AI essentials','Learn to use and evaluate AI assistants',['chatgpt','claude','gemini','perplexity','notebooklm']),('coding','AI-powered development','Build tested software with coding assistants',['cursor','github-copilot','codex','claude-code','openai-api']),('agents','Build real-world AI agents','Retrieval, tool integration and automation',['hugging-face','langchain','llamaindex','qdrant','mcp','n8n','agentforce','ai-security']),('models','Machine learning and local models','Train, evaluate and serve models',['pytorch','tensorflow','ollama','mlflow']),('creative','AI for creators','Responsible visual and video production',['midjourney','adobe-firefly','runway'])]
def read(p,default):return json.loads(p.read_text(encoding='utf-8')) if p.is_file() else default
def render(root,out):
 root,out=Path(root),Path(out); a=out/'natural';a.mkdir(exist_ok=True);shutil.copytree(root/'site/natural',a,dirs_exist_ok=True)
 photos={p['id']:p for p in read(a/'photos.json',[])}; tutorials=read(a/'tutorials.json',[]); byid={t[0]:t for t in tutorials}; index=[]
 def exists(p):return (out/p/'index.html').is_file()
 def url(p,r='',fallback='learn'):
  return r+p+'/' if exists(p) else (r+fallback+'/' if exists(fallback) else r+'index.html')
 def photo(key,r='',lazy=True):
  p=photos[key]; f=p['file'].replace(' ','_');h=hashlib.md5(f.encode()).hexdigest(); q=urllib.parse.quote(f);orig=f'https://upload.wikimedia.org/wikipedia/commons/{h[0]}/{h[:2]}/{q}';thumb=f'https://upload.wikimedia.org/wikipedia/commons/thumb/{h[0]}/{h[:2]}/{q}/960px-{q}'
  local=(a/f'{key}-640.webp').exists(); src=r+f'natural/{key}-640.webp' if local else thumb
  ss=', '.join(r+f'natural/{key}-{w}.webp {w}w' for w in (640,1280,3840) if (a/f'{key}-{w}.webp').exists()) if local else ''
  responsive=f' srcset="{E(ss)}" sizes="(max-width: 680px) 95vw, 420px"' if ss else ''
  return f'<div class="photo"><img src="{E(src)}"{responsive} alt="{E(p["alt"])}" width="640" height="420" {"loading=lazy" if lazy else ""} decoding="async" data-fallback="{E(orig)}"><span class="photo-note">File photo</span></div>'
 def catphoto(text):
  t=text.lower()
  if any(x in t for x in ('health','medical','protein','biotech','medicine')):return 'health'
  if any(x in t for x in ('robot','manufactur','industrial')):return 'robotics'
  if any(x in t for x in ('gpu','chip','cloud','hardware','infrastructure','server')):return 'servers'
  if any(x in t for x in ('space','astronom','climate','agricultur','earth')):return 'earth'
  if any(x in t for x in ('video','media','creative','image','music')):return 'studio'
  return 'developer'
 def nav(r=''):
  items=[('Home',''),('AI News','news'),('Trending','trending'),('AI Academy','academy'),('Tools','tools'),('Research','research'),('Developer Hub','developers'),('Blogs','blogs'),('Tutorials','tutorials'),('Courses','courses'),('Prompt Library','prompts'),('Media','media')]
  return '<header class="top"><a class="brand" href="'+r+'index.html"><b>TH</b> TECHIE<span>HACKER</span></a><button id="menu" aria-expanded="false" aria-controls="navlinks">Menu</button><nav id="navlinks">'+''.join(f'<a href="{E(r+p+"/" if p else r+"index.html")}">{E(t)}</a>' for t,p in items if not p or exists(p) or p in ('tutorials','courses','media','trending'))+f'</nav><a class="searchicon" href="{r}discover/" aria-label="Search">⌕</a></header>'
 def footer(r=''):
  return f'<footer><a class="brand" href="{r}index.html"><b>TH</b> TECHIE<span>HACKER</span></a><p>Explore. Learn. Innovate. · Independent AI education and source-linked news</p><div><a href="{r}about/">About</a> · <a href="{r}photo-credits/">Photography credits</a> · <a href="{r}tutorials/">Tutorials</a></div></footer>'
 def shell(title,desc,body,r='',slug=''):
  return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} | TechieHacker</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{BASE+slug}"><link rel="stylesheet" href="{r}natural/theme.css"><script defer src="{r}natural/site.js"></script></head><body class="natural">{nav(r)}<main>{body}</main>{footer(r)}</body></html>'
 def page(slug,title,desc,body,category='Learning'):
  p=out/slug/'index.html';p.parent.mkdir(parents=True,exist_ok=True);r='../'*len(Path(slug).parts);p.write_text(shell(title,desc,body,r,slug+'/'),encoding='utf-8');index.append(dict(title=title,summary=desc,category=category,url='../'+slug+'/'))
 def head(t,d='',link='',label='View all'):
  return f'<div class="section-head"><div><h2>{E(t)}</h2><p>{E(d)}</p></div>'+ (f'<a href="{E(link)}">{E(label)} →</a>' if link else '')+'</div>'
 def film(v,r=''):
  id,title,source,key=v
  return f'<button class="film" data-video="{E(id)}" data-title="{E(title)}">{photo(key,r)}<span class="film-caption"><span class="play">▶</span><span><strong>{E(title)}</strong><small>{E(source)}</small></span></span></button>'
 def dialog():return '<dialog id="videoDialog"><div class="section-head"><h2 id="videoTitle">Video</h2><button id="videoClose">Close ×</button></div><div id="videoFrame"></div><p>Original publisher video. Choose 2160p where available in player settings. <a id="youtubeLink" target="_blank" rel="noopener noreferrer">Open YouTube ↗</a></p></dialog>'
 # Preserve existing simulations; build them if the earlier overlay was not installed.
 if True:
  from natural_experiences import render_experiences
  render_experiences(root,out)
 # Replace experience cinema (old illustration thumbnails) with real photographs.
 page('experience/cinema','AI Cinema','Curated publisher videos, with 4K playback where available.',f'<section class="inner"><div class="kicker">WATCH & LEARN</div><h1>AI Cinema</h1><p>Explore real technology demonstrations and scientific footage. Playback resolution is selected by YouTube.</p><div class="film-grid large">{"".join(film(v,"../../") for v in VIDEOS)}</div></section>{dialog()}','Media')
 page('media','AI Cinema & Media','Original publisher videos and peaceful ambient audio.',f'<section class="inner"><div class="kicker">TECHIEHACKER MEDIA</div><h1>See intelligence in action.</h1><p>Watch original publisher videos. These are not TechieHacker-owned productions.</p><div class="film-grid large">{"".join(film(v,"../") for v in VIDEOS)}</div><h2>Focus soundtrack</h2><audio controls loop preload="none" src="../natural/ambient.mp3"></audio><p>Original synthesized ambient soundscape from the previous multimedia release.</p></section>{dialog()}','Media')
 # Tutorials and course pages with browser-local completion tracking.
 def tutcard(t,r=''):
  s,n,c,l,_,goal,*_=t;return f'<a class="lesson-card" data-filter="{E(c)}" data-text="{E(n+" "+c+" "+goal)}" href="{r}tutorials/{s}/"><small>{E(c)} · {E(l)}</small><h3>{E(n)}</h3><p>{E(goal)}</p><span class="lesson-status" data-status="{s}">Start tutorial →</span></a>'
 options=''.join(f'<option>{E(x)}</option>' for x in sorted({t[2] for t in tutorials}))
 page('tutorials','AI Tool Tutorials','Practical tutorials for popular AI tools, frameworks and deployment methods.',f'<section class="inner"><div class="kicker">LEARN BY BUILDING</div><h1>AI tools, from first steps to production.</h1><p>{len(tutorials)} practical tutorials, each with an exercise, source documentation and a safety note.</p><div class="filterbar"><input id="filterText" type="search" placeholder="Find a tool or skill"><select id="filterCategory"><option value="">All categories</option>{options}</select></div><p id="filterCount" aria-live="polite"></p><div class="lesson-grid" id="filterGrid">{"".join(tutcard(t,"../") for t in tutorials)}</div></section>')
 for s,n,c,l,ref,goal,steps,exercise,risk in tutorials:
  lis=''.join(f'<li>{E(x.strip())}</li>' for x in re.split(r'(?<=\.)\s+(?=[A-Z])',steps))
  page('tutorials/'+s,n+' tutorial',goal,f'<article class="inner reading"><div class="kicker">{E(c)} / {E(l)}</div><h1>{E(n)}: practical learning guide</h1><p class="lead">{E(goal)}</p><p>Use an authorized learning environment and public or synthetic data. Product interfaces and access requirements can change; follow the linked official documentation for setup.</p><h2>Step-by-step exercise</h2><ol>{lis}</ol><h2>Build this</h2><p>{E(exercise)}</p><h2>Check your work</h2><p>Save your input, output and a short explanation of how you independently checked the result. Identify one failure case and repeat the exercise after changing the input.</p><h2>Responsible use</h2><p>{E(risk)}</p><p><a class="gold" href="{E(ref)}" target="_blank" rel="noopener noreferrer">Official learning documentation ↗</a></p><button class="gold" data-complete="{s}" aria-pressed="false">Mark as completed</button> <a href="../">All tutorials →</a><p class="muted">Progress is saved in this browser only. This is an independent learning guide, not a vendor certification.</p></article>')
 coursecards=[]
 for s,n,d,ids in COURSES:
  coursecards.append(f'<a class="lesson-card" href="{s}/"><small>{len(ids)} lessons · Self-paced</small><h3>{E(n)}</h3><p>{E(d)}</p><span data-course="{E(",".join(ids))}">Start course →</span></a>')
  page('courses/'+s,n,d,f'<section class="inner"><div class="kicker">SELF-PACED LEARNING TRACK</div><h1>{E(n)}</h1><p>{E(d)}</p><p data-course="{E(",".join(ids))}" aria-live="polite"></p><div class="lesson-grid">{"".join(tutcard(byid[i],"../../") for i in ids)}</div><p>Complete each practical exercise. The course records local progress and does not issue accredited certificates.</p></section>')
 page('courses','AI Courses & Learning Tracks','Five structured learning tracks with practical projects and progress tracking.',f'<section class="inner"><div class="kicker">AI UNIVERSITY</div><h1>Build skills that matter.</h1><p>Five self-paced tracks. Pick a path and complete the exercises.</p><div class="lesson-grid">{"".join(coursecards)}</div></section>')
 news=[n for n in read(root/'news.json',[]) if isinstance(n,dict) and re.fullmatch('[A-Za-z0-9_-]+',str(n.get('id',''))) and exists('news/'+str(n['id']))];news.sort(key=lambda n:str(n.get('date','')),reverse=True)
 blogs=[b for b in read(root/'blogs.json',[]) if isinstance(b,dict) and re.fullmatch('[A-Za-z0-9_-]+',str(b.get('slug',''))) and exists('blogs/'+str(b['slug']))]
 def news_card(n,r=''):
  return f'<a class="story" href="{r}news/{E(n["id"])}/">{photo(catphoto(str(n.get("title",""))+str(n.get("category",""))),r)}<div><small>{E(n.get("category","AI News"))}</small><h3>{E(n.get("title","News"))}</h3><p>{E(str(n.get("summary",""))[:190])}</p><small>{E(n.get("source",""))} · {E(n.get("date",""))}</small></div></a>'
 topics=Counter(str(n.get('category','AI')) for n in news[:30]);topicitems=''.join(f'<li>{E(t)} — {v} archived stories</li>' for t,v in topics.most_common()) or '<li>No published categories yet.</li>'
 page('trending','Recent AI Topics','Topic counts from the latest 30 archived news articles, not a global trend ranking.',f'<section class="inner"><div class="kicker">NEWSROOM SIGNALS</div><h1>What the newsroom is following</h1><p>Counts reflect the latest 30 archived news articles and are recalculated during each build.</p><ul>{topicitems}</ul><div class="news-grid">{"".join(news_card(n,"../") for n in news[:12])}</div></section>','News')
 credit=''.join(f'<li><a href="https://commons.wikimedia.org/wiki/File:{urllib.parse.quote(p["file"].replace(" ","_"))}">{E(p["file"])}</a> — {E(p["credit"])}; <a href="{E(p["license_url"])}">{E(p["license"])}</a>; source resolution {E(p["size"])}. Displayed resized/cropped for layout. Cached derivatives retain applicable licenses.</li>' for p in photos.values())
 page('photo-credits','Photography Credits','Original photography provenance and licenses.',f'<article class="inner reading"><h1>Photography credits</h1><p>All editorial photographs are thematic file photos, not evidence of the reported events or video scenes. The author photograph was supplied by the site owner; the face has not been edited.</p><ul>{credit}</ul></article>','About')
 # Replace existing about page with text; only homepage displays the portrait.
 page('about','Meet Satishwar Mallekedi','Tech blogger, AI enthusiast and founder of TechieHacker.', '<article class="inner reading"><div class="kicker">THE AUTHOR’S DESK</div><h1>Satishwar Mallekedi</h1><p class="lead">Tech Blogger · AI Enthusiast · Founder</p><p>I’m passionate about understanding artificial intelligence and sharing useful, practical technology insights. TechieHacker brings together source-linked news, technical guides, learning resources and balanced perspectives on what AI can do and where it needs careful engineering.</p><h2>Our mission</h2><p>Explore. Learn. Innovate. Make AI approachable without losing technical depth. Technical articles may be AI-assisted and should be reviewed by the named author before publication.</p><a href="../blogs/">Read technical blogs →</a></article>','About')
 # Unified search uses existing search-index data, with all added pages appended below.
 page('discover','Search TechieHacker','Search articles, tutorials, tools and learning tracks.', '<section class="inner"><div class="kicker">KNOWLEDGE SEARCH</div><h1>Find your next idea.</h1><input id="discoverQuery" type="search" placeholder="Search AI, RAG, coding, healthcare…"><p id="discoverCount" aria-live="polite"></p><div id="discoverResults" class="lesson-grid"></div></section>','Search')
 # Home: compact desktop editorial dashboard; reflows into readable mobile sections.
 tiles=[('Latest AI Intelligence','Breaking news & analysis','news','N'),('AI Academy','Structured learning paths','academy','A'),('Tools & Resources','Curated AI resources','library','T'),('Research','Papers and scientific insights','research','R'),('Developer Hub','APIs, code and projects','developers','D'),('Interactive Labs','Learn by experimenting','experience','L'),('Podcast / Media','Publisher video library','media','M'),(f'{len(blogs)} Technical Blogs','Balanced technical perspectives','blogs','B'),('Tutorials','Hands-on tool guides','tutorials','G'),('Courses','Self-paced learning tracks','courses','C')]
 tilehtml=''.join(f'<a class="quick" href="{E(url(p))}"><b>{i}</b><span><strong>{E(t)}</strong><small>{E(d)}</small></span><span>↗</span></a>' for t,d,p,i in tiles if exists(p))
 stats=[(len(blogs),'Technical blogs'),(len(tutorials),'Tool tutorials'),(len(COURSES),'Learning tracks'),(len(news),'News articles'),(len(VIDEOS),'Publisher films')];statshtml=''.join(f'<div><strong>{n}</strong><small>{E(t)}</small></div>' for n,t in stats)
 groups={}
 for b in blogs:groups.setdefault(b.get('category','AI'),[]).append(b)
 order=[g[i] for i in range(max(map(len,groups.values()),default=0)) for g in groups.values() if i<len(g)]
 bloghtml=''.join(f'<a class="story" href="blogs/{E(b["slug"])}/">{photo(catphoto(str(b.get("category",""))+str(b.get("title",""))))}<div><small>{E(b.get("category","AI"))}</small><h3>{E(b.get("title","Blog"))}</h3><p>{E(str(b.get("reflection",b.get("summary","")))[:145])}</p><small>Author: Satishwar Mallekedi</small></div></a>' for b in order)
 pills=''.join(f'<a href="discover/?q={urllib.parse.quote(t)}">{E(t)}</a>' for t in ['Agentic AI','AI Agents','RAG','LangChain','MCP','AI Security','Automation','Deployment'])
 top_tools=''.join(f'<a class="tool" href="tutorials/{s}/"><span class="tool-mark">{E(byid[s][1][:2].upper())}</span><strong>{E(byid[s][1])}</strong><small>Tutorial ↗</small></a>' for s in ['chatgpt','claude','gemini','cursor','midjourney'])
 sixth=f'<a class="film" href="{url("tutorials/gemini")}">{photo("health",lazy=False)}<span class="film-caption"><span class="play">↗</span><span><strong>AI in practice</strong><small>Multimodal learning guide</small></span></span></a>'
 home=f'''<section class="hero"><div class="hero-portrait"><img src="natural/portrait.webp" alt="Satishwar Mallekedi in the original outdoor photograph" width="900" height="1600"></div><div class="hero-copy"><div class="kicker">WELCOME TO TECHIEHACKER</div><h1>Tomorrow’s<br>Intelligence. <em>Today.</em></h1><p>Your destination for AI resources, learning, news, research, tools and real-world innovation.</p><div class="actions"><a class="gold" href="{url('experience')}">Explore AI World →</a><a class="outline" href="{url('academy',fallback='courses')}">Join AI Academy</a></div><div class="sound"><span>♫ &nbsp; Ambient AI Soundscape</span><audio id="ambient" controls loop preload="none" src="natural/ambient.mp3"></audio></div></div><div class="film-grid">{''.join(film(v) for v in VIDEOS)}{sixth}</div></section><div class="searchrow"><form action="discover/" method="get"><input type="search" name="q" aria-label="Search the website" placeholder="Search AI news, tutorials, tools, research, courses and more…"><button class="gold">Search</button></form><div class="pills">{pills}</div></div><section class="identity"><div class="panel author"><div class="kicker">THE FOUNDER</div><h2>Satishwar Mallekedi</h2><strong>Tech Blogger · AI Enthusiast · Founder</strong><p>Exploring AI and emerging technology through practical insights, tutorials and balanced analysis.</p><a href="about/">Meet the founder →</a></div><div class="metrics panel">{statshtml}</div><div class="panel about"><h2>About TechieHacker</h2><p>Independent AI media, learning and research resources for curious minds and builders.</p><a href="photo-credits/">Photography sources</a> · <a href="media/">Watch & listen →</a></div></section><section class="quickgrid">{tilehtml}</section><div class="dashboard"><section class="panel newsroom">{head('Latest AI Intelligence','Source-linked news and breakthroughs',url('news'))}<div class="news-grid">{''.join(news_card(n) for n in news[:4]) or '<p>Awaiting the next newsroom run.</p>'}</div></section><section class="panel feature">{head('Featured Learning Track','Practical AI engineering','courses/')}<div class="feature-photo">{photo('developer')}<div><h2>Build Real-World<br>AI Agents</h2><p>RAG, MCP, tools and automation.</p><a class="gold" href="courses/agents/">Start Learning →</a></div></div></section><section class="panel tools">{head('Top AI Tools','Learn popular tools','tutorials/')}<div class="tool-grid">{top_tools}</div></section></div><section class="panel tutorialstrip">{head('Tutorials & Learning Pages','Practical guides for AI tools and frameworks','tutorials/')}<div class="pills">{''.join(f'<a href="tutorials/{t[0]}/">{E(t[1])}</a>' for t in tutorials)}</div></section><section class="panel blogsection">{head('The Author’s Desk','Technical perspectives by Satishwar Mallekedi',url('blogs'))}<div class="actions"><button id="blogPrev">←</button><button id="blogNext">→</button><button id="blogPause" aria-pressed="false">Pause auto-scroll</button></div><div id="blogRail" class="rail" tabindex="0" aria-label="Technical blogs">{bloghtml or '<p>Blog archive unavailable in this source backup.</p>'}</div></section><section class="panel">{head('AI Courses & Learning Tracks','Follow a guided sequence and track progress','courses/')}<div class="course-grid">{''.join(f'<a class="lesson-card" href="courses/{s}/"><h3>{E(n)}</h3><p>{E(d)}</p><span data-course="{E(",".join(ids))}"></span></a>' for s,n,d,ids in COURSES)}</div></section>{dialog()}'''
 (out/'index.html').write_text(shell('Tomorrow’s Intelligence. Today.','AI news, learning, research, tools and tutorials.',home),encoding='utf-8')
 # Existing content remains; neutralize old visual styling and remove decorative author thumbnails.
 for p in out.rglob('index.html'):
  s=p.read_text(encoding='utf-8');rel='../'*len(p.relative_to(out).parts[:-1]);
  if 'natural/theme.css' in s:continue
  s=re.sub(r'<img\b[^>]*(?:satishwar-[^"\s>]+|author-scene\.webp|cinematic/author\.webp)[^>]*>', '',s,flags=re.I)
  # Convert known old decorative article visuals to credited thematic photo references.
  def replace_visual(m):
   tag=m.group(0);src=re.search(r'\bsrc=["\']([^"\']+)["\']',tag,re.I)
   if not src:return tag
   old=src.group(1)
   if re.search(r'(?:cinematic/(?:android|chip|code|future|hologram|infrastructure|neural|robotics|security)\.webp|(?:^|/)(?:illustrations|art)/[^/]+\.(?:svg|webp|png))',old,re.I):return photo(catphoto(p.parent.name+' '+old),rel)
   return tag
  s=re.sub(r'<img\b[^>]*>',replace_visual,s,flags=re.I)
  s=s.replace('</head>',f'<link rel="stylesheet" href="{rel}natural/legacy.css"><script defer src="{rel}natural/site.js"></script></head>',1)
  if '</body>' in s:s=s.replace('</body>',f'<div class="natural-links"><a href="{rel}tutorials/">AI Tutorials</a> · <a href="{rel}courses/">Courses</a> · <a href="{rel}media/">Media</a> · <a href="{rel}photo-credits/">Photo credits</a></div></body>',1)
  p.write_text(s,encoding='utf-8')
 # Merge generated URLs and index entries, replacing only matching records.
 idx=out/'search-index.json'; old=read(idx,[]); old=old if isinstance(old,list) else []; new={x['url']:x for x in index};records=[x for x in old if isinstance(x,dict) and x.get('url') not in new]+index
 if not old:
  records += [dict(title=n.get('title','News'),summary=n.get('summary',''),category=n.get('category','News'),url='../news/'+str(n['id'])+'/') for n in news]
  records += [dict(title=b.get('title','Blog'),summary=b.get('reflection',''),category=b.get('category','Blog'),url='../blogs/'+str(b['slug'])+'/') for b in blogs]
 idx.write_text(json.dumps(records,ensure_ascii=False),encoding='utf-8')
 sitemap=out/'sitemap.xml'
 if sitemap.exists():tree=ET.parse(sitemap); sr=tree.getroot()
 else:sr=ET.Element('{http://www.sitemaps.org/schemas/sitemap/0.9}urlset');tree=ET.ElementTree(sr)
 ns=sr.tag.split('}')[0]+'}' if '}' in sr.tag else '';known={e.text for e in sr.iter(ns+'loc')}
 for x in index:
  u=BASE+x['url'].removeprefix('../');
  if u not in known:ET.SubElement(ET.SubElement(sr,ns+'url'),ns+'loc').text=u;known.add(u)
 if ns:ET.register_namespace('',ns[1:-1])
 tree.write(sitemap,encoding='utf-8',xml_declaration=True)
 print(f'Natural Edition: {len(blogs)} existing blogs; {len(news)} news items; {len(tutorials)} tutorials; {len(COURSES)} courses; {len(index)} generated routes.')
