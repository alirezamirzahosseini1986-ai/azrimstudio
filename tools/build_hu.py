#!/usr/bin/env python3
"""Generate the server-rendered Hungarian homepage /hu/index.html from index.html.

The English homepage switches language with JavaScript, so search engines only
ever see English. This script applies every data-hu translation the same way
setLang('hu') does, fixes relative URLs, and writes Hungarian head tags.
Run from the repo root: python3 tools/build_hu.py  (build_blog.py calls it too).
"""
import os, re
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://azrimstudio.com'

HU_TITLE = 'Azrim Studio | Arculat, social media és weboldal Budapesten'
HU_DESC = 'Kreatív marketingstúdió Budapesten: arculat- és logótervezés, közösségimédia-kezelés és weboldal-készítés kis- és középvállalkozásoknak.'
HTML_TAGS = {'div', 'h1', 'h2', 'h3', 'p', 'span', 'button', 'a'}


def absolutize(v):
    if not v or re.match(r'^(https?:|//|/|#|mailto:|tel:|data:|javascript:)', v):
        return v
    return '/' + v


def main():
    src = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    soup = BeautifulSoup(src, 'html.parser')
    for el in soup.select('[data-hu]'):
        v = el['data-hu']
        el.clear()
        if el.name in HTML_TAGS:
            frag = BeautifulSoup(v, 'html.parser')
            for c in list(frag.contents):
                el.append(c)
        else:
            el.string = v
    html = soup.find('html')
    html['lang'] = 'hu'
    html['dir'] = 'ltr'
    head = soup.head
    head.title.string = HU_TITLE
    for sel, attr, val in [('meta[name=description]', 'content', HU_DESC),
                           ('meta[property="og:title"]', 'content', HU_TITLE),
                           ('meta[property="og:description"]', 'content', HU_DESC),
                           ('meta[property="og:url"]', 'content', f'{SITE}/hu/'),
                           ('meta[property="og:locale"]', 'content', 'hu_HU'),
                           ('link[rel=canonical]', 'href', f'{SITE}/hu/')]:
        t = head.select_one(sel)
        if t is not None:
            t[attr] = val
    for t in soup.find_all(['img', 'script', 'source', 'video', 'link', 'a']):
        for attr in ('src', 'href', 'poster'):
            if t.has_attr(attr):
                t[attr] = absolutize(t[attr])
    # link to Hungarian versions of service pages and blog articles
    import json
    sp = os.path.join(ROOT, 'pages', 'services.json')
    m = {i['en']['path']: i['hu']['path'] for i in json.load(open(sp, encoding='utf-8'))} if os.path.exists(sp) else {}
    for t in soup.find_all('a', href=True):
        hr = t['href']
        if hr in m:
            t['href'] = m[hr]
        elif re.match(r'^/blog/[^/]+/$', hr):
            t['href'] = hr + 'hu/'
        elif hr in ('/#contact', '/#portfolio', '/#services'):
            t['href'] = '/hu/' + hr[1:]
    # anchors to homepage sections stay on the Hungarian page
    for b in soup.select('.lb-btn'):
        cls = [c for c in b.get('class', []) if c != 'on']
        if "setLang('hu')" in (b.get('onclick') or ''):
            cls.append('on')
        b['class'] = cls
    out_dir = os.path.join(ROOT, 'hu')
    os.makedirs(out_dir, exist_ok=True)
    open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8').write(str(soup))
    print('built hu/index.html')


if __name__ == '__main__':
    main()
