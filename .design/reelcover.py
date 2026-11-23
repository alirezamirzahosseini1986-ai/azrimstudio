import asyncio, pathlib, sys
from playwright.async_api import async_playwright
D = pathlib.Path(__file__).parent
LOGO = pathlib.Path("../img/logo.png").as_uri()
BG = pathlib.Path("/home/claude/work/tvframe.png").as_uri()
Y = 1536
d = f"M-5 {Y} L 1085 {Y}"
d0 = f"M-5 {Y} C 220 {Y}, 300 {Y-60}, 380 {Y-30} C 460 {Y}, 430 {Y+50}, 500 {Y+10} C 570 {Y-30}, 600 {Y-70}, 660 {Y-20} C 700 {Y+15}, 760 {Y-10}, 820 {Y} C 920 {Y+10}, 980 {Y}, 1085 {Y}"
import sys; sys.path.insert(0,str(D))
from monosig import monoline
_img,_base,_=monoline("rim Stu",175); _p=D/"out"/"sig_rimstu.png"; _img.save(_p)
SIG=f'<img src="{_p.as_uri()}" style="position:absolute;left:60px;top:{Y-_base-10}px">'
html = f"""<!doctype html><html><head><link rel=stylesheet href="v2.css"><style>html,body{{width:1080px;height:1920px}}</style></head><body>
<div style="position:relative;width:1080px;height:1920px;overflow:hidden;background:#111">
<img src="{BG}" style="position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover;filter:contrast(1.05)">
<div style="position:absolute;inset:0;background:linear-gradient(#0d0d0d 0,rgba(13,13,13,.0) 22%,rgba(13,13,13,0) 55%,rgba(13,13,13,.92) 74%,#0d0d0d 79%)"></div>
<div class=meta style="top:280px;left:84px;color:#EFEBE1;font-size:22px">Azrim Studio — Reel · Meet Ali</div>
<div class=serif style="position:absolute;top:1150px;left:84px;width:900px;font-size:100px;line-height:.95;color:#EFEBE1">Who says you have to<br><span class=it style="color:#C9A84C">stay inside the frame?</span></div>
<svg width=1080 height=1920 style="position:absolute;inset:0"><path d="{d}" fill=none stroke="#C9A84C" stroke-width=7 stroke-linecap=round/></svg>
<img src="{LOGO}" style="position:absolute;top:1600px;right:84px;width:56px">
{SIG}
</div></body></html>"""
async def main():
    (D/"_rc.html").write_text(html)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width":1080,"height":1920})
        await pg.goto((D/"_rc.html").as_uri()); await pg.wait_for_timeout(500)
        await pg.screenshot(path="/home/claude/work/reel_intro_cover.png"); await b.close()
asyncio.run(main())
