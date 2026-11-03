"""Generates the SVG assets for the SaniaNemade profile README.

Every asset is built twice, into assets/dark and assets/light, with a transparent
background so it blends into GitHub's page in either theme.  Run: python3 build.py
"""
import os
from xml.sax.saxutils import escape as esc

ROOT = os.path.dirname(os.path.abspath(__file__))
W = 900

SERIF = "'Iowan Old Style', 'Palatino Linotype', Palatino, Georgia, 'DejaVu Serif', serif"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, 'DejaVu Sans', sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'DejaVu Sans Mono', monospace"

THEMES = {
    "dark": dict(fg="#e6edf3", dim="#9198a1", muted="#656c76", ink="#ffffff", ink_op=0.035,
                 edge="#ffffff", edge_op=0.09, accent="#b9a7ff", accent2="#7dd3fc", on_acc="#0d1117"),
    "light": dict(fg="#1f2328", dim="#59636e", muted="#8c959f", ink="#000000", ink_op=0.025,
                  edge="#000000", edge_op=0.09, accent="#6d4aff", accent2="#0284c7", on_acc="#ffffff"),
}
T = THEMES["dark"]  # current theme, swapped in main()


def style():
    return f"""<style>
  .serif {{ font-family: {SERIF}; }} .sans {{ font-family: {SANS}; }} .mono {{ font-family: {MONO}; }}
  @keyframes up {{ from {{ opacity: 0; transform: translateY(6px) }} to {{ opacity: 1; transform: none }} }}
  @keyframes twinkle {{ 0%,100% {{ opacity: .25 }} 50% {{ opacity: 1 }} }}
  @keyframes pulse {{ 0% {{ opacity: .9; r: 3.5 }} 80%,100% {{ opacity: 0; r: 10 }} }}
  @keyframes travel {{ from {{ offset-distance: 0% }} to {{ offset-distance: 100% }} }}
  @keyframes draw {{ to {{ stroke-dashoffset: 0 }} }}
  .up {{ opacity: 0; animation: up .7s cubic-bezier(.2,.7,.2,1) forwards; }}
  .tw {{ animation: twinkle 3.2s ease-in-out infinite; }}
  .pulse {{ animation: pulse 2.2s ease-out infinite; }}
</style>
<defs>
  <linearGradient id="acc" x1="0" x2="1" y1="0" y2="0">
    <stop offset="0" stop-color="{T['accent']}"/><stop offset="1" stop-color="{T['accent2']}"/>
  </linearGradient>
  <radialGradient id="glow" cx=".5" cy=".5" r=".5">
    <stop offset="0" stop-color="{T['accent']}" stop-opacity=".22"/>
    <stop offset="1" stop-color="{T['accent']}" stop-opacity="0"/>
  </radialGradient>
</defs>"""


def svg(h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" '
            f'fill="none">{style()}{body}</svg>')


def t(x, y, s, size=14, color=None, font="sans", weight=400, anchor="start", extra=""):
    color = color or T["fg"]
    return (f'<text x="{x}" y="{y}" class="{font}" font-size="{size}" fill="{color}" '
            f'font-weight="{weight}" text-anchor="{anchor}" {extra}>{esc(s)}</text>')


def card(x, y, w, h, r=16):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{T["ink"]}" '
            f'fill-opacity="{T["ink_op"]}" stroke="{T["edge"]}" stroke-opacity="{T["edge_op"]}"/>')


def pill(x, y, label, size=11.5, pad=11, h=24):
    w = len(label) * size * 0.6 + pad * 2
    s = (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="{T["ink"]}" '
         f'fill-opacity="{T["ink_op"]*2.2}" stroke="{T["edge"]}" stroke-opacity="{T["edge_op"]*0.8}"/>')
    s += t(x + w / 2, y + h / 2 + size * 0.36, label, size, T["fg"], "mono", anchor="middle")
    return s, w


def label(x, y, n, name):
    """Small section label: 01 · ABOUT ———"""
    s = t(x, y, f"{n:02d}", 11, T["accent"], "mono", 600, extra='letter-spacing="1"')
    s += t(x + 28, y, name.upper(), 11, T["dim"], "mono", 500, extra='letter-spacing="2.5"')
    x0 = x + 28 + len(name) * 11 * 0.6 + len(name) * 2.5 + 16
    s += f'<line x1="{x0:.0f}" y1="{y-4}" x2="{W-2}" y2="{y-4}" stroke="{T["edge"]}" stroke-opacity="{T["edge_op"]}"/>'
    return s


def d(i, step=0.12, base=0.1):
    return f'style="animation-delay:{base + i*step:.2f}s"'


def write(theme, name, content):
    os.makedirs(os.path.join(ROOT, "assets", theme), exist_ok=True)
    with open(os.path.join(ROOT, "assets", theme, name), "w") as f:
        f.write(content)


# ------------------------------------------------------------------ header
def header():
    h = 300
    b = f'<circle cx="715" cy="150" r="148" fill="url(#glow)"/>'
    # embedding-space constellation on the right
    pts = [(560, 70), (610, 120), (668, 82), (720, 150), (780, 96), (830, 170), (640, 200),
           (700, 232), (770, 214), (860, 110), (590, 170), (820, 250), (740, 60)]
    edges = [(0, 1), (1, 2), (2, 4), (1, 3), (3, 4), (4, 9), (3, 5), (1, 10), (10, 6), (6, 7),
             (7, 8), (8, 5), (5, 11), (2, 12), (12, 4)]
    for a, c in edges:
        (x1, y1), (x2, y2) = pts[a], pts[c]
        b += (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{T["accent"]}" '
              f'stroke-opacity=".22" stroke-width="1"/>')
    for i, (x, y) in enumerate(pts):
        big = i in (3, 7)
        b += (f'<circle class="tw" style="animation-delay:{(i*0.37)%3:.2f}s" cx="{x}" cy="{y}" '
              f'r="{4 if big else 2.4}" fill="{T["accent2"] if big else T["accent"]}"/>')
    # the "query" vector landing on its nearest neighbour
    b += (f'<circle cx="720" cy="150" r="14" stroke="{T["accent2"]}" stroke-opacity=".5" '
          f'stroke-dasharray="2 4"/>')
    b += t(738, 138, "nearest neighbour", 10, T["muted"], "mono")

    b += f'<g class="up" {d(0)}>' + t(4, 92, "hi, i'm", 15, T["accent"], "mono") + "</g>"
    b += f'<g class="up" {d(1)}>' + t(0, 160, "Sania Nemade", 68, T["fg"], "serif", 500,
                                       extra='letter-spacing="-1"') + "</g>"
    b += f'<g class="up" {d(2)}>' + t(4, 200, "AI engineer building retrieval systems,", 17, T["dim"]) + \
         t(4, 224, "LLM agents and explainable machine learning.", 17, T["dim"]) + "</g>"
    # status pill
    b += f'<g class="up" {d(3)}>'
    b += (f'<rect x="2" y="252" width="268" height="30" rx="15" fill="{T["accent"]}" fill-opacity=".1" '
          f'stroke="{T["accent"]}" stroke-opacity=".35"/>')
    b += f'<circle cx="20" cy="267" r="3.5" fill="{T["accent"]}"/>'
    b += f'<circle class="pulse" cx="20" cy="267" r="3.5" stroke="{T["accent"]}"/>'
    b += t(34, 271.5, "open to AI engineering roles", 12, T["fg"], "mono")
    b += "</g>"
    return svg(h, b)


# ------------------------------------------------------------------ about
def about():
    h = 250
    b = label(2, 20, 1, "about")
    para = [
        "I like problems where the answer is buried somewhere",
        "in a lot of data. Most of what I build is about finding",
        "it: hybrid search, RAG pipelines and agents that cite",
        "their sources, from prototype to 10M-row production.",
    ]
    for i, line in enumerate(para):
        b += f'<g class="up" {d(i, .08)}>' + t(2, 70 + i * 28, line, 16.5, T["fg"], "serif") + "</g>"
    b += f'<g class="up" {d(5, .08)}>' + t(2, 200, "Hoboken, NJ  ·  saniapnemade@gmail.com", 12, T["muted"], "mono") + "</g>"

    x = 530
    b += card(x, 44, W - x - 2, 186)
    b += t(x + 24, 74, "EDUCATION", 10.5, T["dim"], "mono", 500, extra='letter-spacing="2"')
    edu = [("M.Eng, Engineering Management", "Stevens Institute of Technology", "4.0 GPA · May 2027"),
           ("B.E., Computer Engineering", "St. Francis Institute of Technology", "Mumbai · 2025")]
    y = 108
    for i, (deg, sch, note) in enumerate(edu):
        b += f'<circle cx="{x+28}" cy="{y-5}" r="3.5" fill="{T["accent"] if i == 0 else T["muted"]}"/>'
        b += t(x + 42, y, deg, 14, T["fg"], "sans", 600)
        b += t(x + 42, y + 20, sch, 12.5, T["dim"])
        b += t(x + 42, y + 38, note, 11, T["muted"], "mono")
        y += 64
    b += (f'<line x1="{x+28}" y1="{108}" x2="{x+28}" y2="{167}" stroke="{T["edge"]}" '
          f'stroke-opacity="{T["edge_op"]*2}"/>')
    return svg(h, b)


# ------------------------------------------------------------------ projects
PROJECTS = [
    ("Causal Studio", "Agentic LLM dashboard that guides scientists", "through causal study design.",
     "70+", "papers indexed", ["OpenAI", "LangChain", "DoWhy"]),
    ("QuackQuery", "Question answering over documents, with", "citations and evidence passages.",
     "hybrid", "beat semantic-only", ["ChromaDB", "BM25", "Groq"]),
    ("Knowledge Platform", "Self-validating LLM pipeline that routes,", "decomposes and caches queries.",
     "−40%", "redundant LLM calls", ["Gemini", "Django", "Redis"]),
    ("Autoimmune Dx", "Explainable diagnosis of six diseases", "from 12,500 patient records.",
     "86.3%", "accuracy · 0.88 F1", ["XGBoost", "SHAP", "pandas"]),
]


def projects():
    gap, ch = 18, 196
    cw = (W - 4 - gap) / 2
    h = 44 + 2 * ch + gap + 142 + 6
    b = label(2, 20, 2, "selected work")
    for i, (name, d1, d2, big, sub, tags) in enumerate(PROJECTS):
        r, c = divmod(i, 2)
        x, y = 2 + c * (cw + gap), 44 + r * (ch + gap)
        b += f'<g class="up" {d(i)}>' + card(x, y, cw, ch)
        b += t(x + 26, y + 40, name, 21, T["fg"], "serif", 600)
        b += t(x + cw - 26, y + 40, "↗", 15, T["muted"], anchor="end")
        b += t(x + 26, y + 66, d1, 13, T["dim"]) + t(x + 26, y + 85, d2, 13, T["dim"])
        b += t(x + 26, y + 132, big, 30, "url(#acc)", "sans", 700, extra='letter-spacing="-.5"')
        b += t(x + cw - 26, y + 130, sub, 11.5, T["muted"], "mono", anchor="end")
        px = x + 26
        for tag in tags:
            p, w = pill(px, y + ch - 44, tag, 10.5, 10, 22)
            b += p
            px += w + 6
        b += "</g>"
    # wide card
    y = 44 + 2 * (ch + gap)
    b += f'<g class="up" {d(4)}>' + card(2, y, W - 4, 142)
    b += t(28, y + 40, "RoomieMatch", 21, T["fg"], "serif", 600)
    b += t(28, y + 66, "Roommate matching on lifestyle, location and budget,", 13, T["dim"])
    b += t(28, y + 85, "using cosine similarity and K-Means clustering.", 13, T["dim"])
    b += t(W - 28, y + 64, "1,000+", 30, "url(#acc)", "sans", 700, "end")
    b += t(W - 28, y + 88, "profiles ranked", 11.5, T["muted"], "mono", anchor="end")
    px = 28
    for tag in ["FastAPI", "scikit-learn", "MongoDB", "React Native"]:
        p, w = pill(px, y + 104, tag, 10.5, 10, 22)
        b += p
        px += w + 6
    b += "</g>"
    return svg(h, b)


# ------------------------------------------------------------------ impact
def impact():
    stats = [("10M+", "products narrowed to", "a top-10 shortlist"),
             ("30%", "faster retrieval with", "sentence embeddings"),
             ("40%", "fewer redundant", "LLM calls"),
             ("0.88", "macro F1 across", "six diseases")]
    h = 170
    b = label(2, 20, 3, "impact")
    cw = (W - 4) / 4
    for i, (n, l1, l2) in enumerate(stats):
        x = 2 + i * cw
        b += f'<g class="up" {d(i, .15)}>'
        b += t(x + (0 if i == 0 else 28), 100, n, 44, T["fg"], "serif", 500, extra='letter-spacing="-1"')
        b += t(x + (0 if i == 0 else 28), 128, l1, 12.5, T["dim"])
        b += t(x + (0 if i == 0 else 28), 146, l2, 12.5, T["dim"])
        b += "</g>"
        if i:
            b += (f'<line x1="{x:.0f}" y1="62" x2="{x:.0f}" y2="150" stroke="{T["edge"]}" '
                  f'stroke-opacity="{T["edge_op"]}"/>')
    return svg(h, b)


# ------------------------------------------------------------------ journey
def journey():
    h = 400
    b = label(2, 20, 4, "journey")
    y = 92
    stops = [(30, "2021", "Started B.E.", "Computer Engineering"),
             (230, "2025", "Graduated", "moved to New Jersey"),
             (430, "2025", "M.Eng at Stevens", "Engineering Management"),
             (630, "Summer 2026", "AI Developer Intern", "X eleva Group"),
             (870, "May 2027", "M.Eng complete", "next chapter →")]
    b += (f'<line x1="30" y1="{y}" x2="745" y2="{y}" stroke="url(#acc)" stroke-width="1.5" '
          f'stroke-opacity=".8"/>')
    b += (f'<line x1="745" y1="{y}" x2="870" y2="{y}" stroke="{T["muted"]}" stroke-width="1.5" '
          f'stroke-dasharray="2 5"/>')
    for i, (x, yr, title, sub) in enumerate(stops):
        anchor = "start" if i == 0 else "end" if i == len(stops) - 1 else "middle"
        future = i == len(stops) - 1
        b += f'<g class="up" {d(i)}>'
        if future:
            b += f'<circle cx="{x}" cy="{y}" r="5" stroke="{T["muted"]}" stroke-width="1.5" fill="none"/>'
        else:
            b += f'<circle cx="{x}" cy="{y}" r="5" fill="{T["accent"]}"/>'
        b += t(x, y - 20, yr, 11, T["muted"], "mono", anchor=anchor)
        b += t(x, y + 32, title, 13.5, T["fg"], "sans", 600, anchor)
        b += t(x, y + 51, sub, 12, T["dim"], anchor=anchor)
        b += "</g>"
    b += f'<circle cx="745" cy="{y}" r="3.5" fill="{T["accent2"]}"/>'
    b += f'<circle class="pulse" cx="745" cy="{y}" r="3.5" stroke="{T["accent2"]}"/>'

    # experience card
    cy = 190
    b += f'<g class="up" {d(5)}>' + card(2, cy, W - 4, 196)
    b += t(28, cy + 40, "AI Developer Intern", 21, T["fg"], "serif", 600)
    b += t(28, cy + 62, "X eleva Group", 13, T["dim"])
    b += t(W - 28, cy + 40, "Jun – Aug 2026", 11.5, T["muted"], "mono", anchor="end")
    steps = ["10M+ products", "hard filters", "pgvector HNSW", "keyword re-rank", "top 10"]
    widths = [len(s) * 11.5 * 0.6 + 26 for s in steps]
    gapx = (W - 56 - sum(widths)) / (len(steps) - 1)
    px, py = 28, cy + 92
    centers = []
    for i, s in enumerate(steps):
        w = widths[i]
        last = i == len(steps) - 1
        if last:
            b += (f'<rect x="{px:.1f}" y="{py}" width="{w:.1f}" height="30" rx="15" fill="url(#acc)" '
                  f'fill-opacity=".9"/>')
            b += t(px + w / 2, py + 19.5, s, 11.5, T["on_acc"], "mono", 700, "middle")
        else:
            p, _ = pill(px, py, s, 11.5, 13, 30)
            b += p
        if i:
            b += (f'<line x1="{centers[-1]:.1f}" y1="{py+15}" x2="{px-6:.1f}" y2="{py+15}" '
                  f'stroke="{T["accent"]}" stroke-opacity=".45"/>')
        centers.append(px + w + 6)
        px += w + gapx
    b += t(28, cy + 160, "Restructured a 10M+ row catalog into a 3-level hierarchy and embedded every description,", 12.5, T["dim"])
    b += t(28, cy + 178, "cutting retrieval time by 30%.", 12.5, T["dim"])
    b += "</g>"
    return svg(h, b)


# ------------------------------------------------------------------ stack
STACK = [
    ("LLMs & agents", ["LangChain", "LangGraph", "LangSmith", "MCP", "OpenAI", "Gemini", "Groq"]),
    ("Retrieval", ["RAG", "hybrid search", "BM25 + RRF", "Sentence Transformers", "FAISS"]),
    ("Data stores", ["pgvector", "ChromaDB", "Qdrant", "PostgreSQL", "MongoDB"]),
    ("Machine learning", ["Python", "scikit-learn", "XGBoost", "SHAP", "pandas", "NumPy"]),
    ("Engineering", ["FastAPI", "Django REST", "Docker", "React", "Git"]),
    ("Analytics", ["SQL", "Tableau", "Power BI"]),
]


def stack():
    rowh = 46
    h = 48 + len(STACK) * rowh
    b = label(2, 20, 5, "toolkit")
    y = 54
    for i, (cat, items) in enumerate(STACK):
        b += f'<g class="up" {d(i, .08)}>'
        b += t(2, y + 16, cat, 15, T["fg"], "serif", 500)
        x = 190
        for it in items:
            p, w = pill(x, y, it, 11.5, 12, 26)
            b += p
            x += w + 7
        assert x < W, (cat, x)
        b += "</g>"
        y += rowh
    return svg(h, b)


# ------------------------------------------------------------------ footer
def footer():
    h = 90
    b = (f'<line x1="2" y1="20" x2="{W-2}" y2="20" stroke="{T["edge"]}" stroke-opacity="{T["edge_op"]}"/>')
    b += t(W / 2, 58, "retrieve  ·  reason  ·  cite  ·  ship", 15, T["dim"], "serif", 400, "middle",
           'font-style="italic" letter-spacing=".5"')
    b += t(W / 2, 82, "thanks for stopping by", 10.5, T["muted"], "mono", anchor="middle",
           extra='letter-spacing="1.5"')
    return svg(h, b)


ASSETS = {"header.svg": header, "about.svg": about, "projects.svg": projects, "impact.svg": impact,
          "journey.svg": journey, "stack.svg": stack, "footer.svg": footer}

if __name__ == "__main__":
    for name, theme in THEMES.items():
        T = theme
        globals()["T"] = theme
        for fname, fn in ASSETS.items():
            write(name, fname, fn())
    print("built", len(ASSETS), "assets × 2 themes")
