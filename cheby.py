import copy
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

filter_order = 6
band_attenuation = 3
cutoff_frequencies = [0.3, 2.5]
filter_type = 'bandpass'
sampling_frequency = 20


# noinspection PyTupleAssignmentBalance
# def filtering(x):
#     b, a = signal.cheby2(filter_order, band_attenuation, cutoff_frequencies,
#                          btype=filter_type, fs=sampling_frequency, output='ba')
#     return signal.filtfilt(b, a, x)


# def scipy_filter(x):
#     sos = signal.cheby2(filter_order, band_attenuation, cutoff_frequencies,
#                         btype=filter_type, fs=sampling_frequency, output='sos')
#     return signal.sosfiltfilt(sos, copy.deepcopy(data))


if __name__ == '__main__':
    # noinspection PyTupleAssignmentBalance
    b, a = signal.cheby2(filter_order, band_attenuation, cutoff_frequencies,
                         btype=filter_type, fs=sampling_frequency, output='ba')

    print("double m_a[] = {", end='')
    for i in a:
        print(i, end=', ')
    print("};")
    print("double m_b[] = {", end='')
    for i in b:
        print(i, end=', ')
    print("};")

    # w, h = signal.freqz(b, a)
    #
    # f = w / (2 * np.pi)  # Convert radians per second to Hertz
    # plt.plot(f, 20 * np.log10(abs(h)))  # Use plot instead of semilogx
    # plt.title('Chebyshev Type II frequency response (rs=40)')
    # plt.xlabel('Frequency [Hz]')  # Update x-axis label
    # plt.ylabel('Amplitude [dB]')
    # # plt.margins(0, 0.1)
    # plt.xlim([cutoff_frequencies[0] / (2 * np.pi), cutoff_frequencies[1] / (2 * np.pi)])
    # plt.grid(which='both', axis='both')
    # plt.axvline(cutoff_frequencies[0] / (2 * np.pi), color='green')
    # plt.axvline(cutoff_frequencies[1] / (2 * np.pi), color='green')
    # plt.axhline(-band_attenuation, color='green')  # rs
    # plt.show()

    a = [1.0000, -5.0444, 12.5719, -19.8200, 21.7362, -17.2699, 10.0968, -4.3253, 1.3272, -0.2770, 0.0354, -0.0021]
    b = [0.0025, -0.0025, 0.0073, -0.0023, 0.0069, 0.0025, 0.0025, 0.0069, -0.0023, 0.0073, -0.0025, 0.0025]

    w, h = signal.freqz(b, a)

    # Convert frequency from radians/sample to Hz
    f = w * sampling_frequency / (2 * np.pi)

    # Plot frequency response
    fig, ax = plt.subplots(1, 1, figsize=(10, 7))
    ax.plot(f, 20 * np.log10(np.abs(h)), label='Frequency Response')
    ax.set_title('Chebyshev II Frequency Response')
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Amplitude [dB]')
    ax.grid(True)

    # Add cutoff frequencies as vertical lines
    for cutoff in cutoff_frequencies:
        ax.axvline(cutoff, color='green', linestyle='dashed', label=f'Cutoff Frequency: {cutoff} Hz')

    ax.legend()

    # Set custom x-ticks at cutoff frequencies
    ax.set_xticks(cutoff_frequencies+[4], ['0.3Hz', '2.5Hz', '4Hz'])

    plt.xlim([min(f), 5])
    plt.tight_layout()
    plt.show()
