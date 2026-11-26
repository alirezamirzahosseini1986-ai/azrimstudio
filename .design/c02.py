"""Carousel 02 — 5 website mistakes costing you clients (€500 vs €5,000 series). 8 slides 1080x1350."""
import asyncio, pathlib
from playwright.async_api import async_playwright
D = pathlib.Path(__file__).parent
LOGO = pathlib.Path("/home/claude/azrimstudio/img/logo.png").as_uri()
ALI = pathlib.Path("/home/claude/azrimstudio/img/alireza-mirzahosseini.webp").as_uri()
N, RED, GOLD, Y = 8, "#D8432A", "#C9A84C", 1215

def thread(d=None, w=7):
    d = d or f"M-5 {Y} C 270 {Y-34}, 540 {Y+34}, 810 {Y} S 1085 {Y} 1085 {Y}"
    return f'<svg width="1080" height="1350" style="position:absolute;inset:0;pointer-events:none;z-index:3"><path d="{d}" fill="none" stroke="{GOLD}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def loop(w, h, col=RED, sw=6):
    return f'''<svg width="{w}" height="{h}" viewBox="0 0 200 100" preserveAspectRatio="none" style="overflow:visible;position:absolute;z-index:4"><path d="M18 52 C 14 18, 120 4, 176 26 C 204 38, 196 78, 140 90 C 84 102, 12 92, 10 58 C 8 40, 40 22, 92 16" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" vector-effect="non-scaling-stroke"/></svg>'''

def phone(inner, x, y, r=0, w=380, h=760, dark=False):
    bg = "#fbfaf6"
    return f'''<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:54px;background:#151515;padding:16px;transform:rotate({r}deg);box-shadow:0 40px 60px -24px rgba(0,0,0,.55)">
<div style="position:relative;width:100%;height:100%;border-radius:40px;overflow:hidden;background:{bg};font-family:IT;color:#151515">
<div style="position:absolute;top:12px;left:50%;margin-left:-55px;width:110px;height:30px;border-radius:20px;background:#151515"></div>
{inner}</div></div>'''

def page(i, body, dark=False, label="", th=None):
    c = "#EFEBE1" if dark else "#151515"
    return f"""<!doctype html><html><head><link rel=stylesheet href="v2.css"><style>
.num{{font-family:AN;font-size:200px;line-height:.8}}
.ttl{{font-family:IS;font-style:italic;font-size:72px;line-height:1}}
.why{{font-size:32px;line-height:1.32}}
.fix{{position:absolute;left:64px;width:560px;font-size:31px;line-height:1.3}}
.fix b{{font-family:RC;font-weight:700;font-size:22px;letter-spacing:.08em;display:inline-block;background:{GOLD};color:#151515;padding:6px 12px;margin-bottom:10px}}
.bar{{height:14px;border-radius:7px;background:#d9d4c8;margin:10px 0}}
</style></head><body>
<div class="s{' dark' if dark else ''}">
<div class=meta style="top:52px;left:64px;color:{c}">Azrim Studio — {label}</div>
<div class=meta style="top:52px;right:64px;color:{c};opacity:.6">{i:02d}/{N:02d}</div>
{body}
{thread(th)}
<div class=meta style="bottom:52px;left:64px;color:{c};opacity:.6">azrimstudio.com</div>
<img class=logo src="{LOGO}" style="bottom:44px;right:64px">
</div></body></html>"""

def mistake(i, n, title, why, fix, ph, dark, note, note_pos, loop_pos, label):
    lx, ly, lw, lh = loop_pos
    nx, ny, nr = note_pos
    return page(i, f"""
<div class=num style="position:absolute;top:140px;left:56px;color:{GOLD if dark else '#151515'}">{n}</div>
<div class=ttl style="position:absolute;top:330px;left:64px;width:530px">{title}</div>
<div class=why style="position:absolute;top:570px;left:64px;width:520px;color:{'#cfcac0' if dark else '#3a3833'}">{why}</div>
{ph}
<div style="left:{lx}px;top:{ly}px;position:absolute">{loop(lw, lh)}</div>
<div class=hw style="position:absolute;left:{nx}px;top:{ny}px;font-size:48px;color:{RED};transform:rotate({nr}deg);z-index:5;width:330px;line-height:1">{note}</div>
<div class=fix style="top:900px;color:{'#EFEBE1' if dark else '#151515'}"><b>THE FIX</b><br>{fix}</div>
""", dark=dark, label=label)

S = []
# 1 COVER — thread loops round the big 5
S.append(page(1, f"""
<div class=an style="position:absolute;top:150px;left:60px;font-size:800px;line-height:.82;color:#151515">5</div>
<div style="position:absolute;top:200px;left:560px;width:470px">
<div class=an style="font-size:118px;line-height:.9">website<br>mistakes</div>
<div class=it style="font-size:72px;line-height:1;margin-top:22px">that quietly cost you clients.</div></div>
<div class=hw style="position:absolute;top:880px;left:600px;font-size:52px;transform:rotate(-5deg);width:420px">café owners:<br>look at nº 3</div>
<div class=hw style="position:absolute;top:1100px;left:620px;font-size:46px;transform:rotate(-4deg)">swipe →</div>
""", label="Websites, explained",
 th=f"M-5 {Y} C 140 {Y}, 200 1080, 205 930 A 245 410 0 1 1 206 930 C 215 1100, 380 {Y}, 560 {Y} C 740 {Y-30}, 900 {Y+30}, 1085 {Y}"))

# 2 phone number hidden
ph2 = phone(f'''<div style="padding:70px 26px 0"><div style="display:flex;justify-content:space-between;align-items:center"><b style="font-size:30px">Bró Café</b><span style="font-size:34px">☰</span></div>
<div style="margin-top:26px;height:230px;background:#c9b79a;border-radius:16px"></div>
<div class=bar style="width:90%;margin-top:26px"></div><div class=bar style="width:70%"></div><div class=bar style="width:80%"></div>
<div style="margin-top:26px;height:120px;background:#e4ded2;border-radius:16px"></div>
<div class=bar style="width:60%;margin-top:22px"></div>
<div style="position:absolute;bottom:22px;left:26px;font-size:15px;color:#9a958a">Contact · Imprint · +36 1 234 5678</div></div>''', 620, 170, 4)
S.append(mistake(2, "01", "Your phone number is hiding.", "On a phone, people want to call or message you with one tap. If the number lives in the footer, most never reach it.",
 "A sticky call / WhatsApp button on mobile. Number in the header, tappable.", ph2, True,
 "buried in<br>the footer", (640, 980, -5), (628, 860, 380, 90), "Mistake 01"))

# 3 slow
ph3 = phone(f'''<div style="padding:70px 26px 0"><div style="height:520px;border-radius:16px;background:repeating-linear-gradient(45deg,#e4ded2 0 18px,#efebe1 18px 36px);display:flex;align-items:center;justify-content:center;flex-direction:column">
<div style="width:70px;height:70px;border-radius:50%;border:8px solid #cfc9bc;border-top-color:#151515"></div>
<div style="margin-top:24px;font-family:RC;font-size:20px;color:#6e6a60">hero-photo-FINAL2.png</div><div style="font-family:RC;font-size:20px;color:#6e6a60">8.4 MB</div></div>
<div style="height:12px;border-radius:6px;background:#e4ded2;margin-top:30px;overflow:hidden"><div style="width:14%;height:100%;background:#151515"></div></div></div>''', 640, 190, -4)
S.append(mistake(3, "02", "It loads like it's 2009.", "Huge photos straight from the camera make the first screen crawl on mobile data. Visitors don't wait — they go back to Google.",
 "Resize and compress every image. Test your homepage on PageSpeed Insights.", ph3, False,
 "still<br>loading…", (690, 990, -6), (650, 180, 380, 590), "Mistake 02"))

# 4 PDF menu
ph4 = phone(f'''<div style="padding:60px 0 0;background:#525659;height:100%"><div style="font-family:RC;font-size:16px;color:#ddd;padding:0 20px 10px">menu_2023_v4.pdf  ·  1 / 6</div>
<div style="margin:0 16px;background:#fff;height:540px;padding:24px 20px;font-size:11px;line-height:1.5;color:#555">
<div style="font-family:IS;font-size:30px;color:#222;text-align:center">MENU</div>
{''.join('<div style="display:flex;justify-content:space-between"><span>Espresso macchiato con latte…</span><span>1.290</span></div>' for _ in range(14))}</div></div>''', 640, 180, 3)
S.append(mistake(4, "03", "Your menu<br>is a PDF.", "Pinch, zoom, scroll sideways, wait for the download. On a phone a PDF menu is a small punishment — and it's often an old one.",
 "A simple menu page in HTML: readable text, real prices, updated in two minutes.", ph4, True,
 "pinch &amp; zoom", (650, 780, -4), (636, 300, 390, 480), "Mistake 03"))

# 5 no prices
ph5 = phone(f'''<div style="padding:70px 26px 0"><b style="font-size:30px">Our services</b>
{''.join(f'<div style="margin-top:22px;padding:20px;border:2px solid #e4ded2;border-radius:14px"><b style="font-size:22px">{t}</b><div class=bar style="width:85%"></div><div style="margin-top:8px;font-size:18px;color:#D8432A;font-weight:700">Price on request</div></div>' for t in ["Logo design","Website","Social media"])}</div>''', 640, 180, -3)
S.append(mistake(5, "04", "No prices. Not even a “from”.", "When there's no number at all, many people assume “too expensive” and ask your competitor instead.",
 "Show a starting price or 2–3 packages. “From €___” is enough to start the conversation.", ph5, False,
 "×3 “ask us”", (680, 1010, -5), (640, 520, 380, 420), "Mistake 04"))

# 6 Google profile mismatch
card = lambda t, l, h, a, x, y, r: f'''<div style="position:absolute;left:{x}px;top:{y}px;width:360px;background:#fbfaf6;color:#151515;padding:24px 26px;transform:rotate({r}deg);box-shadow:0 20px 36px -16px rgba(0,0,0,.6)">
<div class=meta style="position:static;color:#8b867b">{t}</div><div style="font-size:30px;font-weight:700;margin-top:10px">{l}</div>
<div style="font-size:24px;margin-top:8px">{h}</div><div style="font-size:24px;color:#6e6a60">{a}</div></div>'''
ph6 = card("Website", "Bró Café", "Mon–Sun 8:00–20:00", "Király u. 12", 640, 200, 3) + card("Google", "Bro Cafe &amp; Bistro", "Mon–Fri 7:00–18:00", "Király utca 12/b", 610, 470, -4)
S.append(mistake(6, "05", "Google and your site disagree.", "Different hours, a different name, an old address. Customers trust neither — and Google gets confused about which one is right.",
 "Same name, address, phone and hours everywhere: site, Google Business Profile, Instagram bio.", ph6, True,
 "which one<br>is true?", (720, 760, -4), (600, 420, 420, 110), "Mistake 05"))

# 7 checklist (save)
items = ["Tap-to-call button on mobile", "Photos compressed, page loads fast", "Menu as a web page, not a PDF", "A “from” price or packages", "Same details on Google &amp; site"]
rows = "".join(f'<div style="display:flex;align-items:center;gap:26px;margin-top:34px"><div style="width:58px;height:58px;border:4px solid #151515;flex:none"></div><span style="font-size:44px">{t}</span></div>' for t in items)
S.append(page(7, f"""
<div class=an style="position:absolute;top:140px;left:64px;font-size:150px;line-height:.9">The 5-minute<br>check</div>
<div style="position:absolute;top:470px;left:64px">{rows}</div>
<div class=hw style="position:absolute;top:1090px;left:560px;font-size:56px;color:{RED};transform:rotate(-5deg)">save this ↓</div>
""", label="Checklist"))

# 8 CTA
S.append(page(8, f"""
<img src="{ALI}" style="position:absolute;right:-60px;bottom:0;height:980px;filter:grayscale(1) contrast(1.2) brightness(.9) sepia(.25);-webkit-mask:linear-gradient(90deg,transparent 0,#000 30%),linear-gradient(transparent 0,#000 18%);-webkit-mask-composite:source-in">
<div style="position:absolute;top:170px;left:64px;width:640px">
<div class=serif style="font-size:112px;line-height:.95">Want me to<br>check <span class=it style="color:{GOLD}">yours?</span></div>
<div style="font-size:34px;line-height:1.35;margin-top:44px;color:#d8d3c8">Comment your website address. I'll reply with the one fix that matters most. Free.</div>
<div class=an style="font-size:120px;color:{GOLD};margin-top:36px">.com / .hu</div>
<div class=hw style="font-size:46px;margin-top:6px;transform:rotate(-3deg)">— Ali, founder</div>
<div style="font-size:24px;color:#8c877c;margin-top:36px;width:540px">Írd kommentbe a weboldalad címét — megmondom a legfontosabb javítást.</div></div>
""", dark=True, label="Free website check"))

async def main():
    out = D/"out"/"c02"; out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width":1080,"height":1350})
        for i, h in enumerate(S, 1):
            f = D/f"_c02_{i}.html"; f.write_text(h)
            await pg.goto(f.as_uri()); await pg.wait_for_timeout(500)
            await pg.screenshot(path=str(out/f"slide-{i}.png"))
        await b.close()
    from PIL import Image
    w, h = 540, 675; sh = Image.new('RGB', (w*4, h*2))
    for i in range(8): sh.paste(Image.open(out/f"slide-{i+1}.png").resize((w, h)), ((i%4)*w, (i//4)*h))
    sh.save(out/"contact.jpg", quality=85)
asyncio.run(main())
