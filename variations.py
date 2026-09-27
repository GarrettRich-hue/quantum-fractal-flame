from math import *
import numpy as np

def r(x):
    return np.linalg.norm(x)
def r2(x):
    return np.dot(x, x)
def theta(x):
    return atan(x[0]/x[1])
def phi(x):
    return atan(x[1]/x[0])

def linear(x):
    return x
def sinusoidal(x):
    return np.sin(x)
def spherical(x):
    return x / r2(x)
def swirl(x):
    xr2 = r2(x)
    return np.array([x[0] * sin(xr2) - x[1] * cos(xr2), x[0]*cos(xr2) + x[1]*sin(xr2)])
def horseshow(x):
    return 1/r(x) * np.array([(x[0]-x[1])*(x[0]+x[1]), 2 * x[0]*x[1]])
def polar(x):
    return np.array([theta(x)/pi, r(x)-1])
def handkerchief(x):
    xtheta = theta(x)
    xr = r(x)
    return xr*np.array([sin(xtheta + xr), cos(xtheta-xr)])
def heart(x):
    xtheta = theta(x)
    xr = r(x)
    return xr * np.array([sin(xtheta * xr), -cos(xtheta*xr)])
def disc(x):
    xtheta = theta(x)
    xr = r(x)
    return xtheta/pi * np.array([sin(pi*xr), cos(pi * xr)])
def spiral(x):
    xtheta = theta(x)
    xr = r(x)
    return 1/xr * np.array([cos(xtheta) + sin(xr), sin(xtheta) - cos(xr)])
def hyperbolic(x):
    xtheta = theta(x)
    xr = r(x)
    return np.array([sin(xtheta)/xr, xr * cos(xtheta)])


    
