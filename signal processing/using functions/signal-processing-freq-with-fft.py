import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

MAX_DEGREE = 360

def get_data_from_csv(path: str) -> tuple:
    """Gets csv file path and returns first two columns

    :param path: The file location of the spreadsheet
    :type path: str
    :returns: a tuple of numpy array representing the columns
    :rtype: tuple
    """
    data = pd.read_csv(path)
    x = np.array(data['series3_x'])
    x = x[x != '-'].astype(float) if '-' in x  else x.astype(float)
    y = np.array(data['series3_y'])
    y = y[y != '-'].astype(float) if '-' in y  else y.astype(float)
    return x, y


def calc_amplitude(y: np.ndarray, offset: int) -> int:
    """Calculate Amplitude

    :param y: The data of a Sine signal
    :type y: numpy.ndarray
    :returns: amplitude value
    :rtype: int
    """
    amplitude = np.round((max(abs(y)) - offset))

    return amplitude


def calc_frequency(y: np.ndarray) -> int:
    """Calculate Frequency

    :param y: The data of a Sine signal
    :type y: numpy.ndarray
    :returns: frequency value
    :rtype: int
    """
    fs = 1000                  # sample rate (Hz)
    t = np.linspace(0, 1, fs)  # time vector
    fft = np.fft.fft(y)

    # Get frequency
    y_fft = fft[:round(len(t)/2)]   # First half ( pos freqs )
    y_fft = np.abs(y_fft)           # Absolute value of magnitudes
    y_fft = y_fft/max(y_fft)        # Normalized
    y_fft = y_fft[1:]
    freq_x_axis = np.linspace(0, fs/2, len(y_fft) + 1)
    f_loc = np.argmax(y_fft)        # Finds the index of the max
    frequency = freq_x_axis[f_loc]  # The strongest frequency value
    return np.round(frequency, 2)


def calc_offset(y: np.ndarray) -> int:
    """Calculate Offset

    :param y: The data of a Sine signal
    :type y: numpy.ndarray
    :returns: offset value
    :rtype: int
    """
    return np.round(min(y) + (max(y) - min(y))/2)


def calc_phase(y: np.ndarray, x, amplitude, frequency, offset):
    """Calculate Phase

    :param y: The data of a Sine signal
    :type y: numpy.ndarray
    :returns: offset value
    :rtype: int
    """
    phase_rad = np.arcsin((y[0]-offset)/amplitude) - (frequency*x[0])
    phase_deg = (phase_rad * MAX_DEGREE/2) / np.pi
    return np.round(phase_deg, 2)


def plot_signal(x: np.ndarray, y: np.ndarray, amplitude: int, frequency: int, phase, offset: int):
    """Plot Signal

    :param x: Sine signal degrees
    :type x: numpy.ndarray
    :param y: The data of a Sine signal
    :type y: numpy.ndarray
    :param amplitude: amplitude value
    :type amplitude: int
    :param frequency: frequency value
    :type frequency: int
    :param phase: phase value
    :type phase: int
    :param offset: offset value
    :type offset: int
    :returns: None
    """
    _, (ax1, ax2) = plt.subplots(1, 2)
    ax1.plot(x, y)
    ax1.plot(x, [offset]*len(x), 'r')
    ax1.set_title('f(x) = ' + str(amplitude) + '*sin(' +
                  str(frequency) + 'x + ' + str(phase) + ') + ' + str(offset), fontsize=9,  fontweight='bold')
    ax1.set(xlabel='Degrees', ylabel='Sin(θ)')

    equation_texts = ['$f(x) = a*sin(bx + c) + d$',
                      'Amplitude: a = ' + str(amplitude),
                      'Frequency: b = ' + str(frequency),
                      'Phase: c = ' + str(phase),
                      'Offset: d = ' + str(offset)]
    for i, t in enumerate(equation_texts[::-1]):
        ax2.text(0, i, t, fontsize=10, fontweight='bold',
                 bbox=dict(facecolor='red', alpha=0.5),
                 transform=ax2.get_yaxis_transform(), ha='left')

    # removing border and axis
    ax2.set_ylim(-0.5, len(equation_texts) - 0.5)
    ax2.spines['top'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    plt.axis('off')
    ax2.set_title('Sine Functions Variables', fontsize=9, fontweight='bold')

    plt.tight_layout()
    plt.show()


def main():
    path = input(
        "Enter csv file full path 'C:/example/my_example_data_file.csv': ")
    x, y = get_data_from_csv(path)
    # Sine function: y(x) = a*sin(bx + c) + d
    # a - Amplitude
    # b - Frequency
    # c - Phase
    # d - Offset

    frequency = calc_frequency(y)
    offset = calc_offset(y)
    amplitude = calc_amplitude(y, offset)
    phase = calc_phase(y, x, amplitude, frequency, offset)

    plot_signal(x, y, amplitude, frequency, phase, offset)


if __name__ == '__main__':
    main()
