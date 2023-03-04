from matplotlib import pyplot as plt
import numpy as np
from pyampd.ampd import find_peaks


times = []
values_red = []
values_ir = []

with open('out4.txt', 'r') as f:
    data = f.readlines()
    data = [line for line in data if "app" in line
            and "HERE" not in line and "Temperature" not in line
            and "temperature" not in line]
    for line in data:
        line = line.strip().split(" app: ")
        line = line[1].split(" ")

        nums = [int(i, base=16) for i in line]
        try:
            values_red.append(nums[0])
            values_ir.append(nums[1])
        except Exception:
            print(line)


x_red = np.arange(len(values_red))
x_ir = np.arange(len(values_ir))

print(values_red)
print(values_ir)
peaks_red = [12, 56, 103, 151, 189, 284, 328, 369, 413, 458, 499, 543, 590, 634, 677, 722, 763, 804, 831]
peaks_red_x = [values_red[i] for i in peaks_red]

peaks_ir = [11, 57, 101, 149, 189, 283, 328, 369, 413, 457, 499, 543, 590, 634, 677, 722, 761, 803, 831]
peaks_ir_x = [values_ir[i] for i in peaks_ir]


plt.plot(x_red, values_red, label="red")
plt.plot(x_ir, values_ir, label="ir")
plt.legend()

plt.plot(peaks_red, peaks_red_x, 'r+')
plt.plot(peaks_ir, peaks_ir_x, 'b+')
plt.show()


