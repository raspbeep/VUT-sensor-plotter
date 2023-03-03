from matplotlib import pyplot as plt
import numpy as np

times = []
values_red = []
values_ir = []

with open('out8.txt', 'r') as f:
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
plt.plot(x_red, values_red, label="red")
plt.plot(x_ir, values_ir, label="ir")
plt.legend()
plt.show()

plt.show()
