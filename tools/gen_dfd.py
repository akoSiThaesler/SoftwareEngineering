"""Data flow diagram for the threat model (focus: accounts and login) of the Lagerraum app, version 1.

Kept small on purpose: five elements, six flows, labels written on the arrows.
Rectangle = external actor, circle = process, cylinder = data store, dashed red = trust boundary.
Style comes from diagram_style.py.
Usage: python gen_dfd.py <out.svg>
"""
import math
import sys

from diagram_style import W, head, arrowhead

H = 560
EXTRA = """  <style>
    .tb { fill: none; stroke: #B3261E; } .tb-f { fill: #B3261E; font: 600 14px Bahnschrift, "Segoe UI", sans-serif; }
    .lbl { fill: #252A31; font: 400 14px Bahnschrift, "Segoe UI", sans-serif; }
    .lbl-b { fill: #252A31; font: 600 14px Bahnschrift, "Segoe UI", sans-serif; }
    @media (prefers-color-scheme: dark) {
      .tb { stroke: #F0A29B; } .tb-f { fill: #F0A29B; } .lbl, .lbl-b { fill: #E1E7DE; }
    }
  </style>"""

out = head(H, "Datenflussdiagramm: Konto und Login im Lagerraum Box-Check",
           "Julia meldet sich im Browser an. Login, Änderungen an der Reservierung und das Zurücksetzen des "
           "Passworts gehen über das Internet an unser Backend. Das Backend speichert Konten und Reservierungen "
           "in einer Datenbank und verschickt den Link zum Zurücksetzen über einen fremden E-Mail-Dienst in "
           "Julias Postfach. Drei Trust Boundaries: Julias Gerät, unser Server, Drittanbieter.", "tm-dfd")
out.append(EXTRA)
out.append(f'  <rect class="paper" x="0" y="0" width="{W}" height="{H}"/>')


def boundary(x, y, w, h, label, lx, ly, anchor="start"):
    out.append(f'  <rect class="tb" x="{x}" y="{y}" width="{w}" height="{h}" rx="10" stroke-width="1.6" stroke-dasharray="7 5"/>')
    out.append(f'  <text class="tb-f" x="{lx}" y="{ly}" text-anchor="{anchor}">{label}</text>')


def actor(x, y, w, h, name, sub):
    out.append(f'  <rect class="input" x="{x}" y="{y}" width="{w}" height="{h}" stroke-width="1.4"/>')
    out.append(f'  <text class="name" x="{x + w / 2}" y="{y + h / 2 - 3}" text-anchor="middle">{name}</text>')
    out.append(f'  <text class="lbl" x="{x + w / 2}" y="{y + h / 2 + 16}" text-anchor="middle">{sub}</text>')


def process(cx, cy, r, lines, cls="paper ink-s", name_cls="name"):
    out.append(f'  <circle class="{cls}" cx="{cx}" cy="{cy}" r="{r}" stroke-width="1.4"/>')
    y = cy - (len(lines) - 1) * 9 + 5
    for t in lines:
        out.append(f'  <text class="{name_cls}" x="{cx}" y="{y:.0f}" text-anchor="middle">{t}</text>')
        y += 18


def store(cx, top, name, sub, w=176, h=66, ry=9):
    x0, x1 = cx - w / 2, cx + w / 2
    out.append(f'  <path class="paper ink-s" stroke-width="1.4" d="M{x0},{top + ry} V{top + h - ry} A{w / 2},{ry} 0 0 0 {x1},{top + h - ry} V{top + ry} A{w / 2},{ry} 0 0 0 {x0},{top + ry} A{w / 2},{ry} 0 0 0 {x1},{top + ry}"/>')
    out.append(f'  <text class="name" x="{cx}" y="{top + 34}" text-anchor="middle">{name}</text>')
    out.append(f'  <text class="lbl" x="{cx}" y="{top + 52}" text-anchor="middle">{sub}</text>')


def flow(points, r=8):
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
    out.append(f'  <path class="muted-s" d="{" ".join(d)}" fill="none" stroke-width="1.8"/>')
    (ax, ay), (bx, by) = points[-2], points[-1]
    n = math.hypot(bx - ax, by - ay)
    out.append(arrowhead(bx, by, (bx - ax) / n, (by - ay) / n, "muted-f"))


def label(x, y, num, text, anchor="start"):
    out.append(f'  <text class="lbl" x="{x}" y="{y}" text-anchor="{anchor}"><tspan class="lbl-b">{num}</tspan> {text}</text>')


BACK = (160, 318)
MAIL = (566, 318)

boundary(40, 12, 248, 104, "Julias Gerät", 52, 32)
boundary(40, 234, 404, 236, "Unser Server", 52, 458)
boundary(470, 234, 190, 170, "Drittanbieter", 482, 392)

# flows
flow([(160, 104), (160, BACK[1] - 56)])                                        # 1-3, one arrow
flow([(BACK[0] + 56, BACK[1]), (252, BACK[1])])                                # 4
flow([(BACK[0], BACK[1] + 56), (BACK[0], 428), (MAIL[0], 428), (MAIL[0], MAIL[1] + 50)])  # 5
flow([(MAIL[0], MAIL[1] - 50), (MAIL[0], 104)])                                # 6
flow([(470, 72), (270, 72)])                                                   # 7

label(178, 150, "1", "Anmelden · HTTPS · noch anonym")
label(178, 174, "2", "Reservierung ändern · HTTPS · Cookie")
label(178, 198, "3", "Passwort zurücksetzen · HTTPS · Link aus der Mail")
out.append('  <text class="aside" x="142" y="178" text-anchor="end">Internet</text>')
label(334, 274, "4", "Konten, Reservierungen · SQL", "middle")
label(364, 420, "5", "Mail mit Link · HTTPS · API-Schlüssel", "middle")
label(578, 176, "6", "Mail · SMTP")
label(370, 62, "7", "öffnet den Link", "middle")

# elements
actor(60, 44, 210, 60, "Julia", "im Browser")
actor(470, 44, 190, 60, "Julias Postfach", "bei ihrem E-Mail-Anbieter")
process(*BACK, 56, ["Backend"], cls="acc", name_cls="name-acc")
process(*MAIL, 50, ["E-Mail-", "Dienst"])
store(334, 285, "Datenbank", "Konten · Reservierungen", w=164)

out.append(f'  <text class="mono" x="40" y="{H - 44}">Rechteck = Person oder fremdes System · Kreis = unser Code · Zylinder = Daten</text>')
out.append(f'  <text class="mono" x="40" y="{H - 24}">rot gestrichelt = Trust Boundary: hier wechselt, wer die Kontrolle hat</text>')
out.append("</svg>")

with open(sys.argv[1], "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(out) + "\n")
print("wrote", sys.argv[1], "height", H)
