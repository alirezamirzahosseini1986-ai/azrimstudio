import asyncio, pathlib
from playwright.async_api import async_playwright
D=pathlib.Path(__file__).parent; W=pathlib.Path("/home/claude/work/bd")
LOGO=pathlib.Path("/home/claude/azrimstudio/img/logo.png").as_uri(); U=lambda p:(W/p).as_uri()
Y=1536
HB=f"M-5 {Y} L 700 {Y} L 740 {Y-22} L 775 {Y+12} L 815 {Y-230} L 865 {Y+120} L 905 {Y-45} L 940 {Y} L 1085 {Y}"
html=f"""<!doctype html><html><head><link rel=stylesheet href="v2.css"><style>
html,body{{width:1080px;height:1920px}} .s{{height:1920px}} .x{{position:absolute}}
.pol{{position:absolute;background:#FBFAF6;padding:20px 20px 88px;box-shadow:0 30px 50px -18px rgba(0,0,0,.45),0 6px 14px -6px rgba(0,0,0,.25)}}
.pol img{{display:block;object-fit:cover}} .pol .cap{{position:absolute;left:0;right:0;bottom:18px;text-align:center;font-family:HW;font-weight:600;font-size:52px}}
</style></head><body><div class=s>
<div class=meta style="top:270px;left:72px;font-size:24px">Azrim Studio — Reel · Brand Doctor Nº 01</div>
<div class=pol style="top:360px;left:70px;transform:rotate(-5deg)"><img src="{U('inside_still.jpg')}" style="width:440px;height:520px;object-position:50% 40%"><div class=cap>inside</div></div>
<div class=pol style="top:400px;left:560px;transform:rotate(4deg)"><img src="{U('b2b.png')}" style="width:420px;height:500px;object-position:50% 45%;filter:saturate(.8)"><div class=cap style="color:#D8432A">outside</div></div>
<span class=tape style="top:350px;left:250px;transform:rotate(-8deg)"></span><span class=tape style="top:385px;left:700px;transform:rotate(5deg)"></span>
<div class="x it" style="top:1060px;left:72px;font-size:124px;line-height:.92">Cosy inside.</div>
<div class="x an" style="top:1190px;left:72px;font-size:178px">Invisible<br>outside.</div>
<svg width=1080 height=1920 style="position:absolute;inset:0;z-index:3"><path d="{HB}" fill=none stroke="#C9A84C" stroke-width=7 stroke-linecap=round stroke-linejoin=round/></svg>
<div class=x style="top:1590px;left:72px;font-size:30px;color:#6E6A60">Belül otthonos. Kívül láthatatlan.</div>
<img class=logo src="{LOGO}" style="top:258px;right:72px;width:46px">
</div></body></html>"""
async def main():
    (D/"_bd01c.html").write_text(html)
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg=await b.new_page(viewport={"width":1080,"height":1920})
        await pg.goto((D/"_bd01c.html").as_uri()); await pg.wait_for_timeout(700)
        await pg.screenshot(path=str(W/"bd01_cover.png")); await b.close()
asyncio.run(main())
