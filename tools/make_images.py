"""Build-time image generator for the README (Pillow only).

Run: python3 tools/make_images.py
Outputs: assets/hero.png (1200x630) + 4 gallery PNGs (800x500).
NOT imported by main.py — the entry itself is pure stdlib.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "assets")
os.makedirs(ASSETS, exist_ok=True)

FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def rrect(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def sky_lawn(d, w, h, horizon=0.62):
    d.rectangle([0, 0, w, int(h * horizon)], fill=(191, 227, 242))
    d.rectangle([0, int(h * horizon), w, h], fill=(124, 184, 92))
    # sun
    d.ellipse([w - 150, 30, w - 70, 110], fill=(255, 214, 90))
    # clouds
    for cx, cy, s in [(120, 70, 1.0), (300, 45, 0.7), (w - 320, 110, 0.8)]:
        d.ellipse([cx, cy, cx + 90 * s, cy + 34 * s], fill=(255, 255, 255))
        d.ellipse([cx + 30 * s, cy - 14 * s, cx + 110 * s, cy + 22 * s], fill=(255, 255, 255))


def fence(d, w, y_top, y_bot, color=(138, 90, 43), rail=(110, 70, 32)):
    d.rectangle([0, y_top + 28, w, y_top + 44], fill=rail)
    d.rectangle([0, y_bot - 44, w, y_bot - 28], fill=rail)
    x = 6
    while x < w:
        d.rectangle([x, y_top, x + 26, y_bot], fill=color)
        d.rectangle([x, y_top, x + 26, y_top + 8], fill=(160, 110, 55))
        x += 38


def dog_body(d, x, y, s=1.0):
    """Dog body/legs/tail — drawn BEFORE the fence (behind it)."""
    body = (176, 122, 69)
    dark = (120, 78, 40)
    # tail (wagging up)
    d.line([(x + 52 * s, y - 58 * s), (x + 78 * s, y - 96 * s)], fill=dark, width=int(10 * s))
    d.ellipse([x + 70 * s, y - 106 * s, x + 88 * s, y - 88 * s], fill=dark)
    # body
    d.ellipse([x - 70 * s, y - 78 * s, x + 62 * s, y - 6 * s], fill=body)
    # legs
    for lx in (-52, -28, 28, 50):
        d.rectangle([x + lx * s, y - 22 * s, x + (lx + 12) * s, y], fill=dark)


def dog_head(d, x, y, s=1.0):
    """Dog head + bark — drawn AFTER the fence (peeking over it)."""
    body = (176, 122, 69)
    dark = (120, 78, 40)
    light = (232, 196, 150)
    # head
    d.ellipse([x + 30 * s, y - 128 * s, x + 108 * s, y - 56 * s], fill=body)
    # floppy ear
    d.ellipse([x + 34 * s, y - 126 * s, x + 66 * s, y - 74 * s], fill=dark)
    # snout + nose
    d.ellipse([x + 84 * s, y - 92 * s, x + 122 * s, y - 62 * s], fill=light)
    d.ellipse([x + 110 * s, y - 90 * s, x + 126 * s, y - 74 * s], fill=(40, 26, 18))
    # eye
    d.ellipse([x + 74 * s, y - 112 * s, x + 86 * s, y - 100 * s], fill=(30, 20, 12))
    # front paws resting on the fence top rail
    d.rounded_rectangle([x + 40 * s, y - 62 * s, x + 58 * s, y - 40 * s], radius=int(6 * s), fill=light)
    d.rounded_rectangle([x + 66 * s, y - 62 * s, x + 84 * s, y - 40 * s], radius=int(6 * s), fill=light)
    # bark lines
    for i, (bx, by) in enumerate([(x + 140 * s, y - 130 * s), (x + 158 * s, y - 108 * s)]):
        d.line([(bx, by), (bx + 16 * s, by - 12 * s)], fill=(60, 60, 60), width=4)


def mailman(d, x, y, s=1.0):
    """Mailman walking away, blue uniform, cap, satchel. (x, y) = ground point."""
    navy = (47, 93, 138)
    dark = (32, 64, 96)
    skin = (232, 188, 150)
    # legs (mid-stride)
    d.line([(x, y - 70 * s), (x - 22 * s, y)], fill=dark, width=int(12 * s))
    d.line([(x, y - 70 * s), (x + 24 * s, y - 6 * s)], fill=dark, width=int(12 * s))
    # body / uniform
    d.rounded_rectangle([x - 26 * s, y - 140 * s, x + 26 * s, y - 64 * s], radius=int(14 * s), fill=navy)
    # arm + satchel strap
    d.line([(x + 18 * s, y - 128 * s), (x + 40 * s, y - 96 * s)], fill=navy, width=int(10 * s))
    d.rounded_rectangle([x + 22 * s, y - 104 * s, x + 66 * s, y - 58 * s], radius=int(8 * s), fill=(178, 134, 84))
    d.rectangle([x + 22 * s, y - 104 * s, x + 66 * s, y - 92 * s], fill=(150, 110, 66))
    # head + cap
    d.ellipse([x - 20 * s, y - 178 * s, x + 20 * s, y - 138 * s], fill=skin)
    d.pieslice([x - 22 * s, y - 186 * s, x + 22 * s, y - 152 * s], 180, 360, fill=navy)
    d.rectangle([x - 22 * s, y - 168 * s, x + 26 * s, y - 160 * s], fill=navy)


def hero():
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(img)
    sky_lawn(d, w, h, horizon=0.60)
    # path
    d.polygon([(760, 378), (1200, 378), (1200, 630), (700, 630)], fill=(214, 196, 160))
    dog_body(d, 330, 540, s=1.5)
    fence(d, w, 400, 560)
    dog_head(d, 330, 540, s=1.5)
    mailman(d, 1010, 472, s=1.0)  # stands on the path, behind the review card
    # title banner
    rrect(d, [36, 36, 700, 128], 18, fill=(24, 42, 66))
    d.text((60, 52), "THE DOG REVIEWS", font=font(FONT_B, 44), fill=(255, 255, 255))
    d.text((60, 100), "THE MAILMAN", font=font(FONT_B, 22), fill=(255, 214, 90))
    # review banner (bottom)
    rrect(d, [36, 470, 1164, 596], 18, fill=(255, 255, 255), outline=(24, 42, 66), width=3)
    f = font(FONT_R, 27)
    lines = wrap(d, "\u201cDear mailman: the fence is not keeping me in. It is keeping you alive. You\u2019re welcome.\u201d", f, 1060)
    yy = 484
    for ln in lines:
        d.text((60, yy), ln, font=f, fill=(24, 42, 66))
        yy += 34
    d.text((60, yy + 4), "\u2605\u2606\u2606\u2606\u2606  1 star  \u2014  from the dog on duty", font=font(FONT_B, 22), fill=(176, 122, 69))
    img.save(os.path.join(ASSETS, "hero.png"))


def gallery_fence():
    w, h = 800, 500
    img = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(img)
    sky_lawn(d, w, h, horizon=0.58)
    d.polygon([(520, 290), (800, 290), (800, 500), (480, 500)], fill=(214, 196, 160))
    dog_body(d, 240, 430, s=1.35)
    fence(d, w, 300, 440)
    dog_head(d, 240, 430, s=1.35)
    mailman(d, 640, 440, s=1.0)
    img.save(os.path.join(ASSETS, "gallery-fence.png"))


def gallery_review():
    w, h = 800, 500
    img = Image.new("RGB", (w, h), (250, 244, 230))
    d = ImageDraw.Draw(img)
    rrect(d, [60, 50, 740, 450], 24, fill=(255, 255, 255), outline=(24, 42, 66), width=3)
    d.text((100, 80), "\u2605\u2606\u2606\u2606\u2606", font=font(FONT_B, 54), fill=(255, 176, 32))
    d.text((100, 150), "1 out of 5 stars", font=font(FONT_B, 26), fill=(176, 122, 69))
    f = font(FONT_R, 30)
    lines = wrap(d, "\u201cDear mailman: the fence is not keeping me in. It is keeping you alive. You\u2019re welcome.\u201d", f, 580)
    yy = 210
    for ln in lines:
        d.text((100, yy), ln, font=f, fill=(24, 42, 66))
        yy += 42
    d.text((100, 380), "\u2014 The Dog, Head of Security", font=font(FONT_B, 24), fill=(90, 90, 90))
    img.save(os.path.join(ASSETS, "gallery-review.png"))


def gallery_bag():
    w, h = 800, 500
    img = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(img)
    sky_lawn(d, w, h, horizon=0.58)
    # big satchel centre
    d.rounded_rectangle([250, 150, 550, 360], radius=24, fill=(178, 134, 84))
    d.rectangle([250, 150, 550, 196], fill=(150, 110, 66))
    d.rectangle([370, 120, 430, 160], fill=(120, 88, 50))
    # tag
    d.polygon([(470, 210), (545, 210), (545, 260), (507, 285), (470, 260)], fill=(255, 255, 255), outline=(24, 42, 66))
    d.text((483, 224), "NO", font=font(FONT_B, 20), fill=(180, 40, 40))
    d.text((476, 248), "TREATS", font=font(FONT_B, 13), fill=(180, 40, 40))
    # dog head sniffing from the left (profile)
    d.ellipse([45, 285, 165, 405], fill=(176, 122, 69))  # head
    d.ellipse([55, 288, 105, 350], fill=(120, 78, 40))   # ear
    d.ellipse([140, 318, 235, 368], fill=(176, 122, 69))  # snout bridge
    d.ellipse([205, 322, 258, 362], fill=(232, 196, 150))  # muzzle
    d.ellipse([240, 328, 266, 354], fill=(40, 26, 18))    # nose
    d.ellipse([105, 320, 119, 334], fill=(30, 20, 12))    # eye
    # sniff lines
    for i, y in enumerate((300, 330, 360)):
        d.line([(272, y), (302, y - 8)], fill=(90, 90, 90), width=4)
    # caption
    f = font(FONT_B, 30)
    d.text((60, 420), "Six years. 1,500 visits. Zero sniffs allowed.", font=f, fill=(24, 42, 66))
    img.save(os.path.join(ASSETS, "gallery-bag.png"))


def gallery_tournament():
    w, h = 800, 500
    img = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((40, 24), "How the line was picked", font=font(FONT_B, 32), fill=(24, 42, 66))
    boxes = [
        (40, 90, 250, 170, "31 candidates", "12 comedy devices", (191, 227, 242)),
        (40, 200, 250, 280, "Top 8 seeds", "scored /25", (191, 227, 242)),
        (40, 310, 250, 390, "Knockout", "QF \u2192 SF \u2192 Final", (191, 227, 242)),
        (40, 410, 250, 480, "Self-pairwise", "vs 2 runners-up", (191, 227, 242)),
    ]
    for x0, y0, x1, y1, t1, t2, fill in boxes:
        rrect(d, [x0, y0, x1, y1], 14, fill=fill)
        d.text((x0 + 16, y0 + 12), t1, font=font(FONT_B, 24), fill=(24, 42, 66))
        d.text((x0 + 16, y0 + 46), t2, font=font(FONT_R, 18), fill=(60, 60, 60))
    # arrows
    for y in (130, 240, 350, 445):
        d.line([(252, y), (300, y)], fill=(24, 42, 66), width=4)
        d.polygon([(300, y), (286, y - 8), (286, y + 8)], fill=(24, 42, 66))
    # winner box
    rrect(d, [310, 90, 760, 470], 18, fill=(255, 244, 200), outline=(176, 122, 69), width=3)
    d.text((340, 110), "WINNER  \u00b7  24/25", font=font(FONT_B, 26), fill=(176, 122, 69))
    f = font(FONT_R, 26)
    lines = wrap(d, "\u201cDear mailman: the fence is not keeping me in. It is keeping you alive. You\u2019re welcome.\u201d", f, 400)
    yy = 170
    for ln in lines:
        d.text((340, yy), ln, font=f, fill=(24, 42, 66))
        yy += 36
    d.text((340, 400), "86 characters  \u00b7  1 line  \u00b7  0 treats", font=font(FONT_B, 19), fill=(90, 90, 90))
    img.save(os.path.join(ASSETS, "gallery-tournament.png"))


if __name__ == "__main__":
    hero()
    gallery_fence()
    gallery_review()
    gallery_bag()
    gallery_tournament()
    for name in ("hero.png", "gallery-fence.png", "gallery-review.png",
                 "gallery-bag.png", "gallery-tournament.png"):
        p = os.path.join(ASSETS, name)
        print(name, os.path.getsize(p), "bytes")
