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
pubs=''.join('<article class="publication" data-kind="'+('preprint' if re.search(r'under review|arxiv|biorxiv',p,re.I) else 'published')+'"><div>'+rich(p)+'</div></article>' for i,p in enumerate(d['publications']))
news=''.join('<li'+(' hidden class="older-news"' if i>3 else '')+'>'+rich(n)+'</li>' for i,n in enumerate(d['news']))
projects=rich(d['projects'])
projects=re.sub(r'<h2[^>]*>(.*?)</h2>',r'</div><div class="project"><h3>\1</h3>',projects)
projects='<div>'+projects+'</div>'
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>@@NAME@@ · Biophysics</title><meta name="description" content="@@INTRO@@"><link rel="icon" href="assets/favicon.svg"><link rel="stylesheet" href="home.css"></head><body>
<a class="skip" href="#about">Skip to content</a>
<div class="page">
<aside class="profile"><img class="portrait" src="assets/ZhuJinProfile.png" alt="Jin Zhu" width="200" height="200">
<h1>@@NAME@@ <span lang="zh">@@CHINESE@@</span></h1>
<p>@@ROLE@@<br>@@INSTITUTION@@</p>
<div class="links"><a href="mailto:@@EMAIL@@">Email</a><a href="assets/ZhuJin_CV_US.pdf">CV</a><a href="@@SCHOLAR@@">Google Scholar</a><a href="@@ORCID@@">ORCID</a></div>
<nav aria-label="Sections"><a href="#about">About</a><a href="#publications">Publications</a><a href="#news">News</a><a href="#experience">Experience</a></nav>
</aside>
<main>
<section id="about"><h2>About</h2><p>@@ABOUT@@</p><p>@@BACKGROUND@@</p></section>
<section id="publications"><h2>Publications</h2><p class="note"><sup>*</sup> Equal contribution.</p><div id="paper-list">@@PUBLICATIONS@@</div></section>
<section id="news"><h2>News</h2><ul class="news">@@NEWS@@</ul><button id="more-news" aria-expanded="false">Show earlier updates +</button></section>
<section id="experience"><h2>Experience</h2>
<details><summary>Education</summary>@@EDUCATION@@</details>
<details><summary>Research experience</summary>@@EXPERIENCE@@</details>
<details><summary>Selected presentations</summary>@@PRESENTATIONS@@</details>
<details><summary>Earlier research and engineering projects</summary>@@PROJECTS@@</details>
<details><summary>Teaching</summary>@@TEACHING@@</details>
<details><summary>Honors and leadership</summary>@@HONORS@@</details>
<details><summary>Technical skills</summary>@@SKILLS@@</details>
</section>
<footer><a href="Gallary/">Gallery</a><a href="editor.html">Edit content</a></footer>
</main></div><script src="app.js"></script></body></html>'''
values={k.upper():esc(str(v)) for k,v in d.items() if isinstance(v,str)}
values.update(ABOUT=rich(d['about']),BACKGROUND=rich(d['background']),PROJECTS=projects,NEWS=news,PUBLICATIONS=pubs,TEACHING=rich(d['teaching']),CHINESE=esc(d['chineseName']))
for key in ['education','experience','honors','skills','presentations']:
 values[key.upper()]=rich(d.get(key,''))
for k,v in values.items():page=page.replace('@@'+k+'@@',v)
if '@@' in page:raise ValueError('Unresolved template value')
(DIST/'index.html').write_text(page)
(DIST/'content.json').write_text(json.dumps(d,ensure_ascii=False,indent=2))
print('Built homepage with',len(d['publications']),'publications and',len(d['news']),'updates.')
