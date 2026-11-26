import json,html,pathlib,shutil,datetime
ROOT=pathlib.Path(__file__).resolve().parents[1]; OUT=ROOT/'dist'; SITE=ROOT/'site'
E=lambda s:html.escape(str(s),quote=True)
if OUT.exists(): shutil.rmtree(OUT)
shutil.copytree(SITE,OUT)
news=json.loads((ROOT/'news.json').read_text()); resources=json.loads((ROOT/'resources.json').read_text())
nav=[('Home',''),('News','news/'),('Methodologies','methodologies/'),('Tools','tools/'),('Learn','learn/'),('Research','research/'),('Prompts','prompts/'),('Developers','developers/')]
def page(title,body,path='',desc='Explore artificial intelligence with TechieHacker.',hero=False):
 p=OUT/path/'index.html';p.parent.mkdir(parents=True,exist_ok=True); r='../'*len(path.strip('/').split('/')) if path else './'; links=''.join(f'<a href="{r}{u}">{n}</a>' for n,u in nav)
 p.write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} | TechieHacker</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="https://www.techiehacker.com/{path}"><link rel="stylesheet" href="{r}style.css"><link rel="icon" href="{r}logo.svg" type="image/svg+xml"></head><body><header><a class="brand" href="{r}"><img src="{r}logo.svg" alt="">TECHIE<span>HACKER</span></a><nav>{links}</nav><button id="theme" aria-label="Toggle theme">◐</button></header><main>{body}</main><footer><b>TECHIEHACKER</b> · Explore. Learn. Innovate.<p>Independent AI knowledge hub · AI-assisted news is labeled · Always consult original sources.</p><a href="{r}news/">News archive</a> · <a href="{r}learn/">Learning resources</a></footer><script src="{r}app.js" defer></script></body></html>''')
def card(x,href=None):
 link=href or x.get('url',''); return f'<article class="tile"><div class="tag">{E(x.get("category","AI"))}</div><h3>{E(x["title"])}</h3><p>{E(x.get("summary", ""))}</p>'+ (f'<a href="{E(link)}">Explore →</a>' if link else '')+'</article>'
def section(title,sub,items):return f'<section><div class="eyebrow">KNOWLEDGE / {E(title.upper())}</div><h1>{E(title)}</h1><p class="lead">{E(sub)}</p><label class="search">Filter resources <input id="filter" type="search" placeholder="Search topics, names, concepts"></label><div class="grid" id="cards">'+''.join(items)+'</div></section>'
news_cards=[card(n,'../news/'+n['id']+'/') for n in news]
empty='<div class="empty">The automated newsroom is ready. New stories appear after the first successful publishing run. Explore the learning library in the meantime.</div>'
hero='''<section class="hero"><canvas id="neural" aria-hidden="true"></canvas><div class="hero-copy"><div class="eyebrow"><i></i> THE INTELLIGENCE FRONTIER</div><h1>Beyond the<br>ordinary.<br><em>Build with AI.</em></h1><p>Explore breakthroughs, master AI engineering and discover the tools shaping tomorrow.</p><div class="buttons"><a class="primary" href="learn/">Start learning ↗</a><a class="secondary" href="news/">Explore the newsroom →</a></div></div><div class="hud">NEURAL FIELD / 01<br>GENERATIVE VISUAL SYSTEM<br><span>● LIVE RENDER</span></div></section><div class="ticker">LLMs <b>✳</b> AGENTIC AI <b>✳</b> RAG <b>✳</b> MULTIMODAL <b>✳</b> MCP <b>✳</b> AI ENGINEERING</div>'''
page('AI intelligence hub',hero+'<section><div class="eyebrow">01 / THE NEWSROOM</div><h2>Intelligence, in motion.</h2><p class="lead">Source-linked news with original AI-assisted headlines and summaries.</p><div class="grid">'+(''.join(card(n,'news/'+n['id']+'/') for n in news[:6]) or empty)+'</div><a href="news/">All news →</a></section><section><div class="eyebrow">02 / EXPLORE</div><h2>Engineer the future.</h2><div class="grid">'+''.join(card({'title':t,'category':'EXPLORE','summary':d},p+'/') for t,p,d in [('AI methodologies','methodologies','Understand the architectures behind modern intelligence.'),('AI tools','tools','Discover practical tools for work and creativity.'),('Learning academy','learn','Follow a structured path from basics to advanced AI.'),('Research radar','research','Find primary research and open models.'),('Prompt studio','prompts','Reusable templates for reliable outcomes.'),('Developer hub','developers','Frameworks, APIs and engineering resources.')])+'</div></section>',hero=True)
page('AI News',section('AI News','Source-linked editorial briefs. AI-generated analysis is not independent reporting.',news_cards or [empty]),'news/')
for n in news:
 body=f'<section class="article"><div class="eyebrow">{E(n["category"])} / AI-ASSISTED NEWS</div><h1>{E(n["title"])}</h1><p class="meta">{E(n["date"])} · {E(n["source"])}</p><h2>What happened</h2><p>{E(n["summary"])}</p><h2>Why it matters</h2><p>{E(n["impact"])}</p><p><a href="{E(n["url"])}" rel="noopener noreferrer">Read original source ↗</a></p><p class="meta">Generated from source feed excerpts; verify details in the original publication.</p></section>'
 page(n['title'],body,'news/'+n['id']+'/',n['summary'])
for k,items in resources.items():
 cards=[]
 for i,x in enumerate(items):
  if k in ('methodologies','prompts'):
   slug=x['slug'];cards.append(card(x,slug+'/')); detail=f'<section class="article"><div class="eyebrow">{E(x["category"])}</div><h1>{E(x["title"])}</h1><p class="lead">{E(x["summary"])}</p>'+''.join(f'<h2>{E(a)}</h2><p>{E(b)}</p>' for a,b in x['details'])+f'<p><a href="{E(x["url"])}">Further reading ↗</a></p></section>';page(x['title'],detail,k+'/'+slug+'/')
  else:cards.append(card(x))
 page(k.title(),section(k.title(),'Curated resources for the AI practitioner.',cards),k+'/')
(OUT/'CNAME').write_text('www.techiehacker.com\n');(OUT/'.nojekyll').touch()
urls=['https://www.techiehacker.com/'+str(p.relative_to(OUT).parent).replace('.','',1).strip('/')+('/' if p.parent!=OUT else '') for p in OUT.rglob('index.html')];(OUT/'sitemap.xml').write_text('<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+E(u)+'</loc></url>' for u in urls)+'</urlset>');(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://www.techiehacker.com/sitemap.xml\n')
print('Built',len(list(OUT.rglob('index.html'))),'pages')
