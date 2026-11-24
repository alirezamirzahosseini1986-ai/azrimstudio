import numpy as np, wave
SR=44100; T=23.0; n=int(SR*T); t=np.arange(n)/SR
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
chords=[[45,57,60,64,67,71],[41,53,57,60,64,69],[48,55,60,64,67,74],[43,55,59,62,64,71],[45,57,60,64,67,71]]
pad=np.zeros(n)
for k,ch in enumerate(chords):
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
for b in np.arange(5.25,11.4,0.86): beat(b,0.55)
beat(18.6+0.35,1.0); beat(18.6+1.2,0.6)
# pen scribble on circle draws
def scrib(L=.38):
    x=rng.normal(0,1,int(L*SR)); x=x-lp(x,2500); am=0.6+0.4*np.sin(2*np.pi*14*np.arange(len(x))/SR)
    return x*am*env(.02,.05,.8,.12,L)*0.35
for a in (5.45,6.9,8.25,9.75): add(scrib(),a)
add(scrib(1.2)*.7,11.55); add(scrib(.7)*.6,20.9)
# whoosh at cuts
def whoosh(L=.5):
    x=rng.normal(0,1,int(L*SR)); y=np.zeros_like(x); acc=0; m=len(x)
    for i in range(m):
        c=300+3000*np.sin(np.pi*i/m); a=np.exp(-2*np.pi*c/SR); acc=(1-a)*x[i]+a*acc; y[i]=acc
    return y*np.sin(np.pi*np.arange(m)/m)**2*0.5
for a in (2.85,5.05,9.45,11.25,17.85,20.05): add(whoosh(),a)
# paper pop for tags
def pop(): x=np.arange(int(.06*SR))/SR; return (np.sin(2*np.pi*900*x)*np.exp(-x*90)+rng.normal(0,.3,len(x))*np.exp(-x*120))*0.35
for a in (5.75,7.2,8.5,10.05,13.1,14.1,15.1,16.1,12.75): add(pop(),a)
out*=np.clip(t/0.15,0,1)*np.clip((T-t)/1.2,0,1)
out=out/np.max(np.abs(out))*0.89
w=wave.open('/home/claude/work/bd/bed.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
