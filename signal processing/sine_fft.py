import numpy as np
import matplotlib.pyplot as plt

# Generate a sine wave with a frequency of 1 Hz, phase of 0.1, amplitude of 2, and offset of 1
fs = 10000  # sample rate (Hz)
MAX_DEGREE = 2*np.pi
t = np.linspace(0, 1, fs)  # time vector
y1 = np.sin(2*np.pi*48*t + 0)
y = 56*y1 + 70

fft = np.fft.fft(y)


# Get frequency
y_fft = fft[:round(len(t)/2)]   # First half ( pos freqs )
y_fft = np.abs(y_fft)           # Absolute value of magnitudes
y_fft = y_fft/max(y_fft)        # Normalized 
y_fft = y_fft[1:]

freq_x_axis = np.linspace(0, fs/2, len(y_fft)+1)
# print(y_fft)
f_loc = np.argmax(y_fft) + 1 # Finds the index of the max
f_val = freq_x_axis[f_loc] # The strongest frequency value

#Get Offset
offset = y.mean()

#Get amplitude
amplitude = np.ceil((max(abs(y))-offset))

#Get phase
# Calculate the phase
phase = np.arctan2(y1,np.cos(np.arcsin(y1)))

# Print results
print("Frequency:", np.floor(f_val))
print("Phase:", round(phase[0],2))
print("Amplitude:", amplitude)
print("Offset:", np.floor(offset))