import asyncio, pathlib
from playwright.async_api import async_playwright
from PIL import Image
D = pathlib.Path(__file__).parent
LOGO = (D.parent/"img"/"logo.png").resolve().as_uri()
ALI = (D.parent/"img"/"alireza-mirzahosseini.webp").resolve().as_uri()
Y = 1215
def th(d, w=7): return f'<svg width="1080" height="1350" style="position:absolute;inset:0;z-index:3"><path d="{d}" fill="none" stroke="#C9A84C" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def cov(body, d, dark=False, label=""):
    c = "#EFEBE1" if dark else "#151515"
    return f"""<!doctype html><html><head><link rel=stylesheet href="v2.css"></head><body><div class="s{' dark' if dark else ''}">
<div class=meta style="top:52px;left:64px;color:{c}">Azrim Studio — {label}</div>{body}{th(d)}
<div class=meta style="bottom:52px;left:64px;color:{c};opacity:.6">azrimstudio.com</div><img class=logo src="{LOGO}" style="bottom:44px;right:64px"></div></body></html>"""
covers = {}
# reel intro: Ali, thread becomes a signature underline
covers["intro"] = cov(f"""<img src="{ALI}" style="position:absolute;left:50%;transform:translateX(-50%);bottom:0;height:1100px;filter:grayscale(1) contrast(1.15) sepia(.2)">
<div class=serif style="position:absolute;top:130px;left:64px;font-size:118px;line-height:.92;z-index:2">18 years.<br><span class=it style="color:#C9A84C">One rule.</span></div>""",
 f"M-5 {Y} C 200 {Y}, 260 1120, 330 1150 C 390 1175, 380 1240, 450 1200 C 520 1160, 560 1110, 610 1170 C 650 1220, 700 1160, 760 1180 C 860 1210, 950 {Y}, 1085 {Y}", dark=True, label="Reel · Meet Ali")
# brand doctor: heartbeat
covers["doctor"] = cov("""<div class=an style="position:absolute;top:140px;left:64px;font-size:190px">Brand<br>doctor</div>
<div class=it style="position:absolute;top:520px;left:64px;font-size:72px">Patient: a shop sign<br>on Király utca</div>
<div class=stamp style="top:760px;left:560px;transform:rotate(6deg);font-size:58px">Critical</div>""",
 f"M-5 {Y} L 300 {Y} L 340 {Y-20} L 380 {Y+10} L 420 {Y-220} L 470 {Y+120} L 510 {Y-40} L 545 {Y} L 1085 {Y}", label="Reel · Brand Doctor")
# logo in 60s: thread draws a stopwatch
covers["logo60"] = cov("""<div class=an style="position:absolute;top:140px;left:64px;font-size:250px;line-height:.8">Logo<br>in 60s</div>
<div class=hw style="position:absolute;top:640px;left:100px;font-size:64px;transform:rotate(-4deg)">café edition</div>""",
 f"M-5 {Y} L 520 {Y} C 600 {Y}, 610 1100, 640 1040 A 190 190 0 1 1 641 1040 L 760 870 M 832 1015 L 832 960 C 900 {Y}, 980 {Y}, 1085 {Y}", label="Reel · Logo in 60 seconds")
# ali vs ai: thread splits in two
covers["vsai"] = cov("""<div class=an style="position:absolute;top:150px;left:64px;font-size:220px">Ali <span style="color:#D8432A">vs</span><br>A.I.</div>
<div class=it style="position:absolute;top:640px;left:64px;font-size:70px">One is human.<br>Guess which.</div>""",
 f"M-5 {Y} L 380 {Y} C 520 {Y}, 560 1080, 700 1080 C 820 1080, 860 {Y}, 1085 {Y} M 380 {Y} C 520 {Y}, 560 1290, 700 1290 C 820 1290, 860 {Y}, 1085 {Y}", dark=True, label="Reel · Ali vs AI")
# premium rebrand: ribbon bow
covers["premium"] = cov("""<div class=serif style="position:absolute;top:140px;left:64px;font-size:130px;line-height:.92">What if<br><span class=it>Túró Rudi</span><br>went luxury?</div>
<div class=pill style="position:absolute;top:640px;left:64px">Unofficial concept</div>""",
 f"M-5 {Y} L 420 {Y} C 480 {Y}, 470 1080, 540 1100 C 620 1120, 560 {Y}, 540 {Y} C 520 {Y}, 460 1120, 540 1100 C 610 1080, 600 {Y}, 660 {Y} L 1085 {Y}", label="Reel · Premium Rebrand")

async def main():
    out = D/"out"/"grid"; out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width":1080,"height":1350})
        for k,h in covers.items():
            f = D/f"_cov_{k}.html"; f.write_text(h)
            await pg.goto(f.as_uri()); await pg.wait_for_timeout(500)
            await pg.screenshot(path=str(out/f"{k}.png"))
        await b.close()
asyncio.run(main())
order = ["premium","vsai","logo60","doctor","intro", None]
tiles = [Image.open(D/"out"/"grid"/f"{k}.png") if k else Image.open(D/"out"/"c01v2"/"slide-1.png") for k in order]
# instagram profile grid: 3:4 tiles (crop sides of 4:5), 2px gaps
tw, thh = 360, 480; g = 3
sheet = Image.new("RGB", (tw*3+g*2, thh*2+g), "white")
for i,t in enumerate(tiles):
    cw = int(1350*3/4); x0 = (1080-cw)//2
    t = t.crop((x0,0,x0+cw,1350)).resize((tw,thh))
    sheet.paste(t, ((i%3)*(tw+g), (i//3)*(thh+g)))
sheet.save(D/"out"/"grid"/"feed.png")
