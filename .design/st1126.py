import asyncio, pathlib
from playwright.async_api import async_playwright
D=pathlib.Path(__file__).parent; LOGO=pathlib.Path("/home/claude/azrimstudio/img/logo.png").as_uri()
C=(D/"out/c02/slide-1.png").as_uri(); Y=1536
html=f"""<!doctype html><html><head><link rel=stylesheet href="v2.css"><style>html,body{{width:1080px;height:1920px}} .s{{height:1920px}} .x{{position:absolute}}</style></head><body><div class="s dark">
<div class=meta style="top:250px;left:84px;font-size:24px;color:#EFEBE1">Azrim Studio — today's post</div>
<div class="x it" style="top:320px;left:84px;font-size:104px;line-height:.98;color:#EFEBE1">Is your website<br>losing clients?</div>
<img src="{C}" style="position:absolute;top:620px;left:200px;width:680px;transform:rotate(-3deg);box-shadow:0 40px 70px -20px rgba(0,0,0,.8)">
<span class=tape style="top:600px;left:440px;transform:rotate(-5deg)"></span>
<div class="x hw" style="top:1500px;left:120px;font-size:60px;color:#C9A84C;transform:rotate(-3deg);z-index:5;background:#161616;padding:0 16px">count how many you have ↑</div>
<div class=x style="top:1620px;left:84px;font-size:30px;color:#9C978B">5 hiba, ami ügyfeleket visz el. Hány van a te oldaladon?</div>
<img class="logo x" src="{LOGO}" style="bottom:200px;right:84px">
</div></body></html>"""
async def main():
    (D/"_st1126.html").write_text(html)
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome"); pg=await b.new_page(viewport={"width":1080,"height":1920})
        await pg.goto((D/"_st1126.html").as_uri()); await pg.wait_for_timeout(700)
        await pg.screenshot(path="/home/claude/work/st1126.png"); await b.close()
asyncio.run(main())
