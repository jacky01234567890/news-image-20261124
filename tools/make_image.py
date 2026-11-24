#!/usr/bin/env python3
"""Draw the front page for Tuesday 24 November 2026.

A single 1024x1024 broadsheet-style image: masthead naming the day,
one lead story, four secondary stories and eight briefs, all verified
as events of 24 November 2026. Deterministic: fixed text, fixed
geometry, no randomness, no network, no timestamps in the output.
"""

from PIL import Image, ImageDraw, ImageFont
import os

# The rendered page lives at the entry root, beside tools/.
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "entry.png")

# --- canvas -----------------------------------------------------------------
W, H = 1024, 1024
PAPER = (248, 244, 234)   # warm newsprint
INK = (26, 26, 26)        # near-black body ink
RED = (164, 30, 34)       # kicker / rule red
NAVY = (31, 42, 68)       # night-sky panel
GREY = (90, 90, 90)       # captions and rules
FAINT = (210, 204, 188)   # hairline separators
MARGIN = 36
CW = W - 2 * MARGIN        # 952 usable width

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF = "DejaVuSerif-Bold.ttf"
SERIF_REG = "DejaVuSerif.ttf"
SANS = "DejaVuSans.ttf"
SANS_BOLD = "DejaVuSans-Bold.ttf"


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    """Draw wrapped lines top-down; returns the y just below the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, y, weight=2, fill=INK):
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=fill, width=weight)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead -----------------------------------------------------------
    small = font(SANS_BOLD, 12)
    d.text((MARGIN, 20), "ONE DAY  ·  ONE PAGE", font=small, fill=GREY)
    right = "ALL THE WORLD'S NEWS"
    d.text((W - MARGIN - d.textlength(right, font=small), 20),
           right, font=small, fill=GREY)

    title_f = font(SERIF, 56)
    title = "THE WORLD TODAY"
    d.text(((W - d.textlength(title, font=title_f)) / 2, 36),
           title, font=title_f, fill=INK)

    date_f = font(SERIF, 29)
    date = "Tuesday, 24 November 2026"
    d.text(((W - d.textlength(date, font=date_f)) / 2, 102),
           date, font=date_f, fill=RED)

    rule(d, 138, 3)
    rule(d, 143, 1)

    # --- lead story: the overnight drone war --------------------------------
    kicker_f = font(SANS_BOLD, 14)
    d.text((MARGIN, 156), "WAR IN UKRAINE  —  OVERNIGHT",
           font=kicker_f, fill=RED)

    head_f = font(SERIF, 44)
    head = "Russia says it downed 699 drones in one night"
    head_lines = wrap(d, head, head_f, CW)
    assert len(head_lines) == 2, head_lines
    y = draw_lines(d, head_lines, MARGIN, 178, head_f, INK, 50)

    deck_f = font(SANS, 19)
    deck = ("Moscow claims 355 of the drones were bound for the capital, "
            "with no casualties reported. Hours earlier, its strike on "
            "Zaporizhzhia killed two and wounded dozens, partly destroying "
            "a five-storey block.")
    deck_lines = wrap(d, deck, deck_f, CW)
    assert len(deck_lines) <= 3, deck_lines
    y = draw_lines(d, deck_lines, MARGIN, y + 8, deck_f, INK, 25)

    # Night-sky panel: a still, abstract picture of the drone wave.
    # Fixed dot positions from modular arithmetic, never random.
    px, py, pw, ph = MARGIN, y + 10, CW, 68
    d.rectangle([px, py, px + pw, py + ph], fill=NAVY)
    # crescent moon, upper left
    d.ellipse([px + 22, py + 12, px + 46, py + 36], fill=(240, 230, 180))
    d.ellipse([px + 32, py + 10, px + 54, py + 34], fill=NAVY)
    # drone dots drifting in from the left
    for i in range(26):
        dx = px + 90 + (i * 53) % 640
        dy = py + 12 + (i * 29) % 44
        d.ellipse([dx, dy, dx + 3, dy + 3], fill=(235, 235, 235))
    # interceptor streaks
    for sx, sy, ex, ey in [(120, 58, 330, 18), (300, 60, 520, 22),
                           (470, 58, 690, 20)]:
        d.line([(px + sx, py + sy), (px + ex, py + ey)],
               fill=(180, 190, 210), width=1)
    # red burst where one is hit, right side
    bx, by = px + 830, py + 34
    for ang in range(0, 360, 30):
        import math
        r = 26
        x2 = bx + r * math.cos(math.radians(ang))
        y2 = by + r * math.sin(math.radians(ang))
        d.line([(bx, by), (x2, y2)], fill=(230, 90, 60), width=2)
    d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=(240, 120, 70))

    cap_f = font(SERIF_REG, 13)
    cap = ("Night over Moscow: Russia claims a record drone wave — "
           "Kyiv has not commented on the figures.")
    d.text((MARGIN, py + ph + 6), cap, font=cap_f, fill=GREY)

    rule(d, 486, 1, fill=FAINT)

    # --- four secondary stories, two by two ---------------------------------
    # (tag, headline, body) — every story verified as 24 November 2026.
    stories = [
        ("KOREA",
         "Jet scare sends Ulleung islanders to shelters",
         "A suspected aircraft near the island at 07:52 prompts a shelter "
         "alert, lifted in five minutes. Seoul says a Russian plane entered "
         "the defence zone; the \u2018North Korean\u2019 wording may have been "
         "a training-template error."),
        ("NEPAL",
         "M5.3 quake shakes Nepal, felt in four nations",
         "A morning tremor in Koshi province rattles homes across India, "
         "Bhutan, Bangladesh and China. No casualties are reported."),
        ("SPACE",
         "China names Shenzhou-24 crew — first foreigner to visit Tiangong",
         "Commander Tang Hongbo, Wu Yi and Pakistani payload specialist "
         "Muhammad Zeeshan Ali — the first foreigner to visit Tiangong — "
         "lift off on Wednesday at 08:18 Beijing time."),
        ("MARKETS",
         "Nvidia shares soar 36% as Huang returns",
         "Hong Kong-listed shares jump in Tuesday trading after the board "
         "reinstates Jensen Huang as chief executive, following "
         "intervention by Donald Trump."),
    ]
    tag_f = font(SANS_BOLD, 13)
    sec_head_f = font(SERIF, 21)
    sec_body_f = font(SANS, 14)
    cell_w = (CW - 24) // 2
    cell_h = 148
    top0 = 500
    for i, (tag, headline, body) in enumerate(stories):
        col, row = i % 2, i // 2
        x = MARGIN + col * (cell_w + 24)
        y = top0 + row * (cell_h + 12)
        d.text((x, y), tag, font=tag_f, fill=RED)
        hl = wrap(d, headline, sec_head_f, cell_w)
        assert len(hl) <= 2, (tag, hl)
        y = draw_lines(d, hl, x, y + 18, sec_head_f, INK, 24)
        bl = wrap(d, body, sec_body_f, cell_w)
        assert len(bl) <= 4, (tag, bl)
        draw_lines(d, bl, x, y + 4, sec_body_f, INK, 19)
        if col == 0:
            d.line([(x + cell_w + 12, top0 + row * (cell_h + 12)),
                    (x + cell_w + 12,
                     top0 + row * (cell_h + 12) + cell_h)],
                   fill=FAINT, width=1)

    rule(d, 812, 1, fill=FAINT)

    # --- briefs --------------------------------------------------------------
    brief_head_f = font(SANS_BOLD, 15)
    d.text((MARGIN, 824), "ALSO TODAY", font=brief_head_f, fill=INK)
    briefs = [
        "PYONGYANG — North Korea may shut Switzerland's Pyongyang office "
        "after Bern sanctions a children's camp linked to Russia.",
        "WASHINGTON — Trump assails Newsom in a crime speech, condemning "
        "500-plus commuted death sentences.",
        "ISLAMABAD — A magnitude 4.1 earthquake strikes Pakistan in the "
        "morning, seismologists report.",
        "ISTANBUL — A lioness is spotted on the city's outskirts; 70-plus "
        "officers and drones search the forest.",
        "MEXICO CITY — Mexico and China agree a trade working group to "
        "narrow the gap in farm exports.",
        "WASHINGTON — Aviation groups seek $30bn to modernise the FAA "
        "after nationwide flight disruption.",
        "LONDON — Labour leader Burnham rules out rejoining the EU "
        "without a referendum.",
        "MOSCOW — Leaked Russian data points to nearly 500,000 soldiers "
        "dead, reports say.",
    ]
    brief_f = font(SANS, 14)
    for i, b in enumerate(briefs):
        col, row = i % 2, i // 2
        x = MARGIN + col * (cell_w + 24)
        y = 848 + row * 38
        bl = wrap(d, b, brief_f, cell_w)
        assert len(bl) <= 2, (i, bl)
        draw_lines(d, bl, x, y, brief_f, INK, 18)

    # --- footer: the day, once more ------------------------------------------
    rule(d, 999, 1, fill=FAINT)
    foot_f = font(SANS, 11)
    foot = ("Tuesday, 24 November 2026  ·  The world in one page  ·  "
            "All stories as reported on 24 November 2026")
    d.text(((W - d.textlength(foot, font=foot_f)) / 2, 1005),
           foot, font=foot_f, fill=GREY)

    img.save(OUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
