import numpy as np
import matplotlib.pyplot as plt

samples_per_wave = 512
amplitude = 511 # maximum amplitude 0-511

# Generate sine wave
x = np.arange(samples_per_wave)
sine_wave = np.round(amplitude * 0.5 * (1 + np.sin(2 * np.pi * x / samples_per_wave)))

# Generate triangle wave
triangle_wave = np.concatenate([
    np.linspace(0, amplitude, samples_per_wave // 2, endpoint=False),
    np.linspace(amplitude, 0, samples_per_wave // 2, endpoint=False)
])

# Generate square wave
square_wave = np.concatenate([
    np.full(samples_per_wave // 2, amplitude),
    np.full(samples_per_wave // 2, 0)
])

waveform = np.concatenate([sine_wave, triangle_wave, square_wave])
waveform = waveform.astype(int)

# Write to txt file
with open('sinetrianglesquare.txt', 'w') as f:
    for v in waveform:
        f.write(f'{v:03x}\n')

# # Plot to verify shapes
# plt.figure(figsize=(12, 6))
# plt.plot(waveform[:samples_per_wave], label='Sine')
# plt.plot(waveform[samples_per_wave:2*samples_per_wave], label='Triangle')
# plt.plot(waveform[2*samples_per_wave:], label='Square')
# plt.title("Generated Waveforms (from waveform.txt)")
# plt.xlabel("Sample Index")
# plt.ylabel("Amplitude (0–511)")
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
# plt.show()