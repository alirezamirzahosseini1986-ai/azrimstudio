import numpy as np, wave
SR=44100; T=45.0; n=int(SR*T); t=np.arange(n)/SR
rng=np.random.default_rng(7)
out=np.zeros(n)
def env(a,d,s,r,L):
    x=np.arange(int(L*SR))/SR; e=np.ones_like(x)*s
    e[x<a]=x[x<a]/a; m=(x>=a)&(x<a+d); e[m]=1-(1-s)*(x[m]-a)/d
    e[x>L-r]*=np.clip((L-x[x>L-r])/r,0,1); return e
def lp(x,c):  # one-pole lowpass
    a=np.exp(-2*np.pi*c/SR); y=np.zeros_like(x); acc=0.0
    for i in range(len(x)): acc=(1-a)*x[i]+a*acc; y[i]=acc
    return y
def add(sig,at,g=1.0):
    i=int(at*SR); j=min(n,i+len(sig)); out[i:j]+=g*sig[:j-i]
# pad: Am9 - Fmaj7 - C(add9) - G6 , 5.5s each, soft detuned sines
f=lambda m:440*2**((m-69)/12)
chords=[[45,57,60,64,67,71],[41,53,57,60,64,69],[48,55,60,64,67,74],[43,55,59,62,64,71]]*2+[[45,57,60,64,67,71]]
pad=np.zeros(n)
for k,ch in enumerate(chords):
    if k*5.5>=T: break
    L=5.9; x=np.arange(int(L*SR))/SR; s=np.zeros_like(x)
    for m in ch:
        for det in (-0.12,0.12):
            s+=np.sin(2*np.pi*f(m+det/1)*x+rng.uniform(0,6))*(0.5 if m<50 else 0.22)
    s*=env(1.2,0.5,0.9,1.4,L); i=int(k*5.5*SR); j=min(n,i+len(s)); pad[i:j]+=s[:j-i]
pad*=0.10*(1+0.15*np.sin(2*np.pi*0.25*t))
# soft vinyl-ish noise bed
bed=lp(rng.normal(0,1,n),900)*0.015
out+=pad+bed
# heartbeat
def thump(fr=55,L=.22,g=1):
    x=np.arange(int(L*SR))/SR; return g*np.sin(2*np.pi*(fr+40*np.exp(-x*30))*x)*np.exp(-x*18)
def beat(at,g=1): add(thump(58,.25,g),at); add(thump(52,.22,.7*g),at+.24)
def tick(g=.25):
    x=np.arange(int(.03*SR))/SR; return g*(np.sin(2*np.pi*2400*x)*np.exp(-x*300))
for b in np.arange(0,40,1.0): add(tick(.22 if int(b)%2 else .3),b)
def chime():
    x=np.arange(int(1.6*SR))/SR; return .35*sum(np.sin(2*np.pi*f*x)*np.exp(-x*(2.5+i)) for i,f in enumerate((880,1318.5,1760)))
add(chime(),40.1)

# pen scribble on circle draws
def scrib(L=.38):
    x=rng.normal(0,1,int(L*SR)); x=x-lp(x,2500); am=0.6+0.4*np.sin(2*np.pi*14*np.arange(len(x))/SR)
    return x*am*env(.02,.05,.8,.12,L)*0.35
for a in (7.0,7.6,14.4,28.8,29.3,29.9): add(scrib(),a)
add(scrib(1.4)*.7,20.4); add(scrib(1.4)*.5,41.2)
# whoosh at cuts
def whoosh(L=.5):
    x=rng.normal(0,1,int(L*SR)); y=np.zeros_like(x); acc=0; m=len(x)
    for i in range(m):
        c=300+3000*np.sin(np.pi*i/m); a=np.exp(-2*np.pi*c/SR); acc=(1-a)*x[i]+a*acc; y[i]=acc
    return y*np.sin(np.pi*np.arange(m)/m)**2*0.5
for a in (4.35,10.85,17.85,25.85,32.85,39.85): add(whoosh(),a)
# paper pop for tags
def pop(): x=np.arange(int(.06*SR))/SR; return (np.sin(2*np.pi*900*x)*np.exp(-x*90)+rng.normal(0,.3,len(x))*np.exp(-x*120))*0.35
for a in (1.0,5.3,5.8,11.7,12.3,12.9,26.7,27.1,27.5,33.7,34.9,36.3): add(pop(),a)
out*=np.clip(t/0.15,0,1)*np.clip((T-t)/1.2,0,1)
out=out/np.max(np.abs(out))*0.89
w=wave.open('/home/claude/work/l01/bed.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
