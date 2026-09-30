"""Theme discovery: every module in this package with THEME + CLIPS is a theme.
CLIPS = [(clip_name, frame_count, frame_fn[, options]), ...] where frame_fn(f) -> PIL image
(engine.clip() builds these). DEFAULT_OFF = True in a theme ships its clips off by default."""
import importlib, pkgutil

def normalize(items, default_off):
    """-> [(name, frames, frame_fn, off)]: a clip's own `off` wins over the theme's DEFAULT_OFF."""
    out=[]
    for name,n,fn,*opts in items:
        off=(opts[0] if opts else {}).get('off')
        out.append((name,n,fn,default_off if off is None else off))
    return out

def load_themes():
    themes={}
    for m in sorted(pkgutil.iter_modules(__path__), key=lambda m: m.name):
        mod=importlib.import_module(f'{__name__}.{m.name}')
        if hasattr(mod,'THEME') and hasattr(mod,'CLIPS'):
            themes[mod.THEME]=normalize(mod.CLIPS,getattr(mod,'DEFAULT_OFF',False))
    return themes
