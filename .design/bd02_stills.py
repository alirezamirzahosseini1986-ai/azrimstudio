import asyncio, pathlib, importlib.util
from playwright.async_api import async_playwright
D=pathlib.Path(__file__).parent; W=pathlib.Path("/home/claude/work/bd02")
spec=importlib.util.spec_from_file_location("bd02m", D/"bd02.py"); 
src=(D/"bd02.py").read_text().split("async def main")[0]; ns={"__file__":str(D/"bd02.py")}; exec(src, ns)
loud, FIX, LOGO = ns['loud'], ns['FIXPOSTER'], ns['LOGO']
Y=1536
HB=f"M-5 {Y} L 690 {Y} L 725 {Y-20} L 755 {Y+12} L 790 {Y-140} L 835 {Y+110} L 870 {Y-40} L 900 {Y} L 1085 {Y}"
css="""<link rel=stylesheet href="v2.css"><style>html,body{width:1080px;height:1920px} .s{height:1920px} .x{position:absolute}
.loud{position:absolute;left:0;top:0;width:900px;height:1125px;overflow:hidden}
.box{position:absolute;overflow:hidden;box-shadow:0 30px 50px -18px rgba(0,0,0,.5)}
#clean{left:0!important;top:0!important;transform:scale(.5);transform-origin:0 0}</style>"""
cover=f"""<!doctype html><html><head>{css}</head><body><div class=s>
<div class=meta style="top:270px;left:72px;font-size:24px">Azrim Studio — Reel · Brand Doctor Nº 02</div>
<div class=box style="left:60px;top:360px;width:450px;height:562px;transform:rotate(-4deg)">{loud(.5,0,"0 0")}</div>
<div class=box style="left:560px;top:380px;width:400px;height:500px;transform:rotate(3deg)">{FIX}</div>
<div class="x hw" style="top:940px;left:110px;font-size:50px;color:#D8432A;transform:rotate(-4deg)">before</div>
<div class="x hw" style="top:930px;left:700px;font-size:50px;color:#151515;transform:rotate(3deg)">after</div>
<div class="x it" style="top:1060px;left:72px;font-size:112px;line-height:.92">Your Black Friday post</div>
<div class="x an" style="top:1190px;left:72px;font-size:200px;line-height:.9">is invisible.</div>
<svg width=1080 height=1920 style="position:absolute;inset:0;z-index:3"><path d="{HB}" fill=none stroke="#C9A84C" stroke-width=7 stroke-linecap=round stroke-linejoin=round/></svg>
<div class=x style="top:1590px;left:72px;font-size:30px;color:#6E6A60">A Black Friday posztod láthatatlan. Itt a javítás.</div>
<img class=logo src="{LOGO}" style="top:258px;right:72px;width:46px">
</div></body></html>"""
story=f"""<!doctype html><html><head>{css}</head><body><div class="s dark">
<div class=meta style="top:250px;left:84px;font-size:24px;color:#EFEBE1">Azrim Studio — Black Friday</div>
<div class="x it" style="top:320px;left:84px;font-size:104px;line-height:.98;color:#EFEBE1">Does yours look<br>like this?</div>
<div class=box style="left:240px;top:620px;width:600px;height:750px;transform:rotate(-3deg)">{loud(.6667,0,"0 0")}</div>
<svg width=1080 height=1920 style="position:absolute;inset:0;z-index:4"><path d="M260 660 L 830 1340 M 830 660 L 260 1340" stroke="#D8432A" stroke-width=14 stroke-linecap=round/></svg>
<div class="x hw" style="top:1440px;left:150px;font-size:60px;color:#C9A84C;transform:rotate(-3deg)">the 3-step fix is in today's reel</div>
<div class=x style="top:1620px;left:84px;font-size:30px;color:#9C978B">Így néz ki a tiéd? A javítás a mai reelben.</div>
<img class="logo x" src="{LOGO}" style="bottom:200px;right:84px">
</div></body></html>"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome"); pg=await b.new_page(viewport={"width":1080,"height":1920})
        for name,h in (("bd02_cover",cover),("st1127",story)):
            f=D/f"_{name}.html"; f.write_text(h); await pg.goto(f.as_uri()); await pg.wait_for_timeout(700)
            await pg.screenshot(path=str(W/f"{name}.png"))
        await b.close()
asyncio.run(main())
