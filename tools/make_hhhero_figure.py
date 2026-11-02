"""Draw the HHhero card figure: the HH sodium activation gate (m), two ways.

Left panel: alpha (solid) and beta (dashed). Right panel: the same gate as
x-infinity (solid) and tau (dashed). Above them, HHhero's own switch between
the two views. Labels are the symbols alone: the card does not explain them.

Rates are the paper's, in the modern sign (rest -65 mV), at 6.3 C (phi = 1):
    alpha_m = 0.1 (V + 40) / (1 - exp(-(V + 40) / 10))
    beta_m  = 4 exp(-(V + 65) / 18)
    m_inf = alpha / (alpha + beta),   tau_m = 1 / (alpha + beta)

Prints one <svg> to stdout, to be pasted into site/index.html in place of the
previous one. Run: python3 tools/make_hhhero_figure.py
"""
import math

V0, V1 = -100.0, 50.0
N = 151

M_COLOR = "#d35400"  # HHhero's --m


def alpha(v):
    x = v + 40.0
    if abs(x) < 1e-9:
        return 1.0
    return 0.1 * x / (1.0 - math.exp(-x / 10.0))


def beta(v):
    return 4.0 * math.exp(-(v + 65.0) / 18.0)


VS = [V0 + (V1 - V0) * i / (N - 1) for i in range(N)]
A = [alpha(v) for v in VS]
B = [beta(v) for v in VS]
MINF = [a / (a + b) for a, b in zip(A, B)]
TAU = [1.0 / (a + b) for a, b in zip(A, B)]

# Panel geometry, in the 420-wide frame every card figure shares.
TOP, BOT = 46.0, 132.0
PANELS = [(14.0, 196.0), (224.0, 406.0)]


def path(xs_panel, ys, ymax):
    x0, x1 = xs_panel
    pts = []
    for v, y in zip(VS, ys):
        px = x0 + (v - V0) / (V1 - V0) * (x1 - x0)
        py = BOT - min(y, ymax) / ymax * (BOT - TOP)
        pts.append(f"{px:.1f},{py:.1f}")
    return "M" + " L".join(pts)


rate_max = max(max(A), max(B))
tau_max = max(TAU)

left, right = PANELS
svg = f'''<svg class="ga ga-h" viewBox="0 0 420 138" role="img" aria-label="One Hodgkin-Huxley gate in both views: alpha and beta, and x-infinity and tau, under HHhero's switch between them."><style>.ga-h .g{{fill:none;stroke:{M_COLOR};stroke-width:1.7;stroke-linejoin:round}}
.ga-h .g.d{{stroke-dasharray:4 3}}
.ga-h .sw{{fill:var(--surface);stroke:var(--ink);stroke-width:1.2}}
.ga-h .on{{fill:var(--ink)}}
.ga-h text.sl{{font-family:var(--f-display);font-size:12px;font-weight:700;fill:var(--ink)}}
.ga-h text.sl.w{{fill:var(--surface)}}
.ga-h text.lg{{font-family:var(--f-display);font-size:13px;font-style:italic;fill:{M_COLOR}}}</style>
<rect class="sw" x="150" y="4" width="120" height="24" rx="5"/><rect class="on" x="150" y="4" width="60" height="24" rx="5"/>
<text class="sl w" x="180" y="20.5" text-anchor="middle">&#945;, &#946;</text><text class="sl" x="240" y="20.5" text-anchor="middle">x&#8734;, &#964;</text>
<line class="ax" x1="{left[0]}" y1="{BOT}" x2="{left[1]}" y2="{BOT}"/><line class="ax" x1="{right[0]}" y1="{BOT}" x2="{right[1]}" y2="{BOT}"/>
<path class="g" d="{path(left, A, rate_max)}"/><path class="g d" d="{path(left, B, rate_max)}"/>
<path class="g" d="{path(right, MINF, 1.0)}"/><path class="g d" d="{path(right, TAU, tau_max)}"/>
<text class="lg" x="{left[1]}" y="{BOT - A[-1] / rate_max * (BOT - TOP) - 6:.1f}" text-anchor="end">&#945;</text>
<text class="lg" x="{left[0] + 4}" y="{TOP + 4}">&#946;</text>
<text class="lg" x="{right[1]}" y="{TOP - 6}" text-anchor="end">x&#8734;</text>
<text class="lg" x="288" y="54" text-anchor="end">&#964;</text>
</svg>'''

print(svg)
