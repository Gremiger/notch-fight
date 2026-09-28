"""Asterisk-iris transition between two themes' loop keyframes."""
from engine import *

def asterisk_thick(d,x,y,r,f,c=(217,119,87)):
    for k in range(8):
        a=k*math.pi/4+f*0.25; L=r*(1 if k%2==0 else 0.75)
        d.line([x,y,x+math.cos(a)*L,y+math.sin(a)*L],fill=c,width=max(1,int(r/5)))
    d.ellipse([x-r*0.18,y-r*0.18,x+r*0.18,y+r*0.18],fill=c)

def transition(a_img,b_img,T=22):
    out=[]
    for i in range(T):
        half=T//2; src=a_img if i<half else b_img
        t=i/(half-1) if i<half else (T-1-i)/(half-1)   # 0 -> 1 (closed) -> 0
        r=int(lerp(115,0,t)); cx,cy=W//2,GROUND-12
        m=Image.new('L',(W,H),0); ImageDraw.Draw(m).ellipse([cx-r,cy-r,cx+r,cy+r],fill=255)
        im=Image.composite(src,Image.new('RGB',(W,H)),m)
        d=ImageDraw.Draw(im); asterisk_thick(d,cx,cy,int(4+14*t),i)
        out.append(im)
    return out
