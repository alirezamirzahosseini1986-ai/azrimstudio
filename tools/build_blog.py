#!/usr/bin/env python3
"""Build the Azrim Studio blog from blog/posts/*.json.

Each JSON post has: slug, date (YYYY-MM-DD), category_en, category_hu, read_min,
title_en, desc_en, body_en (HTML), title_hu, desc_hu, body_hu (HTML).

Run from the repo root:  python3 tools/build_blog.py
It writes blog/<slug>/index.html (EN), blog/<slug>/hu/index.html (HU),
blog/<slug>/cover.jpg (if missing), blog/index.html, the homepage blog cards
between <!-- BLOG:START --> and <!-- BLOG:END -->, the Blog JSON-LD, and sitemap.xml.
"""
import glob, html, json, os, re, sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://azrimstudio.com'
GA = '''<script async src="https://www.googletagmanager.com/gtag/js?id=G-X6B1VZHJMV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-X6B1VZHJMV');</script>'''
MONTHS_EN = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
MONTHS_HU = ['január', 'február', 'március', 'április', 'május', 'június', 'július', 'augusztus', 'szeptember', 'október', 'november', 'december']

CSS = '''
:root{--gold:#C9A84C;--gl:#E8C97A;--bg:#07070A;--bd:rgba(201,168,76,.15);--t:rgba(255,255,255,.88);--tm:rgba(255,255,255,.6)}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--t);font-family:'Segoe UI',system-ui,-apple-system,sans-serif;line-height:1.75;font-size:18px}
a{color:var(--gold)}a:hover{color:var(--gl)}
.top{display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap;max-width:1100px;margin:0 auto;padding:24px 20px;border-bottom:1px solid var(--bd)}
.brand{display:flex;align-items:center;gap:12px;color:var(--t);text-decoration:none;font-weight:700;letter-spacing:3px;font-size:14px}
.mark{width:30px;height:30px;border:2px solid var(--gold);transform:rotate(45deg);display:inline-flex;align-items:center;justify-content:center}
.mark span{transform:rotate(-45deg);color:var(--gold);font-family:Georgia,serif;font-weight:700}
.nav{display:flex;gap:18px;font-size:14px;letter-spacing:1px;flex-wrap:wrap}.nav a{text-decoration:none}
main{max-width:760px;margin:0 auto;padding:48px 20px 80px}
.crumb{font-size:13px;letter-spacing:2px;color:var(--tm);text-transform:uppercase}.crumb a{text-decoration:none}
h1{font-family:Georgia,'Times New Roman',serif;font-weight:400;font-size:clamp(34px,6vw,54px);line-height:1.1;margin:18px 0 18px;color:#fff}
.meta{font-size:14px;color:var(--tm);letter-spacing:1px;display:flex;gap:14px;flex-wrap:wrap}
.cover{width:100%;height:auto;display:block;margin:32px 0;border:1px solid var(--bd)}
article h2{font-family:Georgia,serif;font-weight:400;font-size:30px;color:#fff;margin:44px 0 12px;line-height:1.25}
article p{margin:0 0 18px}article strong{color:#fff}
.cta{margin:48px 0 0;padding:28px;border:1px solid var(--gold);background:rgba(201,168,76,.05)}
.cta b{display:block;font-family:Georgia,serif;font-weight:400;font-size:24px;color:#fff;margin-bottom:8px}
.btn{display:inline-block;margin-top:14px;padding:12px 22px;background:var(--gold);color:#07070A;text-decoration:none;font-weight:700;letter-spacing:1px;font-size:14px}
.btn:hover{background:var(--gl);color:#07070A}
.list{display:grid;gap:20px;margin-top:32px}
.card{display:block;border:1px solid var(--bd);text-decoration:none;color:inherit;overflow:hidden}
.card:hover{border-color:var(--gold)}
.card img{width:100%;height:auto;display:block}
.card div{padding:20px}.card h2{margin:6px 0 8px;font-size:24px}.card p{margin:0;color:var(--tm);font-size:16px}
footer{border-top:1px solid var(--bd);text-align:center;padding:28px 20px;font-size:13px;color:var(--tm)}
'''


def head(title, desc, url, lang, alternates, image, extra=''):
    alt = ''.join(f'<link rel="alternate" hreflang="{l}" href="{u}">' for l, u in alternates)
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} | Azrim Studio</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
{alt}
<meta property="og:type" content="article">
<meta property="og:site_name" content="Azrim Studio">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{image}">
<link rel="icon" href="/og.jpg">
{GA}
{extra}
<style>{CSS}</style>
</head>
<body>
<header class="top"><a class="brand" href="/"><span class="mark"><span>A</span></span>AZRIM STUDIO</a>
<nav class="nav"><a href="/#services">Services</a><a href="/#portfolio">Work</a><a href="/blog/">Blog</a><a href="/#contact">Contact</a></nav></header>
'''


FOOT = '<footer>© 2026 Azrim Studio · Budapest · <a href="/">azrimstudio.com</a> · <a href="https://www.instagram.com/azrimstudio_bp">Instagram</a></footer>\n</body>\n</html>\n'


def fmt_date(d, lang):
    y, m, dd = map(int, d.split('-'))
    return f'{y}. {MONTHS_HU[m-1]} {dd}.' if lang == 'hu' else f'{dd} {MONTHS_EN[m-1].title()} {y}'


def post_page(p, lang):
    slug = p['slug']
    en_url = f'{SITE}/blog/{slug}/'
    hu_url = f'{SITE}/blog/{slug}/hu/'
    url = hu_url if lang == 'hu' else en_url
    t, d, body, cat = (p['title_hu'], p['desc_hu'], p['body_hu'], p['category_hu']) if lang == 'hu' else (p['title_en'], p['desc_en'], p['body_en'], p['category_en'])
    img = f'{SITE}/blog/{slug}/cover.jpg'
    ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": t, "description": d, "datePublished": p['date'],
          "inLanguage": lang, "image": img, "mainEntityOfPage": url,
          "author": {"@type": "Person", "name": "Alireza Mirzahosseini"},
          "publisher": {"@type": "Organization", "name": "Azrim Studio", "url": SITE}}
    extra = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
    other = ('English', en_url) if lang == 'hu' else ('Magyarul', hu_url)
    cta = ('<div class="cta"><b>Szeretnél egy külső szemet a márkádra?</b>Írj nekünk – megmondjuk, mit látunk elsőként.<br><a class="btn" href="https://wa.me/36705738870">Írj WhatsAppon</a></div>'
           if lang == 'hu' else
           '<div class="cta"><b>Want a second pair of eyes on your brand?</b>Send us a message — we’ll tell you what we notice first.<br><a class="btn" href="https://wa.me/36705738870">Message us on WhatsApp</a></div>')
    crumb = 'Blog' if lang == 'en' else 'Blog'
    return (head(t, d, url, lang, [('en', en_url), ('hu', hu_url), ('x-default', en_url)], img, extra) +
            f'''<main>
<div class="crumb"><a href="/blog/">{crumb}</a> · {html.escape(cat)}</div>
<h1>{html.escape(t)}</h1>
<div class="meta"><span>{fmt_date(p['date'], lang)}</span><span>{p['read_min']} {'perc olvasás' if lang == 'hu' else 'min read'}</span><span>Alireza Mirzahosseini</span><a href="{other[1]}" hreflang="{'en' if lang == 'hu' else 'hu'}">{other[0]}</a></div>
<img class="cover" src="/blog/{slug}/cover.jpg" alt="{html.escape(t)}" width="1200" height="630">
<article>
{body}
</article>
{cta}
</main>
''' + FOOT)


def list_page(posts):
    cards = ''.join(f'''<a class="card" href="/blog/{p['slug']}/"><img src="/blog/{p['slug']}/cover.jpg" alt="" width="1200" height="630" loading="lazy"><div><div class="crumb">{html.escape(p['category_en'])} · {fmt_date(p['date'], 'en')}</div><h2>{html.escape(p['title_en'])}</h2><p>{html.escape(p['desc_en'])}</p></div></a>''' for p in posts)
    return (head('Blog', 'Branding, design and social media advice for small businesses, from Azrim Studio in Budapest.', f'{SITE}/blog/', 'en', [('en', f'{SITE}/blog/')], f'{SITE}/og.jpg') +
            f'<main><div class="crumb">Azrim Studio</div><h1>Blog</h1><p style="color:var(--tm)">Practical branding, design and social media advice for small businesses. New article every week.</p><div class="list">{cards}</div></main>\n' + FOOT)


def cover(p, path):
    from playwright.sync_api import sync_playwright
    t = html.escape(p['title_en'])
    page = f'''<!doctype html><html><head><meta charset="utf-8"><style>body{{margin:0}}
.c{{width:1200px;height:630px;background:#1C1C1E;color:#F5F5F0;position:relative;overflow:hidden;padding:64px 80px;box-sizing:border-box;display:flex;flex-direction:column;justify-content:space-between;font-family:'DejaVu Sans',sans-serif}}
.r{{position:absolute;right:-200px;top:-200px;width:600px;height:600px;border:2px solid #C9A84C;border-radius:50%;opacity:.35}}
.k{{font-family:'DejaVu Sans Mono',monospace;letter-spacing:4px;font-size:18px;color:#C9A84C;text-align:right;position:relative}}
h1{{margin:0;font-family:'DejaVu Serif',Georgia,serif;font-weight:400;font-size:58px;line-height:1.12;max-width:980px;position:relative}}
.f{{display:flex;justify-content:space-between;font-size:20px;color:#CFCBC0}}</style></head><body><div class="c"><div class="r"></div>
<div class="k">AZRIM STUDIO · {html.escape(p['category_en'].upper())}</div><h1>{t}</h1><div class="f"><span>Blog · {fmt_date(p['date'], 'en')}</span><b style="color:#fff">azrimstudio.com/blog</b></div></div></body></html>'''
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={'width': 1200, 'height': 630})
        pg.set_content(page)
        pg.screenshot(path=path, type='jpeg', quality=88)
        b.close()


def homepage_cards(posts):
    out = []
    for i, p in enumerate(posts[:3]):
        y, m, _ = p['date'].split('-')
        dt = f'{MONTHS_EN[int(m)-1]} {y}'
        te, th = html.escape(p['title_en'], quote=True), html.escape(p['title_hu'], quote=True)
        de, dh = html.escape(p['desc_en'], quote=True), html.escape(p['desc_hu'], quote=True)
        out.append(f'''
      <a class="blog-card rv d{i+1}" href="/blog/{p['slug']}/">
        <div class="blog-img">
          <img src="/blog/{p['slug']}/cover.jpg" alt="{te}" loading="lazy">
          <span class="blog-cat">{html.escape(p['category_en'])}</span>
        </div>
        <div class="blog-body">
          <div class="blog-date">{dt}</div>
          <h3 class="blog-title" data-en="{te}" data-hu="{th}" data-fa="{te}" data-ar="{te}">{te}</h3>
          <p class="blog-excerpt" data-en="{de}" data-hu="{dh}" data-fa="{de}" data-ar="{de}">{de}</p>
          <span class="blog-read" data-en="READ MORE →" data-hu="TOVÁBB OLVASÁS →" data-fa="← ادامه مطلب" data-ar="← اقرأ المزيد">READ MORE →</span>
        </div>
      </a>''')
    out.append('''
      <a class="blog-card rv" href="/blog/" style="display:flex;align-items:center;justify-content:center;min-height:200px">
        <span class="blog-read" data-en="ALL ARTICLES →" data-hu="ÖSSZES CIKK →" data-fa="← همهٔ مقالات" data-ar="← جميع المقالات">ALL ARTICLES →</span>
      </a>''')
    return ''.join(out) + '\n'


def main():
    posts = []
    for f in glob.glob(os.path.join(ROOT, 'blog', 'posts', '*.json')):
        posts.append(json.load(open(f, encoding='utf-8')))
    posts.sort(key=lambda p: p['date'], reverse=True)
    for p in posts:
        d = os.path.join(ROOT, 'blog', p['slug'])
        os.makedirs(os.path.join(d, 'hu'), exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(post_page(p, 'en'))
        open(os.path.join(d, 'hu', 'index.html'), 'w', encoding='utf-8').write(post_page(p, 'hu'))
        cp = os.path.join(d, 'cover.jpg')
        if not os.path.exists(cp):
            cover(p, cp)
    open(os.path.join(ROOT, 'blog', 'index.html'), 'w', encoding='utf-8').write(list_page(posts))

    ip = os.path.join(ROOT, 'index.html')
    s = open(ip, encoding='utf-8').read()
    s, n = re.subn(r'(<!-- BLOG:START -->).*?(<!-- BLOG:END -->)', lambda m: m.group(1) + homepage_cards(posts) + '      ' + m.group(2), s, flags=re.S)
    if n != 1:
        sys.exit('BLOG markers not found in index.html')
    ld = {"@context": "https://schema.org", "@type": "Blog", "name": "Azrim Studio Blog", "url": f"{SITE}/blog/",
          "description": "Branding, design and social media advice for small businesses from Azrim Studio Budapest",
          "blogPost": [{"@type": "BlogPosting", "headline": p['title_en'], "datePublished": p['date'], "url": f"{SITE}/blog/{p['slug']}/",
                        "author": {"@type": "Person", "name": "Alireza Mirzahosseini"}} for p in posts[:10]]}
    s, n = re.subn(r'<script type="application/ld\+json">\{"@context": ?"https://schema.org", ?"@type": ?"Blog".*?</script>',
                   lambda m: '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False, separators=(',', ':')) + '</script>', s, flags=re.S)
    if n != 1:
        sys.exit('Blog JSON-LD not found in index.html')
    open(ip, 'w', encoding='utf-8').write(s)

    today = date.today().isoformat()
    urls = [f'''  <url>\n    <loc>{SITE}/</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>1.0</priority>\n  </url>''',
            f'''  <url>\n    <loc>{SITE}/blog/</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>''']
    for p in posts:
        en, hu = f'{SITE}/blog/{p["slug"]}/', f'{SITE}/blog/{p["slug"]}/hu/'
        alt = f'    <xhtml:link rel="alternate" hreflang="en" href="{en}"/>\n    <xhtml:link rel="alternate" hreflang="hu" href="{hu}"/>'
        for u in (en, hu):
            urls.append(f'  <url>\n    <loc>{u}</loc>\n    <lastmod>{p["date"]}</lastmod>\n    <priority>0.7</priority>\n{alt}\n  </url>')
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + '\n'.join(urls) + '\n</urlset>\n')
    print(f'built {len(posts)} post(s)')


if __name__ == '__main__':
    main()
