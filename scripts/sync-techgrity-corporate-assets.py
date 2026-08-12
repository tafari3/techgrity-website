from __future__ import annotations

from pathlib import Path
import hashlib
import json
import math
import shutil

import PIL
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'public' / 'assets' / 'techgrity-primary-horizontal-approved.png'
OUTPUT = ROOT / 'build' / 'techgrity-corporate-web-assets'

IDENTITY_REPOSITORY = 'tafari3/Techgrity-Brand-Identity-'
IDENTITY_COMMIT = '418e15ec95a53d67810397fa6c12e5f54822e137'
SOURCE_SHA256 = '76d40c46a1a9a1fde6b5a1bf7af506f4639bf29da86d0a3741416a5c2f8eeb1f'
SOURCE_DIMENSIONS = (1183, 250)
PINNED_PILLOW = '12.2.0'

NAVY = (3, 26, 69)
TEAL = (11, 126, 124)
WHITE = (255, 255, 255)
BASES = (NAVY, TEAL)

EXPECTED = {
    'techgrity-horizontal-primary-1600.png': '69fc47babd46f4b6711c6264a33cbc9f2c84478325b28b4253a690b7889275cd',
    'techgrity-horizontal-reversed-1600.png': 'da78093eaf7826709cd3c942d052b18813c3b294727a954014f3b2a858bbdb39',
    'techgrity-symbol-primary-512.png': '96b8b4900aa2e0b6c40ae82b70f49aa3a3f3a8535dafda7e34d5b75a49277ae9',
}

if PIL.__version__ != PINNED_PILLOW:
    raise SystemExit(f'Pillow version drift: expected {PINNED_PILLOW}, got {PIL.__version__}')

source_bytes = SOURCE.read_bytes()
source_digest = hashlib.sha256(source_bytes).hexdigest()
if source_digest != SOURCE_SHA256:
    raise SystemExit(f'exact founder-approved source SHA-256 mismatch: {source_digest}')

source_rgb = Image.open(SOURCE).convert('RGB')
if source_rgb.size != SOURCE_DIMENSIONS:
    raise SystemExit(f'exact founder-approved source dimensions mismatch: {source_rgb.size}')

if OUTPUT.exists():
    shutil.rmtree(OUTPUT)
OUTPUT.mkdir(parents=True)

w, h = source_rgb.size
sp = source_rgb.load()
distance_from_white = [0.0] * (w * h)
core = bytearray(w * h)

for y in range(h):
    for x in range(w):
        r, g, b = sp[x, y]
        distance = math.sqrt((255 - r) ** 2 + (255 - g) ** 2 + (255 - b) ** 2)
        idx = y * w + x
        distance_from_white[idx] = distance
        if distance > 30.0:
            core[idx] = 1

seen = bytearray(w * h)
kept_core = bytearray(w * h)
components = []
for y in range(h):
    for x in range(w):
        idx = y * w + x
        if not core[idx] or seen[idx]:
            continue
        stack = [(x, y)]
        seen[idx] = 1
        points = []
        while stack:
            cx, cy = stack.pop()
            points.append((cx, cy))
            for ny in range(max(0, cy - 1), min(h, cy + 2)):
                for nx in range(max(0, cx - 1), min(w, cx + 2)):
                    nidx = ny * w + nx
                    if core[nidx] and not seen[nidx]:
                        seen[nidx] = 1
                        stack.append((nx, ny))
        if len(points) >= 20:
            xs = [p[0] for p in points]
            ys = [p[1] for p in points]
            bbox = (min(xs), min(ys), max(xs) + 1, max(ys) + 1, len(points))
            components.append(bbox)
            for px, py in points:
                kept_core[py * w + px] = 1

if not components:
    raise SystemExit('no valid corporate artwork components found')

core_im = Image.new('L', (w, h), 0)
core_im.putdata([255 if value else 0 for value in kept_core])
support = core_im.filter(ImageFilter.MaxFilter(5)).load()

def fit_alpha_and_residual(rgb, base):
    r, g, b = rgb
    dr, dg, db = 255 - r, 255 - g, 255 - b
    vr, vg, vb = 255 - base[0], 255 - base[1], 255 - base[2]
    denom = vr * vr + vg * vg + vb * vb
    alpha = max(0.0, min(1.0, (dr * vr + dg * vg + db * vb) / denom))
    pr, pg, pb = 255 - alpha * vr, 255 - alpha * vg, 255 - alpha * vb
    residual = (r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2
    return alpha, residual

transparent_master = Image.new('RGBA', (w, h), (0, 0, 0, 0))
tp = transparent_master.load()
for y in range(h):
    for x in range(w):
        idx = y * w + x
        if support[x, y] == 0 or distance_from_white[idx] <= 1.5:
            continue
        rgb = sp[x, y]
        fits = [fit_alpha_and_residual(rgb, base) for base in BASES]
        choice = 0 if fits[0][1] <= fits[1][1] else 1
        best_alpha = fits[choice][0]
        if distance_from_white[idx] > 85.0 or best_alpha > 0.92:
            tp[x, y] = (rgb[0], rgb[1], rgb[2], 255)
        else:
            alpha = int(max(0, min(255, round(best_alpha * 255))))
            if alpha >= 8:
                base = BASES[choice]
                tp[x, y] = (base[0], base[1], base[2], alpha)

if transparent_master.getchannel('A').getbbox() is None:
    raise SystemExit('transparent corporate derivative has no visible pixels')

white_check = Image.new('RGBA', transparent_master.size, (255, 255, 255, 255))
white_check.alpha_composite(transparent_master)
cp = white_check.convert('RGB').load()
max_diff = 0
sum_diff = 0
samples = w * h * 3
for y in range(h):
    for x in range(w):
        sr, sg, sb = sp[x, y]
        cr, cg, cb = cp[x, y]
        for diff in (abs(sr - cr), abs(sg - cg), abs(sb - cb)):
            max_diff = max(max_diff, diff)
            sum_diff += diff
mean_abs_diff = sum_diff / samples
if max_diff > 20 or mean_abs_diff > 1.5:
    raise SystemExit(
        f'transparent conversion drift too high: max={max_diff}, mean={mean_abs_diff:.4f}'
    )

divider_candidates = [
    component for component in components
    if (component[2] - component[0]) <= max(18, w // 50)
    and (component[3] - component[1]) >= int(h * 0.55)
    and int(w * 0.15) < component[0] < int(w * 0.55)
]
if not divider_candidates:
    raise SystemExit('could not deterministically identify corporate divider')
divider = max(divider_candidates, key=lambda component: component[3] - component[1])
if list(divider[:4]) != [378, 27, 383, 232]:
    raise SystemExit(f'corporate divider geometry drift: {divider[:4]}')

def visible_bbox(region: Image.Image):
    bbox = region.getchannel('A').point(lambda alpha: 255 if alpha > 7 else 0).getbbox()
    if bbox is None:
        raise SystemExit('empty derivative crop')
    return bbox

left = transparent_master.crop((0, 0, max(1, divider[0] - 4), h))
symbol_raw = left.crop(visible_bbox(left))
padding = max(8, round(max(symbol_raw.size) * 0.08))
symbol = Image.new(
    'RGBA',
    (symbol_raw.width + 2 * padding, symbol_raw.height + 2 * padding),
    (0, 0, 0, 0),
)
symbol.alpha_composite(symbol_raw, (padding, padding))

def recolour_reversed(image: Image.Image) -> Image.Image:
    src = image.convert('RGBA')
    out = Image.new('RGBA', src.size, (0, 0, 0, 0))
    srcp, outp = src.load(), out.load()
    for yy in range(src.height):
        for xx in range(src.width):
            r, g, b, alpha = srcp[xx, yy]
            if alpha == 0:
                continue
            navy_distance = (r - NAVY[0]) ** 2 + (g - NAVY[1]) ** 2 + (b - NAVY[2]) ** 2
            teal_distance = (r - TEAL[0]) ** 2 + (g - TEAL[1]) ** 2 + (b - TEAL[2]) ** 2
            nr, ng, nb = TEAL if teal_distance < navy_distance else WHITE
            outp[xx, yy] = (nr, ng, nb, alpha)
    return out

def save_width(image: Image.Image, width: int, filename: str):
    height = round(image.height * width / image.width)
    image.resize((width, height), Image.Resampling.LANCZOS).save(OUTPUT / filename)

save_width(transparent_master, 1600, 'techgrity-horizontal-primary-1600.png')
save_width(recolour_reversed(transparent_master), 1600, 'techgrity-horizontal-reversed-1600.png')

symbol_size = 512
scale = min(symbol_size / symbol.width, symbol_size / symbol.height)
rw = max(1, round(symbol.width * scale))
rh = max(1, round(symbol.height * scale))
resized_symbol = symbol.resize((rw, rh), Image.Resampling.LANCZOS)
symbol_canvas = Image.new('RGBA', (symbol_size, symbol_size), (0, 0, 0, 0))
symbol_canvas.alpha_composite(
    resized_symbol,
    ((symbol_size - rw) // 2, (symbol_size - rh) // 2),
)
symbol_canvas.save(OUTPUT / 'techgrity-symbol-primary-512.png')

actual = {}
for filename, expected_sha in EXPECTED.items():
    output_file = OUTPUT / filename
    digest = hashlib.sha256(output_file.read_bytes()).hexdigest()
    actual[filename] = digest
    if digest != expected_sha:
        raise SystemExit(f'formal derivative SHA-256 mismatch for {filename}: {digest}')

provenance = {
    'identityRepository': IDENTITY_REPOSITORY,
    'identityCommit': IDENTITY_COMMIT,
    'approvedSourceSha256': SOURCE_SHA256,
    'approvedSourceDimensions': list(SOURCE_DIMENSIONS),
    'pillow': PINNED_PILLOW,
    'derivativeSha256': actual,
    'dividerBBox': list(divider[:4]),
    'whiteRecompositionMaxChannelDifference': max_diff,
    'whiteRecompositionMeanAbsoluteDifference': round(mean_abs_diff, 6),
    'method': 'exact founder-approved raster source; deterministic governed derivative generation; no redraw, tracing, vector reconstruction or re-typesetting',
}
(OUTPUT / 'provenance.json').write_text(json.dumps(provenance, indent=2) + '\n', encoding='utf-8')

print(json.dumps(provenance, indent=2))
