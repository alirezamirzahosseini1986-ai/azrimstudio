import asyncio, pathlib
from playwright.async_api import async_playwright
D = pathlib.Path(__file__).parent
LOGO = pathlib.Path("../img/logo.png").as_uri()
FPS, SEC = 24, 3.5
N = int(FPS*SEC)
Y = 1640
PATH = f"M-5 {Y} C 200 {Y}, 260 {Y-110}, 340 {Y-70} C 420 {Y-30}, 380 {Y+40}, 460 {Y-10} C 540 {Y-60}, 590 {Y-110}, 640 {Y-40} C 680 {Y+20}, 740 {Y-30}, 800 {Y-10} C 900 {Y+20}, 960 {Y}, 1085 {Y}"
HTML = f"""<!doctype html><html><head><link rel=stylesheet href="v2.css"><style>
html,body{{width:1080px;height:1920px;background:#0d0d0d}}
.c{{position:relative;width:1080px;height:1920px;overflow:hidden;color:#EFEBE1;font-family:IT}}
.l{{position:absolute;left:90px;opacity:0;transform:translateY(30px)}}
</style></head><body><div class=c>
<div class="l serif" id=a style="top:560px;font-size:170px;line-height:.9">30 days.</div>
<div class="l it" id=b style="top:740px;font-size:150px;line-height:.95;color:#C9A84C">30 brand<br>fixes.</div>
<div class="l" id=c style="top:1080px;font-size:44px;line-height:1.3;color:#cfc9bd">One every day,<br>starting tomorrow.</div>
<div class="l meta" id=d style="top:1260px;font-size:30px;color:#C9A84C;position:absolute">Follow @azrimstudio_bp</div>
<div class="l" id=e style="top:1320px;font-size:28px;color:#8c877c">30 nap, 30 márkajavítás. Holnaptól.</div>
<svg width=1080 height=1920 style="position:absolute;inset:0"><path id=p d="{PATH}" fill=none stroke="#C9A84C" stroke-width=8 stroke-linecap=round/></svg>
<img src="{LOGO}" style="position:absolute;bottom:90px;right:90px;width:70px">
</div><script>
const p=document.getElementById('p');const L=p.getTotalLength();p.style.strokeDasharray=L;
function ease(t){{return t<0?0:t>1?1:1-Math.pow(1-t,3)}}
window.setT=function(t){{p.style.strokeDashoffset=L*(1-ease(t/1.6));
 [['a',.15],['b',.45],['c',.85],['d',1.15],['e',1.3]].forEach(([id,s])=>{{const k=ease((t-s)/.5);const el=document.getElementById(id);el.style.opacity=k;el.style.transform=`translateY(${{30*(1-k)}}px)`}})}}
</script></body></html>"""
async def main():
    out = pathlib.Path("/home/claude/work/end"); out.mkdir(exist_ok=True)
    (D/"_end.html").write_text(HTML)
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width":1080,"height":1920})
        await pg.goto((D/"_end.html").as_uri()); await pg.wait_for_timeout(600)
        for i in range(N):
            await pg.evaluate(f"setT({i/FPS})")
            await pg.screenshot(path=str(out/f"e{i:03d}.png"))
        await b.close()
asyncio.run(main())
