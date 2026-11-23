from monosig import monoline
def connector(p, q, Y, L=70):
    """thread from p to q. p/q are (x,y) or (x,y,(dx,dy)) where (dx,dy) is the stroke's outward direction at that end.
    Leaves p along its stroke direction, settles on the baseline Y, and enters q along q's stroke direction."""
    x1,y1 = p[:2]; x2,y2 = q[:2]
    t1 = p[2] if len(p)>2 else (1,0)        # leaving p: continue outward
    t2 = q[2] if len(q)>2 else (-1,0)       # entering q: arrive moving opposite to q's outward dir
    c1 = (x1+t1[0]*L, y1+t1[1]*L); c2 = (x2+t2[0]*L, y2+t2[1]*L)
    if x2-x1 < 220:
        return f"M{x1:.1f} {y1:.1f} C {c1[0]:.1f} {c1[1]:.1f}, {c2[0]:.1f} {c2[1]:.1f}, {x2:.1f} {y2:.1f}"
    a=(x1+110, Y); b=(x2-110, Y)
    return (f"M{x1:.1f} {y1:.1f} C {c1[0]:.1f} {c1[1]:.1f}, {a[0]-50:.1f} {Y:.1f}, {a[0]:.1f} {Y:.1f} "
            f"L {b[0]:.1f} {Y:.1f} C {b[0]+50:.1f} {Y:.1f}, {c2[0]:.1f} {c2[1]:.1f}, {x2:.1f} {y2:.1f}")
def words(spec, Y, outdir, drop=0):
    """spec: list of (text, x_left). returns (html imgs, list of (entry, exit) absolute)"""
    import pathlib
    html=[]; pts=[]
    for txt,x in spec:
        im, base, ein, eout = monoline(txt)
        top = Y - base + drop
        p = pathlib.Path(outdir)/f"w_{txt}.png"; im.save(p)
        html.append(f'<img src="{p.resolve().as_uri()}" style="position:absolute;left:{x}px;top:{top:.1f}px;z-index:4">')
        pts.append(((x+ein[0], top+ein[1], ein[2]), (x+eout[0], top+eout[1], eout[2])))
    return "".join(html), pts
def path_through(pts, Y, x_start=-5, x_end=1085, tail_to=None):
    """thread from left edge at Y into first word, word to word, out to right edge (or to tail_to point)."""
    d = [connector((x_start, Y), pts[0][0], Y)]
    for a,b in zip(pts, pts[1:]): d.append(connector(a[1], b[0], Y))
    end = tail_to or (x_end, Y)
    d.append(connector(pts[-1][1], end, Y))
    return " ".join(d)
