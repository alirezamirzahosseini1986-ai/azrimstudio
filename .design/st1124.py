import asyncio, pathlib
from playwright.async_api import async_playwright
D=pathlib.Path(__file__).parent
LOGO=pathlib.Path("/home/claude/azrimstudio/img/logo.png").as_uri()
TV=pathlib.Path("/home/claude/work/tvframe.png").as_uri()
FPS,SEC,Y=30,7,1536
d=f"M-5 {Y} C 200 {Y}, 300 {Y-40}, 420 {Y-10} C 520 {Y+20}, 600 {Y}, 700 {Y} C 780 {Y}, 820 1380, 900 1380 C 980 1380, 990 {Y}, 1085 {Y}"
html=f"""<!doctype html><html><head><link rel=stylesheet href="v2.css"><style>
html,body{{width:1080px;height:1920px}} .s{{height:1920px}} .x{{position:absolute}}
.pol{{position:absolute;background:#FBFAF6;padding:20px 20px 30px;box-shadow:0 34px 60px -18px rgba(0,0,0,.7)}}
.pol .im{{width:620px;height:560px;background:url('{TV}') -230px -470px/1080px 1920px}}
</style></head><body><div class="s dark">
<div class=meta id=m style="top:250px;left:84px;font-size:24px;color:#EFEBE1">Azrim Studio — new reel</div>
<div class="x it" id=q style="top:330px;left:84px;font-size:118px;line-height:.95;color:#EFEBE1">Someone’s trying<br>to get out.</div>
<div class=pol id=p style="top:640px;left:220px"><div class=im></div></div>
<span class=tape id=tp style="top:625px;left:430px;transform:rotate(-4deg)"></span>
<div class="x hw" id=hw style="top:1300px;left:150px;font-size:66px;color:#C9A84C;transform:rotate(-3deg)">watch it on my profile →</div>
<svg width=1080 height=1920 style="position:absolute;inset:0;z-index:3"><path id=th d="{d}" fill=none stroke="#C9A84C" stroke-width=7 stroke-linecap=round/></svg>
<div class=x id=tm style="top:1590px;left:84px;font-family:RC;font-size:26px;letter-spacing:.05em;color:#EFEBE1">TOMORROW 18:00 · BRAND DOCTOR Nº 01</div>
<div class=x id=hu style="top:1640px;left:84px;font-size:30px;color:#9C978B">Új reel a profilon. Holnap: Brand Doctor.</div>
<img class="logo x" id=lg src="{LOGO}" style="bottom:240px;right:84px">
</div><script>
const $=i=>document.getElementById(i),P=$('th'),L=P.getTotalLength();P.style.strokeDasharray=L;
const E=t=>t<=0?0:t>=1?1:1-Math.pow(1-t,3);
const B=t=>{{if(t<=0)return 0;if(t>=1)return 1;const c=1.70158;return 1+(c+1)*Math.pow(t-1,3)+c*Math.pow(t-1,2)}};
let T=0;function rise(i,s,d=.5,dy=40){{const k=E((T-s)/d);$(i).style.opacity=k;$(i).style.translate=`0 ${{dy*(1-k)}}px`}}
window.setT=t=>{{T=t;rise('m',.1);rise('q',.3,.6,60);
 {{const k=B((t-.9)/.6),p=$('p');p.style.opacity=Math.min(1,Math.max(0,(t-.9)/.15));p.style.transform=`rotate(${{-8+5*k}}deg) scale(${{.8+.2*k}})`;$('tp').style.opacity=E((t-1.4)/.3)}}
 {{const k=E((t-1.8)/1.0);$('hw').style.clipPath=`inset(-30px ${{100-100*k}}% -30px 0)`}}
 P.style.strokeDashoffset=L*(1-E((t-2.4)/1.4));rise('tm',3.2,.5,20);rise('hu',3.5,.5,20);rise('lg',3.6,.5,0);
 if(t>4.2)$('p').style.transform=`rotate(${{-3+.6*Math.sin((t-4.2)*2.2)}}deg)`;}}
</script></body></html>"""
async def main():
    out=pathlib.Path("/home/claude/work/st24"); out.mkdir(exist_ok=True)
    for f in out.glob("*.png"): f.unlink()
    (D/"_st1124.html").write_text(html)
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg=await b.new_page(viewport={"width":1080,"height":1920})
        await pg.goto((D/"_st1124.html").as_uri()); await pg.wait_for_timeout(700)
        for i in range(FPS*SEC):
            await pg.evaluate(f"setT({i/FPS})"); await pg.screenshot(path=str(out/f"f{i:04d}.png"))
        await b.close()
asyncio.run(main())
