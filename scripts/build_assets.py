"""Draw the profile header and project cards into assets/.

Usage: python3 scripts/build_assets.py

To add a project, add a row to CARDS, re-run, and link the new card in README.md.
Colors, fonts and the contribution-graph greens are GitHub's own dark theme, so the
images read as part of the page. Fonts are GitHub's system stacks; an SVG shown
through <img> cannot load web fonts anyway.
"""
import random
import textwrap
from html import escape
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

# GitHub dark
CANVAS, SURFACE, BORDER = "#0d1117", "#161b22", "#30363d"
FG, MUTED, LINK = "#e6edf3", "#8b949e", "#58a6ff"
LEVELS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]  # contribution graph, none to most

# Label colors: text, border
STATUS = {
    "live": ("#3fb950", "#238636"),
    "new": ("#58a6ff", "#1f6feb"),
    "shipped": ("#8b949e", "#30363d"),
    "ongoing": ("#a371f7", "#8957e5"),
}
# Linguist colors
LANG = {"Python": "#3572A5", "TypeScript": "#3178c6", "HTML": "#e34c26", "Markdown": "#083fa1",
        "Claude Code plugin": "#8b949e"}

# slug, title, status, link text, blurb, language, month shipped in 2026 (1-12)
CARDS = [
    ("sentinel", "Sentinel", "live", "sentinel.sandip.dev",
     "Governed agentic data science for a regulated bank. Twenty-six controls, each naming the regulation it answers to.",
     "Python", 7),
    ("ludllm", "LudLLM", "shipped", "github.com/devsandip/ludLLM",
     "An agentic pipeline that writes a full-length spy novel. A secret holds for 80,000 words and lands on schedule.",
     "Python", 6),
    ("mailmcp", "mailmcp", "new", "github.com/devsandip/mailmcp",
     "A self-hosted Gmail MCP server for Claude. Many Google accounts, your own AWS account, about $1 a month.",
     "TypeScript", 10),
    ("wndrist", "wndr.ist", "live", "wndr.ist",
     "An AI road-trip planner for multi-day drives across the US. It builds the route, picks the night stops, writes the days.",
     "HTML", 4),
    ("samaritan", "samaritan", "shipped", "github.com/devsandip/samaritan",
     "An AI PM operating system. Capture, file, recall and synthesize across Obsidian, Notion and a task manager.",
     "Claude Code plugin", 5),
    ("skills", "my-claude-skills", "ongoing", "github.com/devsandip/my-claude-skills",
     "The Claude Code skills I use every day. The big one keeps a journal for solo projects across sessions.",
     "Markdown", 5),
]

# 5-row pixel glyphs, drawn into rows 1-5 of the 7-row graph
GLYPHS = {
    "S": [".###", "#...", ".##.", "...#", "###."],
    "A": [".##.", "#..#", "####", "#..#", "#..#"],
    "N": ["#..#", "##.#", "#.##", "#..#", "#..#"],
    "D": ["###.", "#..#", "#..#", "#..#", "###."],
    "I": ["###", ".#.", ".#.", ".#.", "###"],
    "P": ["###.", "#..#", "###.", "#...", "#..."],
    "E": ["####", "#...", "###.", "#...", "####"],
    "V": ["#...#", "#...#", "#...#", ".#.#.", "..#.."],
    " ": ["..", "..", "..", "..", ".."],
}
REPO_ICON = ("M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 "
             "0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 "
             "9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 "
             "15.7a.25.25 0 0 1-.4-.2Z")


def svg_open(w, h, title, desc, style=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-labelledby="t d">\n<title id="t">{escape(title)}</title>'
            f'<desc id="d">{escape(desc)}</desc>\n<style>{style}</style>\n')


def text(x, y, s, size, fill, fam=SANS, anchor="start", weight=None):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    w = f' font-weight="{weight}"' if weight else ""
    return f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" fill="{fill}"{a}{w}>{s}</text>\n'


def header():
    W, H = 960, 300
    cols, rows, cell, pitch = 53, 7, 13, 16
    gx, gy = 80, 128  # graph origin

    # name as a set of lit cells, centred in the 53-week grid
    word = "SANDIP DEV"
    width = sum(len(GLYPHS[ch][0]) for ch in word) + len(word) - 1
    lit, x = {}, (cols - width) // 2
    rng = random.Random(2012)
    for ch in word:
        g = GLYPHS[ch]
        for r, line in enumerate(g):
            for c, px in enumerate(line):
                if px == "#":
                    lit[(x + c, r + 1)] = rng.choice([3, 4, 4, 4])
        x += len(g[0]) + 1

    s = svg_open(W, H, "Sandip Dev", "SANDIP DEV spelled out in a GitHub contribution graph.")
    s += f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="6" fill="{CANVAS}" stroke="{BORDER}"/>\n'
    s += text(24, 44, "Sandip Dev", 24, FG, weight=600)
    s += text(24, 70, "Senior product manager. Nine years at Amazon. Builds things at night.", 15, MUTED)
    s += text(W - 24, 44, "Guwahati, IN", 14, MUTED, anchor="end")

    # month labels for the year ending Oct 2026, the way GitHub draws them
    months = ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"]
    for i, m in enumerate(months):
        s += text(gx + round(i * 4.42) * pitch, gy - 10, m, 12, MUTED)
    for r, d in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        s += text(gx - 12, gy + r * pitch + 11, d, 12, MUTED, anchor="end")

    for c in range(cols):
        for r in range(rows):
            x0, y0 = gx + c * pitch, gy + r * pitch
            lvl = lit.get((c, r))
            if lvl:
                s += f'<rect x="{x0}" y="{y0}" width="{cell}" height="{cell}" rx="2" fill="{LEVELS[lvl]}"/>\n'
            else:
                s += f'<rect x="{x0}" y="{y0}" width="{cell}" height="{cell}" rx="2" fill="{LEVELS[0]}" stroke="#1b1f23" stroke-width="0.5"/>\n'

    by = gy + rows * pitch + 26
    s += text(gx, by, "9 side projects shipped in 2026", 12, MUTED)
    lx = gx + cols * pitch - 3
    s += text(lx, by, "More", 12, MUTED, anchor="end")
    for i in range(5):
        s += f'<rect x="{lx - 36 - (4 - i) * pitch - cell}" y="{by - 11}" width="{cell}" height="{cell}" rx="2" fill="{LEVELS[i]}"/>\n'
    s += text(lx - 36 - 4 * pitch - cell - 6, by, "Less", 12, MUTED, anchor="end")
    return s + "</svg>\n"


def card(title, status, dest, blurb, lang, month):
    W, H = 480, 196
    s = svg_open(W, H, title, blurb)
    s += f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="6" fill="{CANVAS}" stroke="{BORDER}"/>\n'
    s += f'<path transform="translate(20 22)" fill="{MUTED}" d="{REPO_ICON}"/>\n'
    s += text(44, 36, escape(title), 17, LINK, weight=600)
    fg, bd = STATUS[status]
    pw = len(status) * 7 + 18
    s += f'<rect x="{W - 20 - pw}" y="22" width="{pw}" height="20" rx="10" fill="none" stroke="{bd}"/>\n'
    s += text(W - 20 - pw / 2, 36, status, 12, fg, anchor="middle", weight=500)
    s += text(44, 58, escape(dest), 12, MUTED, fam=MONO)
    for i, line in enumerate(textwrap.wrap(blurb, 60, break_on_hyphens=False)[:3]):
        s += text(20, 90 + i * 21, escape(line), 14, MUTED)
    # language
    s += f'<circle cx="26" cy="168" r="6" fill="{LANG[lang]}"/>\n'
    s += text(38, 172, escape(lang), 12, MUTED)
    # the 2026 strip: one cell per month, the shipping month lit
    names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sx = W - 20 - 12 * 12 + 2
    for m in range(12):
        fill = LEVELS[4] if m + 1 == month else SURFACE
        s += f'<rect x="{sx + m*12}" y="162" width="10" height="10" rx="2" fill="{fill}"/>\n'
    s += text(sx - 8, 172, f"shipped {names[month-1]} 2026", 12, MUTED, anchor="end")
    return s + "</svg>\n"


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "header.svg").write_text(header(), encoding="utf-8")
    for slug, *fields in CARDS:
        (ASSETS / f"card-{slug}.svg").write_text(card(*fields), encoding="utf-8")
    print(f"wrote header and {len(CARDS)} cards to {ASSETS}")
