"""Theme discovery: every module in this package with THEME + CLIPS is a theme.
CLIPS = [(clip_name, frame_count, frame_fn), ...] where frame_fn(f) -> PIL image."""
import importlib, pkgutil

def load_themes():
    themes={}
    for m in sorted(pkgutil.iter_modules(__path__), key=lambda m: m.name):
        mod=importlib.import_module(f'{__name__}.{m.name}')
        if hasattr(mod,'THEME') and hasattr(mod,'CLIPS'): themes[mod.THEME]=mod.CLIPS
    return themes
