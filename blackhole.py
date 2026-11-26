import numpy as np
from scipy.ndimage import gaussian_filter as blur

W, H = 1080, 920
CX, CY = W / 2, H / 2
rng = np.random.default_rng(7)
P = dict(stars=1, disk=1, hole=1, zoom=1)

#disk particles
N = 52000
r0 = 1.45+ 4.8 * rng.random(N) ** 1.6
a0 = rng.uniform(0, 6.283, N)
STAR = rng.uniform(-1, 1, (1500,2)) * (W/2, H/2)
TINT = rng.uniform(0, 1, (1500,1))
JIT = rng.normal(0, .008, 3000)
DIST = np.hypot(*np.meshgrid(np.arange(W) - CX,
                             np.arange(H) - CY))
NEB = blur (rng.random((H // 8, W // 8)), 6)
NEB = np.kron((NEB -NEB.min()) / np.ptp(NEB),
              np.ones((8,8)))

#hot core --> cold rim
def heat(u):
    pts = [0, .25, .55,.8, 1]
    c = np.array([[255, 255, 170], [255, 140, 60],
                  [255, 50, 150], [150, 60, 255],
                  [40, 150, 255]]) / 255
    return np.stack([np.interp(u, pts, c[:, i])
                     for i in range(3)], 1)

COL =  heat((r0 - 1.45) / 4.8) ** 1.0

#1 horizon radius, in px
def unit():
    return 120 * P["zoom"]
#how flat we see the disk
def tilt(t):
    return .22 * (1 + .35 * np.sin(.25 * t))
#adds dots to the canvas
def splat(buf, x, y, c):
    i = (x + CX).astype(int)
    j = (y + CY).astype(int)
    ok = (i >= 0) & (i < W) & (j >= 0) & (j < H)
    k = j[ok] * W + i[ok]
    for ch in range(3):
        buf[..., ch] += np.bincount(
            k, c[ok, ch], W * H).reshape(H, W)

#neon glow
def bloom(x):
    def down(k):
            return x.reshape(H // k , k, W // k, k, 3).mean((1,3))
    wide = blur(down(4), (6, 6, 0)).repeat(4,0).repeat(4,1)
    mid = blur(down(2), (2.5, 2.5, 0)).repeat(2,0).repeat(2,1)
    return x + 1.6 * mid + 3.2 * wide

#inner rings spin faster
def orbit(t):
    m = r0 < 1.45 + 4.8 * P["disk"]
    u = r0[m]
    a = a0[m] + 1.8 * t / u ** 1.5
    w =  (1 - .55 * np.cos(a)) *  (1.45 / u) **  .8 * .35
    return u, np.cos(a), np.sin(a), COL[m] * w [:, None]

#lights bend around the hold
def stars(buf, t):
    n = int(len(STAR) * P["stars"])
    c, s = np.cos(.03 * t), np.sin(.03 * t)
    x = STAR[:n, 0] * c - STAR[:n, 1] * s
    y = STAR[:n, 0] * s + STAR[:n, 1] * c
    b = np.hypot(x, y) * P["zoom"] + 1
    e = 1.3 * unit()
    k = (b + np.sqrt(b * b + 4 * e * e)) / 2 / b
    tw = .55 + .45 * np.sin(3 * t + 9 * TINT[:n])
    c = (1 - TINT[:n]) * [1, 1, 1] + TINT[:n] * [.5, .8,1]
    splat(buf, x * k * P["zoom"], y * k * P["zoom"], c * tw * .9)

#far side, bent over the top
def halo(buf, t):
    u,c,s,col = orbit(t)
    back = s < 0
    rho = unit() * (1.06 + .16 * (u - 1.45))
    splat(buf, (rho * c)[back], (rho * s)[back], col[back])
    splat(buf, (rho * c)[back], (-rho * s * .97)[back],
          col[back] * .45)
    x, y = u * unit() * c, u * unit () * s * tilt(t)
    far = back & (abs(x) > 1.1 * unit())
    splat(buf, x[far], y[far], col[far]* .45)

#photon ring
def ring(buf, t):
    a = np.linspace(0, 6.238, 3000)
    r = unit() * (1.04 + JIT) * P["hole"]
    hot = .5 + .9 * np.cos((a - .9 * t) / 2) ** 2
    c = np.array([1, .86, .62]) * hot[:, None] * .9 * P["hole"] ** 1.5
    splat(buf, r * np.cos(a), r * np.sin(a), c)

#the event horizon
def hole(buf):
    r = unit() * P["hole"]
    buf *= np.clip((DIST - r) / 3, 0, 1)[..., None]

#near side crosses the hole
def disk(buf, t):
    u,c,s,col = orbit(t)
    near = s >= 0
    x, y = u * unit() * c, u * unit() * s * tilt(t)
    layer = np.zeros_like(buf)
    splat(layer, x[near], y[near], col[near] * 2.4)
    buf += bloom(layer)

#matters falling in
def sparks(buf, t, n=450):
    f = (np.arange(n) / n + .07 * t) % 1
    r = unit() * (6.3 - 4.9 * f)
    a = np.arange(n) * 2.4 + t * 1.2 + f * 14
    x, y = r * np.cos(a) , r * np.sin(a) * tilt(t)
    ok = (np.sin(a) > 0) | (np.hypot(x,y) > unit())
    c = np.array([.7, .9, 1]) * (1 - f[:, None] ** 3)
    layer = np.zeros_like(buf)
    splat(layer, x[ok], y[ok], c[ok] * 1.6)
    buf += bloom(layer)

def frame(t):
    buf = np.zeros((H, W, 3), np.float32)
    stars(buf, t)
    halo(buf, t)
    ring(buf, t)
    buf[:] = bloom(buf)
    hole(buf)
    disk(buf, t)
    sparks(buf, t)
    sky = NEB[..., None] ** 3 * [.05, .02, .09]
    sky += [.01, .015, .04]
    out = 2.2 * buf / (1 + 2.2 * buf) + sky
    return (255 * out).clip(0,255).astype(np.uint8)