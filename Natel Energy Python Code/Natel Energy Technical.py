import json
import numpy as np
import matplotlib.pyplot as plt
import math


#Read JSON File into an array Turbine1
with open('data.json') as data_file:
    data = json.load(data_file)

Turbine1 = data["results"][0]["series"][0]["values"]

#Arrays for further parsing
time = []
shaft_speed = []
shaft_torque = []
turbine_head = []
nozzle_percentage = []

#Reading values into corresponding arrays
#Removing any 0 RPM Measurments or null nozzle positions
for value in Turbine1:
    if(value[1] != 0 or value[4] != None):
        time.append(value[0])
        shaft_speed.append(value[1]*(2*(math.pi))/60) # Conversing from RPM to Rads/s
        shaft_torque.append(np.abs(value[2]))
        turbine_head.append(value[3])
        nozzle_percentage.append((value[4]))

#Calcuating Shaft Power as a function of RPM and Torque
shaft_power = np.abs([sT*rpm for sT,rpm in zip(shaft_torque,shaft_speed)])

#Array for simple graphing for easy pattern analysis
a = time
b = shaft_speed
c = shaft_torque
d = turbine_head
e = nozzle_percentage
f = shaft_power

arr = [a, b, c, d, e, f]
arrNames = ["Time (Uniz Epoch ms)", "Shaft Speed (Rads/s)",
            "Shaft Torque (Nm)", "Turbine Head (m)",
            "Nozzle Position (%)", "Shaft Power (W)"]

#Loop to make all possible graphs
k = 1
for i in range (0,6):
    for j in range (i,6):
        if(j != i):
            plt.figure(k)
            plt.scatter(arr[i],arr[j], marker='.')
            k += 1
            plt.xlabel(arrNames[i])
            plt.ylabel(arrNames[j])
            plt.title(arrNames[i] + " vs " + arrNames[j])


#Configuration of corresponding data on same plots
fig, ax1 = plt.subplots()
ax1.plot(a, f, 'b-')
ax1.set_xlabel('Time (Unix Epoch ms)')
# Make the y-axis label, ticks and tick labels match the line color.
ax1.set_ylabel('Shaft Power (W)', color='b')
ax1.tick_params('y', colors='b')

ax2 = ax1.twinx()
ax2.plot(a, e, 'r.')
ax2.set_ylabel('Nozzle Position (%)', color='r')
ax2.tick_params('y', colors='r')
plt.title("Shaft Power and Nozzle Position Overlay Vs. Time")


fig, ax1 = plt.subplots()
ax1.plot(a, f, 'b-')
ax1.set_xlabel('Time (Unix Epoch ms)')
# Make the y-axis label, ticks and tick labels match the line color.
ax1.set_ylabel('Shaft Power (W)', color='b')
ax1.tick_params('y', colors='b')

ax2 = ax1.twinx()
ax2.plot(a, d, 'r.')
ax2.set_ylabel('Turbine Head (m)', color='r')
ax2.tick_params('y', colors='r')
plt.title("Shaft Power and Turbine Head Overlay Vs. Time")

plt.show()