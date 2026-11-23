"""Monoline 'written with the thread' words.
monoline(text) -> (RGBA image, baseline_px, entry(x,y), exit(x,y)) in image pixel coords.
entry/exit are the skeleton end-points where the thread should flow in/out."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, os, pathlib
from scipy.ndimage import convolve
from skimage.morphology import skeletonize, disk, dilation
FONT = str(pathlib.Path(__file__).parent/"node_modules"/"@fontsource/allura/files/allura-latin-400-normal.woff2")
def _ttf(font):
    if not font.endswith('.woff2'): return font
    ttf = font.replace('.woff2','.ttf')
    if not os.path.exists(ttf):
        from fontTools.ttLib import TTFont
        t = TTFont(font); t.flavor=None; t.save(ttf)
    return ttf
def monoline(text, size_px=175, stroke=7, color=(201,168,76), font=FONT, S=4):
    f = ImageFont.truetype(_ttf(font), size_px*S)
    l,t,r,b = f.getbbox(text); pad = 40*S
    W,H = r-l+2*pad, b-t+2*pad
    im = Image.new('L',(W,H),0); ImageDraw.Draw(im).text((pad-l,pad-t), text, font=f, fill=255)
    asc,_ = f.getmetrics(); baseline = pad - t + asc
    sk = skeletonize(np.array(im) > 128)
    nb = convolve(sk.astype(int), np.ones((3,3),int), mode='constant') - sk
    ends = np.argwhere(sk & (nb == 1))          # (y,x)
    ends = np.argwhere(sk & (nb == 1))          # (y,x) skeleton end points
    e_in = ends[np.argmin(ends[:,1])]; e_out = ends[np.argmax(ends[:,1])]
    def tangent(e, n=14*S):
        # walk n pixels along the stroke from the end point; outward direction = e - walked point
        from collections import deque
        seen={tuple(e)}; q=deque([(tuple(e),0)]); far=tuple(e)
        while q:
            (y,x),dd=q.popleft()
            if dd>=n: far=(y,x); break
            far=(y,x)
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    p=(y+dy,x+dx)
                    if p not in seen and 0<=p[0]<sk.shape[0] and 0<=p[1]<sk.shape[1] and sk[p]:
                        seen.add(p); q.append((p,dd+1))
        v=np.array(e,float)-np.array(far,float); v/= (np.linalg.norm(v)+1e-9)
        return (v[1], v[0])   # (dx,dy)
    t_in, t_out = tangent(e_in), tangent(e_out)
    th = dilation(sk, disk(int(stroke*S/2)))
    a = Image.fromarray((th*255).astype('uint8')).filter(ImageFilter.GaussianBlur(S*0.6)).resize((W//S,H//S), Image.LANCZOS)
    rgba = Image.new('RGBA', a.size, color+(0,)); rgba.putalpha(a)
    return rgba, baseline/S, (e_in[1]/S, e_in[0]/S, t_in), (e_out[1]/S, e_out[0]/S, t_out)
