from pathlib import Path
import json,re,html
ROOT=Path(__file__).parent
DIST=ROOT/'dist'
DIST.mkdir(exist_ok=True)
if not (ROOT/'content.json').exists():
 s=(ROOT/'original.html').read_text()
 body=s.split('<section class="page__content" itemprop="text">')[1].split('</section>')[0]
 def section(start,end):return body.split(start,1)[1].split(end,1)[0]
 pubs=section('<h1 id="publications">Publications</h1>','<hr')
 news=section('<h1 id="news">News</h1>','<hr')
 teaching=section('<h1 id="teaching">Teaching</h1>','<hr')
 projects=section('<h1 id="projects-before-my-phd">Projects before my PhD</h1>','<hr')
 data={'name':'Jin Zhu','chineseName':'朱晋','role':'PhD student · Quantitative Biosciences','institution':'Georgia Institute of Technology','email':'zhujin@gatech.edu','intro':'I study the physics of microbial life — how bacteria move, interact, and build communities.', 'about':'I am a PhD student in Quantitative Biosciences (Physics) at Georgia Tech, advised by <a href="https://physics.gatech.edu/user/peter-yunker">Prof. Peter Yunker</a> in the <a href="https://yunkerlab.gatech.edu/">Yunker Lab</a>. My research focuses on the biophysics of biofilms.', 'background':'I received my bachelor’s and master’s degrees in mechanical engineering from the UM–SJTU Joint Institute, Shanghai Jiao Tong University, where I worked with <a href="https://sites.gc.sjtu.edu.cn/qulab/">Dr. Zijie Qu</a> in the Bio-inspired Fluid Mechanics Lab.', 'scholar':'https://scholar.google.com/citations?user=gW6_WPgAAAAJ&hl=en','orcid':'https://orcid.org/0009-0008-2086-9551','news':re.findall(r'<li>(.*?)</li>',news,re.S),'publications':re.findall(r'<li><p>(.*?)</p></li>',pubs,re.S),'teaching':teaching,'projects':projects}
 (ROOT/'content.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
d=json.loads((ROOT/'content.json').read_text())
def esc(t):return html.escape(t,quote=True)
# Rich content comes only from the owner's content file. Reject active content and unsafe URLs.
def rich(s):
 if re.search(r'<\s*(script|iframe|object|embed|style)|\son\w+\s*=|(?:javascript|data):',s,re.I):raise ValueError('Unsafe markup in content')
 s=s.replace('/images//','assets/').replace('/images/','assets/')
 return s
pubs=''.join('<article class="publication" data-kind="'+('preprint' if 'Under Review' in p else 'published')+'"><span class="paper-number">'+str(i+1).zfill(2)+'</span><div>'+rich(p)+'</div></article>' for i,p in enumerate(d['publications']))
news=''.join('<li'+(' hidden class="older-news"' if i>3 else '')+'>'+rich(n)+'</li>' for i,n in enumerate(d['news']))
projects=rich(d['projects'])
projects=re.sub(r'<h2[^>]*>(.*?)</h2>',r'</div><div class="project"><h3>\1</h3>',projects)
projects='<div>'+projects+'</div>'
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>@@NAME@@ · Biophysics</title><meta name="description" content="@@INTRO@@"><link rel="icon" href="assets/favicon.svg"><link rel="stylesheet" href="style.css"></head><body>
<a class="skip" href="#main">Skip to content</a>
<header><a class="wordmark" href="#">JZ<span> / </span>@@CHINESE@@</a><nav aria-label="Main navigation"><a href="#about">About</a><a href="#research">Research</a><a href="#publications">Publications</a><a href="#life">Beyond research</a><a class="nav-contact" href="mailto:@@EMAIL@@">Get in touch ↗</a></nav></header>
<main id="main"><section class="hero"><div class="hero-copy"><p class="eyebrow"><span class="dot"></span> BIOPHYSICS · GEORGIA TECH</p><h1>@@NAME@@ <span>@@CHINESE@@</span></h1><p class="hero-statement">@@INTRO@@</p><p class="role">@@ROLE@@<br>@@INSTITUTION@@ · Atlanta, GA</p><div class="hero-links"><a class="button" href="#publications">Explore my work <span>↘</span></a><a class="text-link" href="assets/ZhuJin_Resume.pdf">Curriculum vitae ↗</a></div></div><figure class="portrait"><img src="assets/ZhuJinProfile.png" alt="Portrait of Jin Zhu"><figcaption><span>朱晋 / Jin Zhu</span><span>Atlanta, GA ↗</span></figcaption></figure><div class="hero-bottom"><span>MICROBIAL LIFE, THROUGH A PHYSICIST’S LENS.</span><a href="#about">SCROLL TO EXPLORE ↓</a></div></section>
<section id="about" class="split-section"><div class="section-label"><span>01 / ABOUT</span><h2>Small organisms.<br>Big questions.</h2></div><div class="about-copy"><p>@@ABOUT@@</p><p>@@BACKGROUND@@</p><div class="academic-links"><a href="@@SCHOLAR@@">Google Scholar ↗</a><a href="@@ORCID@@">ORCID ↗</a><a href="mailto:@@EMAIL@@">Email ↗</a></div></div></section>
<section id="research" class="research-section"><div class="section-heading"><div><p class="eyebrow">02 / RESEARCH</p><h2>The physics of living systems</h2></div><p>From individual motion<br>to collective behavior.</p></div><div class="research-grid"><article><span class="research-index">I</span><div class="microbe-art" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div><h3>Biofilm formation</h3><p>Understanding the physical processes behind microbial communities.</p></article><article><span class="research-index">II</span><div class="wave-art" aria-hidden="true">∿<span>∿</span>∿</div><h3>Microorganism locomotion</h3><p>Exploring swimming, swarming, flagellar propulsion, and hydrodynamic interactions.</p></article><article><span class="research-index">III</span><div class="rings-art" aria-hidden="true"><i></i><i></i><i></i></div><h3>Antibiotic resistance</h3><p>A research interest at the intersection of microbial life and its physical environment.</p></article></div><details class="projects"><summary>Earlier research & engineering projects <span>+</span></summary>@@PROJECTS@@</details></section>
<section id="publications" class="publications-section"><div class="section-heading"><div><p class="eyebrow">03 / PUBLICATIONS</p><h2>Selected work</h2></div><a class="text-link" href="@@SCHOLAR@@">Google Scholar ↗</a></div><div class="filters" role="group" aria-label="Filter publications"><button class="active" data-filter="all" aria-pressed="true">All work</button><button data-filter="published" aria-pressed="false">Published</button><button data-filter="preprint" aria-pressed="false">Preprints</button></div><div id="paper-list">@@PUBLICATIONS@@</div></section>
<section class="split-section news-section"><div class="section-label"><span>04 / NEWS</span><h2>Along the way</h2><p>Research updates & milestones.</p></div><div><ul class="news-list">@@NEWS@@</ul><button id="more-news" class="text-button" aria-expanded="false">Show earlier updates +</button></div></section>
<section class="split-section teaching-section"><div class="section-label"><span>05 / TEACHING</span><h2>Learning, shared.</h2></div><div class="teaching">@@TEACHING@@</div></section>
<section id="life" class="life-section"><p class="eyebrow">06 / BEYOND RESEARCH</p><h2>A little outside the lab.</h2><p>Moments and photographs from along the way.</p><a class="text-link" href="https://zhujin2002.github.io/Gallary/">Visit my photo gallery ↗</a></section>
<section class="contact"><p class="eyebrow">LET’S CONNECT</p><h2>Curious about<br>the microscopic world?</h2><a href="mailto:@@EMAIL@@">@@EMAIL@@ ↗</a></section></main><footer><a class="wordmark" href="#">JZ / @@CHINESE@@</a><span>© <span id="year"></span> @@NAME@@</span><a href="editor.html">Edit content ↗</a><a href="#">Back to top ↑</a></footer><script src="app.js"></script></body></html>'''
values={k.upper():esc(str(v)) for k,v in d.items() if isinstance(v,str)}
values.update(ABOUT=rich(d['about']),BACKGROUND=rich(d['background']),PROJECTS=projects,NEWS=news,PUBLICATIONS=pubs,TEACHING=rich(d['teaching']),CHINESE=esc(d['chineseName']))
for k,v in values.items():page=page.replace('@@'+k+'@@',v)
if '@@' in page:raise ValueError('Unresolved template value')
(DIST/'index.html').write_text(page)
(DIST/'content.json').write_text(json.dumps(d,ensure_ascii=False,indent=2))
print('Built homepage with',len(d['publications']),'publications and',len(d['news']),'updates.')
