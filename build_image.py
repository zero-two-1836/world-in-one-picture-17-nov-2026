#!/usr/bin/env python3
"""Build the front-page image for the make.fun bounty
"Sum up 17 November's world news in one image".

v2 (current): a poster, not a newspaper page. v1 was text-dense and
ranked #2828 live; its flaw, per the judge's own criteria, is craft:
at ~300 pixels across its 14-18px body copy is unreadable, so it loses
pairwise games to images that read at a glance. v2 has three large
flat-illustration hero panels (Gulf, Kerch Bridge, Voyager), an 8-story
grid with one-line headlines, and the numbers strip. No text under 15px
except the source footer. Same 12 stories, same verified facts
(see NEWS.md).

Run once, locally, to produce assets/entry.png (1024x1024, <=1 MiB).
The submitted program (main.py) is stdlib-only and copies that asset to
/output/entry.png deterministically; this builder is kept in the repo so
anyone can see exactly how the image was made.

News verified 2026-11-18 from BBC, Reuters/AP wires via One Turn News,
Hansen Intel, Foreign Exchanges and NPR summaries of 17 Nov 2026.
Procedural drawing only (Pillow): no AI image generation, no photos.
"""
import math
import random
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (20, 20, 22)
NAVY = (20, 33, 61)
RED = (178, 34, 34)
GREY = (90, 88, 82)
RULE = (180, 175, 160)
CARD = (255, 252, 245)
GOLD = (214, 200, 150)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Word-wrap text to fit pixel width; returns list of lines."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=None):
    lines = wrap(draw, text, fnt, width)
    lh = leading or int(fnt.size * 1.32)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def kicker(draw, x, y, text, color=RED, size=17):
    f = font(SANS_B, size)
    draw.text((x, y), text.upper(), font=f, fill=color)
    return y + size + 6


def fit_font(draw, text, path, start_size, max_width, min_size=15):
    """Largest font size at/below start_size whose text fits max_width."""
    size = start_size
    while size > min_size:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 1
    return font(path, min_size)


def starburst(d, cx, cy, r_out, r_in, spikes, fill):
    pts = []
    for i in range(spikes * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / spikes - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


def bezier(p0, p1, p2, n=40):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        pts.append((x, y))
    return pts


# ---------- hero illustrations (flat, procedural) ----------

def draw_gulf(d, x0, y0, w, h):
    """Dusk sea, explosion starburst, missile streaks, ship silhouette."""
    d.rectangle([x0, y0, x0 + w, y0 + 58], fill=(43, 58, 85))
    d.rectangle([x0, y0 + 58, x0 + w, y0 + 82], fill=(216, 110, 55))
    d.rectangle([x0, y0 + 82, x0 + w, y0 + h], fill=(18, 66, 79))
    for yy in (y0 + 104, y0 + 126, y0 + 150):
        for xx in range(0, w, 44):
            d.arc([x0 + xx, yy, x0 + xx + 30, yy + 12], 180, 360,
                  fill=(120, 180, 190), width=2)
    cx, cy = x0 + w // 2, y0 + 70
    # missile streaks from the top corners toward the blast
    d.line([(x0 + 24, y0 + 6), (cx - 34, cy - 26)], fill=(255, 255, 255), width=3)
    d.line([(x0 + w - 24, y0 + 6), (cx + 34, cy - 26)], fill=(255, 255, 255), width=3)
    d.ellipse([cx - 40, cy - 32, cx - 28, cy - 20], fill=(255, 220, 90))
    d.ellipse([cx + 28, cy - 32, cx + 40, cy - 20], fill=(255, 220, 90))
    # smoke puffs hugging the blast
    for (sx, sy, sr) in ((cx - 46, cy - 34, 9), (cx + 44, cy - 38, 10),
                         (cx + 58, cy - 14, 7)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(90, 88, 82))
    # explosion: layered starbursts
    starburst(d, cx, cy, 52, 30, 12, (178, 34, 34))
    starburst(d, cx, cy, 38, 22, 12, (232, 110, 40))
    starburst(d, cx, cy, 24, 13, 10, (255, 205, 60))
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(255, 255, 255))
    # ship silhouette, bottom left
    d.polygon([(x0 + 14, y0 + h - 14), (x0 + 70, y0 + h - 14),
               (x0 + 60, y0 + h - 26), (x0 + 24, y0 + h - 26)], fill=(10, 12, 14))
    d.rectangle([x0 + 36, y0 + h - 40, x0 + 48, y0 + h - 26], fill=(10, 12, 14))


def draw_kerch(d, x0, y0, w, h):
    """Pale sky, strait, bridge deck with a gap and a falling span."""
    d.rectangle([x0, y0, x0 + w, y0 + 70], fill=(201, 212, 220))
    d.rectangle([x0, y0 + 70, x0 + w, y0 + h], fill=(94, 126, 150))
    for yy in (y0 + 104, y0 + 132, y0 + 158):
        for xx in range(0, w, 46):
            d.arc([x0 + xx, yy, x0 + xx + 30, yy + 12], 180, 360,
                  fill=(180, 205, 220), width=2)
    # smoke right at the broken ends
    for (sx, sy, sr) in ((x0 + 124, y0 + 50, 7), (x0 + 184, y0 + 48, 8)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 118, 112))
    # deck segments left and right of the gap, with red broken ends
    d.rectangle([x0 + 6, y0 + 58, x0 + 126, y0 + 70], fill=(70, 72, 78))
    d.rectangle([x0 + 182, y0 + 58, x0 + w - 6, y0 + 70], fill=(70, 72, 78))
    d.rectangle([x0 + 122, y0 + 58, x0 + 126, y0 + 70], fill=(178, 34, 34))
    d.rectangle([x0 + 182, y0 + 58, x0 + 186, y0 + 70], fill=(178, 34, 34))
    # pylons
    for px in (30, 98, 204, 272):
        d.rectangle([x0 + px, y0 + 70, x0 + px + 6, y0 + 118], fill=(70, 72, 78))
    # falling middle span: bigger, steeper, dropping toward the water
    d.polygon([(x0 + 136, y0 + 66), (x0 + 174, y0 + 96),
               (x0 + 164, y0 + 108), (x0 + 126, y0 + 78)],
              fill=(150, 40, 36), outline=(90, 20, 18))
    # splash under the falling span: vertical spray lines + droplets
    for (sx, sh) in ((146, 16), (154, 24), (162, 20), (170, 14)):
        d.line([(x0 + sx, y0 + 122), (x0 + sx, y0 + 122 + sh)],
               fill=(255, 255, 255), width=3)
    for (sx, sy) in ((140, 118), (176, 116), (158, 112)):
        d.ellipse([x0 + sx - 3, y0 + sy - 3, x0 + sx + 3, y0 + sy + 3],
                  fill=(255, 255, 255))


def draw_voyager(d, x0, y0, w, h):
    """Black space, starfield, gold trajectory, probe with dish."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(11, 16, 38))
    rnd = random.Random(7)
    for _ in range(60):
        sx = x0 + rnd.randint(2, w - 3)
        sy = y0 + rnd.randint(2, h - 3)
        r = rnd.choice([1, 1, 1, 2])
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))
    px, py = x0 + 232, y0 + 52
    # dashed gold trajectory from Earth (bottom left) to the probe
    pts = bezier((x0 + 16, y0 + h - 14), (x0 + 110, y0 + 150), (px, py))
    for i in range(0, len(pts) - 1, 2):
        d.line([pts[i], pts[i + 1]], fill=(255, 205, 60), width=2)
    # Earth: small blue dot at the trajectory start
    d.ellipse([x0 + 10, y0 + h - 20, x0 + 22, y0 + h - 8], fill=(70, 130, 220))
    # probe: dish, body, boom, RTG tip
    d.line([(px, py), (px + 34, py + 20)], fill=(200, 200, 200), width=3)
    d.ellipse([px + 30, py + 16, px + 40, py + 26], fill=(255, 255, 255))
    d.rectangle([px - 14, py - 6, px + 2, py + 8], fill=(180, 180, 190))
    d.ellipse([px - 26, py - 22, px + 6, py + 10], fill=(255, 205, 60))
    d.ellipse([px - 20, py - 16, px + 0, py + 4], fill=(200, 150, 30))


# ---------- small story icons (40x40 rounded square + white glyph) ----------

def icon_chip(d, x, y, bg):
    d.rounded_rectangle([x, y, x + 40, y + 40], radius=8, fill=bg)
    d.rectangle([x + 12, y + 12, x + 28, y + 28], fill=(255, 255, 255))
    for i in (15, 20, 25):
        d.line([(x + i, y + 8), (x + i, y + 12)], fill=(255, 255, 255), width=2)
        d.line([(x + i, y + 28), (x + i, y + 32)], fill=(255, 255, 255), width=2)
        d.line([(x + 8, y + i), (x + 12, y + i)], fill=(255, 255, 255), width=2)
        d.line([(x + 28, y + i), (x + 32, y + i)], fill=(255, 255, 255), width=2)


def icon_cross(d, x, y, bg):
    d.rounded_rectangle([x, y, x + 40, y + 40], radius=8, fill=bg)
    d.rectangle([x + 17, y + 9, x + 23, y + 31], fill=(255, 255, 255))
    d.rectangle([x + 9, y + 17, x + 31, y + 23], fill=(255, 255, 255))


def icon_heart(d, x, y, bg):
    d.rounded_rectangle([x, y, x + 40, y + 40], radius=8, fill=bg)
    d.ellipse([x + 8, y + 11, x + 20, y + 23], fill=(255, 255, 255))
    d.ellipse([x + 20, y + 11, x + 32, y + 23], fill=(255, 255, 255))
    d.polygon([(x + 8, y + 19), (x + 32, y + 19), (x + 20, y + 33)],
              fill=(255, 255, 255))


def icon_swap(d, x, y, bg):
    d.rounded_rectangle([x, y, x + 40, y + 40], radius=8, fill=bg)
    d.line([(x + 9, y + 15), (x + 27, y + 15)], fill=(255, 255, 255), width=3)
    d.polygon([(x + 27, y + 10), (x + 33, y + 15), (x + 27, y + 20)],
              fill=(255, 255, 255))
    d.line([(x + 31, y + 25), (x + 13, y + 25)], fill=(255, 255, 255), width=3)
    d.polygon([(x + 13, y + 20), (x + 7, y + 25), (x + 13, y + 30)],
              fill=(255, 255, 255))


def icon_flame(d, x, y, bg):
    d.rounded_rectangle([x, y, x + 40, y + 40], radius=8, fill=bg)
    d.polygon([(x + 20, y + 7), (x + 28, y + 18), (x + 30, y + 26),
               (x + 24, y + 33), (x + 16, y + 33), (x + 10, y + 26),
               (x + 12, y + 18)], fill=(255, 255, 255))


def icon_shield(d, x, y, bg):
    d.rounded_rectangle([x, y, x + 40, y + 40], radius=8, fill=bg)
    d.polygon([(x + 11, y + 9), (x + 29, y + 9), (x + 29, y + 20),
               (x + 20, y + 32), (x + 11, y + 20)], fill=(255, 255, 255))
    d.line([(x + 15, y + 19), (x + 19, y + 23), (x + 26, y + 14)],
           fill=bg, width=3)


def icon_plane(d, x, y, bg):
    d.rounded_rectangle([x, y, x + 40, y + 40], radius=8, fill=bg)
    d.polygon([(x + 8, y + 22), (x + 30, y + 12), (x + 32, y + 16),
               (x + 18, y + 24), (x + 26, y + 30), (x + 22, y + 31),
               (x + 14, y + 26), (x + 10, y + 26)], fill=(255, 255, 255))


def icon_crowd(d, x, y, bg):
    d.rounded_rectangle([x, y, x + 40, y + 40], radius=8, fill=bg)
    for cx in (14, 20, 26):
        d.ellipse([x + cx - 3, y + 10, x + cx + 3, y + 16], fill=(255, 255, 255))
        d.rectangle([x + cx - 4, y + 17, x + cx + 4, y + 30], fill=(255, 255, 255))


# ---------- page ----------

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 28  # margin

# ---- Masthead ----
d.rectangle([0, 0, W, 88], fill=NAVY)
d.text((M, 14), "THE WORLD IN ONE PICTURE", font=font(SERIF_B, 40),
       fill=(255, 255, 255))
d.text((M, 62), "TUESDAY  17  NOVEMBER  2026  ·  12 STORIES  ·  6 CONTINENTS",
       font=font(SANS_B, 16), fill=GOLD)
d.rectangle([0, 88, W, 92], fill=RED)

# ---- Day line ----
d.text((M, 104),
       "THE DAY THE GULF CAUGHT FIRE — AND UKRAINE BROUGHT DOWN A BRIDGE",
       font=font(SANS_B, 19), fill=GREY)
d.line([(M, 134), (W - M, 134)], fill=RULE, width=2)

# ---- Hero row: 3 illustrated panels ----
hero_y, hero_h, illus_h = 146, 348, 180
col_w = (W - 2 * M - 2 * 16) // 3
heroes = [
    (draw_gulf, "LEAD  ·  THE GULF ON EDGE",
     "U.S. and Iran trade fire across the Gulf",
     "U.S. jets hit Qeshm Island; Iran's drones struck a U.S. base in Bahrain."),
    (draw_kerch, "WAR  ·  UKRAINE",
     "Kerch Bridge section falls into the strait",
     "Ukrainian drones hit the bridge a second day; a road span fell."),
    (draw_voyager, "SPACE",
     "Voyager 1 reaches one light-day out",
     "Nearly 50 years after launch, the probe is 16 billion miles from Earth."),
]
for i, (draw_fn, tag, head, sub) in enumerate(heroes):
    x = M + i * (col_w + 16)
    d.rectangle([x, hero_y, x + col_w, hero_y + hero_h],
                fill=CARD, outline=RULE, width=2)
    draw_fn(d, x + 2, hero_y + 2, col_w - 4, illus_h)
    ty = hero_y + illus_h + 12
    ty = kicker(d, x + 14, ty, tag, size=13)
    ty = para(d, x + 14, ty, head, font(SERIF_B, 24), col_w - 28, leading=29)
    para(d, x + 14, ty + 2, sub, font(SANS, 15), col_w - 28, leading=19)

# ---- Grid: 8 more stories, 2 columns x 4 rows ----
gy = hero_y + hero_h + 14
gy = kicker(d, M, gy, "More from Tuesday", size=16)
gy += 2
grid = [
    (icon_chip, (34, 120, 60), "MARKETS",
     "Nvidia tops $115bn — Huang stays out",
     "Record revenue, about double a year earlier."),
    (icon_cross, (178, 34, 34), "HEALTH",
     "Ebola in DR Congo passes 11,000 cases",
     "Cases doubled in three months; 5,400 deaths."),
    (icon_heart, (30, 90, 160), "MIDDLE EAST",
     "West urges Israel: open Gaza crossings",
     "Four allies call the aid situation catastrophic."),
    (icon_swap, (20, 110, 110), "UKRAINE",
     "1,000-for-1,000 prisoner swap agreed",
     "Zelenskyy announces the swap after Abu Dhabi talks."),
    (icon_flame, (200, 90, 20), "ENERGY",
     "Houthis hit Saudi oil pipeline",
     "Drones hit the East-West line as forces advance."),
    (icon_shield, (100, 60, 140), "UNITED STATES",
     "America loses measles-free status",
     "After 26 years, amid 5,400+ cases — a 40-year high."),
    (icon_plane, (20, 33, 61), "DIPLOMACY",
     "Trump flies to Manila, then Shenzhen",
     "APEC talks with Xi and Putin; Ukraine on agenda."),
    (icon_crowd, (140, 40, 40), "EUROPE",
     "146,000 march across France",
     "Unions strike over the cost of living."),
]
gcol_w = (W - 2 * M - 16) // 2
row_h = 80
for i in range(0, len(grid), 2):
    for j, (icon_fn, color, tag, head, sub) in enumerate(grid[i:i + 2]):
        x = M + j * (gcol_w + 16)
        y = gy + (i // 2) * row_h
        d.rounded_rectangle([x, y, x + gcol_w, y + row_h - 10], radius=8,
                            fill=CARD, outline=RULE, width=1)
        icon_fn(d, x + 10, y + 10, color)
        tx = x + 60
        d.text((tx, y + 8), tag, font=font(SANS_B, 12), fill=RED)
        d.text((tx, y + 26), head,
               font=fit_font(d, head, SANS_B, 20, gcol_w - 70), fill=INK)
        d.text((tx, y + 52), sub, font=font(SANS, 15), fill=INK)
gy = gy + 4 * row_h + 8

# ---- Numbers strip ----
d.rectangle([M, gy, W - M, gy + 70], fill=NAVY)
nums = [("$115bn", "Nvidia revenue"), ("11,000", "Ebola cases"),
        ("1,000+", "POWs to swap"), ("146,000", "French protesters"),
        ("19", "killed in jet crash")]
seg = (W - 2 * M) // len(nums)
for i, (n, label) in enumerate(nums):
    cx = M + i * seg + seg // 2
    f1, f2 = font(SANS_B, 26), font(SANS, 13)
    d.text((cx - d.textlength(n, font=f1) / 2, gy + 8), n, font=f1,
           fill=(255, 255, 255))
    d.text((cx - d.textlength(label, font=f2) / 2, gy + 42), label, font=f2,
           fill=GOLD)
gy += 70 + 10

# ---- Footer ----
d.text((M, gy),
       "Compiled from BBC, Reuters, AP, Al Jazeera and NPR reporting of 17 November 2026.",
       font=font(SANS, 14), fill=GREY)
d.text((M, gy + 18),
       "Also: Meta fined $887m in Italy · Mongolia's president resigns · Moldova shuts its airspace",
       font=font(SANS, 14), fill=GREY)
gy += 36

img.save("assets/entry.png", optimize=True)
print("saved assets/entry.png", img.size, "final y =", gy)
