"""Shared style for the threat model diagrams: tokens, fonts, dark mode, SVG head and arrowheads.

Drawn at 672 px wide so font sizes are the sizes shown. Theme-aware via prefers-color-scheme.
"""
W = 672
SANS = 'Bahnschrift, "Segoe UI", sans-serif'
MONO = '"Cascadia Mono", Consolas, monospace'
SERIF = '"Sitka Text", Georgia, serif'

STYLE = f"""  <style>
    .paper {{ fill: #FBFCFE; }} .gap {{ stroke: #FBFCFE; }}
    .ink-s {{ stroke: #252A31; }} .ink-f {{ fill: #252A31; }}
    .muted-s {{ stroke: #636D79; }} .muted-f {{ fill: #636D79; }}
    .soft-s {{ stroke: #98A1AC; }}
    .input {{ fill: #F0F3F7; stroke: #98A1AC; }}
    .acc {{ fill: #E8EDF8; stroke: #1C3D96; }} .acc-f {{ fill: #1C3D96; }}
    .name {{ fill: #252A31; font: 600 15px {SANS}; }}
    .name-s {{ fill: #252A31; font: 600 14px {SANS}; }}
    .name-acc {{ fill: #1C3D96; font: 600 15px {SANS}; }}
    .mono {{ fill: #636D79; font: 400 13px {MONO}; }}
    .aside {{ fill: #636D79; font: italic 400 15px {SERIF}; }}
    .num {{ fill: #252A31; font: 600 13px {MONO}; }}
    @media (prefers-color-scheme: dark) {{
      .paper {{ fill: #1F2E28; }} .gap {{ stroke: #1F2E28; }}
      .ink-s {{ stroke: #E1E7DE; }} .ink-f {{ fill: #E1E7DE; }}
      .muted-s {{ stroke: #9BAAA0; }} .muted-f {{ fill: #9BAAA0; }}
      .soft-s {{ stroke: #6F8177; }}
      .input {{ fill: #26372F; stroke: #6F8177; }}
      .acc {{ fill: #2A3D46; stroke: #A9C9F1; }} .acc-f {{ fill: #A9C9F1; }}
      .name, .name-s {{ fill: #E1E7DE; }} .name-acc {{ fill: #A9C9F1; }}
      .mono, .aside {{ fill: #9BAAA0; }} .num {{ fill: #E1E7DE; }}
    }}
  </style>"""


def head(h, title, desc, slug):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" viewBox="0 0 {W} {h}" role="img" aria-labelledby="{slug}-title {slug}-desc">',
            f'  <title id="{slug}-title">{title}</title>', f'  <desc id="{slug}-desc">{desc}</desc>', STYLE]


def arrowhead(x, y, tx, ty, cls, size=7.0):
    """filled triangle with its tip at (x, y), pointing along (tx, ty)"""
    nx, ny = -ty, tx
    bx, by = x - tx * size * 1.3, y - ty * size * 1.3
    return (f'  <polygon class="{cls}" points="{x:.1f},{y:.1f} {bx + nx * size * 0.6:.1f},{by + ny * size * 0.6:.1f} '
            f'{bx - nx * size * 0.6:.1f},{by - ny * size * 0.6:.1f}"/>')
