from pathlib import Path
import html,json,xml.etree.ElementTree as ET
E=lambda x:html.escape(str(x),quote=True)
# Labels reflect publisher descriptions, not independently measured stream resolution.
VIDEOS=[('29ECwExc-_M','All New Atlas | Boston Dynamics','Humanoid robotics','robotics','Source video'),('wQF61J0Yd54','NASA: Synthesis — Data Visualizations in Ultra-HD (4K)','Science in 4K','neural','4K labeled'),('4lSQnrMC6nY','Gemini Robotics 2 brings whole body intelligence to robots','Physical AI','infrastructure','Source video'),('d66Qv2WASqw','GOES18 — Earth Day 2026 · 4K','Earth in 4K','future','4K labeled'),('bY8RDKoBwU0','Seedance 4K Just Made AI Filmmaking Look Ultra Realistic!','AI filmmaking','code','4K topic')]
PAGES=[('cinema','AI Cinema','Original films and demonstrations from technology and research publishers.'),('attention','Attention Lab','Change query weights and temperature to see softmax attention in action.'),('retrieval','RAG Explorer','Search a small teaching corpus and inspect evidence ranking.'),('agents','Agent Control','Practice a bounded agent workflow with approval gates.'),('quiz','AI Challenge','Test your understanding of AI engineering with ten questions.')]
def render_experiences(root,out):
 root,out=Path(root),Path(out)
 base='https://www.techiehacker.com/'
 def page(slug,title,desc,body):
  path=out/'experience'/slug;path.mkdir(parents=True,exist_ok=True);r='../../' if slug else '../';
  (path/'index.html').write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} | TechieHacker</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{base}experience/{slug+"/" if slug else ""}"><link rel="stylesheet" href="{r}natural/theme.css"><link rel="stylesheet" href="{r}natural/experience.css"><script defer src="{r}natural/experience.js"></script></head><body><header class="nav"><a class="brand" href="{r}">TECHIE<span class="cyan">HACKER</span></a><a href="{r}experience/">Experience hub</a><a href="{r}news/">News</a></header><main class="experience"><div class="eyebrow">TECHIEHACKER / INTERACTIVE WORLDS</div><h1>{E(title)}</h1><p class="lead">{E(desc)}</p>{body}<p class="back"><a href="{r}experience/">← All experiences</a> · <a href="{r}">Home</a></p></main></body></html>''',encoding='utf-8')
 cards=''.join(f'<a class="xp-card" href="{slug}/"><h2>{E(t)}</h2><p>{E(d)}</p><span>Enter →</span></a>' for slug,t,d in PAGES)
 page('','AI Experience Universe','Watch, explore, experiment and learn. All simulations run locally in your browser.',f'<div class="xp-grid">{cards}</div>')
 cards=''.join(f'<article class="xp-card"><img src="../../cinematic/{v[3]}.webp" alt="Illustration for {E(v[2])}" loading="lazy"><h2>{E(v[1])}</h2><p>{E(v[4])} · Original publisher on YouTube</p><button data-film="{v[0]}" data-title="{E(v[1])}">Play video</button> <a href="https://www.youtube.com/watch?v={v[0]}" target="_blank" rel="noopener">YouTube ↗</a></article>' for v in VIDEOS)
 page('cinema',PAGES[0][1],PAGES[0][2],f'<p>Playback quality depends on the original upload, bandwidth and device. Select 2160p where offered. Videos load only after you choose one.</p><div class="cinema-screen" id="filmScreen"><p>Select a film below.</p></div><p id="filmTitle" aria-live="polite"></p><button id="filmStop">Close player</button><div class="xp-grid">{cards}</div>')
 page('attention',PAGES[1][1],PAGES[1][2],'''<div class="xp-panel" id="attention"><p>Illustrative query–key scores for four tokens. The softmax turns the scores into probabilities that sum to one.</p><label>Temperature <input id="temp" type="range" min="0.2" max="3" step="0.1" value="1"><output id="tempOut"></output></label><div id="weights"></div><div id="bars"></div><p id="attentionNote" aria-live="polite"></p><p>Formula: weight = exp(score / temperature) / sum(exp(scores / temperature)). Real transformers also apply learned projections, masks and value vectors.</p></div>''')
 page('retrieval',PAGES[2][1],PAGES[2][2],'''<div class="xp-panel"><label>Ask a question <input id="ragQuery" value="How do I prevent prompt injection?" type="search"></label><label>Top results <input id="ragK" type="range" min="1" max="5" value="3"><output id="ragKOut"></output></label><button id="ragRun">Retrieve evidence</button><div id="ragResults" aria-live="polite"></div><p>This is a deterministic keyword retriever, not a live LLM. It demonstrates how retrieval can ground a later generation step.</p></div>''')
 page('agents',PAGES[3][1],PAGES[3][2],'''<div class="xp-panel"><p>Scenario: prepare a support ticket using public documentation. Choose permitted actions and see what the controller allows.</p><div class="xp-actions"><button data-action="search">Search documentation</button><button data-action="draft">Draft ticket</button><button data-action="send">Send ticket</button><button data-action="approve">Approve send</button><button data-action="secret">Read private secret</button><button id="agentReset">Reset</button></div><p id="agentState" aria-live="polite"></p><ol id="agentLog"></ol><p>All actions are simulated. No external requests, real credentials or real tickets are used.</p></div>''')
 page('quiz',PAGES[4][1],PAGES[4][2],'''<div class="xp-panel"><p id="quizProgress"></p><h2 id="question"></h2><div id="answers" class="xp-actions"></div><p id="feedback" aria-live="polite"></p><button id="quizNext" disabled>Next question</button><button id="quizReset">Restart</button></div>''')
 # Append URLs to existing sitemap and search index without changing existing records.
 urls=[('', 'AI Experience Universe','Interactive AI cinema and learning simulations.')]+PAGES
 sitemap=out/'sitemap.xml'
 if sitemap.is_file():
  tree=ET.parse(sitemap);sr=tree.getroot();ns=sr.tag.split('}')[0]+'}' if '}' in sr.tag else '';existing={e.text for e in sr.iter(ns+'loc')}
  for slug,t,d in urls:
   u=base+'experience/'+(slug+'/' if slug else '')
   if u not in existing:ET.SubElement(ET.SubElement(sr,ns+'url'),ns+'loc').text=u
  if ns:ET.register_namespace('',ns[1:-1])
  tree.write(sitemap,encoding='utf-8',xml_declaration=True)
 idx=out/'search-index.json'
 if idx.is_file():
  records=json.loads(idx.read_text());existing={x.get('url') for x in records}
  for slug,t,d in urls:
   u='../experience/'+(slug+'/' if slug else '')
   if u not in existing:records.append(dict(title=t,summary=d,category='Interactive experiences',url=u))
  idx.write_text(json.dumps(records,ensure_ascii=False),encoding='utf-8')
