"""Render text in a script font, reduce it to a centre-line, and redraw it with the thread's stroke width -> monoline 'written with the thread' PNG (RGBA)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from skimage.morphology import skeletonize, disk, dilation as binary_dilation
FONT = str(__import__("pathlib").Path(__file__).parent/"node_modules")+"/@fontsource/allura/files/allura-latin-400-normal.woff2"
def monoline(text, size_px=175, stroke=7, color=(201,168,76), font=FONT, S=4):
    import subprocess, os
    ttf = font.replace('.woff2','.ttf')
    if font.endswith('.woff2') and not os.path.exists(ttf):
        from fontTools.ttLib import TTFont
        t = TTFont(font); t.flavor=None; t.save(ttf)
    f = ImageFont.truetype(ttf if font.endswith('.woff2') else font, size_px*S)
    l,t,r,b = f.getbbox(text)
    pad = 40*S
    W,H = r-l+2*pad, b-t+2*pad
    im = Image.new('L',(W,H),0); d = ImageDraw.Draw(im)
    d.text((pad-l,pad-t), text, font=f, fill=255)
    asc,_ = f.getmetrics(); baseline = pad - t + asc
    m = np.array(im) > 128
    sk = skeletonize(m)
    th = binary_dilation(sk, disk(int(stroke*S/2)))
    a = Image.fromarray((th*255).astype('uint8')).filter(ImageFilter.GaussianBlur(S*0.6)).resize((W//S,H//S), Image.LANCZOS)
    rgba = Image.new('RGBA', a.size, color+(0,)); rgba.putalpha(a)
    # leftmost / rightmost ink at baseline band for joining
    return rgba, baseline//S, (pad-l)//S
if __name__ == "__main__":
    img, base, x0 = monoline("Azrim Studio", 175)
    bg = Image.new('RGBA',(img.width+80,img.height+40),(239,235,225,255)); bg.alpha_composite(img,(40,20))
    d = ImageDraw.Draw(bg); d.line([(0,base+20),(60,base+20)],fill=(201,168,76),width=7)
    bg.save('/home/claude/work/monosig_test.png'); print(img.size, base)
