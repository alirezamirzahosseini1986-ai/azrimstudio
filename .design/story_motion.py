import asyncio, pathlib, subprocess
from playwright.async_api import async_playwright
D = pathlib.Path(__file__).parent
LOGO = pathlib.Path("/home/claude/azrimstudio/img/logo.png").resolve().as_uri()
FPS, SEC = 30, 8
Y = 1536
d = f"M-5 {Y} C 200 {Y}, 300 {Y-40}, 420 {Y-10} C 520 {Y+20}, 600 {Y}, 700 {Y} C 780 {Y}, 820 1380, 900 1380 C 980 1380, 990 {Y}, 1085 {Y}"
html = f"""<!doctype html><html><head><link rel=stylesheet href="v2.css"><style>
html,body{{width:1080px;height:1920px}} .x{{position:absolute}}
#e5k{{color:transparent;-webkit-text-stroke:4px #151515}}
</style></head><body>
<div class=s style="width:1080px;height:1920px">
<div class="meta x" id=m style="top:250px;left:84px;font-size:24px">Azrim Studio — new on the feed</div>
<div class="it x" id=q style="top:400px;left:84px;font-size:110px;line-height:1">Which one did<br>you pay for?</div>
<div class="an x" id=e5 style="top:720px;left:84px;font-size:300px">€500</div>
<div class="it x" id=or style="top:1010px;left:100px;font-size:80px">or</div>
<div class="an" id=e5k style="position:absolute;top:1080px;left:84px;font-size:290px;letter-spacing:.03em">€5,000</div>
<div class="hw x" id=hw style="top:1420px;left:84px;font-size:58px;transform:rotate(-3deg)">the difference is in today's post →</div>
<svg width=1080 height=1920 style="position:absolute;inset:0;z-index:3"><path id=p d="{d}" fill=none stroke="#C9A84C" stroke-width=7 stroke-linecap=round/></svg>
<div class=x id=hu style="top:1590px;left:84px;font-size:30px;color:#6E6A60">Melyikért fizettél? A válasz a mai posztban.</div>
<img class="logo x" id=lg src="{LOGO}" style="bottom:240px;right:84px">
</div><script>
const P=document.getElementById('p'),L=P.getTotalLength();P.style.strokeDasharray=L;
const E=t=>t<=0?0:t>=1?1:1-Math.pow(1-t,3);
const B=t=>{{if(t<=0)return 0;if(t>=1)return 1;const c=1.70158;return 1+(c+1)*Math.pow(t-1,3)+c*Math.pow(t-1,2)}};
function rise(id,s,dur=.55,dy=40){{const k=E((T-s)/dur),el=document.getElementById(id);el.style.opacity=k;el.style.translate=`0 ${{dy*(1-k)}}px`}}
let T=0;
window.setT=function(t){{T=t;
 rise('m',.1);rise('q',.3,.7,60);
 // €500 stamps in (scale down from 1.25 with overshoot)
 {{const k=B((t-1.1)/.45),el=document.getElementById('e5');el.style.opacity=Math.min(1,(t-1.1)/.15);el.style.scale=1.25-.25*k;el.style.transformOrigin='left top'}}
 rise('or',1.7,.4,20);
 // €5,000 outline revealed left to right
 {{const k=E((t-2.0)/.9),el=document.getElementById('e5k');el.style.clipPath=`inset(-60px ${{100-100*k}}% -60px -20px)`}}
 P.style.strokeDashoffset=L*(1-E((t-2.7)/1.4));
 // handwriting writes on
 {{const k=E((t-3.6)/1.1),el=document.getElementById('hw');el.style.clipPath=`inset(-20px ${{100-100*k}}% -20px 0)`}}
 rise('hu',4.6,.6,20);rise('lg',4.8,.6,0);
 // subtle breathing on €500 at the end
 if(t>5.4){{document.getElementById('e5').style.scale=1+0.015*Math.sin((t-5.4)*3)}}
}}
</script></body></html>"""
async def main():
    out = pathlib.Path("/home/claude/work/stm"); out.mkdir(exist_ok=True)
    for f in out.glob("*.png"): f.unlink()
    (D/"_stm.html").write_text(html)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width":1080,"height":1920})
        await pg.goto((D/"_stm.html").as_uri()); await pg.wait_for_timeout(600)
        for i in range(FPS*SEC):
            await pg.evaluate(f"setT({i/FPS})")
            await pg.screenshot(path=str(out/f"f{i:04d}.png"))
        await b.close()
asyncio.run(main())
