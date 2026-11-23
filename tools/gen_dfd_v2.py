"""Outlook data flow diagram (version 2) for the ASE security threat model, focus TT01, Lagerraum app.

Version 2 shows only what is new or changes against version 1: tokens (JWT) instead of server sessions,
two services behind the proxy, and a cache. Password reset by mail is unchanged and not drawn again.
Style comes from diagram_style.py. Usage: python gen_dfd_v2.py <out.svg>
"""
import math
import sys

from diagram_style import W, head, arrowhead

H = 1024
EXTRA = """  <style>
    .tb { fill: none; stroke: #B3261E; } .tb-f { fill: #B3261E; font: 600 13px "Cascadia Mono", Consolas, monospace; }
    .legend { fill: #252A31; font: 400 13px "Cascadia Mono", Consolas, monospace; }
    @media (prefers-color-scheme: dark) {
      .tb { stroke: #F0A29B; } .tb-f { fill: #F0A29B; } .legend { fill: #E1E7DE; }
    }
  </style>"""

out = head(H, "Datenflussdiagramm Version 2: Token, zwei Dienste und Cache",
           "Ausblick auf Version 2. Die Web-App meldet sich über den Reverse Proxy beim Konto-Dienst an und erhält "
           "ein kurzlebiges Access-Token (JWT) und ein Refresh-Cookie. Der Reservierungs-Dienst prüft das Token "
           "selbst. Der Konto-Dienst hält Konten und Refresh-Token in der zentralen Datenbank, beide Dienste nutzen "
           "einen Cache für Fehlversuchs-Zähler, eine Sperrliste widerrufener Token und die Verfügbarkeit. Zwei "
           "Trust Boundaries: Julias Gerät und das Backend. Zehn nummerierte Datenflüsse.", "tm-dfd-v2")
out.append(EXTRA)
out.append(f'  <rect class="paper" x="0" y="0" width="{W}" height="{H}"/>')


def boundary(x, y, w, h, label, lx, ly, anchor="start"):
    out.append(f'  <rect class="tb" x="{x}" y="{y}" width="{w}" height="{h}" rx="10" stroke-width="1.6" stroke-dasharray="7 5"/>')
    out.append(f'  <text class="tb-f" x="{lx}" y="{ly}" text-anchor="{anchor}">{label}</text>')


def actor(x, y, w, h, name, sub):
    out.append(f'  <rect class="input" x="{x}" y="{y}" width="{w}" height="{h}" stroke-width="1.4"/>')
    out.append(f'  <text class="name-s" x="{x + w / 2}" y="{y + h / 2 - 3}" text-anchor="middle">{name}</text>')
    out.append(f'  <text class="mono" x="{x + w / 2}" y="{y + h / 2 + 15}" text-anchor="middle">{sub}</text>')


def process(cx, cy, r, lines, sub, cls="paper ink-s", name_cls="name-s"):
    out.append(f'  <circle class="{cls}" cx="{cx}" cy="{cy}" r="{r}" stroke-width="1.4"/>')
    n = len(lines) + (1 if sub else 0)
    y = cy - (n - 1) * 9 + 5
    for t in lines:
        out.append(f'  <text class="{name_cls}" x="{cx}" y="{y:.0f}" text-anchor="middle">{t}</text>')
        y += 18
    if sub:
        out.append(f'  <text class="mono" x="{cx}" y="{y:.0f}" text-anchor="middle">{sub}</text>')


def store(cx, top, name, sub, w=176, h=66, ry=9, cls="paper ink-s"):
    x0, x1 = cx - w / 2, cx + w / 2
    out.append(f'  <path class="{cls}" stroke-width="1.4" d="M{x0},{top + ry} V{top + h - ry} A{w / 2},{ry} 0 0 0 {x1},{top + h - ry} V{top + ry} A{w / 2},{ry} 0 0 0 {x0},{top + ry} A{w / 2},{ry} 0 0 0 {x1},{top + ry}"/>')
    out.append(f'  <text class="name-s" x="{cx}" y="{top + 34}" text-anchor="middle">{name}</text>')
    out.append(f'  <text class="mono" x="{cx}" y="{top + 52}" text-anchor="middle">{sub}</text>')


def flow(points, both=False, r=8):
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
    out.append(f'  <path class="muted-s" d="{" ".join(d)}" fill="none" stroke-width="1.6"/>')
    (ax, ay), (bx, by) = points[-2], points[-1]
    n = math.hypot(bx - ax, by - ay)
    out.append(arrowhead(bx, by, (bx - ax) / n, (by - ay) / n, "muted-f"))
    if both:
        (ax, ay), (bx, by) = points[1], points[0]
        n = math.hypot(bx - ax, by - ay)
        out.append(arrowhead(bx, by, (bx - ax) / n, (by - ay) / n, "muted-f"))


def badge(x, y, n):
    out.append(f'  <circle class="paper ink-s" cx="{x}" cy="{y}" r="11" stroke-width="1.4"/>')
    out.append(f'  <text class="num" x="{x}" y="{y + 4.5}" text-anchor="middle">{n}</text>')


def chord(cy, r, dx, lower=True):
    dy = math.sqrt(max(0.0, r * r - dx * dx))
    return cy + dy if lower else cy - dy


R = 50
WEB = (104, 190)
PROXY = (104, 400)
KONTO = (310, 400)
RES = (528, 400)

boundary(16, 122, 320, 132, "Julias Gerät", 326, 142, "end")
boundary(16, 306, 640, 374, "Backend Lagerraum (Server, Docker Compose)", 28, 668)
out.append('  <text class="aside" x="176" y="285">Internet</text>')
out.append('  <text class="aside" x="372" y="170">Passwort-Reset per Mail: wie in</text>')
out.append('  <text class="aside" x="372" y="192">Version 1, hier nicht gezeichnet.</text>')
out.append('  <text class="aside" x="372" y="226">Neu sind Token, zwei Dienste, Cache.</text>')

# flows
flow([(104, 82), (104, WEB[1] - R)])                                                        # 1
for dx in (-34, 0, 34):                                                                     # 2, 3, 4
    flow([(WEB[0] + dx, chord(WEB[1], R, dx)), (PROXY[0] + dx, chord(PROXY[1], R, dx, lower=False))])
flow([(PROXY[0] + R, PROXY[1]), (KONTO[0] - R, KONTO[1])])                                  # 5
flow([(PROXY[0] + 40, chord(PROXY[1], R, 40, lower=False)), (PROXY[0] + 40, 334), (RES[0], 334), (RES[0], RES[1] - R)])  # 6
flow([(KONTO[0] - 20, chord(KONTO[1], R, -20)), (KONTO[0] - 20, 520)])                      # 7
flow([(KONTO[0] + 28, chord(KONTO[1], R, 28)), (KONTO[0] + 28, 482), (452, 482), (452, 520)])  # 8
flow([(RES[0] - 24, chord(RES[1], R, -24)), (RES[0] - 24, 520)])                            # 9
flow([(RES[0] + R, RES[1]), (622, 400), (622, 618), (250, 618), (250, 588)])                # 10

# elements
actor(28, 26, 152, 56, "Julia", "Kundin")
process(*WEB, R, ["Web-App"], "Browser")
process(*PROXY, R, ["Reverse", "Proxy"], "Traefik")
process(*KONTO, R, ["Konto-", "Dienst"], "Aussteller", cls="acc", name_cls="name-acc")
process(*RES, R, ["Reservie-", "rungs-Dienst"], "prüft JWT")
store(250, 520, "Zentrale Datenbank", "Konten · Reservierungen", w=216)
store(486, 520, "Cache", "Zähler · Sperrliste", w=176)

for (x, y, n) in ((104, 104, 1), (70, 282, 2), (104, 282, 3), (138, 282, 4), (207, 400, 5),
                  (350, 334, 6), (290, 486, 7), (400, 482, 8), (504, 486, 9), (430, 618, 10)):
    badge(x, y, n)

y = 716
out.append(f'  <text class="name" x="16" y="{y}">Datenflüsse Version 2: was · wie · als wer</text>')
lines = [
    (1, "E-Mail-Adresse, Passwort · Eingabe am Gerät · Julia"),
    (2, "Login · HTTPS · anonym. Antwort: Access-Token (JWT) + Refresh-Cookie"),
    (3, "Box-Reservierung lesen, ändern, stornieren · HTTPS · Access-Token (JWT)"),
    (4, "Access-Token erneuern · HTTPS · Refresh-Cookie"),
    (5, "Login und Erneuern weitergereicht · HTTP intern · Proxy"),
    (6, "Anfragen mit JWT weitergereicht · HTTP intern · JWT der Kundin"),
    (7, "Konten, Passwort-Hash, Hash des Refresh-Tokens · SQL · DB-Benutzer Konto"),
    (8, "Fehlversuchs-Zähler, Sperrliste schreiben · Redis-Protokoll · Cache-Passwort"),
    (9, "Sperrliste lesen, Verfügbarkeit zwischenspeichern · Redis · Cache-Passwort"),
    (10, "Reservierungen lesen und schreiben · SQL · DB-Benutzer Reservierung"),
]
for n, text in lines:
    y += 22
    out.append(f'  <text class="num" x="34" y="{y}" text-anchor="end">{n}</text>')
    out.append(f'  <text class="legend" x="46" y="{y}">{text}</text>')
y += 30
out.append(f'  <text class="mono" x="16" y="{y}">Pfeil = Richtung der Anfrage, Antworten sind nicht gezeichnet</text>')
y += 20
out.append(f'  <text class="mono" x="16" y="{y}">Rechteck = externer Akteur · Kreis = Prozess · Zylinder = Datenspeicher</text>')
out.append(f'  <text class="mono" x="16" y="{y + 20}">rot gestrichelt = Trust Boundary · blau = Schwerpunkt TT01</text>')
out.append("</svg>")

with open(sys.argv[1], "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(out) + "\n")
print("wrote", sys.argv[1], "height", H, "legend ends at", y + 20)
