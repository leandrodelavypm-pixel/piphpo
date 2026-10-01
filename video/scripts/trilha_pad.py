import numpy as np, wave
sr=44100; T=80; t=np.arange(int(sr*T))/sr
def hz(m): return 440*2**((m-69)/12)
# progressão (MIDI): Am, F, C, G, Am, F, Dm, E
ch=[[45,57,60,64],[41,53,57,60],[48,55,60,64],[43,55,59,62],[45,57,60,64],[41,53,57,60],[38,53,57,62],[40,56,59,64]]
seg=10; out=np.zeros_like(t)
for i,c in enumerate(ch):
    a=i*seg-1.5; b=(i+1)*seg+1.5
    m=(t>=max(0,a))&(t<min(T,b)); tt=t[m]
    env=np.clip((tt-a)/2.5,0,1)*np.clip((b-tt)/2.5,0,1)
    s=np.zeros_like(tt)
    for n in c:
        f=hz(n)
        for det in (-0.12,0.12):
            ph=2*np.pi*(f+det)*tt
            s+=np.sin(ph)+0.25*np.sin(2*ph)+0.08*np.sin(3*ph)
    lfo=1+0.15*np.sin(2*np.pi*0.2*tt+i)
    out[m]+=s*env*lfo/len(c)
out*=0.18
# pulso grave 80 bpm entre 10.5 e 69 s
beat=60/80; pulse=np.zeros_like(t)
for k in np.arange(10.5,69,beat):
    m=(t>=k)&(t<k+0.6); d=t[m]-k
    pulse[m]+=np.sin(2*np.pi*(52+30*np.exp(-d*30))*d)*np.exp(-d*9)
ramp=np.clip((t-10.5)/6,0,1)*np.clip((69-t)/1.5,0,1)
out+=0.22*pulse*ramp
# impactos
for k,g in ((18.0,0.5),(23.2,0.45),(70.0,0.4)):
    m=(t>=k)&(t<k+3); d=t[m]-k
    out[m]+=g*np.sin(2*np.pi*(40+40*np.exp(-d*12))*d)*np.exp(-d*1.8)
fade=np.clip(t/2,0,1)*np.clip((T-t)/2.5,0,1); out*=fade
out=out/np.max(np.abs(out))*0.6
st=np.stack([out,out],1)
with wave.open('out/trilha_pad.wav','wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((st*32767).astype('<i2').tobytes())
print('ok')
