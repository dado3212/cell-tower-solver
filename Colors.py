from Types import Color

# Adapted from https://github.com/python/cpython/blob/3.10/Lib/colorsys.py
# and https://www.andrewt.net/puzzles/cell-tower/common/colours.js
PHI = (5 ** 0.5 + 1) * 0.5
ONE_THIRD = 1.0/3.0
TWO_THIRD = 2.0/3.0
ONE_SIXTH = 1.0/6.0

def _v(m1: float, m2: float, hue: float) -> float:
    hue = hue % 1.0
    if hue < ONE_SIXTH:
        return m1 + (m2-m1)*hue*6.0
    if hue < 0.5:
        return m2
    if hue < TWO_THIRD:
        return m1 + (m2-m1)*(TWO_THIRD-hue)*6.0
    return m1

def nthSunflowerColor(n: int) -> Color:
    l = 0.5
    s = 0.8
    h = ((PHI * n) % 1)
    if l <= 0.5:
        m2 = l * (1.0+s)
    else:
        m2 = l+s-(l*s)
    m1 = 2.0*l - m2
    # This is kind of bugged, it doesn't handle some light blues correctly
    is_dark = (h*365) > 180 or (h*365) < 30
    return (int(_v(m1, m2, h+ONE_THIRD)*256), int(_v(m1, m2, h) * 256), int(_v(m1, m2, h-ONE_THIRD) * 256), is_dark)


def printColor(color: Color, text: str) -> str:
    r = color[0]
    g = color[1]
    b = color[2]
    text = text.upper()
    if color[3]: # is_dark
        return f'\x1b[48;2;{r};{g};{b}m {text} \x1b[0m'
    else:
        return f'\x1b[48;2;{r};{g};{b}m\x1b[30m {text} \x1b[0m\x1b[0m'
