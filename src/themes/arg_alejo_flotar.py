"""Argentina sub-theme "arg-alejo-flotar": Alejo y Valentina (LocoArts), no fight, on the series' other set:
the orange wall with its black band, the brown curtain, the green floor. Claude as Carlitox floats beside
the curtain, arms out, legs hanging. Clip `flotar`: HOLA, VENGO A FLOTAR — he drifts off across the panel,
comes back in from the other side, slips behind the curtain and floats out again to where he was."""
from engine import *
from themes.arg_alejo import CARLITOX_UP, CAST, INK                  # the same cast as arg-alejo

THEME = 'arg-alejo-flotar'
N_ = 288                                                            # a multiple of 12 (and of 48: the bob)
FX_ = 146                                                           # where he floats, beside the curtain
CURTAIN = (70,128)

def _stage(d):
    d.rectangle([0,0,W,H],fill=(244,160,30))
    d.rectangle([0,4,W,12],fill=(20,20,20)); d.line([0,14,W,14],fill=(200,200,200),width=2)
    d.rectangle([0,GROUND,W,H],fill=(40,110,30)); d.line([0,GROUND,W,GROUND],fill=INK)
register_bg(THEME, lambda v: (v+40,v+60,v+20), decor=_stage)

@fx('fl_curtain')
def _fx_curtain(d,im,e,f):
    """The brown curtain, drawn over him when he passes behind it."""
    x0,x1=CURTAIN
    d.rectangle([x0,14,x1,GROUND],fill=(140,62,20),outline=INK)
    for x in (80,92,99,112,120): d.line([x,18,x+(1 if x%2 else -1),GROUND-2],fill=INK)

@fx('fl_bubble')
def _fx_bubble(d,im,e,f):
    _,txt,cx,y=e; w=len(txt)*4+7; x=max(1,min(W-w-2,int(cx-w/2))); tx=max(x+4,min(x+w-4,int(cx)))
    d.rectangle([x,y,x+w,y+10],fill=(255,255,255),outline=INK)
    d.polygon([(tx-2,y+10),(tx+2,y+10),(tx,y+15)],fill=(255,255,255),outline=INK); d.line([tx-1,y+10,tx+1,y+10],fill=(255,255,255))
    text(d,txt,x+4,y+3,INK,shadow=None)

def clip_flotar(f):
    s=scene(f,THEME)
    bob=int(round(3*math.sin(2*math.pi*f/48)))
    x=FX_
    if 62<=f<120: x=lerp(FX_,W+20,ease((f-62)/58))                    # off to the right...
    if 120<=f<130: x=-30                                                # (out of sight)
    if 130<=f<250: x=lerp(-20,FX_,(f-130)/120)                          # ...back in from the left, behind the curtain
    s['actors']=[actor(CARLITOX_UP,x,y=GROUND-12+bob,pal=CAST)]
    s['fx'].append(('fl_curtain',))
    if 14<=f<62: s['fx'].append(('fl_bubble',"HOLA, VENGO A FLOTAR",x,6))
    return s

CLIPS = [clip('flotar', N_, clip_flotar)]
