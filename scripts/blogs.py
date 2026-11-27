"""Static blog library and author profile. No runtime API or external scripts needed."""
from pathlib import Path
import json
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
AUTHOR='Satishwar Mallekedi'
BIO=("I’m Satishwar Mallekedi, a tech blogger and passionate AI enthusiast behind TechieHacker. "
     "Artificial intelligence fascinates me because it connects technology, creativity and the problems we face in everyday life. "
     "Here, I explore how AI works, what it can genuinely improve, where it falls short and how we can build with it responsibly. "
     "Whether you are starting from scratch or working on production systems, I want TechieHacker to be a place where curiosity turns into practical understanding.")
TAGLINE='Curiosity drives innovation. Critical thinking makes it meaningful.'
DISCLOSURE='AI-assisted editorial draft prepared for the named author’s review. Opinions are proposed editorial viewpoints, not independently reported personal experiences.'

def load():
    rows=json.loads((ROOT/'blogs.json').read_text())
    assert len(rows)>=200 and len({r['slug'] for r in rows})==len(rows)
    return rows

def portrait(r,E):
    return f'<img class="author-photo" src="{r}author/satishwar-480.webp" srcset="{r}author/satishwar-480.webp 480w, {r}author/satishwar-960.webp 960w" sizes="(max-width: 700px) 80vw, 320px" width="480" height="720" alt="Portrait of {E(AUTHOR)}" loading="lazy" decoding="async">'

def author_banner(r,E):
    return f'''<section class="author-feature"><div class="author-portrait">{portrait(r,E)}</div><div class="author-copy"><div class="eyebrow">THE VOICE BEHIND TECHIEHACKER</div><h2>Meet {E(AUTHOR)}.</h2><p class="author-role">Tech Blogger · AI Enthusiast · Technology Explorer</p><p>{E(BIO)}</p><blockquote>{E(TAGLINE)}</blockquote><div class="buttons"><a class="primary" href="{r}about/">Meet the author →</a><a class="secondary" href="{r}blogs/">Explore the blogs →</a></div></div></section>'''

def blogcard(a,r,E):
    url=r+'blogs/'+a['slug']+'/'
    return f'''<article class="tile blog-tile" data-topic="{E(a['category'])}"><div class="tag">{E(a['category'])}</div><h3><a href="{E(url)}">{E(a['title'])}</a></h3><p>{E(a['reflection'])}</p><div class="blog-byline">Author: {E(AUTHOR)} · Technical perspective</div><a href="{E(url)}">Read the article →</a></article>'''

def featured(E,rows):
    # Scroll through the complete collection, interleaved by topic for variety.
    groups={}
    for a in rows:groups.setdefault(a['category'],[]).append(a)
    order=[g[i] for i in range(max(map(len,groups.values()))) for g in groups.values() if i<len(g)]
    cards=''.join(blogcard(a,'./',E) for a in order)
    return f'''<section class="blog-feature"><div class="eyebrow">AUTHOR'S DESK / TECHIEHACKER EDITORIAL</div><h2>Ideas worth exploring.</h2><p class="lead">{len(rows)} technical perspectives across {len(groups)} fields. AI explained with curiosity, practical examples and a balanced look at its impact.</p><div class="blog-controls" aria-label="Featured blog controls"><button type="button" id="blogPrev" aria-label="Previous blog">← Previous</button><button type="button" id="blogNext" aria-label="Next blog">Next →</button><button type="button" id="blogPause" aria-pressed="false">Pause auto-scroll</button><a href="blogs/">View all {len(rows)} blogs →</a></div><div class="blog-rail" id="blogRail" tabindex="0" aria-label="Scrollable technical blogs">{cards}</div><p class="meta">Scroll, use the arrow controls, or pause automatic movement. All articles are available in the blog archive.</p></section>'''

def home(E):
    rows=load()
    return author_banner('./',E)+featured(E,rows)

def render(page,E,index):
    rows=load(); counts=Counter(a['category'] for a in rows)
    opts=''.join(f'<option value="{E(c)}">{E(c)} ({n})</option>' for c,n in counts.items())
    items=''.join(blogcard(a,'../',E) for a in rows)
    page('Technical blogs',f'''<section class="edition"><div class="eyebrow">TECHIEHACKER / THE AUTHOR'S DESK</div><h1>Beyond the AI hype.</h1><p class="lead">{len(rows)} original AI-assisted technical columns by {E(AUTHOR)}. Explore the engineering, opportunities and risks behind artificial intelligence.</p><div class="metrics"><div class="metric"><strong>{len(rows)}</strong><span>Technical blogs</span></div><div class="metric"><strong>{len(counts)}</strong><span>Subject areas</span></div><div class="metric"><strong>360°</strong><span>Balanced perspectives</span></div></div><p><a href="../about/">Meet the author →</a> · <a href="../insights/">Read the existing in-depth guides →</a></p><p class="meta">{E(DISCLOSURE)}</p><div class="news-controls"><label>Search blogs <input id="blogQuery" type="search" placeholder="Try RAG, medicine, robotics"></label><label>Subject <select id="blogTopic"><option value="">All subjects</option>{opts}</select></label></div><p id="blogCount" aria-live="polite">{len(rows)} articles</p><div class="grid" id="blogGrid">{items}</div></section>''','blogs/','Technical AI blogs by Satishwar Mallekedi, including practical examples and balanced technology perspectives.')
    page('About the author',f'''{author_banner('../',E)}<section class="article"><div class="eyebrow">EDITORIAL MISSION</div><h2>Explore. Learn. Innovate.</h2><p>I believe the most exciting questions in AI are not just about what models can do, but about how technology can make knowledge more accessible and help people solve real problems. I want to make AI understandable without losing the engineering detail that makes it interesting.</p><h2>What to expect from TechieHacker</h2><p>Technical explanations, balanced perspectives, practical experiments, curated learning resources and source-linked news. I care about both the promise of innovation and the trade-offs in deploying it responsibly.</p><h2>Editorial transparency</h2><p>Technical columns and news may be AI-assisted. The named author should review and approve editorial drafts before publication. Hypothetical examples are not claims about personal experiments, employment or verified outcomes. Follow primary sources and consult appropriate professionals for consequential decisions.</p><p><a href="../author/satishwar-8k.jpg">View the full-resolution portrait (5120 × 7680)</a> · Upscaled from the supplied photograph.</p><a href="../blogs/">Read all technical blogs →</a></section>''','about/','Meet Satishwar Mallekedi, tech blogger and AI enthusiast behind TechieHacker.')
    index.append(dict(title=AUTHOR+' — About the author',summary=BIO,category='Author',url='../about/'))
    index.append(dict(title='TechieHacker technical blogs',summary='200 technical perspectives across 20 AI and industry subjects',category='Blogs',url='../blogs/'))
    for i,a in enumerate(rows):
        title,slug=a['title'],a['slug'];cat=a['category'];ref,url=a['reference']; related=[b for b in rows if b['category']==cat and b['slug']!=slug][:3]
        rel=''.join(f'<li><a href="../{E(b["slug"])}/">{E(b["title"])}</a></li>' for b in related)
        prev=rows[i-1] if i else rows[-1];nxt=rows[(i+1)%len(rows)]
        deep=f'<h2>Engineering walkthrough</h2><p>{E(a["deep_dive"])}</p>' if a.get("deep_dive") else ""
        body=f'''<section class="article longread author-article"><div class="eyebrow">TECHIEHACKER BLOGS / {E(cat)}</div><h1>{E(title)}</h1><div class="article-author"><a href="../../about/"><img src="../../author/satishwar-480.webp" width="56" height="56" alt="" loading="lazy"></a><div><a href="../../about/">Author: {E(AUTHOR)}</a><p class="meta">Tech Blogger · AI Enthusiast · Technical perspective</p></div></div><p class="lead">{E(a['reflection'])}</p><h2>Behind the technology</h2><p>{E(a['technical'])}</p><div class="blog-impact"><div><h2>What excites me</h2><p>{E(a['benefit'])}</p></div><div><h2>Where we need caution</h2><p>{E(a['risk'])}</p></div></div>{deep}<h2>Put the idea to the test</h2><p>{E(a['practice'])}</p><h2>Keep learning</h2><p><a href="{E(url)}" rel="noopener noreferrer">{E(ref)} ↗</a> · Further reading for this subject area; not a claim that the source endorses this editorial.</p><p class="meta">{E(DISCLOSURE)}</p><h2>Related perspectives</h2><ul>{rel}</ul><div class="blog-controls"><a href="../{E(prev['slug'])}/">← Previous article</a><a href="../">All blogs</a><a href="../{E(nxt['slug'])}/">Next article →</a></div></section>'''
        page(title,body,'blogs/'+slug+'/',a['reflection'])
        index.append(dict(title=title,summary=' '.join(a[k] for k in ('reflection','technical','benefit','risk','practice'))+' '+a.get('deep_dive','')+' Author: '+AUTHOR,category=cat,url='../blogs/'+slug+'/'))
