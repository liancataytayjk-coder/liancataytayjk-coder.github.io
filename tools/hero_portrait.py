"""Cut the headshot out of its white background for the front-page hero.

Usage: python3 tools/hero_portrait.py <headshot> <out_dir> [trim_bottom_px]

A headshot that already has a transparent background keeps its own alpha.
Otherwise the background is near-white and touches the top, left and right edges. It is
flood-filled from those edges only, because the white shirt reaches the bottom
edge and must stay opaque. Edge pixels get a soft alpha from how far they are
from white, then the portrait is converted to black and white.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

src, out = Path(sys.argv[1]), Path(sys.argv[2])
trim = int(sys.argv[3]) if len(sys.argv) > 3 else 0  # e.g. a desk edge along the bottom
out.mkdir(parents=True, exist_ok=True)
original = Image.open(src)
original = original.crop((0, 0, original.width, original.height - trim))
rgb = original.convert("RGB")
a = np.asarray(rgb).astype(np.int16)
w, h = rgb.size
has_alpha = original.mode == "RGBA" and np.asarray(original)[..., 3].min() < 10

# 1. Near-white mask, framed on three sides so one flood reaches every edge but the bottom.
near_white = (a.min(axis=2) >= 236).astype(np.uint8) * 255
framed = np.zeros((h + 1, w + 2), np.uint8)
framed[1:, 1:-1] = near_white
framed[0, :] = 255
framed[:, 0] = 255
framed[:, -1] = 255
flood = Image.fromarray(framed, "L").copy()  # copy: floodfill ignores array-backed images
ImageDraw.floodfill(flood, (0, 0), 128)
background = (np.asarray(flood)[1:, 1:-1] == 128)

# 2. Alpha: opaque subject, transparent background, a soft band along the edge.
alpha = np.where(background, 0, 255).astype(np.float32)
edge = np.asarray(Image.fromarray((~background).astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(5))) > 0
edge &= background
whiteness = (255 - a.min(axis=2)).astype(np.float32)
alpha[edge] = np.clip(whiteness[edge] / 40.0, 0, 1) * 255
alpha_img = Image.fromarray(alpha.astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(0.6))

alpha_img = alpha_img.filter(ImageFilter.MinFilter(3))  # pull the edge in one pixel
if has_alpha:  # already cut out: trust the supplied matte
    alpha_img = original.getchannel("A")

# 3. Black and white, gently lifted contrast. Edge pixels were blended with the
#    white backdrop, so un-mix the white out of them to avoid a light fringe.
al = np.asarray(alpha_img).astype(np.float32) / 255
grey = np.asarray(ImageOps.grayscale(rgb)).astype(np.float32)
lo, hi = np.percentile(grey[al > 0.5], [0.5, 99.5])  # contrast from the subject only
grey = np.clip((grey - lo) * 255 / max(hi - lo, 1), 0, 255)
soft = (al > 0.02) & (al < 0.98)
if not has_alpha:
    grey[soft] = np.clip((grey[soft] - 255 * (1 - al[soft])) / al[soft], 0, 255)
portrait = Image.merge("LA", (Image.fromarray(grey.astype(np.uint8), "L"), alpha_img)).convert("RGBA")

# 4. Trim to the subject and export two sizes.
bbox = alpha_img.point(lambda v: 255 if v > 8 else 0).getbbox()
portrait = portrait.crop(bbox)
for width, name in [(900, "portrait.webp"), (560, "portrait-sm.webp")]:
    im = portrait.copy()
    im.thumbnail((width, width * 2), Image.LANCZOS)
    im.save(out / name, "WEBP", quality=88, method=6)
    print(name, im.size)
