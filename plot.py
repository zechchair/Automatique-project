from numpy import *
from numpy.linalg import *
from scipy.integrate import *
from scipy.signal import *
from matplotlib.pyplot import *
R=0.1
D=1
def omega_l(t):
    if t <= 5.0:
        return pi * D
    else:
        return 0.0
    
def omega_r(t):
    if t >= 5.0:
        return pi * D
    else:
        return 0.0
def f(t, X):
    x, y, theta = X
    dx =R*(omega_r(t)+omega_l(t))/2*cos(theta)
    dy=R*(omega_r(t)+omega_l(t))/2*sin(theta)
    dtheta=R*(omega_r(t)-omega_l(t))/D*2
    dX = array([dx, dy, dtheta])
    return dX

options = {
    "dense_output": True,
    'max_step':1/60,
}
tf=10
Y0=[0,0,0]
result = solve_ivp(f, t_span=[0.0, tf], y0=Y0, **options)

t = arange(0, tf, 1/60)
x = result["sol"](t)[0]
y = result["sol"](t)[1]
theta = result["sol"](t)[2]
err=0.1
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation, rc
from IPython.display import HTML
fig=plt.figure()
ax= fig.add_subplot(111,xlim=(min(x)-err, max(x)+err), ylim=(min(y)-err, max(y)+err))

#ax.set_xlim(( 0, 2))
#ax.set_ylim((-2, 2))

line, = ax.plot([], [], lw=2)
# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return (line,)
# animation function. This is called sequentially
def animate(i):
    thisx = [ x[i-1], x[i]]
    thisy = [ y[i-1], y[i]]
    line.set_data(thisx, thisy)
    return (line,)

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               repeat=False, interval=20, blit=True)

plt.show()

