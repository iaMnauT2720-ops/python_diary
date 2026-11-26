import turtle
import colorsys
import math
import random

random.seed(3)
BEATS, PERIOD = 4, 190

screen = turtle.Screen()
screen.setup(780,480)
screen.bgcolor("#07020c")

screen.colormode(1.0)

t = turtle.Turtle()
t.hideturtle()
t.speed(0)
t.penup()

def neon(h, s=0.9, v=1.0):
    return colorsys.hsv_to_rgb(h % 1, s, v)

def stroke(pts, color, width):
    t.pencolor(color)
    t.pensize(width)
    t.goto(*pts[0])
    t.pendown()
    for p in pts[1:]:
        t.goto(*p)
    t.penup()

def bump(x, c, w, h):
    return h * math.exp(-((x - c) / w) ** 2)

def wave(u):
    y = bump(u, 0.15, 0.05, 12)
    y += bump(u, 0.33, 0.012, -14)
    y += bump(u, 0.37, 0.014, 95)
    y += bump(u, 0.41, 0.012, -30)
    y += bump(u, 0.65, 0.06, 26)
    return y

def heart_pts(s, n=100):
    pts = []
    for i in range(n + 1):
        a = 6.283 * i / n
        x = 16 * math.sin(a) ** 3
        y = (13 * math.cos(a) - 5 * math.cos(2 * a)
             - 2 * math.cos(3 * a) - math.cos(4 * a))
        pts.append((x * s, y * s + 6))
    return pts

def grid():
    dim = neon(0.93, 0.8, 0.22)
    for g in range(-360, 361, 30):
        stroke([(g, -240), (g, 240)], dim, 1)
    for g in range(-240, 241, 30):
        stroke([(-390, g), (390, g)], dim, 1)

def ecg():
    pts = []
    total = BEATS * PERIOD
    for i in range(total + 1):
        beat = i // PERIOD
        amp = 1.0 + 0.35 * (beat == BEATS - 1)
        y = wave((i % PERIOD) / PERIOD) * amp
        pts.append((i - total / 2, y))
    for k in range(0, total, 20):
        color = neon(0.5 + 0.42 * k / total)
        stroke(pts[k:k + 21], color, 3)

def hearts(n):
    for i in range(1, n + 1):
        d = i / n
        s = 0.25 + 0.75 * d
        v = 1.0
        color = neon(0.93 + 0.065 * d, s, v)
        stroke(heart_pts(10.5 * d), color, 4.7)

def echo():
    for i in range(6):
        v = 0.9 - i * 0.14
        outline = heart_pts(11.4 + i * 0.55)
        stroke(outline, neon(0.95, 0.8, v), 3)

def sparkles():
    for _ in range(140):
        a = random.uniform(0, 6.283)
        r = random.uniform(185, 230)
        x,y = r * math.cos(a), r * math.sin(a)
        t.goto(x * 1.4, y * 0.95)
        hue = random.choice([0.9, 0.97, 0.55])
        t.dot(random.randint(2, 5), neon(hue, 0.5))

grid()
ecg()
hearts(36)
echo()
sparkles()
screen.update()
turtle.done()