"""Data flow diagram for the ASE security threat model (focus TT01, accounts and login) of the Lagerraum app.

Second version: first-iteration architecture (one backend, one central database, reverse proxy in front).
Style comes from diagram_style.py. Classic DFD notation:
rectangle = external actor, circle = process, cylinder = data store, dashed red = trust boundary.
Usage: python gen_dfd.py <out.svg>
"""
import math
import sys

from diagram_style import W, head, arrowhead

H = 944
EXTRA = """  <style>
    .tb { fill: none; stroke: #B3261E; } .tb-f { fill: #B3261E; font: 600 13px "Cascadia Mono", Consolas, monospace; }
    .legend { fill: #252A31; font: 400 13px "Cascadia Mono", Consolas, monospace; }
    @media (prefers-color-scheme: dark) {
      .tb { stroke: #F0A29B; } .tb-f { fill: #F0A29B; } .legend { fill: #E1E7DE; }
    }
  </style>"""

out = head(H, "Datenflussdiagramm: Benutzerkonto und Login im Lagerraum Box-Check",
           "Julia meldet sich an ihrem Gerät in der Web-App an. Die Web-App schickt Login, Reservierungsänderungen "
           "und Passwort-Reset über das Internet an den Reverse Proxy. Der Proxy leitet an das Backend weiter, das "
           "Konten, Sitzungen und Reservierungen in der zentralen Datenbank hält und Reset-Links über einen externen "
           "E-Mail-Dienst in Julias Postfach schickt. Drei Trust Boundaries: Julias Gerät, Backend im Docker-Netz, "
           "Drittanbieter. Neun nummerierte Datenflüsse mit Daten, Protokoll und Identität.", "tm-dfd")
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


def store(cx, top, name, sub, w=176, h=66, ry=9):
    x0, x1 = cx - w / 2, cx + w / 2
    out.append(f'  <path class="paper ink-s" stroke-width="1.4" d="M{x0},{top + ry} V{top + h - ry} A{w / 2},{ry} 0 0 0 {x1},{top + h - ry} V{top + ry} A{w / 2},{ry} 0 0 0 {x0},{top + ry} A{w / 2},{ry} 0 0 0 {x1},{top + ry}"/>')
    out.append(f'  <text class="name-s" x="{cx}" y="{top + 34}" text-anchor="middle">{name}</text>')
    out.append(f'  <text class="mono" x="{cx}" y="{top + 52}" text-anchor="middle">{sub}</text>')


def flow(points, both=False, r=8):
    """orthogonal polyline with rounded corners; arrowhead at the end (and start when both=True)"""
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
    """y on a circle outline at horizontal offset dx from its centre"""
    dy = math.sqrt(max(0.0, r * r - dx * dx))
    return cy + dy if lower else cy - dy


R = 50
WEB = (104, 190)
PROXY = (104, 392)
BACK = (336, 392)
MAIL = (520, 190)

boundary(16, 122, 320, 132, "Julias Gerät", 326, 142, "end")
boundary(440, 122, 216, 132, "Drittanbieter", 646, 246, "end")
boundary(16, 306, 640, 312, "Backend Lagerraum (Server, Docker Compose)", 28, 606)
out.append('  <text class="aside" x="176" y="285">Internet</text>')

# flows
flow([(104, 82), (104, WEB[1] - R)])                                                        # 1
for dx in (-34, 0, 34):                                                                     # 2, 3, 4
    flow([(WEB[0] + dx, chord(WEB[1], R, dx)), (PROXY[0] + dx, chord(PROXY[1], R, dx, lower=False))])
flow([(PROXY[0] + R, PROXY[1]), (BACK[0] - R, BACK[1])])                                    # 5
flow([(BACK[0], BACK[1] + R), (BACK[0], 520)])                                   # 6
flow([(BACK[0] + 30, chord(BACK[1], R, 30, lower=False)), (BACK[0] + 30, 280), (MAIL[0], 280), (MAIL[0], MAIL[1] + R)])  # 7
flow([(MAIL[0] + 20, chord(MAIL[1], R, 20, lower=False)), (MAIL[0] + 20, 82)])              # 8
flow([(464, 54), (180, 54)])                                                               # 9

# elements
actor(28, 26, 152, 56, "Julia", "Kundin")
actor(464, 26, 152, 56, "Julias Postfach", "E-Mail-Anbieter")
process(*WEB, R, ["Web-App"], "Browser")
process(*PROXY, R, ["Reverse", "Proxy"], "Traefik")
out.append(f'  <text class="mono" x="{PROXY[0]}" y="{PROXY[1] + R + 18}" text-anchor="middle">TLS endet hier</text>')
process(*BACK, R, ["Backend"], "Java-App", cls="acc", name_cls="name-acc")
process(*MAIL, R, ["E-Mail-", "Dienst"], "")
store(336, 520, "Zentrale Datenbank", "Konten · Sitzungen · Reservierungen", w=296)

for (x, y, n) in ((104, 104, 1), (70, 282, 2), (104, 282, 3), (138, 282, 4), (220, 392, 5),
                  (336, 480, 6), (444, 280, 7), (540, 104, 8), (322, 54, 9)):
    badge(x, y, n)

# legend: every flow with data, protocol, identity
y = 652
out.append(f'  <text class="name" x="16" y="{y}">Datenflüsse: was · wie · als wer</text>')
lines = [
    (1, "E-Mail-Adresse, Passwort · Eingabe am Gerät · Julia"),
    (2, "Login, Konto anlegen: E-Mail-Adresse + Passwort · HTTPS · anonym"),
    (3, "Box-Reservierung lesen, ändern, stornieren · HTTPS · Session-Cookie"),
    (4, "Reset anfordern, neues Passwort setzen · HTTPS · anonym, dann Einmal-Token"),
    (5, "Anfragen mit Cookie und Absender-IP weitergereicht · HTTP intern · Proxy"),
    (6, "Konten, Passwort-Hash, Sitzungen, Reservierungen · SQL · DB-Benutzer der App"),
    (7, "Mail mit Link (Bestätigung, Reset) · HTTPS-API · API-Schlüssel"),
    (8, "Mail mit Link · SMTP, TLS nicht garantiert · E-Mail-Dienst"),
    (9, "Link aus der Mail öffnen · Klick, öffnet die Web-App · Julia"),
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
