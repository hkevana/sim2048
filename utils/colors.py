from utils.constants import *

colors = {
    t_bg:     (100, 113, 147),
    t_sq:     (205, 193, 180),
    t_fb:     (122, 112, 102),
    t_fw:     (255, 255, 255),
    t_stg_bg: (155, 143, 130),
    t_hud_bg: (140, 153, 187),
    t_000000: (205, 193, 180),
    t_000002: (250, 240, 230),
    t_000004: (255, 242, 218),
    t_000008: (242, 177, 121),
    t_000016: (245, 149,  99),
    t_000032: (246, 124,  95),
    t_000064: (246,  94,  69),
    t_000128: (237, 207, 114),
    t_000256: (237, 204,  97),
    t_000512: (237, 200,  80),
    t_001024: (237, 197,  63),
    t_002048: (237, 194,  46),
    t_004096: ( 96, 217, 146),
    t_008192: ( 39, 187, 103),
    t_016384: ( 35, 140,  81),
    t_032768: (116, 181, 221),
    t_065536: ( 94, 161, 229),
    t_131072: (  0, 127, 194)
}

def get_color(color):
    return colors.get(color, colors[t_fw])


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import numpy as np

    im = plt.imread("../assets/colors.png")

    clrs = []

    for y in range(1, len(im), 5):
        print()
        for x in range(1, len(im[0]), 5):
            clrs.append(255*im[y,x])

    for r,g,b in clrs:
        print("({:3d}, {:3d}, {:3d}),".format(int(r),int(g),int(b)))
