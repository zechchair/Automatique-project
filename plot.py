from numpy import *
from numpy.linalg import *
from scipy.integrate import *
from scipy.signal import *

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
    #'max_step':1/60,
}


tf=10
Y0=[0,0,0]
result = solve_ivp(f, t_span=[0.0, tf], y0=Y0, **options)
from matplotlib.pyplot import *
import matplotlib.animation as animation
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from IPython.display import HTML
fig = plt.figure()
t = arange(0, tf, 1/60)
x = result["sol"](t)[0]
y = result["sol"](t)[1]
theta = result["sol"](t)[2]

#plot(x, y, "k--")


err=0.01
dt=1/60
ax = fig.add_subplot(111, autoscale_on=False, xlim=(min(x)-err, max(x)+err), ylim=(min(y)-err, max(y)+err))
ax.set_aspect('equal')
ax.grid()

line, = ax.plot([], [], "k", lw=3)
circle = patches.Circle([0.0, 0.0], radius=0.01/max(x), fc="r")
circle_s = patches.Circle([0.0, 0.0], radius=0.001/max(x), fc="g")

ax.add_artist(circle)
ax.add_artist(circle_s)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)


def init():
    line.set_data([], [])
    time_text.set_text('')
    return line, circle,circle_s, time_text


def animate(i):
    thisx = [ x[i], x[i+1]]
    thisy = [ y[i], y[i+1]]
    
    line.set_data(thisx, thisy)
    circle.center = [x[i], y[i]]
    circle_s.center = [x[i+10], y[i+10]]
    time_text.set_text(time_template % (i*dt))
    
    return line, circle,circle_s, time_text

anim = animation.FuncAnimation(fig, animate, range(0, len(t)),
                              interval=dt*1000, blit=True, init_func=init, repeat=False)

plt.plot(x,y)
plt.show()
