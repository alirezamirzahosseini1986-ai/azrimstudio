import asyncio, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from playwright.async_api import async_playwright
D = pathlib.Path(__file__).parent
LOGO = pathlib.Path("/home/claude/azrimstudio/img/logo.png").resolve().as_uri()
Y = 1536
d = f"M-5 {Y} C 200 {Y}, 300 {Y-40}, 420 {Y-10} C 520 {Y+20}, 600 {Y}, 700 {Y} C 780 {Y}, 820 1380, 900 1380 C 980 1380, 990 {Y}, 1085 {Y}"
html = f"""<!doctype html><html><head><link rel=stylesheet href="v2.css"><style>html,body{{width:1080px;height:1920px}}</style></head><body>
<div class=s style="width:1080px;height:1920px">
<div class=meta style="top:250px;left:84px;font-size:24px">Azrim Studio — new on the feed</div>
<div class=it style="position:absolute;top:400px;left:84px;font-size:110px;line-height:1">Which one did<br>you pay for?</div>
<div class=an style="position:absolute;top:720px;left:84px;font-size:300px">€500</div>
<div class=it style="position:absolute;top:1010px;left:100px;font-size:80px">or</div>
<div class=an style="position:absolute;top:1080px;left:84px;font-size:300px;color:transparent;-webkit-text-stroke:4px #151515">€5,000</div>
<div class=hw style="position:absolute;top:1420px;left:84px;font-size:58px;transform:rotate(-3deg)">the difference is in today's post →</div>
<svg width=1080 height=1920 style="position:absolute;inset:0;z-index:3"><path d="{d}" fill=none stroke="#C9A84C" stroke-width=7 stroke-linecap=round/></svg>
<div style="position:absolute;top:1590px;left:84px;font-size:30px;color:#6E6A60">Melyikért fizettél? A válasz a mai posztban.</div>
<img class=logo src="{LOGO}" style="bottom:240px;right:84px">
</div></body></html>"""
async def main():
    (D/"_st.html").write_text(html)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width":1080,"height":1920})
        await pg.goto((D/"_st.html").as_uri()); await pg.wait_for_timeout(500)
        await pg.screenshot(path="/home/claude/work/story_1123.png"); await b.close()
asyncio.run(main())
