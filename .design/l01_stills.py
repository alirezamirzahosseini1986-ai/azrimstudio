import asyncio, pathlib, re
from playwright.async_api import async_playwright
D=pathlib.Path(__file__).parent; W=pathlib.Path("/home/claude/work/l01")
src=(D/"l01.py").read_text().split("html = f")[0]; ns={"__file__":str(D/"l01.py")}; exec(src, ns)
wm, TERRA, CREAM, INK, GOLD, LOGO = ns['wm'], ns['TERRA'], ns['CREAM'], ns['INK'], ns['GOLD'], ns['LOGO']
Y=1536
SW=f"M-5 {Y} L 700 {Y} C 715 {Y}, 726 1528, 732 1520 M 830 1400 A 100 100 0 1 1 829.9 1400 M 830 1500 L 830 1440 M 830 1500 L 872 1522 M 808 1372 L 852 1372 M 830 1372 L 830 1400 M 928 1520 C 934 1528, 970 {Y}, 1085 {Y}"
cover=f"""<!doctype html><html><head><link rel=stylesheet href="v2.css"><style>html,body{{width:1080px;height:1920px}} .s{{height:1920px}} .x{{position:absolute}}</style></head><body><div class=s>
<div class=meta style="top:270px;left:72px;font-size:24px">Azrim Studio — Reel · Logo in 60 seconds Nº 01</div>
<div class=x style="top:360px;left:72px;width:936px;height:600px;background:{TERRA};display:flex;align-items:center;justify-content:center;flex-direction:column;box-shadow:0 30px 50px -20px rgba(0,0,0,.4)">
 {wm(250, CREAM, CREAM)}<div class=meta style="position:static;margin-top:30px;color:{CREAM};opacity:.85">kávézó · budapest VII</div></div>
<div class="x an" style="top:1030px;left:72px;font-size:170px;line-height:.9">A café logo</div>
<div class="x it" style="top:1190px;left:72px;font-size:120px;line-height:1">in 60 seconds.</div>
<svg width=1080 height=1920 style="position:absolute;inset:0;z-index:3"><path d="{SW}" fill="none" stroke="{GOLD}" stroke-width="7" stroke-linecap="round"/></svg>
<div class=x style="top:1600px;left:72px;font-size:30px;color:#6E6A60">Egy kávézó logója 60 másodperc alatt.</div>
<img class=logo src="{LOGO}" style="top:258px;right:72px;width:46px">
</div></body></html>"""
story=f"""<!doctype html><html><head><link rel=stylesheet href="v2.css"><style>html,body{{width:1080px;height:1920px}} .s{{height:1920px}} .x{{position:absolute}}</style></head><body><div class="s dark">
<div class=meta style="top:250px;left:84px;font-size:24px;color:#EFEBE1">Azrim Studio — quiz</div>
<div class="x it" style="top:320px;left:84px;font-size:100px;line-height:.98;color:#EFEBE1">This café is called<br>“Kanál” (spoon).</div>
<div class=x style="top:700px;left:84px;width:912px;height:560px;background:{TERRA};display:flex;align-items:center;justify-content:center">
 <span style="font-family:IS;font-size:240px;line-height:1;color:{CREAM};position:relative">kan<span style="position:relative">a<span class=hw style="position:absolute;left:30px;top:-110px;font-size:140px;color:#C9A84C">?</span></span>l</span></div>
<div class="x hw" style="top:1330px;left:110px;font-size:62px;color:#C9A84C;transform:rotate(-3deg)">guess what the accent becomes →</div>
<div class=x style="top:1480px;left:84px;font-size:34px;color:#EFEBE1">Answer in today's reel.</div>
<div class=x style="top:1600px;left:84px;font-size:30px;color:#9C978B">Mi lesz az ékezetből? A válasz a mai reelben.</div>
<img class="logo x" src="{LOGO}" style="bottom:200px;right:84px">
</div></body></html>"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome"); pg=await b.new_page(viewport={"width":1080,"height":1920})
        for name,h in (("l01_cover",cover),("st1128",story)):
            f=D/f"_{name}.html"; f.write_text(h); await pg.goto(f.as_uri()); await pg.wait_for_timeout(700)
            await pg.screenshot(path=str(W/f"{name}.png"))
        await b.close()
asyncio.run(main())
