from scipy import signal

N = 4
rs = 40

fs = 1000

fl = 30
fh = 50
fn = fs / 2
Wn = (fl / fn, fh / fn)

fc = 200


b, a = signal.cheby2(4, 100, [0.02, 0.03], 'band', analog=False)

lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

n_a = 4
n_b = 4


def cheby_filter(lst):
    for i in range(n_a, len(lst) - n_b - 1):
        # center is i+1
        lst[i + 1] = b[0] * lst[i] + b[1] * lst[i - 1] + b[2] * lst[i - 2] + b[3] * lst[i - 3] - a[0] * lst[i + 2] - a[1] * lst[i + 3] - \
                     a[2] * lst[i + 4] - a[3] * lst[i + 5]
    return lst


print(lst)


