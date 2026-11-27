"""V2.1 static editorial pages, integrated with the existing generator."""
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(name, default):
    p=ROOT/name
    return json.loads(p.read_text()) if p.exists() else default

def render(page, E, card, news, index):
    data=load('editorial.json',{}); feeds=load('feeds.json',{}); health=load('newsroom-status.json',{}); counts=Counter(n['source'] for n in news)
    def link(url,label): return f'<a href="{E(url)}" rel="noopener noreferrer">{E(label)} ↗</a>'
    def metric(n,label): return f'<div class="metric"><strong>{E(n)}</strong><span>{E(label)}</span></div>'
    def options(values): return ''.join(f'<option value="{E(v)}">{E(v)}</option>' for v in sorted(set(values)))
    def sources_rows():
        states=health.get('feeds',{})
        return ''.join(f'<tr><td>{link(url,name)}</td><td>{E(states.get(name,{}).get("status","Not checked"))}</td><td>{E(states.get(name,{}).get("entries","—"))}</td><td>{counts[name]}</td></tr>' for name,url in feeds.items())
    news_items=''.join(f'<div class="news-entry" data-source="{E(n["source"])}" data-category="{E(n["category"])}">{card(n,"../news/"+n["id"]+"/")}</div>' for n in news)
    metrics=metric(len(feeds),'Configured feeds')+metric(len(news),'Published articles')+metric(len(counts),'Published sources')+metric('08:00 IST','Scheduled daily')
    topic_counts=Counter(n['category'] for n in news[:30]); topics=' · '.join(f'{E(k)} ({v})' for k,v in topic_counts.most_common(6)) or 'No published topics yet.'
    page('Global AI Newsroom',f'''<section class="edition"><div class="eyebrow">01 / GLOBAL AI NEWSROOM</div><h1>Intelligence without borders.</h1><p class="lead">Source-linked, AI-assisted reporting briefs. Follow the companies, researchers and technologies building the future.</p><div class="metrics">{metrics}</div><p class="meta">Last recorded collection: {E(health.get('checked_at','Not recorded yet'))} · Last run published: {E(health.get('published','—'))} · Feed checks reflect the last recorded run, not real-time uptime.</p><div class="editorial-note"><b>Recent archive topics</b><p>{topics}</p><small>Frequency in the latest 30 archived briefs, not an internet-wide trend ranking.</small></div></section><section class="compact"><h2>Latest dispatches</h2><div class="news-controls"><label>Search <input type="search" id="newsQuery" placeholder="Search news"></label><label>Source <select id="newsSource"><option value="">All sources</option>{options(counts)}</select></label><label>Topic <select id="newsCategory"><option value="">All topics</option>{options(n['category'] for n in news)}</select></label></div><p id="newsCount" aria-live="polite">{len(news)} articles</p><div class="grid" id="newsGrid">{news_items}</div></section><section class="compact"><h2>Source directory & collection health</h2><p class="lead">Configured RSS endpoints. A successful fetch does not guarantee a usable or recent story.</p><div class="table-scroll"><table><thead><tr><th>Source / feed</th><th>Last fetch</th><th>Entries</th><th>Published</th></tr></thead><tbody>{sources_rows()}</tbody></table></div></section>''','news/','Explore daily source-linked AI news and collection health.')
    tracks=data.get('tracks',[]); guides=data.get('guides',[])
    trackcards=[]
    for t in tracks:
        slug=t['slug']; trackcards.append(card(dict(t,category=t['level']),slug+'/'))
        modules=''.join(f'<li><strong>{E(m[0])}</strong><p>{E(m[1])}</p></li>' for m in t['modules'])
        refs=''.join(f'<li>{link(u,n)}</li>' for n,u in t['references'])
        lessons=''.join(f'<li>{link("../../insights/"+g["slug"]+"/",g["title"])}</li>' for g in guides if g['slug'] in t['guides'])
        body=f'''<section class="article"><div class="eyebrow">ACADEMY / {E(t['level'])}</div><h1>{E(t['title'])}</h1><p class="lead">{E(t['summary'])}</p><div class="editorial-note"><b>Prerequisites</b><p>{E(t['prerequisites'])}</p><b>Suggested study time</b><p>{E(t['duration'])}</p></div><h2>Study sequence</h2><ol class="lesson-list">{modules}</ol><h2>Portfolio project</h2><p>{E(t['project'])}</p><h2>How to assess your progress</h2><p>{E(t['assessment'])}</p><h2>TechieHacker reading</h2><ul>{lessons}</ul><h2>Primary learning resources</h2><ul>{refs}</ul><a href="../">← All learning paths</a></section>'''
        page(t['title'],body,'academy/'+slug+'/',t['summary']);index.append(dict(title=t['title'],summary=t['summary']+' '+' '.join(' '.join(m) for m in t['modules']),category='Learning path',url='../academy/'+slug+'/'))
    page('AI University',f'<section class="edition"><div class="eyebrow">02 / AI UNIVERSITY</div><h1>Learn it. Build it. Master it.</h1><p class="lead">Structured, self-paced learning paths with practical projects, reading and measurable outcomes. Suggested study times are estimates; no accreditation is implied.</p><div class="metrics">{metric(len(tracks),"Learning paths")}{metric(sum(len(t["modules"]) for t in tracks),"Study modules")}{metric(len(guides),"Original guides")}</div><a href="../library/">Explore the expanded AI resource library →</a> · <a href="../learn/">Existing courses →</a><div class="grid">{"".join(trackcards)}</div></section>','academy/')
    guidecards=[]
    for g in guides:
        slug=g['slug']; guidecards.append(card(g,slug+'/'))
        sections=''.join(f'<h2>{E(s[0])}</h2>'+''.join(f'<p>{E(p)}</p>' for p in s[1]) for s in g['sections'])
        refs=''.join(f'<li>{link(u,n)}</li>' for n,u in g['references']); code=f'<h2>Hands-on example</h2><p>{E(g.get("code_note","Illustrative example; test in a local environment."))}</p><pre><code>{E(g["code"])}</code></pre>' if g.get('code') else ''
        quiz=''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q,a in g['quiz'])
        body=f'''<section class="article longread"><div class="eyebrow">TECHIEHACKER INSIGHTS / {E(g['category'])}</div><h1>{E(g['title'])}</h1><p class="lead">{E(g['summary'])}</p><p class="meta">Original AI-assisted educational editorial · {E(g['level'])} · Review before production use</p><div class="editorial-note"><strong>What you will learn</strong><ul>{''.join('<li>'+E(o)+'</li>' for o in g['outcomes'])}</ul></div>{sections}{code}<h2>Practice & self-check</h2><p>{E(g['exercise'])}</p>{quiz}<h2>Further reading</h2><ul>{refs}</ul><a href="../">← All insights</a></section>'''
        page(g['title'],body,'insights/'+slug+'/',g['summary']);index.append(dict(title=g['title'],summary=g['summary']+' '+' '.join(h+' '+' '.join(p) for h,p in g['sections']),category=g['category'],url='../insights/'+slug+'/'))
    page('TechieHacker Insights',f'<section class="edition"><div class="eyebrow">03 / ORIGINAL EDITORIAL</div><h1>Beyond the headline.</h1><p class="lead">Technical deep dives, practical architecture, implementation pitfalls and self-check exercises.</p><label class="search">Filter guides <input id="filter" type="search" placeholder="Search guides"></label><div id="cards" class="grid">{"".join(guidecards)}</div></section>','insights/')

    library=data.get('library',[])
    groups=sorted({x['category'] for x in library})
    libcards=''.join(card(x) for x in library)
    for x in library:index.append(dict(title=x['title'],summary=x['summary'],category=x['category'],url=x['url']))
    page('AI Resource Library',f'<section class="edition"><div class="eyebrow">04 / CURATED DIRECTORY</div><h1>Knowledge, organized.</h1><p class="lead">Primary documentation, courses and research links. Access, pricing and course availability may change; this is a curated starting point, not an exhaustive index.</p><div class="metrics">{metric(len(library),"Curated links")}{metric(len(groups),"Subject areas")}</div><label class="search">Filter by subject or provider <input id="filter" type="search" placeholder="Try security, RAG or PyTorch"></label><div id="cards" class="grid">{libcards}</div></section>','library/')
