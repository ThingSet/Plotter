import serial
import json
from datetime import datetime
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ser = serial.Serial("/dev/ttyACM0", 57600)

t = []
vbat = []
vsolar = []
ibat = []
iload = []
temp = []
soc = []
in_day = []
out_day = []

fig, ((ax_v, ax_i), (ax_soc, ax_e)) = plt.subplots(nrows=2, ncols=2)

#ax_v.set_title('Voltage')
line_vbat, = ax_v.plot([], [], 'b-', label='vBat')
line_vsolar, = ax_v.plot([], [], 'y-', label='vSolar')
ax_v.legend()

#ax_i.set_title('Current')
line_ibat, = ax_i.plot([], [], 'b-', label='iBat')
line_iload, = ax_i.plot([], [], 'r-', label='iLoad')
ax_i.legend()

#ax_soc.set_title('Temperature and SOC')
line_soc, = ax_soc.plot([], [], 'g-', label='SOC')
line_temp, = ax_soc.plot([], [], 'r-', label='tempInt')
ax_soc.legend()

line_in_day, = ax_e.plot([], [], 'g-', label='eInputDay')
line_out_day, = ax_e.plot([], [], 'r-', label='eOutputDay')
ax_e.legend()

ax_v.margins(0.05)

window = 60 # seconds
imin = 0

#xdata, ydata = [0]*100, [0]*100

def init():
#    line_vbat.set_data(t[:2],vbat[:2])
    return line,

def update_plot(line, xdata, ydata, axis):
    line.set_data(xdata, ydata)
    axis.relim()
    axis.autoscale()

def animate(t_latest):
    global imin
    while (t[imin] + window < t_latest):
        imin += 1

    update_plot(line_vbat, t[imin:], vbat[imin:], ax_v)
    update_plot(line_vsolar, t[imin:], vsolar[imin:], ax_v)
    update_plot(line_ibat, t[imin:], ibat[imin:], ax_i)
    update_plot(line_iload, t[imin:], iload[imin:], ax_i)
    update_plot(line_soc, t[imin:], soc[imin:], ax_soc)
    update_plot(line_temp, t[imin:], temp[imin:], ax_soc)
    update_plot(line_in_day, t[imin:], in_day[imin:], ax_e)
    update_plot(line_out_day, t[imin:], out_day[imin:], ax_e)

    return line_vbat,

def read_data():
    first_line = True
    start = datetime.now()
    num_data_objects = 0

    while True:
        raw_data = ser.readline()
        json_data = raw_data.decode('utf-8')[2:]  # remove first two bytes (ThingSet publication message identifier)
        #print(json_data, end='')
        try:
            timediff = datetime.now() - start
            seconds = round(timediff.seconds + timediff.microseconds/1e6, 3)

            data = json.loads(json_data)

            if (first_line):
                print("Time", end=',')
                print("seconds", end=',')
                print(",".join(data.keys()))
                first_line = False
                num_data_objects = len(data)

            assert(len(data) == num_data_objects)

            t.append(seconds)
            vbat.append(data['vBat'])
            vsolar.append(data['vSolar'])
            ibat.append(data['iBat'])
            iload.append(data['iLoad'])
            temp.append(data['tempInt'])
            soc.append(data['SOC'])
            in_day.append(data['eInputDay_Wh'])
            out_day.append(data['eOutputDay_Wh'])

            print(datetime.now(), end=',')
            print(seconds, end=',')
            print(",".join(map(str, data.values())))

            yield seconds
        except (json.decoder.JSONDecodeError, KeyError, AssertionError) as e:
            pass
            
#anim = animation.FuncAnimation(fig, animate, read_data, init_func=init, interval=25)
anim = animation.FuncAnimation(fig, animate, read_data, interval=25)

plt.show()
