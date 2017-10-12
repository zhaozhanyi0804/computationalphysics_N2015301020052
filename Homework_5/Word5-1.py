from pylab import *
from matplotlib import pyplot
import math
import numpy

g = 9.8

b2m = 4e-5

v_=float(input('please input the inital velocity :'))
theta_=float(input('please input the firing angle :'))

class initial_state:
    def __init__(self, _v = 0, _theta = 0):
        _rad = _theta*math.pi/180
        self.vx = _v * math.cos(_rad)
        self.vy = _v * math.sin(_rad)
class flight_state:
    def __init__(self, _x = 0, _y = 0, _vx = 0, _vy = 0, _t = 0):
        self.x = _x
        self.y = _y
        self.vx = _vx
        self.vy = _vy
        self.t = _t

#无阻力，只考虑重力作用
class cannon:
    def __init__(self, _fs = flight_state(0, 0, 0, 0, 0), _dt = 0.1):
        self.cannon_flight_state = []
        self.cannon_flight_state.append(_fs)
        self.dt = _dt
    def next_state1(self, current_state):
        global g
        next_x = current_state.x + current_state.vx * self.dt
        next_vx = current_state.vx
        next_y = current_state.y + current_state.vy * self.dt
        next_vy = current_state.vy - g * self.dt
        return flight_state(next_x, next_y, next_vx, next_vy, current_state.t + self.dt)

    def shoot1(self):
        while not(self.cannon_flight_state[-1].y < 0):
            self.cannon_flight_state.append(self.next_state1(self.cannon_flight_state[-1]))

        r = - self.cannon_flight_state[-2].y / self.cannon_flight_state[-1].y
        self.cannon_flight_state[-1].x = (self.cannon_flight_state[-2].x + r * self.cannon_flight_state[-1].x) / (r + 1)
        self.cannon_flight_state[-1].y = 0
        
    def show_trajectory1(self):
        global x1
        global y1            
        x1 = []
        y1 = []
        for fs in self.cannon_flight_state:
            x1.append(fs.x)
            y1.append(fs.y)
       
class cannon2(cannon):
    def __init__(self, _fs = flight_state(0, 0, 0, 0, 0), _dt = 0.1):
        self.cannon_flight_state2 = []
        self.cannon_flight_state2.append(_fs)
        self.dt = _dt            

    def next_state2(self, current_state):
        global g, b2m
        v = sqrt(current_state.vx * current_state.vx + current_state.vy * current_state.vy)
        #风阻随高度改变的系数
        pp0 = (1 - 6.5e-3 * current_state.y / 288.15) ** (2.5)
        next_x = current_state.x + current_state.vx * self.dt
        #风阻随高度改变时1
        next_vx = current_state.vx - pp0 * b2m * v * current_state.vx * self.dt
        next_y = current_state.y + current_state.vy * self.dt
        #风阻随高度改变时1
        next_vy = current_state.vy - g * self.dt - pp0 * b2m * v * current_state.vy * self.dt
        return flight_state(next_x, next_y, next_vx, next_vy, current_state.t + self.dt)

    def shoot2(self):
        while not(self.cannon_flight_state2[-1].y < 0):
            self.cannon_flight_state2.append(self.next_state2(self.cannon_flight_state2[-1]))
            
        r = - self.cannon_flight_state2[-2].y / self.cannon_flight_state2[-1].y

        self.cannon_flight_state2[-1].x = (self.cannon_flight_state2[-2].x + r * self.cannon_flight_state2[-1].x) / (r + 1)
        self.cannon_flight_state2[-1].y = 0

    def show_trajectory2(self):
        global x2
        global y2
        x2 = []
        y2 = []
        for fs in self.cannon_flight_state2:
            x2.append(fs.x)
            y2.append(fs.y)

    def show_out(self):   
        matplotlib.pyplot.figure(figsize=(8,6))
        matplotlib.pyplot.plot(x1,y1,label="g only cannon",color="blue",linewidth=3,linestyle='--')
        matplotlib.pyplot.plot(x2,y2,label="adiabatic drag cannon",color="red",linewidth=3,linestyle='--')
        matplotlib.pyplot.xlabel("x(m)")
        matplotlib.pyplot.title("Cannon shell trajectory")
        matplotlib.pyplot.ylabel("y(m)")
        matplotlib.pyplot.legend(loc='best')
        matplotlib.pyplot.show()

#给定初速度大小和角度
a = initial_state(v_,theta_)
#无风阻
b = cannon(flight_state(0, 0, a.vx, a.vy, 0), _dt = 0.1)
b.shoot1()
b.show_trajectory1()
c = cannon2(flight_state(0, 0, a.vx, a.vy, 0), _dt = 0.1)
c.shoot2()
c.show_trajectory2()
c.show_out()
show()
