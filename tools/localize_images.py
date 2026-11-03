#!/usr/bin/env python3
"""Download portfolio images hosted on Google Drive, save them as WebP in img/p/,
and point index.html at the local copies. Images that fail to download keep
their Drive URL, so nothing breaks. Run from the repo root."""
import io, os, re, sys, urllib.request
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'img', 'p')
os.makedirs(OUT, exist_ok=True)
p = os.path.join(ROOT, 'index.html')
s = open(p, encoding='utf-8').read()

pat = re.compile(r'https://drive\.google\.com/thumbnail\?id=([A-Za-z0-9_-]+)&(?:amp;)?sz=w(\d+)|https://lh3\.googleusercontent\.com/d/([A-Za-z0-9_-]+)(?:=[^"\')\s]*)?')
ids = {}
for m in pat.finditer(s):
    i = m.group(1) or m.group(3)
    w = int(m.group(2)) if m.group(2) else 1600
    ids[i] = max(ids.get(i, 0), w)

ok, bad = 0, []
for i, w in ids.items():
    dest = os.path.join(OUT, i + '.webp')
    if not os.path.exists(dest):
        target = 1600 if w > 400 else 400
        try:
            req = urllib.request.Request(f'https://drive.google.com/thumbnail?id={i}&sz=w{target}', headers={'User-Agent': 'Mozilla/5.0'})
            data = urllib.request.urlopen(req, timeout=60).read()
            im = Image.open(io.BytesIO(data))
            im = im.convert('RGBA') if im.mode in ('P', 'LA', 'RGBA') else im.convert('RGB')
            im.thumbnail((target, target * 2))
            im.save(dest, 'WEBP', quality=80, method=6)
        except Exception as e:
            bad.append((i, str(e)[:80]))
            continue
    ok += 1

def repl(m):
    i = m.group(1) or m.group(3)
    return f'/img/p/{i}.webp' if os.path.exists(os.path.join(OUT, i + '.webp')) else m.group(0)

s = pat.sub(repl, s)
s = s.replace('  <link rel="preconnect" href="https://drive.google.com">\n', '').replace('  <link rel="dns-prefetch" href="https://drive.google.com">\n', '')
open(p, 'w', encoding='utf-8').write(s)
print(f'localized {ok}/{len(ids)} images; failed: {bad}')
