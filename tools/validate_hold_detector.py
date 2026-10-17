# Build a synthetic stop-motion clip with known exposure schedule, encode like web video, decode, and test the hold detector.
import numpy as np, subprocess, os, json
from PIL import Image, ImageDraw, ImageFilter
W,H,FPS=1280,720,24
rng=np.random.default_rng(1)
bg=(rng.normal(0,1,(H//8,W//8)))
bg=np.array(Image.fromarray(((bg-bg.min())/(np.ptp(bg))*255).astype(np.uint8)).resize((W,H),Image.BICUBIC)).astype(np.float32)
base=np.stack([150+0.15*bg,120+0.12*bg,90+0.1*bg],-1)
# schedule: list of (exposure length, camera dx per frame)
sched=[2]*24+[1]*24+[3]*8+[24]+[2]*12
truth=[]  # per transition: True if image changes
poses=[]
x=200.0
for L in sched:
    poses.append((x,L)); x+=14 if L<24 else 0
frames=[]
for pi,(x,L) in enumerate(poses):
    img=Image.fromarray(np.clip(base*(1+0.01*rng.normal()),0,255).astype(np.uint8))
    d=ImageDraw.Draw(img)
    d.ellipse([x,300,x+160,460],fill=(190,90,60))
    d.ellipse([x+30,320,x+80,360],fill=(215,120,90))
    img=img.filter(ImageFilter.GaussianBlur(1.2))
    arr=np.array(img).astype(np.float32)+rng.normal(0,2.0,(H,W,3))  # per-pose sensor noise
    arr=np.clip(arr,0,255).astype(np.uint8)
    for k in range(L):
        frames.append(arr); truth.append(k==0)
truth=truth[1:]  # transitions
os.makedirs('f',exist_ok=True)
for i,a in enumerate(frames): Image.fromarray(a).save(f'f/{i:04d}.png')
subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','24','-i','f/%04d.png','-c:v','libvpx-vp9','-b:v',os.environ.get('BR','2.5M'),'-pix_fmt','yuv420p','synth.webm'],check=True)
subprocess.run(['ffmpeg','-y','-loglevel','error','-i','synth.webm','-vf','scale=128:72:flags=bilinear','-f','rawvideo','-pix_fmt','rgb24','small.raw'],check=True)
raw=np.fromfile('small.raw',np.uint8).reshape(-1,72,128,3).astype(np.float32)
g=0.2126*raw[...,0]+0.7152*raw[...,1]+0.0722*raw[...,2]
diff=np.abs(g[1:]-g[:-1]); m=diff.mean((1,2)); b=(diff>10).mean((1,2))
pred=(m>0.8)|(b>0.002)
truth=np.array(truth[:len(pred)])
print(json.dumps({'n':int(len(pred)),'acc':float((pred==truth).mean()),'false_change':int((pred&~truth).sum()),'missed_change':int((~pred&truth).sum()),
 'hold_diff_p99':float(np.percentile(m[~truth],99)),'change_diff_p1':float(np.percentile(m[truth],1))}))
