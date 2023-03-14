import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

data = pd.read_csv('sinx-4waves.csv')
x_label = data.columns[0]  # series3_x
y_label = data.columns[1]  # series3_y
x = np.array(data[x_label])
y = np.array(data[y_label])

# Sine function: y(x) = a*sin(bx + c) + d
# a - Amplitude
# b - freq
# c - phase
# d - offset

# Calculate Amplitude
Amplitude = math.ceil(((max(y) - min(y))/2))

# Calculate Frequency
MAX_DEGREE = 360
max_indeces = np.where(y == max(y))[0]
dist_between_peaks = max_indeces[2] - max_indeces[0]
Frequency = math.floor(MAX_DEGREE/dist_between_peaks)

# Calculate Offset
offset = math.ceil(min(y) + (max(y) - min(y))/2)

# Calculate Phase
y_ceil = np.round(y)
x_intersects = np.where(y_ceil == offset)[0]
Phase = x_intersects[-1] - MAX_DEGREE


y_text_offset = 320  # TODO - check how to find size automaticlly
plt.text(-70, y_text_offset, '$f(x) = a*sin(bx + c) + d$', fontsize=10)
plt.text(70, y_text_offset, 'Amplitude a = ' +
         str(Amplitude), fontsize=8, color="red", alpha=0.8)
plt.text(180, y_text_offset, 'Frequency b = ' +
         str(Frequency), fontsize=8, color="blue", alpha=0.8)
plt.text(280, y_text_offset, 'Phase c = ' + str(Phase),
         fontsize=8, color="green", alpha=0.8)
plt.text(350, y_text_offset, 'Offset d = ' + str(offset),
         fontsize=8, color="purple", alpha=0.8)
plt.plot(x, y)
plt.plot(x, [offset]*len(x), 'r')
plt.xlabel('Degrees', fontsize=10)
plt.ylabel('Sin(θ)', fontsize=10)
plt.show()
