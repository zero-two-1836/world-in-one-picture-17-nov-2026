#!/usr/bin/env python3
"""Build the front-page image for the make.fun bounty
"Sum up 17 November's world news in one image".

Run once, locally, to produce assets/entry.png (1024x1024, <=1 MiB).
The submitted program (main.py) is stdlib-only and copies that asset to
/output/entry.png deterministically; this builder is kept in the repo so
anyone can see exactly how the image was made.

News verified 2026-11-18 from BBC, Reuters/AP wires via One Turn News,
Hansen Intel, Foreign Exchanges and NPR summaries of 17 Nov 2026.
"""
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

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 30  # margin

# ---- Masthead ----
d.rectangle([0, 0, W, 84], fill=NAVY)
d.text((M, 12), "THE WORLD IN ONE PICTURE", font=font(SERIF_B, 40), fill=(255, 255, 255))
d.text((M, 58), "TUESDAY  17  NOVEMBER  2026  ·  12 STORIES  ·  6 CONTINENTS",
       font=font(SANS_B, 16), fill=(214, 200, 150))
d.rectangle([0, 84, W, 88], fill=RED)
y = 98
d.text((M, y), "THE DAY THE GULF CAUGHT FIRE — AND UKRAINE BROUGHT DOWN A BRIDGE",
       font=font(SANS_B, 15), fill=GREY)
y += 22
d.line([(M, y), (W - M, y)], fill=RULE, width=2)
y += 12

# ---- Lead story ----
y = kicker(d, M, y, "Lead  ·  The Gulf on edge")
y = para(d, M, y, "U.S. and Iran trade fire across the Gulf",
         font(SERIF_B, 36), W - 2 * M, leading=42)
y = para(d, M, y,
         "U.S. jets struck an Iranian missile site on Qeshm Island after Iran fired "
         "drones at a U.S. radar base in Bahrain — Tehran's third attack there in five "
         "days. Washington calls the strike self-defence; Iran denies a reported "
         "dirty-bomb plot against Washington.",
         font(SANS, 18), W - 2 * M, leading=23)
y += 6
d.line([(M, y), (W - M, y)], fill=RULE, width=2)
y += 8

# ---- Two-column second row ----
col_w = (W - 2 * M - 24) // 2
x2 = M + col_w + 24
y0 = y
yy = kicker(d, M, y0, "War  ·  Ukraine")
yy = para(d, M, yy, "Kerch Bridge section falls into the strait",
          font(SERIF_B, 24), col_w, leading=29)
yy = para(d, M, yy,
          "Ukrainian drones hit the bridge to Crimea for a second day; a road section "
          "collapsed into the water. Kyiv says the strike took weeks to plan.",
          font(SANS, 17), col_w, leading=22)
yy2 = kicker(d, x2, y0, "Diplomacy  ·  Asia")
yy2 = para(d, x2, yy2, "Trump flies to Manila, then on to Shenzhen",
           font(SERIF_B, 24), col_w, leading=29)
yy2 = para(d, x2, yy2,
           "The U.S. president heads to Asia for APEC, with talks lined up with "
           "China's Xi and Russia's Putin — Ukraine on the agenda.",
           font(SANS, 17), col_w, leading=22)
y = max(yy, yy2) + 6
d.line([(M, y), (W - M, y)], fill=RULE, width=2)
y += 8

# ---- Grid: 8 more stories, 2 columns x 4 rows ----
y = kicker(d, M, y, "More from Tuesday", size=16)
stories = [
    ("MARKETS", "Nvidia tops $115bn — Huang stays out",
     "Record revenue, about double a year earlier — yet ousted CEO Jensen Huang will not return."),
    ("HEALTH", "Ebola in DR Congo passes 11,000 cases",
     "Cases have more than doubled in three months, with 5,400 deaths, the UN reports."),
    ("MIDDLE EAST", "West urges Israel: open Gaza crossings",
     "Britain, Australia, Canada and Italy call the aid situation catastrophic; "
     "London sanctions eight settlement builders."),
    ("UKRAINE", "1,000-for-1,000 prisoner swap agreed",
     "Zelenskyy announces a large POW exchange after trilateral talks in Abu Dhabi."),
    ("ENERGY", "Houthis hit Saudi oil pipeline",
     "Drones target the East-West pipeline as Houthi forces advance toward Aden."),
    ("UNITED STATES", "America loses measles-free status",
     "After 26 years, the U.S. loses elimination status amid 5,400+ cases — a 40-year high."),
    ("SPACE", "Voyager 1 reaches one light-day out",
     "Nearly 50 years after launch, NASA's probe is now over 16 billion miles from Earth."),
    ("EUROPE", "146,000 march across France",
     "Unions strike over the cost of living; 28,000 protest in Paris."),
]
row_h = 104
for i in range(0, len(stories), 2):
    for j, (tag, head, body) in enumerate(stories[i:i + 2]):
        x = M + j * (col_w + 24)
        d.rounded_rectangle([x, y, x + col_w, y + row_h - 12], radius=8,
                            fill=CARD, outline=RULE, width=1)
        xx, yy3 = x + 12, y + 8
        yy3 = kicker(d, xx, yy3, tag, size=13)
        yy3 = para(d, xx, yy3, head, font(SERIF_B, 19), col_w - 24, leading=23)
        para(d, xx, yy3, body, font(SANS, 14), col_w - 24, leading=18)
    y += row_h
y += 2

# ---- Numbers strip ----
d.rectangle([M, y, W - M, y + 68], fill=NAVY)
nums = [("$115bn", "Nvidia revenue"), ("11,000", "Ebola cases"),
        ("1,000+", "POWs to swap"), ("146,000", "French protesters"),
        ("19", "killed in jet crash")]
seg = (W - 2 * M) // len(nums)
for i, (n, label) in enumerate(nums):
    cx = M + i * seg + seg // 2
    f1, f2 = font(SANS_B, 24), font(SANS, 13)
    d.text((cx - d.textlength(n, font=f1) / 2, y + 8), n, font=f1, fill=(255, 255, 255))
    d.text((cx - d.textlength(label, font=f2) / 2, y + 40), label, font=f2, fill=(214, 200, 150))
y += 68 + 10

# ---- Footer ----
d.text((M, y), "Compiled from BBC, Reuters, AP, Al Jazeera and NPR reporting of 17 November 2026.",
       font=font(SANS, 14), fill=GREY)
d.text((M, y + 18), "Also: Meta fined $887m in Italy · Mongolia's president resigns · Moldova shuts its airspace",
       font=font(SANS, 14), fill=GREY)

img.save("assets/entry.png", optimize=True)
print("saved assets/entry.png", img.size, "final y =", y)
