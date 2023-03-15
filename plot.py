import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from asyncio import get_event_loop
from serial_asyncio import open_serial_connection
from pyampd.ampd import find_peaks
import numpy as np
from cheby import filter_data

# def get_data():
#     line = serial_input.readline().decode('ascii', errors='replace')
#
#     while "NEW DATA:" not in line:
#         line = serial_input.readline().decode('ascii', errors='replace')
#         serial_input.flushOutput()
#
#     line = line.strip().strip('\x1b[0m').split("NEW DATA: ")[1].split(" ")
#     return [int(i, base=16) for i in line]


x_array = []
red_array = []
ir_array = []
number = 0

# fig = plt.figure()
# ax1 = fig.add_subplot(211)
# ax2 = fig.add_subplot(212, sharex=ax1)


# def animate(*args):
#     global red_array, ir_array, x_array
#     ax1.clear()
#     ax1.plot(x_array, red_array)
#
#     ax2.clear()
#     ax2.plot(x_array, ir_array)
#
#     plt.xticks(rotation=45, ha='right')
#     plt.subplots_adjust(bottom=0.20)
#     # ax.set_title('RED LED')
#     # ax.set_xlabel('# of sample')
#     # ax.set_ylabel('ADC RED Conversion')

values_red = []
peaks_red = []

count = 4

async def run():
    global red_array, ir_array, x_array, number, count
    reader, writer = await open_serial_connection(url='/dev/tty.usbmodem0006851234601', baudrate=115200)
    while count != 0:
        line = await reader.readline()
        line = line.decode('ascii', errors='replace')
        if "#values_red" in line or '#peaks' in line or 'BPM' in line:
            if "#values_red" in line:

                line = line.strip().split(": ")[1].split(" ")
                nums = [int(i) for i in line]
                print("values:\t", nums)
                values_red.append(nums)

            if "#peaks" in line:
                line = line.strip().split(": ")[1].split(" ")
                nums = [int(i) for i in line]
                print("peaks:\t", nums)
                peaks_red.append(nums)

            if "BPM" in line:
                # line = line.split(': ')[1]
                print(line)
                count -= 1

    if count == 0:
        print(values_red)
        print(peaks_red)



            # red_array += nums
            # # ir_array.append(nums[1])
            #
            # x_array.append(number)
            # number += 1
            #
            # red_array = red_array[-256:]
            # # ir_array = ir_array[-256:]
            # if len(red_array) > 100:
            #     pks = find_peaks(red_array, scale=100)
            #     print(pks)
            # x_array = x_array[-256:]
            #
            # ax1.clear()
            # ax1.plot(x_array, red_array)
            #
            # # ax2.clear()
            # # ax2.plot(x_array, ir_array)
            #
            # plt.xticks(rotation=45, ha='right')
            # plt.subplots_adjust(bottom=0.20)

            # plt.draw()
            # plt.pause(0.00001)

# ani = animation.FuncAnimation(fig, animate, interval=1)
# plt.ion()
# plt.show()
loop = get_event_loop()
loop.run_until_complete(run())

x_values_red = [np.arange(len(i)) for i in values_red]
x_peaks_red = []

for x in range(len(peaks_red)):
    vals_red = values_red[x]
    peaks_red_x = [vals_red[i] for i in peaks_red[x]]
    x_peaks_red.append(peaks_red_x)


fig, axs = plt.subplots(8)
for ax in range(4):
    axs[ax].plot(x_values_red[ax], values_red[ax])
    axs[ax].plot(peaks_red[ax], x_peaks_red[ax], 'r+')

    filtered = filter_data(values_red[ax])
    axs[ax+4].plot(x_values_red[ax], filtered)


