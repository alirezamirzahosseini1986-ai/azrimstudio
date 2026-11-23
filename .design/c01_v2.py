import asyncio, pathlib
from playwright.async_api import async_playwright
D = pathlib.Path(__file__).parent
LOGO = pathlib.Path("/home/claude/azrimstudio/img/logo.png").as_uri()
ALI = pathlib.Path("/home/claude/azrimstudio/img/alireza-mirzahosseini.webp").as_uri()
N = 8
RED = "#D8432A"

def circle(w, h, sw=5, col=RED):
    # rough hand-drawn loop
    return f'''<svg width="{w}" height="{h}" viewBox="0 0 200 100" preserveAspectRatio="none" style="overflow:visible">
<path d="M18 52 C 14 18, 120 4, 176 26 C 204 38, 196 78, 140 90 C 84 102, 12 92, 10 58 C 8 40, 40 22, 92 16" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" vector-effect="non-scaling-stroke"/></svg>'''

def arrow(w, h, d="M5 10 C 60 0, 110 30, 140 80", col=RED):
    return f'''<svg width="{w}" height="{h}" viewBox="0 0 150 100" style="overflow:visible"><path d="{d}" fill="none" stroke="{col}" stroke-width="4" stroke-linecap="round"/><path d="M118 70 L141 82 L139 56" fill="none" stroke="{col}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>'''

def tick(col=RED):
    return f'<svg width="54" height="44" viewBox="0 0 54 44"><path d="M4 24 C 12 30, 16 36, 20 40 C 28 24, 38 12, 50 4" fill="none" stroke="{col}" stroke-width="5" stroke-linecap="round"/></svg>'
def cross(col="#9a958a"):
    return f'<svg width="40" height="40" viewBox="0 0 40 40"><path d="M6 8 L34 32 M33 7 L8 33" stroke="{col}" stroke-width="4" stroke-linecap="round"/></svg>'

Y=1215
def thread(d=None,w=7):
    d = d or f"M-5 {Y} C 270 {Y-34}, 540 {Y+34}, 810 {Y} S 1085 {Y} 1085 {Y}"
    return f'<svg width="1080" height="1350" style="position:absolute;inset:0;pointer-events:none;z-index:3"><path d="{d}" fill="none" stroke="#C9A84C" stroke-width="{w}" stroke-linecap="round"/></svg>'
def sig(txt, x, y=1215, size=210):
    return f"""<div class=sigw style="position:absolute;left:{x}px;top:0;font-family:Allura;font-size:{size}px;line-height:1;color:#C9A84C;white-space:nowrap;z-index:4"><span>{txt}</span><span class=bl style="display:inline-block;width:0;height:0"></span></div>
<script>document.querySelectorAll('.sigw').forEach(w=>{{const b=w.querySelector('.bl').getBoundingClientRect().top;w.style.top=({y}+14-b)+'px'}})</script>"""
def page(i, body, dark=False, label="", th=None):
    c = "#EFEBE1" if dark else "#151515"
    return f"""<!doctype html><html><head><link rel=stylesheet href="v2.css"></head><body>
<div class="s{' dark' if dark else ''}">
<div class=meta style="top:52px;left:64px;color:{c}">Azrim Studio — {label}</div>
<div class=meta style="top:52px;right:64px;color:{c};opacity:.6">{i:02d}/{N:02d}</div>
{body}
{thread(th)}
<div class=meta style="bottom:52px;left:64px;color:{c};opacity:.6">azrimstudio.com</div>
<img class=logo src="{LOGO}" style="bottom:44px;right:64px">
</div></body></html>"""

S = []
# 1 COVER
S.append(page(1, f"""
<div class=an style="position:absolute;top:120px;left:52px;font-size:430px;color:#151515">€500</div>
<div class=it style="position:absolute;top:470px;left:70px;font-size:90px;color:#151515">versus</div>
<div class=an style="position:absolute;top:600px;left:48px;font-size:345px;color:transparent;-webkit-text-stroke:4px #151515;white-space:nowrap">€5,000</div>
<div class=hw style="position:absolute;top:470px;left:640px;font-size:60px;transform:rotate(-6deg)">what's in<br>this extra 0?</div>
<div style="position:absolute;top:955px;left:64px;width:640px">
<div class=serif style="font-size:58px;line-height:1.02">Why one brand costs €500<br>and another <span class=it>€5,000.</span></div>
</div>
<div class=hw style="position:absolute;top:1120px;left:90px;font-size:46px;transform:rotate(-5deg)">swipe →</div>
{sig("Az", 395, size=175)}
""", label="Branding, explained", th=f"M-5 {Y} L 640 {Y} C 760 {Y}, 765 1010, 765 745 A 125 175 0 1 1 1015 745 A 125 175 0 0 1 890 920 C 880 1080, 960 {Y}, 1085 {Y}"))
# 2 €500 receipt
S.append(page(2, f"""
<div class=it style="position:absolute;top:130px;left:64px;font-size:84px;line-height:1">What <span style="color:#C9A84C">€500</span> buys you</div>
<div class=rc style="top:290px;left:250px;width:560px;transform:rotate(-3deg)">
<div class=c style="font-weight:700;font-size:30px">LOGO SHOP</div><div class=c>quick &amp; cheap</div><hr>
<div class=row><span>Logo ideas ×3</span><span>✓</span></div>
<div class=row><span>Final logo ×1</span><span>✓</span></div>
<div class=row><span>File formats ×4</span><span>✓</span></div>
<div class=row><span>Research</span><span>0.00</span></div>
<div class=row><span>Strategy</span><span>0.00</span></div>
<div class=row><span>Usage rules</span><span>0.00</span></div><hr>
<div class="row tot"><span>TOTAL</span><span>€500</span></div>
<div class=c style="margin-top:14px;font-size:20px">*** thank you ***</div></div>
<div class=tape style="top:270px;left:430px;transform:rotate(-7deg)"></div>
<div class=hw style="position:absolute;top:990px;left:90px;font-size:80px;transform:rotate(-8deg)">that's it.</div>
<div style="position:absolute;top:870px;left:150px;transform:rotate(-20deg)">{arrow(140,100,"M5 90 C 30 40, 80 20, 140 20")}</div>
<div style="position:absolute;top:1160px;left:64px;font-size:30px;color:#cfcac0;max-width:700px">Fine for testing an idea. Not for a real business.</div>
""", dark=True, label="What €500 buys"))
# 3 €5000 receipt
items = ["Market research","Competitor audit","Audience profile","Positioning","Brand voice","Logo suite ×6","Colour system","Type system","Image style","Brand guidelines","Social templates","Print templates"]
rows = "".join(f'<div class=row><span>{x}</span><span>✓</span></div>' for x in items)
S.append(page(3, f"""
<div class=it style="position:absolute;top:130px;left:64px;font-size:84px;line-height:1">What <span style="color:#C9A84C">€5,000</span> buys you</div>
<div class=rc style="top:270px;left:300px;width:560px;transform:rotate(2deg);font-size:25px;line-height:1.5">
<div class=c style="font-weight:700;font-size:30px">BRAND STUDIO</div><div class=c>built to last</div><hr>{rows}<hr>
<div class="row tot"><span>TOTAL</span><span>€5,000</span></div></div>
<div class=tape style="top:250px;left:480px;transform:rotate(4deg)"></div>
<div class=hw style="position:absolute;top:640px;left:52px;font-size:58px;transform:rotate(-9deg);width:240px">the part<br>nobody<br>sees</div>
<div style="position:absolute;top:500px;left:160px;transform:rotate(-10deg)">{arrow(150,100,"M5 80 C 50 70, 90 40, 140 10")}</div>
""", dark=True, label="What €5,000 buys"))
# 4 spec sheet
spec = [("Logo files",1,1),("Market research",0,1),("Positioning",0,1),("Colour &amp; type system",0,1),("Brand guidelines",0,1),("Templates",0,1),("Looks the same everywhere",0,1)]
tr = "".join(f'<tr><td>{a}</td><td>{tick("#151515") if b else cross()}</td><td>{tick() if c else cross()}</td></tr>' for a,b,c in spec)
S.append(page(4, f"""
<style>table{{width:952px;border-collapse:collapse;font-size:36px}}td{{padding:20px 0;border-bottom:2px solid #151515}}td:nth-child(2),td:nth-child(3){{text-align:center;width:200px}}th{{text-align:center;padding-bottom:18px;border-bottom:6px solid #151515}}</style>
<div style="position:absolute;top:150px;left:64px">
<div class=an style="font-size:150px">Side by side</div>
<table style="margin-top:56px"><tr><th></th><th class=an style="font-size:64px">€500</th><th class=an style="font-size:64px">€5K</th></tr>{tr}</table></div>
<div class=hw style="position:absolute;top:1130px;left:560px;font-size:56px;transform:rotate(-4deg)">7 vs 1. Do the maths.</div>
""", label="The difference"))
# 5 inconsistent logos
scraps = [
 ("Menu", "font-family:IS;font-style:italic;font-size:76px;color:#7a3b1d", -6, 150, 300, "#fff8ea"),
 ("Cup", "font-family:AN;font-size:74px;color:#1b5e57", 5, 600, 290, "#f4efe4"),
 ("Instagram", "font-family:HW;font-size:92px;color:#c0397b", 4, 140, 650, "#fdfdfb"),
 ("Van", "font-family:IT;font-weight:800;font-size:66px;color:#2244aa;transform:scaleX(1.6);display:inline-block", -4, 590, 640, "#f7f7f2"),
]
sc = ""
for lab, st, r, x, y, bg in scraps:
    sc += f'''<div style="position:absolute;left:{x}px;top:{y}px;width:340px;height:250px;background:{bg};transform:rotate({r}deg);box-shadow:0 14px 30px -12px rgba(0,0,0,.4);display:flex;align-items:center;justify-content:center;flex-direction:column">
<span style="{st}">Bró Café</span><span class=meta style="position:static;margin-top:18px;color:#8b867b">on the {lab.lower()}</span></div>
<div class=tape style="left:{x+70}px;top:{y-24}px;transform:rotate({r*2}deg);width:170px;height:46px"></div>'''
S.append(page(5, f"""
<div class=it style="position:absolute;top:120px;left:64px;font-size:80px;line-height:1">Same café. <span style="color:#151515">Four</span> different brands.</div>
{sc}
<div class=stamp style="top:930px;left:300px;transform:rotate(-7deg)">No system</div>
<div style="position:absolute;top:1080px;left:64px;width:900px;font-size:34px;line-height:1.3">A cheap logo with no rules gets used a new way every time. Customers stop recognising you.</div>
""", label="The hidden cost"))
# 6 index cards
qs = ["What research do you do before sketching?","Do I get guidelines, or just files?","How many revision rounds are included?","Who owns the final files and rights?"]
cards = ""
pos = [(64,330,-3),(560,300,2.5),(80,760,2),(570,740,-2.5)]
for k,(q,(x,y,r)) in enumerate(zip(qs,pos),1):
    cards += f'''<div style="position:absolute;left:{x}px;top:{y}px;width:440px;height:360px;background:#fbfaf5;transform:rotate({r}deg);box-shadow:0 18px 34px -16px rgba(0,0,0,.45);padding:34px 36px;background-image:repeating-linear-gradient(#fbfaf5 0 58px,#cfe0ea 58px 60px);background-position:0 92px">
<div style="height:3px;background:{RED};opacity:.6;margin:52px -36px 0"></div>
<div class=an style="position:absolute;top:24px;left:36px;font-size:58px">0{k}</div>
<div style="font-family:HW;font-weight:600;font-size:50px;line-height:60px;margin-top:6px;color:#1f2a55">{q}</div></div>'''
S.append(page(6, f"""
<div class=an style="position:absolute;top:130px;left:64px;font-size:118px">Ask <span style="color:{RED}">any</span> designer</div>
{cards}
""", label="Before you hire"))
# 7 stamps
S.append(page(7, f"""
<div class=it style="position:absolute;top:130px;left:64px;font-size:96px;line-height:1">Which one do <span style="color:#A8862F">you</span> need?</div>
<div class=stamp style="top:330px;left:64px;transform:rotate(-4deg);font-size:96px">Test</div>
<div style="position:absolute;top:350px;left:420px;width:600px;font-size:36px;line-height:1.3"><b>Testing an idea?</b><br>A good logo is enough.</div>
<div class=stamp style="top:600px;left:64px;transform:rotate(3deg);font-size:96px;color:#151515;border-color:#151515">Grow</div>
<div style="position:absolute;top:620px;left:420px;width:600px;font-size:36px;line-height:1.3"><b>Real customers, real shop?</b><br>You need a system.</div>
<div class=stamp style="top:870px;left:64px;transform:rotate(-2deg);font-size:96px;color:#A8862F;border-color:#A8862F">Scale</div>
<div style="position:absolute;top:890px;left:420px;width:600px;font-size:36px;line-height:1.3"><b>Second location or export?</b><br>The system is not optional.</div>
<div style="position:absolute;top:1140px;left:64px;font-size:22px;color:#6E6A60">Example prices. Every project is quoted individually.</div>
""", label="Pick yours"))
# 8 CTA with Ali
S.append(page(8, f"""
<img src="{ALI}" style="position:absolute;right:-60px;bottom:0;height:980px;filter:grayscale(1) contrast(1.2) brightness(.9) sepia(.25);-webkit-mask:linear-gradient(90deg,transparent 0,#000 30%),linear-gradient(transparent 0,#000 18%);-webkit-mask-composite:source-in">
<div style="position:absolute;top:170px;left:64px;width:620px">
<div class=serif style="font-size:120px;line-height:.95">Not sure<br>which one<br>you <span class=it style="color:#C9A84C">need?</span></div>
<div style="font-size:34px;line-height:1.35;margin-top:44px;color:#d8d3c8">Comment the word below. I'll look at your brand and tell you, free, in 10 minutes.</div>
<div class=an style="font-size:170px;color:#C9A84C;margin-top:40px">BRAND</div>
<div class=hw style="font-size:46px;margin-top:6px;transform:rotate(-3deg)">— Ali, founder</div>
<div style="font-size:24px;color:#8c877c;margin-top:40px;width:520px">Írd kommentbe: BRAND — ingyenes 10 perces márka-ellenőrzés.</div></div>
""", dark=True, label="Free brand check"))

async def main():
    out = D/"out"/"c01v2"; out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width":1080,"height":1350})
        for i,h in enumerate(S,1):
            f = D/f"_v2_{i}.html"; f.write_text(h)
            await pg.goto(f.as_uri()); await pg.wait_for_timeout(500)
            await pg.screenshot(path=str(out/f"slide-{i}.png"))
        await b.close()
asyncio.run(main())
from PIL import Image
w,h=540,675; sh=Image.new('RGB',(w*4,h*2))
for i in range(8): sh.paste(Image.open(out/f"slide-{i+1}.png").resize((w,h)),((i%4)*w,(i//4)*h)) if (out:=D/"out"/"c01v2") else None
sh.save(D/"out"/"c01v2"/"contact.png")
