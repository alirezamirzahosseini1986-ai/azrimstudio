"""Brand Doctor Nº02 — Black Friday post (reel, 19.5s, 1080x1920, 30fps). Frames → /home/claude/work/bd02/fr/"""
import asyncio, pathlib, sys
from playwright.async_api import async_playwright
D = pathlib.Path(__file__).parent
W = pathlib.Path("/home/claude/work/bd02"); W.mkdir(parents=True, exist_ok=True)
LOGO = pathlib.Path("/home/claude/azrimstudio/img/logo.png").as_uri()
FPS, SEC, Y = 30, 19.5, 1536

def loud(scale=1.0, hue=0, origin="50% 50%"):
    """A deliberately bad, generic Black Friday poster (no real brand)."""
    return f'''<div class=loud style="transform:scale({scale});transform-origin:{origin};filter:hue-rotate({hue}deg)">
 <div style="position:absolute;inset:0;background:radial-gradient(circle at 30% 20%,#ff2bd6,#3a00ff 55%,#000 100%)"></div>
 <div style="position:absolute;top:40px;left:-20px;right:-20px;text-align:center;font-family:AN;font-size:150px;color:#ffe600;text-shadow:6px 6px 0 #ff0040,12px 12px 0 #000;transform:rotate(-4deg)">BLACK FRIDAY!!!</div>
 <div style="position:absolute;top:230px;left:40px;font-family:HW;font-size:90px;color:#00ffd5;transform:rotate(-8deg)">MEGA SALE</div>
 <div style="position:absolute;top:240px;right:40px;width:250px;height:250px;background:#ff0040;clip-path:polygon(50% 0,61% 35%,98% 35%,68% 57%,79% 91%,50% 70%,21% 91%,32% 57%,2% 35%,39% 35%);display:flex;align-items:center;justify-content:center;font-family:AN;font-size:64px;color:#fff">-50%</div>
 <div style="position:absolute;top:420px;left:60px;font-family:IS;font-style:italic;font-size:70px;color:#fff">up to <b style="font-family:AN;font-style:normal;font-size:130px;color:#ffe600">-70%</b></div>
 <div style="position:absolute;top:610px;left:40px;right:40px;font-family:RC;font-size:34px;color:#fff;line-height:1.35">*on selected items* free shipping over €50 · new arrivals · gift cards · limited stock · while supplies last · T&amp;C apply</div>
 <div style="position:absolute;top:800px;left:80px;font-family:IT;font-weight:800;font-size:86px;color:#000;background:#00ff66;padding:6px 24px;transform:rotate(3deg)">-30% EVERYTHING</div>
 <div style="position:absolute;top:960px;right:50px;font-family:HW;font-size:64px;color:#ffe600;transform:rotate(6deg)">DON'T MISS OUT!!</div>
 <div style="position:absolute;bottom:60px;left:0;right:0;text-align:center"><span style="font-family:AN;font-size:96px;color:#fff;background:#ff0040;padding:10px 50px;border-radius:60px;box-shadow:0 0 40px #ff0040">BUY NOW ►</span></div>
</div>'''

FIXPOSTER = f'''<div id=clean style="position:absolute;left:140px;top:430px;width:800px;height:1000px;background:#151515;color:#EFEBE1;overflow:hidden;box-shadow:0 40px 70px -20px rgba(0,0,0,.6)">
 <div class=meta style="top:44px;left:48px;color:#EFEBE1;opacity:.7">Bró Café · Black Friday</div>
 <div id=c30 class=an style="position:absolute;top:110px;left:40px;font-size:250px;line-height:.9;color:transparent;-webkit-text-stroke:4px #C9A84C">−30%</div>
 <div id=cbag style="position:absolute;top:470px;left:300px;width:220px;height:300px;background:#C9A84C;border-radius:14px 14px 26px 26px;box-shadow:inset 0 -30px 0 rgba(0,0,0,.12)">
  <div style="position:absolute;top:-24px;left:30px;right:30px;height:40px;background:#a8862f;border-radius:6px"></div>
  <div style="position:absolute;top:90px;left:0;right:0;text-align:center;font-family:IS;font-style:italic;font-size:44px;color:#151515">Bró</div>
  <div style="position:absolute;top:150px;left:0;right:0;text-align:center;font-family:RC;font-size:16px;color:#151515;letter-spacing:.1em">HOUSE BEANS</div></div>
 <div id=cline class=it style="position:absolute;top:800px;left:48px;font-size:62px;line-height:1">on every bag of beans.</div>
 <div id=cdate style="position:absolute;top:900px;left:48px;font-family:RC;font-size:28px;letter-spacing:.08em;color:#C9A84C">FRI–SUN ONLY · IN STORE &amp; ONLINE</div>
</div>'''

html = f"""<!doctype html><html><head><link rel=stylesheet href="v2.css"><style>
html,body{{width:1080px;height:1920px;background:#161616;overflow:hidden}}
.x{{position:absolute}} .L{{position:absolute;inset:0;opacity:0}}
.loud{{position:absolute;left:90px;top:380px;width:900px;height:1125px;overflow:hidden;transform-origin:50% 50%}}
.tag{{position:absolute;z-index:6;background:#F6F2E8;color:#151515;font-family:HW;font-weight:600;line-height:1.02;padding:16px 24px 18px;font-size:48px;box-shadow:0 14px 30px -12px rgba(0,0,0,.6)}}
.tag b{{font-family:RC;font-weight:700;font-size:22px;letter-spacing:.06em;display:block;margin-bottom:6px;color:#D8432A}}
.pill{{display:inline-block;font-family:RC;font-size:24px;text-transform:uppercase;letter-spacing:.08em;border-radius:999px;padding:10px 24px}}
.paper{{position:absolute;inset:0;background:var(--paper)}}
svg.o{{position:absolute;inset:0;z-index:5}}
.feedpost{{position:relative;width:640px;height:800px;margin:0 auto 26px;overflow:hidden;border-radius:6px}}
.feedpost .loud{{left:0;top:0}}
</style></head><body>
<!-- S1 hook: loud poster -->
<div class=L id=s1>{loud()}
 <div class=x style="left:0;right:0;top:0;height:420px;background:linear-gradient(#161616 60%,transparent)"></div>
 <div class=x style="top:240px;left:72px"><span class=pill style="border:2px solid #EFEBE1;color:#EFEBE1">Brand Doctor · Nº 02</span></div>
 <div class="x it" id=h1 style="top:1540px;left:72px;font-size:96px;line-height:.95;color:#EFEBE1;z-index:7">Your Black Friday post<br>is <span class=an style="font-style:normal;color:#D8432A">invisible.</span></div>
</div>
<!-- S2 feed -->
<div class=L id=s2>
 <div id=feed class=x style="left:0;right:0;top:0">
  {''.join(f'<div class=feedpost>{loud(.7112, h, "0 0")}</div>' for h in (0, 40, 200, 300, 120, 0))}
 </div>
 <div class=x style="left:0;right:0;bottom:0;height:560px;background:linear-gradient(transparent,#161616 45%)"></div>
 <div class="x serif" id=h2 style="top:1480px;left:72px;font-size:80px;line-height:1;color:#EFEBE1;z-index:7">Because everyone’s<br><span class=it>looks exactly like this.</span></div>
</div>
<!-- S3 diagnosis -->
<div class=L id=s3>{loud()}
 <div class=x style="inset:0;background:rgba(0,0,0,.35);z-index:4"></div>
 <div class=x style="top:240px;left:72px;z-index:7"><span class=pill style="background:#D8432A;color:#fff">Diagnosis</span></div>
 <svg class=o width=1080 height=1920 style="z-index:5">
  <ellipse id=c1 cx=540 cy=560 rx=500 ry=150 fill=none stroke="#D8432A" stroke-width=9 transform="rotate(-3 540 560)"/>
  <ellipse id=c2 cx=700 cy=760 rx=330 ry=170 fill=none stroke="#D8432A" stroke-width=9 transform="rotate(4 700 760)"/>
  <ellipse id=c3 cx=540 cy=1060 rx=470 ry=110 fill=none stroke="#D8432A" stroke-width=9 transform="rotate(-2 540 1060)"/>
  <ellipse id=c4 cx=540 cy=1410 rx=380 ry=110 fill=none stroke="#D8432A" stroke-width=9 transform="rotate(2 540 1410)"/>
 </svg>
 <div class=tag id=t1 style="top:330px;left:520px;width:470px;transform:rotate(3deg)"><span class=tape style="width:120px;height:38px;top:-18px;left:40%"></span><b>01</b>5 fonts, 9 colours, 0 focus</div>
 <div class=tag id=t2 style="top:900px;left:60px;width:440px;transform:rotate(-3deg)"><span class=tape style="width:120px;height:38px;top:-18px;left:40%"></span><b>02</b>−30? −50? −70%? pick one</div>
 <div class=tag id=t3 style="top:1170px;left:520px;width:460px;transform:rotate(2deg)"><span class=tape style="width:120px;height:38px;top:-18px;left:40%"></span><b>03</b>where’s the product?</div>
 <div class=tag id=t4 style="top:1560px;left:100px;width:620px;transform:rotate(-2deg)"><span class=tape style="width:120px;height:38px;top:-18px;left:40%"></span><b>04</b>“buy now” — buy what? until when?</div>
</div>
<!-- S4 fix -->
<div class=L id=s4><div class=paper></div>
 <div class=x style="top:240px;left:72px;z-index:7"><span class=pill style="background:#C9A84C;color:#151515">The fix</span></div>
 <div class="x hw" style="top:300px;left:600px;font-size:44px;transform:rotate(-4deg);z-index:7">same café, same sale</div>
 {FIXPOSTER}
 <svg class=o width=1080 height=1920><path id=fx d="M-5 {Y} L 100 {Y} C 120 {Y}, 120 1450, 120 1420 L 120 410 L 960 410 L 960 1450 L 120 1450" fill=none stroke="#C9A84C" stroke-width=9 stroke-linecap=round stroke-linejoin=round/></svg>
 <div class=tag id=f1 style="top:700px;left:690px;width:330px;font-size:44px;transform:rotate(4deg)"><span class=tape style="width:110px;height:36px;top:-18px;left:40%"></span><b>01</b>one number</div>
 <div class=tag id=f2 style="top:930px;left:30px;width:300px;font-size:44px;transform:rotate(-4deg)"><span class=tape style="width:110px;height:36px;top:-18px;left:40%"></span><b>02</b>one product</div>
 <div class=tag id=f3 style="top:1480px;left:560px;width:430px;font-size:44px;transform:rotate(3deg)"><span class=tape style="width:110px;height:36px;top:-18px;left:40%"></span><b>03</b>one deadline</div>
</div>
<!-- S5 rule -->
<div class=L id=s5><div class=paper></div>
 <div class=meta style="top:270px;left:72px;font-size:24px">Brand Doctor — rule Nº 02</div>
 <div class="x it" id=r1 style="top:600px;left:72px;font-size:140px;line-height:.92;color:#151515">One offer.</div>
 <div class="x an" id=r2 style="top:780px;left:72px;font-size:200px;line-height:.9;color:#151515">Said once.</div>
 <svg class=o width=1080 height=1920><path id=hb d="M-5 {Y} L 380 {Y} L 420 {Y-22} L 455 {Y+12} L 495 {Y-230} L 545 {Y+120} L 585 {Y-45} L 620 {Y} L 1085 {Y}" fill=none stroke="#C9A84C" stroke-width=7 stroke-linecap=round stroke-linejoin=round/></svg>
 <div class=x id=r3 style="top:1600px;left:72px;font-size:32px;color:#6E6A60">Egy ajánlat. Egyszer kimondva.</div>
</div>
<!-- S6 CTA -->
<div class=L id=s6><div class=paper></div>
 <div class=meta style="top:270px;left:72px;font-size:24px">Azrim Studio — Brand Doctor</div>
 <div class="x serif" id=k1 style="top:540px;left:72px;font-size:104px;line-height:.98;color:#151515">Know someone<br>designing theirs<br><span class=it>tonight?</span></div>
 <div class="x hw" id=k2 style="top:960px;left:80px;font-size:80px;transform:rotate(-3deg);color:#D8432A">send them this ↗</div>
 <div class=x id=k3 style="top:1140px;left:72px;font-family:RC;font-size:30px;letter-spacing:.04em;color:#151515">ONE BRAND FIX A DAY · @AZRIMSTUDIO_BP</div>
 <svg class=o width=1080 height=1920><path id=hb2 d="M-5 {Y} L 1085 {Y}" fill=none stroke="#C9A84C" stroke-width=7 stroke-linecap=round/></svg>
 <div class=x id=k4 style="top:1600px;left:72px;font-size:32px;color:#6E6A60">Küldd el annak, aki ma este tervezi a sajátját.</div>
 <img class="logo x" id=lg src="{LOGO}" style="top:1220px;left:72px;width:64px">
</div>
<script>
const $=id=>document.getElementById(id);
const E=t=>t<=0?0:t>=1?1:1-Math.pow(1-t,3);
const BK=t=>{{if(t<=0)return 0;if(t>=1)return 1;const c=1.70158;return 1+(c+1)*Math.pow(t-1,3)+c*Math.pow(t-1,2)}};
let T=0;
const vis=(id,a,b,f=.15)=>{{let o=0;if(T>=a&&T<b)o=Math.min(1,(T-a)/f,(b-T)/f);$(id).style.opacity=Math.max(0,o)}};
function rise(id,s,d=.45,dy=50){{const k=E((T-s)/d),el=$(id);el.style.opacity=k;el.style.translate=`0 ${{dy*(1-k)}}px`}}
function pop(id,s){{const k=BK((T-s)/.4),el=$(id);el.style.opacity=Math.min(1,Math.max(0,(T-s)/.12));el.style.scale=.6+.4*k}}
function draw(id,s,d){{const p=$(id),L=p.getTotalLength();p.style.strokeDasharray=L;p.style.strokeDashoffset=L*(1-E((T-s)/d))}}
window.setT=t=>{{T=t;
 vis('s1',-1,2.6,.1);vis('s2',2.6,5.0,.12);vis('s3',5.0,10.4,.15);vis('s4',10.4,15.4,.15);vis('s5',15.4,17.4,.2);vis('s6',17.4,99,.2);
 // S1 jitter
 const j=t<2.6?Math.sin(t*41)*6:0; document.querySelectorAll('#s1 .loud').forEach(e=>e.style.translate=`${{j}}px ${{-j/2}}px`);
 rise('h1',.15,.35,40);
 $('feed').style.translate=`0 ${{-((t-2.6)/2.4)*1900+60}}px`; rise('h2',2.8,.4,40);
 draw('c1',5.3,.35);pop('t1',5.55);draw('c2',6.6,.35);pop('t2',6.85);draw('c3',7.9,.35);pop('t3',8.15);draw('c4',9.1,.35);pop('t4',9.35);
 draw('fx',10.5,1.0);
 {{const k=E((t-11.3)/.5);$('clean').style.opacity=k;$('clean').style.scale=.92+.08*k}}
 rise('c30',11.6,.4,30);rise('cbag',11.9,.4,30);rise('cline',12.2,.4,20);rise('cdate',12.4,.4,20);
 pop('f1',12.9);pop('f2',13.6);pop('f3',14.3);
 rise('r1',15.55,.45,50);rise('r2',15.85,.4,50);draw('hb',16.0,1.0);rise('r3',16.5,.4,20);
 rise('k1',17.55,.45,50);{{const k=E((t-18.1)/.7);$('k2').style.clipPath=`inset(-30px ${{100-100*k}}% -30px 0)`}}
 rise('k3',18.6,.4,20);rise('k4',18.75,.4,20);rise('lg',18.75,.4,0);draw('hb2',17.5,.9);
}}
</script></body></html>"""

async def main(only=None):
    out = W/"fr"; out.mkdir(exist_ok=True)
    (D/"_bd02.html").write_text(html)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width":1080,"height":1920})
        await pg.goto((D/"_bd02.html").as_uri()); await pg.wait_for_timeout(800)
        frames = only if only is not None else range(int(FPS*SEC))
        for i in frames:
            await pg.evaluate(f"setT({i/FPS})")
            await pg.screenshot(path=str(out/f"f{i:04d}.jpg"), type="jpeg", quality=92)
        await b.close()
if __name__ == "__main__":
    asyncio.run(main([int(round(float(x)*FPS)) for x in sys.argv[1:]] if len(sys.argv) > 1 else None))
