"""Draw the profile header and project cards into assets/.

Usage: python3 scripts/build_assets.py

To add a project, add a row to CARDS, re-run, and link the new card in README.md.
Everything uses the sandip.dev "ink" palette. Fonts are system stacks because an SVG
shown through <img> cannot load web fonts.
"""
import textwrap
from html import escape
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

SERIF = "'Iowan Old Style', 'Palatino Linotype', Palatino, 'Book Antiqua', Georgia, serif"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

PAPER, CARD_BG = "#0E0E10", "#16161A"
INK, SOFT, SOFTER = "#F2F2F4", "#9A9AA3", "#6E6E77"
RULE, ACCENT, LIVE = "#2A2A30", "#E07650", "#6B9F4D"

# slug, title, eyebrow, date, blurb, stack, where the card links (shown bottom right)
CARDS = [
    ("sentinel", "Sentinel", "// ai · governance", "jul 2026",
     "Governed agentic data science for a regulated bank. Twenty-six controls, each naming the regulation it answers to.",
     "python", "sentinel.sandip.dev ↗"),
    ("ludllm", "LudLLM", "// ai · llm", "jun 2026",
     "An agentic pipeline that writes a full-length spy novel. A secret holds for 80,000 words and lands on schedule.",
     "python", "devsandip/ludLLM ↗"),
    ("mailmcp", "mailmcp", "// mcp · aws", "oct 2026",
     "A self-hosted Gmail MCP server for Claude. Many Google accounts, your own AWS account, about $1 a month.",
     "typescript", "devsandip/mailmcp ↗"),
    ("wndrist", "wndr.ist", "// ai · travel", "apr 2026",
     "An AI road-trip planner for multi-day drives across the US. It builds the route, picks the night stops, writes the days.",
     "typescript", "wndr.ist ↗"),
    ("samaritan", "samaritan", "// ai · pm os", "may 2026",
     "An AI PM operating system. Capture, file, recall and synthesize across Obsidian, Notion and a task manager.",
     "claude code plugin", "devsandip/samaritan ↗"),
    ("skills", "my-claude-skills", "// claude code", "may 2026",
     "The Claude Code skills I use every day. The big one keeps a journal for solo projects across sessions.",
     "markdown", "devsandip/my-claude-skills ↗"),
]

PULSE = ("@keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}"
         ".dot{animation:pulse 2.4s ease-in-out infinite}"
         "@media (prefers-reduced-motion: reduce){.dot{animation:none}}")


def svg_open(w, h, title, desc, style=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-labelledby="t d">\n<title id="t">{escape(title)}</title>'
            f'<desc id="d">{escape(desc)}</desc>\n<style>{style}</style>\n')


def text(x, y, s, fam, size, fill, anchor="start", ls=None):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    l = f' letter-spacing="{ls}"' if ls else ""
    return f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" fill="{fill}"{a}{l}>{s}</text>\n'


def header():
    W, H = 960, 320
    s = svg_open(W, H, "Sandip Dev", "Product builder, quietly opinionated. I turn coffee into shipped products.", PULSE)
    s += f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="{PAPER}" stroke="{RULE}"/>\n'
    s += text(48, 58, "// product builder, est. 2012", MONO, 14, SOFTER)
    s += f'<circle class="dot" cx="690" cy="53.5" r="3.5" fill="{LIVE}"/>\n'
    s += text(704, 58, "AVAILABLE · GUWAHATI, IN", MONO, 13, SOFT, ls="0.06em")
    s += (f'<text x="44" y="178" font-family="{SERIF}" font-size="108" fill="{INK}" letter-spacing="-0.02em">'
          f'Sandip Dev<tspan fill="{ACCENT}">.</tspan></text>\n')
    s += text(48, 226, "I turn coffee into shipped products.", SANS, 26, SOFT)
    s += f'<line x1="48" y1="262" x2="{W-48}" y2="262" stroke="{RULE}"/>\n'
    s += text(48, 292, "SENIOR PM · EX-AMAZON · IIM AHMEDABAD · NIT SURAT", MONO, 13, SOFTER, ls="0.06em")
    s += text(W - 48, 292, "26.14°N 91.74°E", MONO, 13, SOFTER, anchor="end", ls="0.06em")
    return s + "</svg>\n"


def card(title, eyebrow, date, blurb, stack, dest):
    W, H = 480, 228
    s = svg_open(W, H, title, blurb)
    s += f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="{CARD_BG}" stroke="{RULE}"/>\n'
    s += text(28, 44, escape(eyebrow), MONO, 13, ACCENT)
    s += text(W - 28, 44, escape(date), MONO, 13, SOFTER, anchor="end")
    s += text(27, 94, escape(title), SERIF, 36, INK, ls="-0.01em")
    for i, line in enumerate(textwrap.wrap(blurb, 48)[:3]):
        s += text(28, 128 + i * 22, escape(line), SANS, 16, SOFT)
    s += f'<line x1="28" y1="186" x2="{W-28}" y2="186" stroke="{RULE}"/>\n'
    s += text(28, 210, escape(stack), MONO, 13, SOFTER)
    s += text(W - 28, 210, escape(dest), MONO, 13, INK, anchor="end")
    return s + "</svg>\n"


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "header.svg").write_text(header(), encoding="utf-8")
    for slug, *fields in CARDS:
        (ASSETS / f"card-{slug}.svg").write_text(card(*fields), encoding="utf-8")
    print(f"wrote header and {len(CARDS)} cards to {ASSETS}")
