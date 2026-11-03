#!/usr/bin/env python3
"""Build the service landing pages (EN + HU) from pages/services.json.

Run from the repo root: python3 tools/build_pages.py  (build_blog.py calls it too).
"""
import html, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_blog import head, FOOT, FOOT_HU, SITE, ROOT  # noqa: E402

PAGE_CSS = '''<style>
.kicker{font-size:13px;letter-spacing:2px;color:var(--gold);text-transform:uppercase}
.lead{font-size:21px;color:#fff;line-height:1.6;margin:0 0 8px}
article ul{padding-left:20px;margin:0 0 18px}article li{margin-bottom:8px}
.faq details{border-top:1px solid var(--bd);padding:14px 0}.faq details:last-child{border-bottom:1px solid var(--bd)}
.faq summary{cursor:pointer;color:#fff;font-weight:600;list-style-position:outside}
.faq p{margin:10px 0 0;color:var(--tm)}
.related{display:flex;gap:12px;flex-wrap:wrap;margin-top:40px;font-size:15px}
.related a{border:1px solid var(--bd);padding:10px 14px;text-decoration:none}.related a:hover{border-color:var(--gold)}
.btn2{display:inline-block;margin:14px 0 0 10px;padding:11px 20px;border:1px solid var(--gold);text-decoration:none;font-weight:700;letter-spacing:1px;font-size:14px}
</style>'''

LABELS = {
    'en': {'faq': 'Questions', 'contact': 'Contact form', 'wa': 'WhatsApp us', 'more': 'Other services', 'home': '/', 'blog': 'Read the blog',
           'cta_text': 'Tell us what you need — we’ll get back to you as soon as we can.', 'other': ('Magyarul', 'hu')},
    'hu': {'faq': 'Gyakori kérdések', 'contact': 'Kapcsolati űrlap', 'wa': 'Írj WhatsAppon', 'more': 'További szolgáltatások', 'home': '/hu/', 'blog': 'Blog',
           'cta_text': 'Írd meg, mire van szükséged – hamarosan jelentkezünk.', 'other': ('English', 'en')},
}


def page(item, lang, all_items):
    d = item[lang]
    o = item['hu' if lang == 'en' else 'en']
    L = LABELS[lang]
    url = SITE + d['path']
    en_url, hu_url = SITE + item['en']['path'], SITE + item['hu']['path']
    ld = [
        {"@context": "https://schema.org", "@type": "Service", "name": d['title'], "description": d['desc'], "url": url,
         "inLanguage": lang, "areaServed": {"@type": "City", "name": "Budapest"},
         "provider": {"@type": "MarketingAgency", "@id": f"{SITE}/#agency", "name": "Azrim Studio", "url": f"{SITE}/"}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d['faq']]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Azrim Studio", "item": SITE + L['home']},
            {"@type": "ListItem", "position": 2, "name": d['title'], "item": url}]},
    ]
    extra = PAGE_CSS + '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False, separators=(',', ':')) + '</script>'
    faq = ''.join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in d['faq'])
    related = ''.join(f'<a href="{x[lang]["path"]}">{html.escape(x[lang]["title"])}</a>' for x in all_items if x is not item)
    contact = L['home'] + '#contact'
    body = f'''<main>
<div class="kicker"><a href="{L['home']}" style="text-decoration:none">Azrim Studio</a> · {html.escape(d['kicker'])}</div>
<h1>{html.escape(d['title'])}</h1>
<div class="meta"><a href="{o['path']}" hreflang="{L['other'][1]}">{L['other'][0]}</a></div>
<p class="lead" style="margin-top:24px">{html.escape(d['lead'])}</p>
<article>
{d['body']}
<h2>{L['faq']}</h2>
<div class="faq">{faq}</div>
</article>
<div class="cta"><b>{html.escape(d['cta'])}</b>{L['cta_text']}<br><a class="btn" href="https://wa.me/36705738870">{L['wa']}</a><a class="btn2" href="{contact}">{L['contact']}</a></div>
<div class="related"><span style="color:var(--tm);align-self:center">{L['more']}:</span>{related}<a href="/blog/">{L['blog']}</a></div>
</main>
'''
    return head(d['title'], d['desc'], url, lang, [('en', en_url), ('hu', hu_url), ('x-default', en_url)], f'{SITE}/og.jpg', extra, og_type='website') + body + (FOOT_HU if lang == 'hu' else FOOT)


def load():
    p = os.path.join(ROOT, 'pages', 'services.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else []


def urls():
    """(en_url, hu_url) pairs for the sitemap."""
    return [(SITE + i['en']['path'], SITE + i['hu']['path']) for i in load()]


def main():
    items = load()
    for it in items:
        for lang in ('en', 'hu'):
            d = os.path.join(ROOT, it[lang]['path'].strip('/'))
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(page(it, lang, items))
    print(f'built {len(items)} service page pair(s)')


if __name__ == '__main__':
    main()
