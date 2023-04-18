def find_peaks(data, delta):
    max_list = []
    min_list = []
    x = [i for i in range(len(data))]

    mn = 0
    ms_set = 0
    mx = 0
    mx_set = 0
    min_pos = 0
    max_pos = 0

    look_for_max = 1

    for i in range(len(data)):
        this = data[i]
        if this > mx or not mx_set:
            mx_set = 1
            mx = this
            max_pos = x[i]
        if this < mn or not ms_set:
            ms_set = 1
            mn = this
            min_pos = x[i]

        if look_for_max:
            if this < mx - delta:
                max_list.append((max_pos, mx))
                mn = this
                min_pos = x[i]
                look_for_max = 0
        else:
            if this > mn + delta:
                min_list.append((min_pos, mn))
                mx = this
                max_pos = x[i]
                look_for_max = 1

    return max_list, min_list
