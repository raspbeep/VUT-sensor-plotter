import statistics as stat


def data_mean(data_array):
    total = 0
    for i in data_array:
        total += i
    return total / len(data_array)


def rounding(f):
    if f-int(f) < 0.5:
        return int(f)
    return int(f) + 1


def data_min(data_array):
    minimum = -1
    for i in data_array:
        if i < minimum or minimum == -1:
            minimum = i
    return minimum


def data_max(data_array):
    maximum = -1
    for i in data_array:
        if i > maximum or maximum == -1:
            maximum = i
    return maximum


tt_2 = 0
buffer_length = 2048
e_buffer = [0] * buffer_length
l_buffer = [0] * buffer_length
aet = 0

fs = 90


# Slope width (170ms) for PPG
slope_width = 0.17
slope_window = rounding(slope_width * fs)


def slp_samp(t, data_array):
    global tt_2, buffer_length, e_buffer, l_buffer, aet, slope_window
    while t > tt_2:

        if tt_2 > 0 and tt_2 - 1 > 0 and tt_2 < len(data_array) and tt_2 - 1 < len(data_array):
            val_2 = data_array[tt_2 - 2]
            val_1 = data_array[tt_2 - 1]
        else:
            val_2 = 0
            val_1 = 0

        dy = val_1 - val_2
        if dy < 0:
            dy = 0
        tt_2 += 1
        M = (tt_2 % (buffer_length - 1)) + 1

        e_buffer[M-1] = dy

        aet = 0
        for i in range(0, slope_window):
            p = M - i
            if p <= 0:
                p += buffer_length
            aet += e_buffer[p-1]
        l_buffer[M-1] = aet

    modul = (t % (buffer_length - 1))
    M3 = rounding(modul + 1)
    return l_buffer[M3 - 1]


invalid_data = -32768
# learning period is the first learning_period samples
learning_period = 2*fs
# eye-closing period is set to 0.34 sec (340 ms) for PPG
eye_closing_period = 0.45
# adjust threshold if no pulse found in NDP seconds
no_detection_period = 2.5
# minimum threshold value (default)
threshold_min_default = 5


def q_ppg(data):
    global tt_2, buffer_length, e_buffer, l_buffer, aet, slope_window
    idx_peaks = []
    beat_n = 1

    if data[0] <= invalid_data + 10:
        data[0] = data_mean(data)

    for i in range(len(data)):
        if data[i] <= invalid_data + 10:
            data[i] = data[i - 1]

    # rescale data to ±2000
    if len(data) < 5 * 60 * fs:
        minimum = data_min(data)
        maximum = data_max(data)
        for i in range(len(data)):
            data[i] = (data[i] - minimum) / (maximum - minimum) * 4000 - 2000
    else:
        step_size = 5 * 60 * fs

        min_data = []
        max_data = []

        for i in range(0, len(data), step_size):
            something = data[i: min(i + 5 * 60 * fs, len(data))]
            max_data.append(max(something))
            min_data.append(min(something))
        med_min = stat.median(min_data)
        med_max = stat.median(max_data)

        for i in range(len(data)):
            data[i] = ((data[i] - med_min) / (med_max - med_min) * 4000) - 2000

    eye_closing = rounding(eye_closing_period * fs)
    expected_period = rounding(no_detection_period * fs)
    timer = 0

    t1 = 8 * fs
    t0 = 0
    n = 0
    for t in range(1, t1 + 2):
        temp = slp_samp(t, data)
        if temp > invalid_data + 10:
            t0 = t0 + temp
            n += 1

    t0 = t0 / n
    ta = 3 * t0

    learning = 1
    t = 0

    while t <= len(data):
        if learning:
            if t > 0 + learning_period:
                learning = 0
                t1 = t0
                t = 0
            else:
                t1 = 2 * t0

        temp = slp_samp(t, data)

        if temp > t1:
            timer = 0
            max_d = temp
            min_d = temp
            t_max = 0
            for tt in range(t + 1, t + eye_closing - 1):
                temp2 = slp_samp(tt, data)
                if temp2 > max_d:
                    max_d = temp2
                    t_max = tt

            if max_d == temp:
                t += 1
                continue
            for tt in range(t_max, (t - (eye_closing // 2) + 1), -1):
                temp2 = slp_samp(tt, data)
                if temp2 < min_d:
                    min_d = temp2

            if max_d > min_d + 10:
                onset = ((max_d - min_d) / 100) + 2
                tpq = t - rounding(0.04 * fs)
                max_min_2_3_threshhold = (max_d - min_d) * (2.0 / 3)

                stop = -1

                for tt in range(t_max, (t - eye_closing // 2) + 1, -1):
                    temp2 = slp_samp(tt, data)
                    if temp2 < max_min_2_3_threshhold:
                        stop = tt
                        break

                if stop == -1:
                    stop = (t - eye_closing // 2)

                for tt in range(stop, t - eye_closing // 2 + rounding(0.024 * fs), -1):
                    temp2 = slp_samp(tt, data)
                    temp3 = slp_samp(tt - rounding(0.024 * fs), data)
                    if temp2 - temp3 < onset:
                        tpq = tt - rounding(0.016 * fs)
                        break

                valley_v = rounding(tpq)
                f = rounding(max(2, tpq - rounding(0.20 * fs)))
                to = rounding(min(tpq + rounding(0.05 * fs), len(data) - 1))
                for valley_i in range(f, to):
                    if valley_v <= 0:
                        t += 1
                        continue
                    if data[valley_v] > data[valley_i] and \
                            data[valley_i] <= data[valley_i - 1] and \
                            data[valley_i] <= data[valley_i + 1]:
                        valley_v = valley_i

                if not learning:
                    if beat_n == 1:
                        if rounding(valley_v) > 0:
                            idx_peaks.append(rounding(valley_v))
                            beat_n += 1
                    else:
                        if rounding(valley_v) > idx_peaks[beat_n - 1 - 1]:
                            idx_peaks.append(rounding(valley_v))
                            beat_n += 1

                ta += (max_d - ta) / 10
                t1 = ta / 3

                t = tpq + eye_closing
        else:
            if not learning:
                timer += 1
                if timer > expected_period and ta > threshold_min_default:
                    ta -= 1
                    t1 = ta / 3

        t += 1

    return idx_peaks
