"""HUD helpers."""
from .core import *

def track(f,marks,full=1.0,refill=(262,280)):
    """A bar value (health, shield) from (frame, value) drops, each draining over 4 frames, then
    refilling to 1.0 over refill=(start, end) frames for the loop (None: no refill)."""
    v=full
    for t0,val in marks:
        if f>=t0: v=lerp(v,val,(f-t0)/4)
    if refill and f>=refill[0]: v=lerp(v,1.0,(f-refill[0])/(refill[1]-refill[0]))
    return v
