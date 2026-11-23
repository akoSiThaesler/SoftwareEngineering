"""Data flow diagram for the threat model of the Lagerraum app: accounts and login in the finished app.

One picture: login with a token, two services, a cache, and the password reset by mail.
Yellow marks show where a threat hits; the numbers match the table in the threat model.
Colours are the app's own tokens. Self-contained, no dependencies.
Usage: python gen_dfd.py <out.svg>
"""
import math
import sys

W, H = 672, 716
INK, MUTED, LINE, BETON, PAPER = "#171B20", "#515A65", "#D6DADF", "#E9EBED", "#FFFFFF"
TOR, TOR_TINT, BAND, RED = "#1F4E8C", "#EDF3FA", "#F4C20D", "#A1241F"
FONT = 'Barlow, "Segoe UI", system-ui, sans-serif'

out = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="tm-title tm-desc">',
    '  <title id="tm-title">Datenflussdiagramm: Konto und Login in der fertigen App</title>',
    '  <desc id="tm-desc">Julia meldet sich im Browser beim Konto-Dienst an und bekommt ein Token. Mit dem Token ändert sie '
    'ihre Reservierung beim Reservierungs-Dienst. Beide Dienste nutzen eine Datenbank und einen Cache. Den Link zum '
    'Zurücksetzen des Passworts verschickt der Konto-Dienst über einen fremden E-Mail-Dienst in Julias Postfach. '
    'Vier Trust Boundaries: Julias Gerät, unser Server, Drittanbieter, Mail-Anbieter. Gelbe Marken T1 bis T11 zeigen, wo eine Bedrohung ansetzt.</desc>',
    f"""  <style>
    text {{ font-family: {FONT}; fill: {INK}; }}
    .name {{ font-size: 15px; font-weight: 700; }}
    .sub {{ font-size: 13px; fill: {MUTED}; }}
    .lbl {{ font-size: 14px; paint-order: stroke; stroke: {PAPER}; stroke-width: 5px; stroke-linejoin: round; }}
    .num {{ font-weight: 700; fill: {TOR}; }}
    .note {{ font-size: 13px; fill: {MUTED}; }}
    .tb {{ fill: none; stroke: {RED}; stroke-width: 1.6; stroke-dasharray: 7 5; }}
    .tb-l {{ font-size: 14px; font-weight: 700; fill: {RED}; }}
    .actor {{ fill: {BETON}; stroke: {MUTED}; stroke-width: 1.4; }}
    .proc {{ fill: {PAPER}; stroke: {INK}; stroke-width: 1.6; }}
    .main {{ fill: {TOR_TINT}; stroke: {TOR}; stroke-width: 2; }}
    .store {{ fill: {PAPER}; stroke: {INK}; stroke-width: 1.6; }}
    .flow {{ fill: none; stroke: {MUTED}; stroke-width: 1.8; }}
    .head {{ fill: {MUTED}; }}
    .chip {{ fill: {BAND}; stroke: {INK}; stroke-width: 1.2; }}
    .chip-t {{ font-size: 13px; font-weight: 700; }}
  </style>""",
    f'  <rect x="0" y="0" width="{W}" height="{H}" fill="{PAPER}"/>',
]


def boundary(x, y, w, h, label, lx, ly, anchor="start"):
    out.append(f'  <rect class="tb" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>')
    out.append(f'  <text class="tb-l" x="{lx}" y="{ly}" text-anchor="{anchor}">{label}</text>')


def actor(x, y, w, h, name, sub):
    out.append(f'  <rect class="actor" x="{x}" y="{y}" width="{w}" height="{h}" rx="4"/>')
    out.append(f'  <text class="name" x="{x + w / 2}" y="{y + h / 2 - 3}" text-anchor="middle">{name}</text>')
    out.append(f'  <text class="sub" x="{x + w / 2}" y="{y + h / 2 + 15}" text-anchor="middle">{sub}</text>')


def process(cx, cy, r, lines, cls="proc"):
    out.append(f'  <circle class="{cls}" cx="{cx}" cy="{cy}" r="{r}"/>')
    y = cy - (len(lines) - 1) * 9 + 5
    for t in lines:
        out.append(f'  <text class="name" x="{cx}" y="{y:.0f}" text-anchor="middle">{t}</text>')
        y += 18


def store(cx, top, name, sub, w=170, h=66, ry=9):
    x0, x1 = cx - w / 2, cx + w / 2
    out.append(f'  <path class="store" d="M{x0},{top + ry} V{top + h - ry} A{w / 2},{ry} 0 0 0 {x1},{top + h - ry} V{top + ry} A{w / 2},{ry} 0 0 0 {x0},{top + ry} A{w / 2},{ry} 0 0 0 {x1},{top + ry}"/>')
    out.append(f'  <text class="name" x="{cx}" y="{top + 35}" text-anchor="middle">{name}</text>')
    out.append(f'  <text class="sub" x="{cx}" y="{top + 53}" text-anchor="middle">{sub}</text>')


def flow(points, r=8, size=7.0):
    d = [f"M{points[0][0]:.1f},{points[0][1]:.1f}"]
    for i in range(1, len(points)):
        (px, py), (x, y) = points[i - 1], points[i]
        if i < len(points) - 1:
            nx, ny = points[i + 1]
            ux, uy = (x - px), (y - py); n = math.hypot(ux, uy); ux, uy = ux / n, uy / n
            vx, vy = (nx - x), (ny - y); m = math.hypot(vx, vy); vx, vy = vx / m, vy / m
            d.append(f"L{x - ux * r:.1f},{y - uy * r:.1f} Q{x:.1f},{y:.1f} {x + vx * r:.1f},{y + vy * r:.1f}")
        else:
            d.append(f"L{x:.1f},{y:.1f}")
    out.append(f'  <path class="flow" d="{" ".join(d)}"/>')
    (ax, ay), (bx, by) = points[-2], points[-1]
    n = math.hypot(bx - ax, by - ay); tx, ty = (bx - ax) / n, (by - ay) / n
    nx, ny = -ty, tx
    cx, cy = bx - tx * size * 1.3, by - ty * size * 1.3
    out.append(f'  <polygon class="head" points="{bx:.1f},{by:.1f} {cx + nx * size * 0.6:.1f},{cy + ny * size * 0.6:.1f} {cx - nx * size * 0.6:.1f},{cy - ny * size * 0.6:.1f}"/>')


def label(x, y, num, text, anchor="start"):
    out.append(f'  <text class="lbl" x="{x}" y="{y}" text-anchor="{anchor}"><tspan class="num">{num}</tspan> {text}</text>')


def line(x, y, text, anchor="start"):
    out.append(f'  <text class="lbl" x="{x}" y="{y}" text-anchor="{anchor}">{text}</text>')


def chip(x, y, text):
    """threat mark, top-left corner at (x, y)"""
    w = 30 if len(text) < 3 else 38
    out.append(f'  <rect class="chip" x="{x}" y="{y}" width="{w}" height="20" rx="5"/>')
    out.append(f'  <text class="chip-t" x="{x + w / 2}" y="{y + 14.5}" text-anchor="middle">{text}</text>')


def chord(r, dx):
    return math.sqrt(max(0.0, r * r - dx * dx))


R = 52
RES = (130, 336)       # Reservierungs-Dienst
KONTO = (350, 336)     # Konto-Dienst
MAILX = 570            # E-Mail-Dienst and Postfach share this centre line

boundary(24, 14, 392, 104, "Julias Gerät", 36, 34)
boundary(484, 14, 172, 104, "Mail-Anbieter", 496, 34)
boundary(24, 254, 436, 356, "Unser Server", 448, 598, "end")
boundary(484, 254, 172, 164, "Drittanbieter", 644, 406, "end")
out.append(f'  <text class="note" x="36" y="240" font-style="italic">Internet</text>')

# flows
flow([(130, 106), (130, RES[1] - R)])                                              # 2
flow([(350, 106), (350, KONTO[1] - R)])                                            # 1, 3
flow([(KONTO[0] + R, KONTO[1]), (498, KONTO[1])])                                  # 8
flow([(MAILX, 306), (MAILX, 106)])                                                 # 9
flow([(498, 76), (402, 76)])                                                       # 10
flow([(RES[0] - 20, RES[1] + chord(R, 20)), (RES[0] - 20, 480)])                   # 6
flow([(KONTO[0] + 20, KONTO[1] + chord(R, 20)), (KONTO[0] + 20, 476)])             # 4
flow([(KONTO[0] - 30, KONTO[1] + chord(R, 30)), (KONTO[0] - 30, 436), (195, 436), (195, 480)])  # 5
flow([(RES[0] - R, RES[1]), (36, RES[1]), (36, 572), (330, 572), (330, 542)])      # 7

# flow labels
label(146, 150, "2", "Reservieren, ändern")
line(146, 170, "HTTPS · mit Token")
label(366, 150, "1", "Anmelden, Konto anlegen")
line(366, 170, "HTTPS · zurück kommt ein Token")
label(366, 198, "3", "Passwort zurücksetzen")
line(366, 218, "HTTPS · Link aus der Mail")
label(431, 314, "8", "Mail", "middle")
line(431, 329, "mit Link", "middle")
label(582, 214, "9", "Mail")
label(450, 68, "10", "Link", "middle")
label(382, 458, "4", "Konten")
label(205, 428, "5", "Zähler, Sperrliste")
label(122, 462, "6", "gesperrt?")
label(186, 564, "7", "Reservierungen", "middle")

# elements
actor(40, 46, 362, 60, "Julia", "im Browser")
actor(498, 46, 144, 60, "Julias Postfach", "bei ihrem Anbieter")
actor(498, 306, 144, 60, "E-Mail-Dienst", "verschickt für uns")
process(*RES, R, ["Reservie-", "rungs-Dienst"])
process(*KONTO, R, ["Konto-", "Dienst"], cls="main")
store(130, 476, "Cache", "Zähler · Sperrliste", w=160)
store(350, 476, "Datenbank", "Konten · Reservierungen")

# threat marks: where each threat hits
chip(306, 136, "T1"); chip(306, 160, "T3"); chip(306, 184, "T2"); chip(306, 208, "T6")
chip(86, 136, "T7"); chip(86, 160, "T8")
chip(366, 22, "T4")
chip(606, 22, "T5")
chip(398, 270, "T9")
chip(54, 448, "T10")
chip(382, 416, "T11")

# legend
chip(24, 632, "T1")
out.append(f'  <text class="note" x="62" y="647">Hier setzt eine Bedrohung an. Die Nummer steht in der Tabelle.</text>')
out.append(f'  <text class="note" x="24" y="676">Rechteck = Person oder fremdes System · Kreis = unser Code (blau = Schwerpunkt) · Zylinder = Daten</text>')
out.append(f'  <text class="note" x="24" y="696">Rot gestrichelt = Trust Boundary: hier wechselt, wer die Kontrolle hat</text>')
out.append("</svg>")

with open(sys.argv[1], "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(out) + "\n")
print("wrote", sys.argv[1])
