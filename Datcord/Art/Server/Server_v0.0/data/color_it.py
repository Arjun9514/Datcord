from colorit import *

r = Colors.red
o = Colors.orange
y = Colors.yellow
g = Colors.green
b = Colors.blue
p = Colors.purple
w = Colors.white

def clr(clr_cde):
    if clr_cde == "r":
        return r
    elif clr_cde == "o":
        return o
    elif clr_cde == "y":
        return y
    elif clr_cde == "g":
        return g
    elif clr_cde == "b":
        return b
    elif clr_cde == "p":
        return p
    elif clr_cde == "w":
        return w
    else:
        return w

def cln():
    init_colorit()

"""
def clrs(clr_cde):
    if clr_cde == "r":
        return r
    elif clr_cde == "o":
        return o
    elif clr_cde == "y":
        return y
    elif clr_cde == "g":
        return g
    elif clr_cde == "b":
        return b
    elif clr_cde == "p":
        return p
    elif clr_cde == "w":
        return w
    else:
        raise Exception
"""