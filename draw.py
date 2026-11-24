#!/usr/bin/env python3
"""news-23 b84 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026."""
from PIL import Image, ImageDraw, ImageFont
import os, textwrap

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

def font(name, size):
    cands = {
        "serif_b": ["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"],
        "serif": ["/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"],
        "sans_b": ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
        "sans": ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
    }
    for p in cands.get(name, []):
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            pass
    return ImageFont.load_default(size)

def wrap(d, text, fnt, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def chip(d, x, y, label, color):
    f = font("sans_b", 9)
    tw = d.textlength(label, font=f)
    w = int(tw) + 10
    d.rounded_rectangle([x, y, x + w, y + 14], radius=3, fill=color)
    d.text((x + 5, y + 2), label, font=f, fill="white")
    return w

img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

BLACK = (0, 0, 0)
RED = (176, 0, 32)
GOLD = (184, 134, 11)
NAVY = (16, 32, 64)
GREEN = (0, 90, 60)
CREAM = (245, 240, 220)
GRAY = (90, 90, 90)
BLUE = (18, 60, 150)
TEAL = (0, 120, 110)
PURPLE = (110, 50, 140)

# ---------- masthead ----------
d.rectangle([0, 0, W, 50], fill=BLACK)
d.text((10, 6), "THE WORLD TODAY", font=font("serif_b", 42), fill="white")
d.text((W - 10, 20), "MONDAY 23 NOVEMBER 2026", font=font("sans_b", 15), fill=(212, 175, 55), anchor="ra")

# ---------- kicker ----------
d.rectangle([0, 50, W, 74], fill=RED)
d.text((W // 2, 56), "AI rout hits Asia  ·  UN chief urges AI rules  ·  US lead over China at record low  ·  Anthropic IPO $107.3B",
       font=font("sans_b", 14), fill="white", anchor="ma")

# ---------- number strip ----------
nums = [
    ("-3.3%", "KOSPI", RED), ("5.3", "US-CHINA POWER GAP", BLUE),
    ("11,762", "EBOLA CASES, DRC", (0, 120, 60)), ("10T won", "SEOUL STABILISATION FUND", (150, 110, 0)),
    ("2%", "BILLIONAIRE TAX IN PARIS", PURPLE),
    ("$450M", "SKUBAL DEAL", BLUE), ("165", "RUSSIAN MISSILES/WEEK", RED),
    ("12,000", "CLEARED IN MANCHESTER", (0, 120, 60)), ("264 kg", "EXPLOSIVES SEIZED", (150, 110, 0)),
    ("$107.3B", "ANTHROPIC IPO", PURPLE),
]
colw = W // 5
for i, (val, lab, col) in enumerate(nums):
    x = (i % 5) * colw + 8
    y = 78 if i < 5 else 110
    d.text((x, y), val, font=font("sans_b", 19), fill=col)
    d.text((x, y + 20), lab, font=font("sans", 9), fill=BLACK)

# ---------- region bar ----------
regions = [("ASIA-PACIFIC 7", NAVY), ("AMERICAS 8", RED), ("MIDDLE EAST 6", (150, 110, 0)),
           ("EUROPE 5", TEAL), ("AFRICA 3", PURPLE), ("WORLD 2", (60, 60, 60))]
seg = W // 6
for i, (lab, col) in enumerate(regions):
    x = i * seg
    d.rectangle([x, 140, x + seg - 1, 158], fill=col)
    d.text((x + seg // 2, 144), lab, font=font("sans_b", 11), fill="white", anchor="ma")

# ---------- UTC strip ----------
d.text((8, 160), "THE DAY IN UTC   ~00:00 Kospi dives   ~06:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles",
       font=font("sans", 10), fill=GRAY)
d.text((W - 8, 160), "~ APPROX", font=font("sans", 10), fill=GRAY, anchor="ra")

# ---------- heroes ----------
HX = [8, 350, 692]
HW = 324
hy = 174
scene_h = 106
# --- hero 1: Kospi chart scene ---
x0 = HX[0]
d.rectangle([x0, hy, x0 + HW, hy + scene_h], fill=NAVY)
d.text((x0 + 8, hy + 6), "-3.3%", font=font("sans_b", 26), fill=(255, 80, 80))
# buildings with lit windows
import random
random.seed(23)
bx = x0 + 6
while bx < x0 + HW - 14:
    bw = random.randint(18, 30)
    bh = random.randint(30, 78)
    d.rectangle([bx, hy + scene_h - bh, bx + bw, hy + scene_h], fill=(8, 18, 44))
    for wy in range(hy + scene_h - bh + 5, hy + scene_h - 6, 9):
        for wx in range(bx + 4, bx + bw - 3, 7):
            if random.random() < 0.55:
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 210, 90))
    bx += bw + 3
# orange chart line
pts = [(x0 + 10, hy + 62), (x0 + 60, hy + 78), (x0 + 110, hy + 58), (x0 + 160, hy + 70),
       (x0 + 210, hy + 44), (x0 + 260, hy + 52), (x0 + 312, hy + 30)]
d.line(pts, fill=(255, 140, 40), width=3)
for p in pts:
    d.ellipse([p[0] - 3, p[1] - 3, p[0] + 3, p[1] + 3], fill="white")
d.rectangle([x0, hy + scene_h - 16, x0 + HW, hy + scene_h], fill=BLACK)
d.text((x0 + 6, hy + scene_h - 14), "KOSPI 4,708.54   -161 PTS", font=font("sans_b", 10), fill="white")

# --- hero 2: Guterres globe scene ---
x0 = HX[1]
d.rectangle([x0, hy, x0 + HW, hy + scene_h], fill=GREEN)
d.text((x0 + 10, hy + 8), "150 DELEGATES", font=font("sans_b", 26), fill=(255, 210, 90))
d.text((x0 + 10, hy + 38), "BACK A RISK", font=font("sans_b", 26), fill=(255, 210, 90))
d.text((x0 + 10, hy + 68), "FRAMEWORK", font=font("sans_b", 26), fill=(255, 210, 90))
# globe
cx, cy, r = x0 + HW - 48, hy + 52, 40
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(190, 225, 200), outline=(255, 255, 255), width=2)
for k in range(-2, 3):
    d.arc([cx - r + abs(k) * 8, cy - r, cx + r - abs(k) * 8, cy + r], 90, 270, fill=(0, 90, 60), width=1)
d.line([cx - r, cy, cx + r, cy], fill=(0, 90, 60), width=1)
d.rectangle([x0, hy + scene_h - 16, x0 + HW, hy + scene_h], fill=BLACK)
d.text((x0 + 6, hy + scene_h - 14), "UN  ·  BRIDGETOWN", font=font("sans_b", 10), fill="white")

# --- hero 3: Power Index bars ---
x0 = HX[2]
d.rectangle([x0, hy, x0 + HW, hy + scene_h], fill=CREAM)
d.text((x0 + 8, hy + 6), "NARROWEST SINCE 2018", font=font("sans_b", 11), fill=BLACK)
d.text((x0 + HW - 8, hy + 6), "GAP 5.3", font=font("sans_b", 11), fill=RED, anchor="ra")
bars = [("78.9", "US", NAVY, 78.9), ("73.6", "CHINA", RED, 73.6), ("40.5", "INDIA", GOLD, 40.5)]
bw = 86
for i, (val, lab, col, v) in enumerate(bars):
    bx = x0 + 14 + i * 104
    bh = int(v / 78.9 * 38)
    d.text((bx + bw // 2, hy + 28), val, font=font("sans_b", 17), fill=BLACK, anchor="ma")
    d.rectangle([bx, hy + 48, bx + bw, hy + 48 + bh], fill=col)
    d.text((bx + bw // 2, hy + 48 + bh - 16), lab, font=font("sans_b", 11), fill="white", anchor="ma")
d.rectangle([x0, hy + scene_h - 16, x0 + HW, hy + scene_h], fill=BLACK)
d.text((x0 + 6, hy + scene_h - 14), "ASIA POWER INDEX 2026", font=font("sans_b", 10), fill="white")

# hero headlines / bodies / source+chip
heroes = [
    ("AI ROUT HITS ASIA", "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.", "KOREA EXCHANGE"),
    ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE", "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.", "UNITED NATIONS"),
    ("US LEAD OVER CHINA AT RECORD LOW", "Asia Power Index 2026: US 78.9, China 73.6 — gap 5.3, narrowest since 2018. India third at 40.5.", "LOWY INSTITUTE"),
]
for i, (hl, body, src) in enumerate(heroes):
    x0 = HX[i]
    y = hy + scene_h + 6
    lines = wrap(d, hl, font("serif_b", 20), HW)
    for ln in lines[:2]:
        d.text((x0, y), ln, font=font("serif_b", 20), fill=BLACK)
        y += 22
    blines = wrap(d, body, font("sans", 11), HW)
    for ln in blines[:2]:
        d.text((x0, y), ln, font=font("sans", 11), fill=BLACK)
        y += 13
    # source + chip row, fixed y so it never touches the MORE strip
    sy = hy + scene_h + 84
    d.text((x0, sy + 2), src, font=font("sans", 9), fill=GRAY)
    chip(d, x0 + HW - 62, sy, "REPORTED", BLUE)

# ---------- MORE strip ----------
d.rectangle([0, 380, W, 398], fill=BLACK)
d.text((8, 384), "MORE OF THE DAY  —  10 STORIES", font=font("sans_b", 12), fill="white")

# ---------- cards ----------
cards = [
    ("AMERICAS", "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "Reuters", "REPORTED", BLUE, NAVY),
    ("FBI", "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED", BLUE, NAVY),
    ("WHITE HOUSE", "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED", BLUE, (150, 110, 0)),
    ("MARKETS", "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", "REPORTED", BLUE, TEAL),
    ("SPORT", "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED", BLUE, RED),
    ("SPORT", "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", "REPORTED", BLUE, RED),
    ("LEGAL", "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED", BLUE, PURPLE),
    ("TECH", "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", "REPORTED", BLUE, TEAL),
    ("EUROPE", "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM", RED, (150, 110, 0)),
    ("SPACE", "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM", RED, PURPLE),
]
cw = 197
gap = 6
for i, (cat, hl, body, src, chip_lab, chip_col, cat_col) in enumerate(cards):
    cx = 8 + (i % 5) * (cw + gap)
    cy = 404 + (i // 5) * 80
    d.rectangle([cx, cy, cx + cw, cy + 13], fill=cat_col)
    d.text((cx + 4, cy + 1), cat, font=font("sans_b", 9), fill="white")
    d.text((cx + cw - 4, cy + 1), str(i + 1), font=font("sans_b", 9), fill="white", anchor="ra")
    y = cy + 17
    for ln in wrap(d, hl, font("sans_b", 12), cw - 4)[:2]:
        d.text((cx + 2, y), ln, font=font("sans_b", 12), fill=BLACK)
        y += 14
    # body, width-guarded so it never reaches the chip
    bl = body
    while d.textlength(bl, font=font("sans", 9)) > 128 and len(bl) > 3:
        bl = bl[:-4].rstrip() + "…"
    d.text((cx + 2, cy + 47), bl, font=font("sans", 9), fill=BLACK)
    d.text((cx + 2, cy + 62), src, font=font("sans", 9), fill=GRAY)
    chip(d, cx + cw - 62, cy + 60, chip_lab, chip_col)

# ---------- WHERE / ALSO strip ----------
d.rectangle([0, 562, W, 580], fill=BLACK)
d.text((8, 566), "WHERE IT HAPPENED", font=font("sans_b", 12), fill="white")
d.text((340, 566), "ALSO ON MONDAY", font=font("sans_b", 12), fill="white")

# ---------- map ----------
mx, my, mw, mh = 8, 586, 320, 232
d.rectangle([mx, my, mx + mw, my + mh], outline=BLACK, width=1)
# stylised continents (light green blobs)
d.polygon([(30, 620), (70, 600), (110, 610), (130, 640), (120, 690), (95, 740), (60, 770), (30, 740), (25, 680)], fill=(200, 230, 190))  # Americas
d.polygon([(150, 610), (200, 600), (240, 615), (250, 650), (220, 675), (175, 670), (150, 640)], fill=(200, 230, 190))  # Europe/Asia top
d.polygon([(190, 690), (250, 680), (300, 700), (295, 740), (240, 760), (195, 735)], fill=(200, 230, 190))  # Asia
d.polygon([(255, 775), (285, 770), (300, 790), (275, 805), (250, 795)], fill=(200, 230, 190))  # Australia
pins = [
    (1, 270, 700), (2, 115, 720), (3, 245, 695), (4, 95, 660), (5, 105, 640),
    (6, 195, 635), (7, 80, 665), (8, 40, 690), (9, 65, 700), (10, 75, 730),
    (11, 175, 625), (12, 160, 615), (13, 225, 685),
]
for n, px, py in pins:
    d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline="white", width=1)
    d.text((px, py - 5), str(n), font=font("sans_b", 8), fill="white", anchor="ma")
d.text((mx + 6, my + mh - 34), "Pins 1-13: 1 Seoul · 2 Bridgetown · 3 Beijing", font=font("sans", 9), fill=BLACK)
d.text((mx + 6, my + mh - 23), "4 Washington · 5 New York · 6 Kyiv · 7 Chicago · 8 SF", font=font("sans", 9), fill=BLACK)
d.text((mx + 6, my + mh - 12), "9 Denver · 10 Austin · 11 Warsaw · 12 London · 13 Moscow", font=font("sans", 9), fill=BLACK)

# ---------- ALSO list ----------
also = [
    ("14. Paris: 100+ back 2% billionaire tax", False),
    ("15. Manchester: 12,000 cleared", False),
    ("16. Zelenskyy: 165 missiles in a week", False),
    ("17. COP31: the day after pact rejected", False),
    ("18. Benghazi: UN demands probe of port attacks", True),
    ("19. Israel unity talks resume", False),
    ("20. Gaza: two killed in Israeli strike", False),
    ("21. West Bank settler attacks", False),
    ("22. Iran war: no deal in sight", False),
    ("23. Lebanon seizes 264 kg explosives", False),
    ("24. Bahrain: strike hits plant, 2 hurt", False),
    ("25. Sudan: defences down drones", True),
    ("26. DRC: fighting traps Ebola teams", False),
    ("27. Bangladesh: Hasina jailed if she returns", False),
    ("28. Seoul minister quits in exam row", False),
    ("29. SK Telecom -7.3% as hype cools", False),
    ("30. China eases margin rules", False),
    ("31. Seoul readies 10T-won fund", False),
]
ay = 588
for txt, is_claim in also:
    d.text((340, ay), txt, font=font("sans", 11), fill=RED if is_claim else BLACK)
    if is_claim:
        d.text((340 + d.textlength(txt, font=font("sans", 11)) + 4, ay), "[CLAIM]", font=font("sans_b", 10), fill=RED)
    ay += 12

# ---------- DATE CHECK ----------
d.rectangle([8, 826, W - 8, 898], outline=RED, width=2)
d.text((14, 830), "DATE CHECK", font=font("sans_b", 12), fill=RED)
d.text((W - 14, 830), "READ 23 NOV 2026, 23:59 UTC — STORIES DATED 23 NOV ONLY", font=font("sans_b", 9), fill=RED, anchor="ra")
d.text((14, 850), "LEFT OUT — NOT 23 NOV:  Dems 258 seats (22 Nov) · Sparta II fire (22 Nov) · El Chapo (22 Nov) · EU-Indonesia (21 Nov) · Nigeria boat (21 Nov) · ICJ Myanmar (19 Nov)",
       font=font("sans", 10), fill=BLACK)
d.text((14, 868), "NOT YET — Dymer search continues (14 missing) · 4 House races uncalled · COP32 venue not set · WHO evacuating trapped Ebola staff",
       font=font("sans", 10), fill=BLACK)

# ---------- footer ----------
d.text((8, 906), "Sources: Reuters · AP · Bloomberg · AFP · Yonhap · BBC · WSJ · NYT · ESPN · Lowy Institute (Asia Power Index 2026).", font=font("sans", 9), fill=GRAY)
d.text((8, 920), "CHIPS: REPORTED = confirmed by wires. CLAIM = one side's claim, not independently confirmed. ONGOING = still developing.", font=font("sans", 9), fill=GRAY)
d.text((8, 934), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.", font=font("sans", 9), fill=GRAY)
d.line([8, 952, W - 8, 952], fill=GOLD, width=2)
d.text((W // 2, 962), "THE WORLD TODAY  —  Monday 23 November 2026  ·  31 stories  ·  6 regions",
       font=font("sans_b", 13), fill=GOLD, anchor="ma")

img.save(OUT)
print("saved", OUT, os.path.getsize(OUT), "bytes")
