import csv
import matplotlib.pyplot as plt
import numpy as np
import math



def plot_sin_data(angles, amplitudes):
    plt.plot(angles, amplitudes)
    plt.xlabel('Angle (radians)')
    plt.ylabel('Amplitude')
    plt.title('Sin Wave')
    plt.show()



def read_sin_data(filename):
    angle = []
    amplitude = []
    
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)  # skip the header row
        for row in reader:
            _, a, phi = row  # _ is used to ignore the time value
            angle.append(float(phi))
            amplitude.append(float(a))
    
    return angle, amplitude

angles, amplitudes = read_sin_data('sin_data.csv')

def print_sin_data(angles, amplitudes):
    for angle, amplitude in zip(angles, amplitudes):
        print(f"Angle: {angle}, Amplitude: {amplitude}")



def show_to_student():
   print_sin_data(angles, amplitudes)
   plot_sin_data(angles, amplitudes)


show_to_student()


