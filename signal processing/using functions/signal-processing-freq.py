import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

MAX_DEGREE = 360
PLOT_TEXT_OFFSET = 320


def get_data_from_csv(path: str) -> tuple:
    """Gets csv file path and returns first two columns

    :param path: The file location of the spreadsheet
    :type path: str
    :returns: a tuple of numpy array representing the columns
    :rtype: tuple
    """

    data = pd.read_csv(path)
    x_label = data.columns[0]  # series3_x
    y_label = data.columns[1]  # series3_y
    x = np.array(data[x_label])
    y = np.array(data[y_label])
    return x, y


def calc_amplitude(y: np.ndarray) -> int:
    """Calculate Amplitude

    :param y: The data of a Sine signal
    :type y: numpy.ndarray
    :returns: amplitude value
    :rtype: int
    """
    amplitude = math.ceil(((max(y) - min(y))/2))
    return amplitude


def calc_frequency(y: np.ndarray) -> int:
    """Calculate Frequency

    :param y: The data of a Sine signal
    :type y: numpy.ndarray
    :returns: frequency value
    :rtype: int
    """
    max_indeces = np.where(y == max(y))[0]
    dist_between_peaks = max_indeces[2] - max_indeces[0]
    frequency = math.floor(MAX_DEGREE/dist_between_peaks)
    return frequency


def calc_offset(y: np.ndarray) -> int:
    """Calculate Offset

    :param y: The data of a Sine signal
    :type y: numpy.ndarray
    :returns: offset value
    :rtype: int
    """
    return math.ceil(min(y) + (max(y) - min(y))/2)


def calc_phase(y: np.ndarray, offset: int) -> int:
    """Calculate Phase

    :param y: The data of a Sine signal
    :type y: numpy.ndarray
    :returns: offset value
    :rtype: int
    """
    y_ceil = np.round(y)
    x_intersects = np.where(y_ceil == offset)[0]
    phase = x_intersects[-1] - MAX_DEGREE
    return phase


def plot_signal(x: np.ndarray, y: np.ndarray, amplitude: int, frequency: int, phase: int, offset: int):
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
    plt.text(-70, PLOT_TEXT_OFFSET, '$f(x) = a*sin(bx + c) + d$', fontsize=10)
    plt.text(70, PLOT_TEXT_OFFSET, 'Amplitude a = ' +
             str(amplitude), fontsize=8, color="red", alpha=0.8)
    plt.text(180, PLOT_TEXT_OFFSET, 'Frequency b = ' +
             str(frequency), fontsize=8, color="blue", alpha=0.8)
    plt.text(280, PLOT_TEXT_OFFSET, 'Phase c = ' + str(phase),
             fontsize=8, color="green", alpha=0.8)
    plt.text(350, PLOT_TEXT_OFFSET, 'Offset d = ' + str(offset),
             fontsize=8, color="purple", alpha=0.8)
    plt.plot(x, y)
    plt.plot(x, [offset]*len(x), 'r')
    plt.xlabel('Degrees', fontsize=10)
    plt.ylabel('Sin(θ)', fontsize=10)
    plt.show()


def main():
    path = input(
        "Enter csv file full path 'C:/example/my_example_data_file.csv': ")
    x, y = get_data_from_csv(path)

    # Sine function: y(x) = a*sin(bx + c) + d
    # a - Amplitude
    # b - freq
    # c - phase
    # d - offset

    amplitude = calc_amplitude(y)
    frequency = calc_frequency(y)
    offset = calc_offset(y)
    phase = calc_phase(y, offset)

    plot_signal(x, y, amplitude, frequency, phase, offset)


if __name__ == '__main__':
    main()
