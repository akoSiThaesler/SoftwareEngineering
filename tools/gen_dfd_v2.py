"""Outlook diagram (version 2) for the threat model of the Lagerraum app: tokens (JWT), two services, a cache.

Shows only what changes against version 1. Resetting the password by mail stays the same and is not drawn.
Style comes from diagram_style.py.
Usage: python gen_dfd_v2.py <out.svg>
"""
import math
import sys

from diagram_style import W, head, arrowhead

H = 624
EXTRA = """  <style>
    .tb { fill: none; stroke: #B3261E; } .tb-f { fill: #B3261E; font: 600 14px Bahnschrift, "Segoe UI", sans-serif; }
    .lbl { fill: #252A31; font: 400 14px Bahnschrift, "Segoe UI", sans-serif; }
    .lbl-b { fill: #252A31; font: 600 14px Bahnschrift, "Segoe UI", sans-serif; }
    @media (prefers-color-scheme: dark) {
      .tb { stroke: #F0A29B; } .tb-f { fill: #F0A29B; } .lbl, .lbl-b { fill: #E1E7DE; }
    }
  </style>"""

out = head(H, "Datenflussdiagramm Version 2: Token, zwei Dienste, Cache",
           "Ausblick. Julia meldet sich beim Konto-Dienst an und bekommt ein Token (JWT). Mit dem Token ändert sie "
           "ihre Reservierung beim Reservierungs-Dienst, der das Token selbst prüft. Beide Dienste nutzen dieselbe "
           "Datenbank und einen Cache für Fehlversuche und gesperrte Token.", "tm-dfd-v2")
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


KONTO = (150, 300)
RES = (450, 300)
R = 56

boundary(40, 12, 592, 104, "Julias Gerät", 52, 32)
boundary(40, 222, 592, 306, "Unser Server", 620, 244, "end")

flow([(150, 104), (150, KONTO[1] - R)])                                         # 1
flow([(450, 104), (450, RES[1] - R)])                                           # 2
flow([(KONTO[0] - 20, KONTO[1] + math.sqrt(R * R - 400)), (KONTO[0] - 20, 410)])  # 3
flow([(KONTO[0] + 30, KONTO[1] + math.sqrt(R * R - 900)), (KONTO[0] + 30, 380), (410, 380), (410, 410)])  # 4
flow([(RES[0] + 20, RES[1] + math.sqrt(R * R - 400)), (RES[0] + 20, 410)])       # 5
flow([(RES[0] + R, RES[1]), (604, RES[1]), (604, 506), (130, 506), (130, 476)])   # 6

label(166, 150, "1", "Anmelden · HTTPS · anonym")
out.append('  <text class="lbl" x="166" y="172">zurück kommt ein Token (JWT)</text>')
label(466, 150, "2", "Reservierung ändern")
out.append('  <text class="lbl" x="466" y="172">HTTPS · mit Token</text>')
out.append('  <text class="lbl" x="466" y="194">Token wird hier geprüft</text>')
out.append('  <text class="aside" x="134" y="194" text-anchor="end">Internet</text>')
label(122, 392, "3", "Konten", "end")
label(296, 372, "4", "Fehlversuche, gesperrte Token", "middle")
label(482, 392, "5", "Token gesperrt?")
label(367, 500, "6", "Reservierungen · SQL", "middle")

actor(60, 44, 552, 60, "Julia", "im Browser")
process(*KONTO, R, ["Konto-", "Dienst"], cls="acc", name_cls="name-acc")
process(*RES, R, ["Reservierungs-", "Dienst"])
store(130, 410, "Datenbank", "Konten · Reservierungen", w=168)
store(440, 410, "Cache", "Zähler · Sperrliste", w=168)

out.append(f'  <text class="mono" x="40" y="{H - 62}">Passwort zurücksetzen per Mail: wie in Version 1, hier nicht gezeichnet</text>')
out.append(f'  <text class="mono" x="40" y="{H - 42}">Rechteck = Person oder fremdes System · Kreis = unser Code · Zylinder = Daten</text>')
out.append(f'  <text class="mono" x="40" y="{H - 22}">rot gestrichelt = Trust Boundary: hier wechselt, wer die Kontrolle hat</text>')
out.append("</svg>")

with open(sys.argv[1], "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(out) + "\n")
print("wrote", sys.argv[1], "height", H)
