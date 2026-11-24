"""Brand Doctor Nº01 — V51 Café reel (22s, 1080x1920, 30fps). Renders frames to /home/claude/work/bd/fr/"""
import asyncio, pathlib, sys
from playwright.async_api import async_playwright
D = pathlib.Path(__file__).parent
W = pathlib.Path("/home/claude/work/bd")
LOGO = pathlib.Path("/home/claude/azrimstudio/img/logo.png").as_uri()
FPS, SEC = 30, 23
Y = 1536
U = lambda p: (W/p).as_uri()
INS = [U(f"in/{i:03d}.jpg") for i in range(1, 92)]
EXS = [U(f"ex/{i:03d}.jpg") for i in range(1, 68)]
# heartbeat thread for the rule card
HB = f"M-5 {Y} L 380 {Y} L 420 {Y-22} L 455 {Y+12} L 495 {Y-230} L 545 {Y+120} L 585 {Y-45} L 620 {Y} L 1085 {Y}"
# fix scene: thread from the left edge up to a blade sign hanging off the wall
FIX = (f"M-5 {Y} L 180 {Y} C 250 {Y}, 245 1300, 245 1000 L 245 640 "
       f"A 118 118 0 1 1 245 641 "          # full circle round disc centre (363,640)
       f"M 363 522 L 363 468 L 552 468")    # hanger + bracket into the wall
html = f"""<!doctype html><html><head><link rel=stylesheet href="v2.css"><style>
html,body{{width:1080px;height:1920px;background:#000}}
.x{{position:absolute}} .L{{position:absolute;inset:0;opacity:0}}
#bgw{{position:absolute;inset:0;overflow:hidden}} #bg{{width:1080px;height:1920px;object-fit:cover;transform-origin:50% 50%}}
.shade{{position:absolute;left:0;right:0;bottom:0;height:1100px;background:linear-gradient(transparent,rgba(10,10,10,.82) 55%,rgba(10,10,10,.9))}}
.top{{position:absolute;left:0;right:0;top:0;height:520px;background:linear-gradient(rgba(10,10,10,.55),transparent)}}
.w{{color:#F4F1EA}}
.pillw{{display:inline-block;font-family:RC;font-size:24px;text-transform:uppercase;letter-spacing:.08em;border:2px solid #F4F1EA;color:#F4F1EA;border-radius:999px;padding:10px 24px;background:rgba(0,0,0,.25)}}
.tag{{position:absolute;z-index:5;background:#F6F2E8;color:#151515;font-family:HW;font-weight:600;line-height:1.02;padding:18px 26px 20px;box-shadow:0 14px 30px -12px rgba(0,0,0,.55)}}
.tag b{{font-family:RC;font-weight:700;font-size:22px;letter-spacing:.06em;display:block;margin-bottom:6px;color:#D8432A}}
.tag .tape{{width:130px;height:40px;top:-20px;left:50%;margin-left:-65px;transform:rotate(-3deg)}}
.pol{{position:absolute;z-index:5;background:#FBFAF6;padding:18px 18px 104px;box-shadow:0 22px 40px -14px rgba(0,0,0,.6)}}
.pol img{{display:block;object-fit:cover}}
.pol .cap{{position:absolute;left:14px;right:14px;bottom:12px;text-align:center;font-family:HW;font-weight:600;font-size:38px;line-height:1;color:#151515}}
.paper{{position:absolute;inset:0;background:var(--paper)}}
.paper:after{{content:"";position:absolute;inset:0;pointer-events:none;mix-blend-mode:multiply;opacity:.55;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .5  0 0 0 0 .47  0 0 0 0 .42  0 0 0 .55 0'/></filter><rect width='400' height='400' filter='url(%23n)'/></svg>")}}
svg.o{{position:absolute;inset:0;z-index:4}}
</style></head><body>
<div id=bgw><img id=bg src="{INS[0]}"></div>
<div class=top id=topsh></div>

<!-- S1 inside -->
<div class=L id=s1><div class=shade></div>
 <div class=x style="top:250px;left:72px"><span class=pillw>Brand Doctor · Nº 01</span></div>
 <div class="x it w" id=s1a style="top:1080px;left:72px;font-size:150px;line-height:.9">Inside:</div>
 <div class="x serif w" id=s1b style="top:1250px;left:72px;font-size:74px;line-height:1.02;width:900px">one of the cosiest rooms<br>in Budapest.</div>
</div>
<!-- S2 outside -->
<div class=L id=s2><div class=shade></div>
 <div class=x style="top:250px;left:72px"><span class=pillw>Brand Doctor · Nº 01</span></div>
 <div class="x it w" id=s2a style="top:1080px;left:72px;font-size:150px;line-height:.9">Outside:</div>
 <div class="x serif w" id=s2b style="top:1250px;left:72px;font-size:74px;line-height:1.02;width:900px">you’d walk right past it.</div>
</div>
<!-- S3 diagnosis on b2 -->
<div class=L id=s3>
 <div class=x style="top:250px;left:72px"><span class=pillw style="border-color:#D8432A;color:#fff;background:#D8432A">Diagnosis</span></div>
 <svg class=o width=1080 height=1920>
  <ellipse id=c1 cx=690 cy=828 rx=175 ry=335 fill=none stroke="#D8432A" stroke-width=9 transform="rotate(-3 690 828)"/>
  <ellipse id=c2 cx=740 cy=1345 rx=165 ry=205 fill=none stroke="#D8432A" stroke-width=9 transform="rotate(4 740 1345)"/>
  <ellipse id=c3 cx=990 cy=470 rx=150 ry=125 fill=none stroke="#D8432A" stroke-width=9 transform="rotate(-6 990 470)"/>
 </svg>
 <div class=tag id=t1 style="top:600px;left:60px;width:440px;font-size:50px;transform:rotate(-3deg)"><span class=tape></span><b>01</b>flat on the wall — invisible from down the street</div>
 <div class=tag id=t2 style="top:1290px;left:60px;width:470px;font-size:50px;transform:rotate(2deg)"><span class=tape></span><b>02</b>chalk too faint to read from 3&nbsp;m</div>
 <div class=tag id=t3 style="top:320px;left:300px;width:460px;font-size:50px;transform:rotate(-2deg)"><span class=tape></span><b>03</b>two names, two colours — which one is the café?</div>
</div>
<!-- S3b window close-up -->
<div class=L id=s3b>
 <div class=x style="top:250px;left:72px"><span class=pillw style="border-color:#D8432A;color:#fff;background:#D8432A">Diagnosis</span></div>
 <svg class=o width=1080 height=1920><ellipse id=c4 cx=545 cy=1092 rx=490 ry=175 fill=none stroke="#D8432A" stroke-width=9 transform="rotate(-2 540 1020)"/></svg>
 <div class=tag id=t4 style="top:1290px;left:120px;width:760px;font-size:62px;transform:rotate(-2deg)"><span class=tape></span><b>04</b>20+ words. 6 colours.<br>Zero focus.</div>
</div>
<!-- S4 the fix -->
<div class=L id=s4>
 <div class=x style="top:250px;left:72px"><span class=pillw style="border-color:#C9A84C;color:#151515;background:#C9A84C">The fix</span></div>
 <div class=x id=disc style="left:245px;top:522px;width:236px;height:236px;border-radius:50%;background:#E8C547;display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 18px 34px -12px rgba(0,0,0,.6);opacity:0">
  <div class=an style="font-size:104px;color:#1F3B2D;line-height:.9">V51</div><div class=it style="font-size:46px;color:#1F3B2D;margin-top:-4px">café</div></div>
 <svg class=o width=1080 height=1920><path id=fx d="{FIX}" fill=none stroke="#C9A84C" stroke-width=9 stroke-linecap=round stroke-linejoin=round/></svg>
 <div class=tag id=f1 style="top:820px;left:60px;width:430px;font-size:48px;transform:rotate(-2deg)"><span class=tape></span><b>01</b>a sign that sticks out — seen from 30&nbsp;m</div>
 <div class=pol id=f2 style="top:1000px;left:560px;transform:rotate(4deg)"><img src="{U('inside_still.jpg')}" style="width:400px;height:330px;object-position:50% 38%"><div class=cap><span style="font-family:RC;font-weight:700;font-size:20px;color:#D8432A">02</span> put the inside<br>on the A-board</div></div>
 <div class=tag id=f3 style="top:1150px;left:50px;width:470px;font-size:48px;transform:rotate(2deg)"><span class=tape></span><b>03</b>window: 3 words, not 20<br><span style="font-family:IS;font-style:italic;font-weight:400;font-size:52px">kávé · reggeli · leves</span></div>
 <div class=tag id=f4 style="top:290px;left:330px;width:470px;font-size:44px;transform:rotate(-2deg)"><span class=tape></span><b>04</b>one lead name outside — the second brand sits under it</div>
</div>
<!-- S5 rule -->
<div class=L id=s5><div class=paper></div>
 <div class="meta" style="top:270px;left:72px;font-size:24px">Brand Doctor — rule Nº 01</div>
 <div class="x it" id=r1 style="top:620px;left:72px;font-size:150px;line-height:.92;color:#151515">Show the<br>inside,</div>
 <div class="x an" id=r2 style="top:930px;left:72px;font-size:230px;color:#151515">outside.</div>
 <svg class=o width=1080 height=1920><path id=hb d="{HB}" fill=none stroke="#C9A84C" stroke-width=7 stroke-linecap=round stroke-linejoin=round/></svg>
 <div class=x id=r3 style="top:1600px;left:72px;font-size:32px;color:#6E6A60">Mutasd meg kívül, ami belül van.</div>
</div>
<!-- S6 CTA -->
<div class=L id=s6><div class=paper></div>
 <div class="meta" style="top:270px;left:72px;font-size:24px">Azrim Studio — Brand Doctor</div>
 <div class="x serif" id=k1 style="top:560px;left:72px;font-size:120px;line-height:.95;color:#151515">Your shopfront<br><span class=it>next?</span></div>
 <div class="x hw" id=k2 style="top:900px;left:80px;font-size:84px;transform:rotate(-3deg)">comment your street ↓</div>
 <div class=x id=k3 style="top:1100px;left:72px;font-family:RC;font-size:30px;letter-spacing:.04em;color:#151515">ONE BRAND FIX A DAY · @AZRIMSTUDIO_BP</div>
 <svg class=o width=1080 height=1920><path id=hb2 d="M-5 {Y} L 1085 {Y}" fill=none stroke="#C9A84C" stroke-width=7 stroke-linecap=round/></svg>
 <div class=x id=k4 style="top:1600px;left:72px;font-size:32px;color:#6E6A60">Melyik utcában vagy? Írd meg kommentben.</div>
 <img class="logo x" id=lg src="{LOGO}" style="top:1180px;left:72px;width:64px">
</div>
<script>
const INS={INS!r}, EXS={EXS!r}, B2="{U('b2.png')}", B1="{U('b1.png')}";
const $=id=>document.getElementById(id);
const E=t=>t<=0?0:t>=1?1:1-Math.pow(1-t,3);
const BK=t=>{{if(t<=0)return 0;if(t>=1)return 1;const c=1.70158;return 1+(c+1)*Math.pow(t-1,3)+c*Math.pow(t-1,2)}};
const vis=(id,a,b,f=.18)=>{{let o=0;if(T>=a&&T<b)o=Math.min(1,(T-a)/f,(b-T)/f);$(id).style.opacity=Math.max(0,o)}};
function rise(id,s,dur=.45,dy=50){{const k=E((T-s)/dur),el=$(id);el.style.opacity=k;el.style.translate=`0 ${{dy*(1-k)}}px`}}
function pop(id,s,r=0){{const k=BK((T-s)/.4),el=$(id);el.style.opacity=Math.min(1,Math.max(0,(T-s)/.12));el.style.scale=.6+.4*k}}
function draw(id,s,dur){{const p=$(id),L=p.getTotalLength();p.style.strokeDasharray=L;p.style.strokeDashoffset=L*(1-E((T-s)/dur))}}
let T=0;
window.setT=async function(t){{T=t;const bg=$('bg');let src,sc=1,ox='50% 50%',filt='none';
 if(t<3.0){{src=INS[Math.min(90,Math.floor(t*30))]}}
 else if(t<5.2){{src=EXS[Math.min(66,Math.floor((t-3)*30))]}}
 else if(t<9.6){{src=B2;sc=1+.04*(t-5.2)/4.4;filt='brightness(.82)'}}
 else if(t<11.4){{src=B1;sc=2.1+.08*(t-9.6)/1.8;ox='35% 56%';filt='brightness(.85)'}}
 else {{src=B2;sc=1.0;filt='saturate(.55) brightness(.9)'}}
 bg.style.transform=`scale(${{sc}})`;bg.style.transformOrigin=ox;bg.style.filter=filt;
 if(bg.getAttribute('src')!==src){{bg.setAttribute('src',src);await bg.decode()}}
 $('topsh').style.opacity=t<11.4?1:.8;
 vis('s1',-1,3.0,.12);vis('s2',3.0,5.2,.12);vis('s3',5.2,9.6,.15);vis('s3b',9.6,11.4,.12);vis('s4',11.4,18.0,.15);vis('s5',18.0,20.2,.2);vis('s6',20.2,99,.2);
 rise('s1a',0,.35,40);rise('s1b',.25,.4,40);
 rise('s2a',3.05,.35,40);rise('s2b',3.35,.4,40);
 draw('c1',5.45,.4);pop('t1',5.75);
 draw('c2',6.9,.4);pop('t2',7.2);
 draw('c3',8.25,.4);pop('t3',8.5);
 draw('c4',9.75,.4);pop('t4',10.05);
 draw('fx',11.55,1.3);{{const k=E((T-12.75)/.4);$('disc').style.opacity=k;$('disc').style.scale=.85+.15*k}}
 pop('f1',13.1);pop('f2',14.1);pop('f3',15.1);pop('f4',16.1);
 rise('r1',18.15,.45,50);rise('r2',18.45,.4,50);draw('hb',18.6,1.0);rise('r3',19.2,.4,20);
 rise('k1',20.35,.45,50);{{const k=E((T-20.9)/.7);$('k2').style.clipPath=`inset(-30px ${{100-100*k}}% -30px 0)`}}
 rise('k3',21.4,.4,20);rise('k4',21.6,.4,20);rise('lg',21.6,.4,0);draw('hb2',20.3,.9);
 if(T>21.8){{$('k2').style.translate=`0 ${{6*Math.sin((T-21.8)*5)}}px`}}
}}
</script></body></html>"""

async def main(only=None):
    out = W/"fr"; out.mkdir(exist_ok=True)
    (D/"_bd01.html").write_text(html)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width":1080,"height":1920})
        await pg.goto((D/"_bd01.html").as_uri()); await pg.wait_for_timeout(800)
        frames = only if only is not None else range(FPS*SEC)
        for i in frames:
            await pg.evaluate(f"setT({i/FPS})")
            await pg.screenshot(path=str(out/f"f{i:04d}.jpg"), type="jpeg", quality=92)
        await b.close()
if __name__ == "__main__":
    if len(sys.argv) > 1:
        asyncio.run(main([int(round(float(x)*FPS)) for x in sys.argv[1:]]))
    else:
        asyncio.run(main())
