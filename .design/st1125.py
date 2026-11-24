import asyncio, pathlib
from playwright.async_api import async_playwright
D=pathlib.Path(__file__).parent; W=pathlib.Path("/home/claude/work/bd")
LOGO=pathlib.Path("/home/claude/azrimstudio/img/logo.png").as_uri(); U=lambda p:(W/p).as_uri()
Y=1536
html=f"""<!doctype html><html><head><link rel=stylesheet href="v2.css"><style>
html,body{{width:1080px;height:1920px}} .s{{height:1920px}} .x{{position:absolute}}
.pol{{position:absolute;background:#FBFAF6;padding:22px 22px 96px;box-shadow:0 30px 50px -18px rgba(0,0,0,.45)}}
.pol img{{display:block;object-fit:cover}}
</style></head><body><div class=s>
<div class=meta style="top:250px;left:84px;font-size:24px">Azrim Studio — Brand Doctor Nº 01</div>
<div class="x it" style="top:330px;left:84px;font-size:112px;line-height:.95">Would you<br>walk in?</div>
<div class=pol style="top:600px;left:150px;transform:rotate(-3deg)"><img src="{U('b2.png')}" style="width:740px;height:700px;object-position:50% 50%"></div>
<span class=tape style="top:585px;left:430px;transform:rotate(-4deg)"></span>
<div class="x hw" style="top:1355px;left:200px;font-size:62px;transform:rotate(-3deg)">wait till you see the inside →</div>
<svg width=1080 height=1920 style="position:absolute;inset:0;z-index:3"><path d="M-5 {Y} L 760 {Y} L 790 {Y-16} L 815 {Y+10} L 850 {Y-105} L 885 {Y+80} L 915 {Y-28} L 945 {Y} L 1085 {Y}" fill=none stroke="#C9A84C" stroke-width=7 stroke-linecap=round stroke-linejoin=round/></svg>
<div class=x style="top:1600px;left:84px;font-size:30px;color:#6E6A60">Bemennél? A belseje a mai reelben.</div>
<img class=logo src="{LOGO}" style="bottom:240px;right:84px">
</div></body></html>"""
async def main():
    (D/"_st1125.html").write_text(html)
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg=await b.new_page(viewport={"width":1080,"height":1920})
        await pg.goto((D/"_st1125.html").as_uri()); await pg.wait_for_timeout(700)
        await pg.screenshot(path=str(W/"st1125.png")); await b.close()
asyncio.run(main())
