"""Close-up helpers shared by the themes' primer planos."""
from .core import *

def zoom_lines(d,c=(255,255,255)):
    """The 10 radial speed lines flashed at the start of a close-up (callers keep their own `if t<...`)."""
    for i in range(10): a=i*0.63; d.line([W//2,H//2,W//2+math.cos(a)*120,H//2+math.sin(a)*60],fill=c)

def fade_to(im,c,a):
    """Return `im` blended towards the flat colour c by alpha a (no clamping: callers clamp).
    Close-ups reassign (`im=fade_to(...)`, then re-create `d`); fx paste it back (`im.paste(fade_to(...))`)."""
    return Image.blend(im,Image.new('RGB',im.size,c),a)
