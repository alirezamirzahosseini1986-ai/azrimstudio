"""Logo in 60 Seconds Nº01 — café 'Kanál' (fictional). Reel 45s 1080x1920 30fps → /home/claude/work/l01/fr/"""
import asyncio, pathlib, sys
from playwright.async_api import async_playwright
D = pathlib.Path(__file__).parent
W = pathlib.Path("/home/claude/work/l01"); W.mkdir(parents=True, exist_ok=True)
LOGO = pathlib.Path("/home/claude/azrimstudio/img/logo.png").as_uri()
FPS, SEC, Y = 30, 45, 1536
TERRA, CREAM, INK, GOLD, RED = "#B9502C", "#F3E9DA", "#151515", "#C9A84C", "#D8432A"
# spoon as an acute accent: bowl + handle, drawn in local 0..100 box
SPOON = "M30 78 C 18 92, 2 88, 4 74 C 6 60, 24 56, 32 66 C 36 71, 34 76, 30 78 Z M31 68 L 88 8"


def wm(size, col, spcol, sid="", acc=False):
    sw = .42*size
    spoon = f'<svg {('id='+sid) if sid else ''} style="position:absolute;left:{.08*size:.0f}px;top:{-.15*size:.0f}px;overflow:visible" width={sw:.0f} height={sw:.0f} viewBox="0 0 100 100"><path {('id='+sid+'p') if sid else ''} d="{SPOON}" fill="{'none' if sid else spcol}" stroke="{spcol}" stroke-width={9 if sid else 8} stroke-linecap=round stroke-linejoin="round"/></svg>'
    bar = f'<div id=dacc style="position:absolute;left:{.17*size:.0f}px;top:{.10*size:.0f}px;width:{.16*size:.0f}px;height:{.045*size:.0f}px;background:{col};transform:rotate(-55deg)"></div>' if acc else ''
    return f'<span style="font-family:IS;font-size:{size}px;line-height:1;color:{col};position:relative;white-space:nowrap;display:inline-block">kan<span style="position:relative;display:inline-block">a{bar}{spoon}</span>l</span>'

html = f"""<!doctype html><html><head><link rel=stylesheet href="v2.css"><style>
html,body{{width:1080px;height:1920px;overflow:hidden}}
.x{{position:absolute}} .L{{position:absolute;inset:0;opacity:0}}
#base{{position:absolute;inset:0;background:var(--paper)}}
.timer{{position:absolute;top:230px;right:72px;font-family:RC;font-size:44px;letter-spacing:.04em;z-index:20;background:{INK};color:{CREAM};padding:8px 20px;border-radius:12px}}
.step{{position:absolute;top:240px;left:72px;font-family:RC;font-size:24px;letter-spacing:.08em;text-transform:uppercase;z-index:20}}
.h{{font-family:IS;font-style:italic;font-size:92px;line-height:.98}}
.card{{position:absolute;background:#FBFAF6;box-shadow:0 24px 44px -18px rgba(0,0,0,.35)}}
.word{{font-family:IS;font-size:250px;line-height:1;color:{INK};letter-spacing:-.01em}}
svg.o{{position:absolute;inset:0;z-index:10;pointer-events:none}}
</style></head><body>
<div id=base></div>
<div class=timer id=tm>00:00</div>
<div class=step id=st></div>

<!-- S1 hook + brief -->
<div class=L id=s1>
 <div class="x an" id=a1 style="top:420px;left:72px;font-size:150px;line-height:.9">A café logo</div>
 <div class="x it" id=a2 style="top:570px;left:72px;font-size:120px">in 60 seconds.</div>
 <div class=card id=a3 style="top:860px;left:110px;width:860px;padding:44px 50px;transform:rotate(-2deg)">
  <div class=meta style="position:static;color:#8b867b">The brief</div>
  <div style="font-size:46px;line-height:1.3;margin-top:18px"><b>Kanál</b> <span style="color:#8b867b">(“spoon”)</span><br>a small café in District VII<br>warm · modern · <span style="color:{RED}">no clichés</span></div>
  <div class=meta style="position:static;color:#b0aa9d;margin-top:22px;font-size:18px">fictional café — design demo</div></div>
</div>
<!-- S2 no clichés -->
<div class=L id=s2>
 <div class="x h" id=b0 style="top:380px;left:72px">First, what it<br>won’t be.</div>
 <div class=card id=b1 style="top:700px;left:90px;width:420px;height:420px;display:flex;align-items:center;justify-content:center;transform:rotate(-3deg)">
  <svg width=240 height=240 viewBox="0 0 100 100"><ellipse cx=50 cy=50 rx=28 ry=40 fill="#6b4a2f" transform="rotate(30 50 50)"/><path d="M38 22 C 56 40, 44 60, 62 78" stroke="#FBFAF6" stroke-width=5 fill="none"/></svg>
  <div class=meta style="bottom:24px;left:24px;color:#8b867b">bean</div></div>
 <div class=card id=b2 style="top:720px;left:570px;width:420px;height:420px;display:flex;align-items:center;justify-content:center;transform:rotate(3deg)">
  <svg width=260 height=260 viewBox="0 0 100 100"><path d="M24 50 L 76 50 L 70 86 L 30 86 Z" fill="#6b4a2f"/><path d="M76 56 C 92 56, 92 74, 72 74" stroke="#6b4a2f" stroke-width=6 fill="none"/><path d="M40 40 C 34 30, 46 24, 40 12 M54 40 C 48 30, 60 24, 54 12" stroke="#9a958a" stroke-width=4 fill=none stroke-linecap="round"/></svg>
  <div class=meta style="bottom:24px;left:24px;color:#8b867b">steaming cup</div></div>
 <svg class=o width=1080 height=1920><path id=x1 d="M110 720 L 490 1100 M 490 720 L 110 1100" stroke="{RED}" stroke-width=14 stroke-linecap=round fill="none"/><path id=x2 d="M590 740 L 970 1120 M 970 740 L 590 1120" stroke="{RED}" stroke-width=14 stroke-linecap=round fill="none"/></svg>
 <div class="x hw" id=b3 style="top:1220px;left:120px;font-size:62px;color:{RED};transform:rotate(-3deg)">seen them a thousand times</div>
</div>
<!-- S3 type -->
<div class=L id=s3>
 <div class="x h" id=c0 style="top:380px;left:72px">Then the letters.</div>
 <div class="x" id=c1 style="top:620px;left:90px;font-family:AN;font-size:170px;color:#a9a397">KANÁL</div>
 <div class="x" id=c2 style="top:860px;left:90px;font-family:IT;font-weight:800;font-size:170px;color:#a9a397">Kanál</div>
 <div class="x" id=c3 style="top:1090px;left:90px;font-family:IS;font-size:190px;color:{INK}">kanál</div>
 <svg class=o width=1080 height=1920><ellipse id=c4 cx=330 cy=1200 rx=320 ry=130 fill=none stroke="{RED}" stroke-width=9 transform="rotate(-3 330 1200)"/></svg>
 <div class="x hw" id=c5 style="top:1120px;left:680px;font-size:58px;color:{RED};transform:rotate(-5deg)">soft, a bit old-school</div>
</div>
<!-- S4 the idea: accent becomes spoon -->
<div class=L id=s4>
 <div class="x h" id=d0 style="top:380px;left:72px">The idea is<br>already in the name.</div>
 <div class="x" id=dw style="top:860px;left:150px">{wm(260, INK, TERRA, "dsp", True)}</div>
 <div class="x hw" id=d1 style="top:640px;left:350px;font-size:60px;color:{RED};transform:rotate(-4deg)">the accent… is a spoon</div>
</div>
<!-- S5 colour -->
<div class=L id=s5>
 <div class="x h" id=e0 style="top:380px;left:72px">Colour: warm,<br>not brown.</div>
 {''.join(f'<div class=x id=e{i+1} style="top:{690+i*250}px;left:90px;display:flex;gap:0;box-shadow:0 18px 30px -14px rgba(0,0,0,.35)">' + ''.join(f'<div style="width:300px;height:190px;background:{c}"></div>' for c in pal) + '</div>' for i, pal in enumerate([["#4b3626", "#c8a77e", "#efe4d2"], ["#1f3b2d", "#e8c547", "#f6f2e8"], [TERRA, CREAM, INK]]))}
 <svg class=o width=1080 height=1920><path id=etick d="M960 1300 C 975 1315, 985 1330, 992 1345 C 1010 1300, 1030 1270, 1055 1245" stroke="{RED}" stroke-width=10 fill=none stroke-linecap="round"/><path id=ex1 d="M960 770 L 1040 850 M 1040 770 L 960 850" stroke="{RED}" stroke-width=9 fill=none stroke-linecap="round"/><path id=ex2 d="M960 1020 L 1040 1100 M 1040 1020 L 960 1100" stroke="{RED}" stroke-width=9 fill=none stroke-linecap="round"/></svg>
 <div class="x hw" id=e4 style="top:1460px;left:120px;font-size:56px;color:{RED};transform:rotate(-3deg)">terracotta = clay cups, not coffee</div>
</div>
<!-- S6 mockups -->
<div class=L id=s6 style="background:{CREAM}">
 <div class="x h" id=f0 style="top:380px;left:72px;color:{INK}">Does it work<br>everywhere?</div>
 <!-- cup -->
 <div class=x id=f1 style="top:680px;left:90px;width:420px;height:560px">
  <div style="position:absolute;top:0;left:20px;width:380px;height:50px;background:#e9e2d4;border-radius:10px"></div>
  <div style="position:absolute;top:44px;left:40px;width:340px;height:500px;background:{TERRA};clip-path:polygon(0 0,100% 0,88% 100%,12% 100%);display:flex;align-items:center;justify-content:center">
   {wm(110, CREAM, CREAM)}</div></div>
 <!-- avatar -->
 <div class=x id=f2 style="top:700px;left:600px;width:380px;height:380px;border-radius:50%;background:{TERRA};display:flex;align-items:center;justify-content:center;box-shadow:0 20px 40px -16px rgba(0,0,0,.4)">
  <svg width=210 height=210 viewBox="0 0 100 100"><path d="{SPOON}" fill={CREAM} stroke={CREAM} stroke-width=6 stroke-linecap="round"/></svg></div>
 <div class=meta id=f2l style="top:1100px;left:700px;color:#6e6a60">profile picture</div>
 <!-- sign -->
 <div class=x id=f3 style="top:1220px;left:560px;width:440px;height:170px;background:{INK};display:flex;align-items:center;justify-content:center;transform:rotate(2deg);box-shadow:0 20px 40px -16px rgba(0,0,0,.5)">
  {wm(100, CREAM, TERRA)}</div>
 <div class=meta id=f3l style="top:1420px;left:700px;color:#6e6a60">street sign</div>
</div>
<!-- S7 reveal + CTA -->
<div class=L id=s7 style="background:{TERRA}">
 <div class="x" id=g1 style="top:560px;left:0;right:0;text-align:center">{wm(280, CREAM, CREAM)}</div>
 <div class=meta id=g2 style="top:880px;left:0;right:0;text-align:center;color:{CREAM};opacity:.8;font-size:24px">kávézó · budapest VII</div>
 <div class="x serif" id=g3 style="top:1080px;left:72px;font-size:84px;line-height:1;color:{CREAM}">Want one for <span class=it>yours?</span></div>
 <div class="x an" id=g4 style="top:1200px;left:72px;font-size:120px;color:{INK}">Comment LOGO</div>
 <svg class=o width=1080 height=1920><path id=sw d="M-5 {Y} L 720 {Y} C 735 {Y}, 746 1528, 752 1520 M 850 1400 A 100 100 0 1 1 849.9 1400 M 850 1500 L 850 1440 M 850 1500 L 892 1522 M 828 1372 L 872 1372 M 850 1372 L 850 1400 M 948 1520 C 954 1528, 990 {Y}, 1085 {Y}" stroke="{GOLD}" stroke-width=7 fill=none stroke-linecap="round"/></svg>
 <div class=x id=g5 style="top:1640px;left:72px;font-size:30px;color:{CREAM};opacity:.85">Írd kommentbe: LOGO. · @azrimstudio_bp</div>
</div>
<script>
const $=id=>document.getElementById(id);
const E=t=>t<=0?0:t>=1?1:1-Math.pow(1-t,3);
const BK=t=>{{if(t<=0)return 0;if(t>=1)return 1;const c=1.70158;return 1+(c+1)*Math.pow(t-1,3)+c*Math.pow(t-1,2)}};
let T=0;
const vis=(id,a,b,f=.2)=>{{let o=0;if(T>=a&&T<b)o=Math.min(1,(T-a)/f,(b-T)/f);$(id).style.opacity=Math.max(0,o)}};
function rise(id,s,d=.45,dy=50){{const k=E((T-s)/d),el=$(id);el.style.opacity=k;el.style.translate=`0 ${{dy*(1-k)}}px`}}
function pop(id,s){{const k=BK((T-s)/.4),el=$(id);el.style.opacity=Math.min(1,Math.max(0,(T-s)/.12));el.style.scale=.7+.3*k}}
function draw(id,s,d){{const p=$(id),L=p.getTotalLength();p.style.strokeDasharray=L;p.style.strokeDashoffset=L*(1-E((T-s)/d))}}
const steps=[[0,'Brief'],[4.5,'Step 1 · kill the clichés'],[11,'Step 2 · type'],[18,'Step 3 · the idea'],[26,'Step 4 · colour'],[33,'Step 5 · test it'],[40,'Done']];
window.setT=t=>{{T=t;
 const s=Math.floor(t);$('tm').textContent='00:'+String(s).padStart(2,'0');
 let lab='';for(const [a,b] of steps) if(t>=a) lab=b; $('st').textContent=lab;
 const dark=(t>=40);$('tm').style.background=dark?'{CREAM}':'{INK}';$('tm').style.color=dark?'{TERRA}':'{CREAM}';$('st').style.color=dark?'{CREAM}':'{INK}';
 vis('s1',-1,4.5);vis('s2',4.5,11);vis('s3',11,18);vis('s4',18,26);vis('s5',26,33);vis('s6',33,40);vis('s7',40,99);
 rise('a1',.1,.35,40);rise('a2',.35,.35,40);pop('a3',1.0);
 rise('b0',4.6);pop('b1',5.3);pop('b2',5.8);draw('x1',7.0,.5);draw('x2',7.6,.5);rise('b3',8.4,.4,20);
 rise('c0',11.1);rise('c1',11.7,.35,30);rise('c2',12.3,.35,30);rise('c3',12.9,.35,30);draw('c4',14.4,.5);rise('c5',15.2,.4,20);
 rise('d0',18.1);rise('dw',18.6,.4,30);
 {{const k=E((t-20.2)/.5);$('dacc').style.opacity=t<18.6?0:(1-k);}}
 {{const p=$('dspp'),L=p.getTotalLength();p.style.strokeDasharray=L;p.style.strokeDashoffset=L*(1-E((t-20.4)/1.4));p.style.fill=t>21.9?'{TERRA}':'none';}}rise('d1',22.4,.4,20);
 rise('e0',26.1);pop('e1',26.7);pop('e2',27.1);pop('e3',27.5);draw('ex1',28.8,.35);draw('ex2',29.3,.35);draw('etick',29.9,.4);rise('e4',30.6,.4,20);
 rise('f0',33.1);pop('f1',33.7);pop('f2',34.9);rise('f2l',35.3,.3,10);pop('f3',36.3);rise('f3l',36.7,.3,10);
 {{const k=BK((t-40.1)/.6);$('g1').style.opacity=Math.min(1,(t-40.1)/.2);$('g1').style.scale=.85+.15*k}}rise('g2',40.7,.4,20);rise('g3',41.6,.45,40);rise('g4',42.1,.45,40);draw('sw',41.2,1.6);rise('g5',42.8,.4,20);
 if(t>43.2)$('g4').style.translate=`0 ${{5*Math.sin((t-43.2)*5)}}px`;
}}
</script></body></html>"""

async def main(only=None):
    out = W/"fr"; out.mkdir(exist_ok=True)
    (D/"_l01.html").write_text(html)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width":1080,"height":1920})
        await pg.goto((D/"_l01.html").as_uri()); await pg.wait_for_timeout(800)
        frames = only if only is not None else range(int(FPS*SEC))
        for i in frames:
            await pg.evaluate(f"setT({i/FPS})")
            await pg.screenshot(path=str(out/f"f{i:04d}.jpg"), type="jpeg", quality=92)
        await b.close()
if __name__ == "__main__":
    asyncio.run(main([int(round(float(x)*FPS)) for x in sys.argv[1:]] if len(sys.argv) > 1 else None))
