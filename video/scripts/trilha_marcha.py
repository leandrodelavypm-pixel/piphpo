import numpy as np, wave
sr=44100; T=80.0; N=int(sr*T); out=np.zeros(N); rng=np.random.default_rng(7)
BPM=120; B=60/BPM
def hz(m): return 440*2**((m-69)/12)
def add(sig,t0,g=1.0):
    i=int(t0*sr); j=min(N,i+len(sig))
    if i<N and j>i: out[i:j]+=g*sig[:j-i]
def hp(x): y=np.diff(x,prepend=0); return y
def brass(m,dur,vel=1.0):
    n=int(sr*(dur+0.2)); t=np.arange(n)/sr; f=hz(m)
    vib=1+0.004*np.sin(2*np.pi*5.5*t)*np.clip((t-0.15)/0.3,0,1)
    bright=0.35+0.65*np.clip(t/0.06,0,1)*np.exp(-t*1.2)+0.25
    s=np.zeros(n)
    for det in (-0.08,0.0,0.08):
        ph=2*np.pi*f*(1+det/100*10)*np.cumsum(vib)/sr
        for k in range(1,14):
            s+=np.sin(k*ph)/k*np.exp(-(k-1)*(1.1-bright*0.8)*0.45)
    env=np.clip(t/0.035,0,1)*np.clip((dur+0.2-t)/0.2,0,1)
    return s*env*vel/3
def chord(ms,t0,dur,g):
    for m in ms: add(brass(m,dur),t0,g/len(ms)**0.6)
def snare(g=1.0):
    n=int(sr*0.25); t=np.arange(n)/sr
    nz=hp(hp(rng.standard_normal(n)))*0.35
    return (nz*np.exp(-t*22)+0.6*np.sin(2*np.pi*185*t)*np.exp(-t*35))*g
def kick():
    n=int(sr*0.45); t=np.arange(n)/sr; f=50+80*np.exp(-t*25)
    return np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-t*7)*1.4
def timp(m=38,dec=1.6):
    n=int(sr*2.5); t=np.arange(n)/sr; f=hz(m)
    return (np.sin(2*np.pi*f*t)+0.5*np.sin(2*np.pi*f*1.5*t)*np.exp(-t*3)+0.2*rng.standard_normal(n)*np.exp(-t*40))*np.exp(-t*dec)*1.3
def crash(g=0.5):
    n=int(sr*2.5); t=np.arange(n)/sr
    return hp(rng.standard_normal(n))*np.exp(-t*1.6)*g
def roll(t0,t1,g0,g1):
    k=t0
    while k<t1:
        a=(k-t0)/(t1-t0); add(snare(g0+(g1-g0)*a),k,0.5); k+=B/8
def march(t0,t1,g=1.0,ghost=True):
    k=t0; i=0
    while k<t1-1e-6:
        beat=i%4
        if beat in (0,2): add(kick(),k,0.9*g)
        if beat in (1,3): add(snare(1.0),k,0.55*g)
        if ghost: add(snare(0.35),k+B*0.75,0.5*g)
        if beat==3: add(snare(0.5),k+B*0.5,0.5*g)
        k+=B; i+=1
D=[50,62,66,69]; G=[43,59,62,67]; A=[45,61,64,69]; Bm=[47,59,62,66]; Em=[40,59,64,67]
# 0-4.8 abertura: rufar crescendo + tímpano
roll(0.3,4.6,0.15,1.0); add(timp(38),0.3,0.6)
add(timp(38),4.8,1.0); add(crash(0.6),4.8)
# 4.8-10.5 fanfarra
motif=[(69,.5),(74,.25),(74,.25),(74,.5),(78,.5),(76,.75),(74,.25),(76,.5),(81,1.5)]
t=4.9
for m,d in motif:
    add(brass(m,d*B*2*0.95),t,0.55); add(brass(m-4 if m!=69 else m-7,d*B*2*0.95),t,0.35); t+=d*B*2
march(4.9,10.5,0.6,ghost=False)
chord(D,8.9,1.6,0.6)
# 10.5-18 marcha + acordes
march(10.5,18.0,0.85)
for i,c in enumerate([D,Bm,G,A]):
    chord(c,10.5+i*2*B*2*0.95,1.8,0.45)
# 18 impacto "Falta gestão"
add(timp(38,1.2),18.0,1.2); add(crash(0.7),18.0); chord([38,50,57,62],18.0,2.2,0.7)
roll(21.2,23.2,0.2,1.0)
# 23.2 revelação PIPHPO
add(timp(38),23.2,1.2); add(crash(0.8),23.2)
t=23.2
for m,d in [(74,.25),(74,.25),(74,.25),(78,.75),(81,2.0)]:
    chord([m,m-5,m-9],t,d*B*2*0.95,0.75); t+=d*B*2
# 28.5-61 marcha principal
march(28.5,61.0,1.0)
prog=[D,Bm,G,A,D,Em,G,A]; k=28.5; i=0
while k<60.9:
    c=prog[i%8]; chord(c,k,2*B*0.97,0.42)
    for s in range(4): add(brass(c[-1]+12 if s%2==0 else c[-2]+12,B*0.4),k+s*B*0.5,0.12)
    k+=2*B; i+=1
for tt in (43.9,): add(crash(0.5),tt); add(timp(38),tt,0.8)
# 61-70 build
march(61.0,68.0,1.0)
for i,c in enumerate([G,A,Bm,A]): chord(c,61+i*1.75,1.7,0.5)
roll(68.0,70.0,0.3,1.2)
# 70 final
add(timp(38,0.9),70.0,1.4); add(crash(0.9),70.0)
t=70.0
for m,d in [(69,.5),(74,.5),(78,.5),(81,3.0)]:
    chord([m,m-5,m-9],t,d*B*2*0.95,0.8); t+=d*B*2
chord([38,50,57,62,66,69,74],t,4.5,1.0)
k=t
while k<t+3.5: add(timp(38,6),k,0.25); k+=B/4
add(timp(38),t+4.0,1.2)
fade=np.clip(np.arange(N)/sr/0.05,0,1)*np.clip((T-np.arange(N)/sr)/1.5,0,1)
out*=fade
# compressão suave
out=np.tanh(out/np.percentile(np.abs(out),99.5)*0.9)
out=out/np.max(np.abs(out))*0.85
st=np.stack([out,out],1)
with wave.open('out/marcha.wav','wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((st*32767).astype('<i2').tobytes())
print('ok')
