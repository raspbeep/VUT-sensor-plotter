import numpy as np


def convolve(x_arr, size):
    out = []
    out2 = []

    for i in range(len(x_arr) - (size - 1)):
        total = 0
        for j in range(i, i+size):
            total += x_arr[j]

        out.append(sum(x_arr[i:i + size]) / size)
        out2.append(total / size)

    return out


if __name__ == '__main__':
    x = [1, 2, 3, 4, 5, 6, 8, 4, 5, 1, 2, 3, 6, 7, 4]
    size = 3
    print(convolve(x, size))
    print((np.convolve(x, np.ones(size), 'valid') / size).tolist())
