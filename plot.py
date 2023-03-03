import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from asyncio import get_event_loop
from serial_asyncio import open_serial_connection

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

fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212, sharex=ax1)


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


async def run():
    global red_array, ir_array, x_array, number
    reader, writer = await open_serial_connection(url='/dev/tty.usbmodem0006850495561', baudrate=115200)
    while True:
        line = await reader.readline()
        line = line.decode('ascii', errors='replace')
        print(line)
        if "NEW DATA:" in line:
            line = line.strip().strip('\x1b[0m').split("NEW DATA: ")[1].split(" ")
            nums = [int(i, base=16) for i in line]
            red_array.append(nums[0])
            ir_array.append(nums[1])
            x_array.append(number)

            number += 1

            red_array = red_array[-256:]
            ir_array = ir_array[-256:]
            x_array = x_array[-256:]

            ax1.clear()
            ax1.plot(x_array, red_array)

            ax2.clear()
            ax2.plot(x_array, ir_array)

            plt.xticks(rotation=45, ha='right')
            plt.subplots_adjust(bottom=0.20)

            plt.draw()
            plt.pause(0.00001)

# ani = animation.FuncAnimation(fig, animate, interval=1)
plt.ion()
plt.show()
loop = get_event_loop()
loop.run_until_complete(run())
