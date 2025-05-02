import numpy as np
import matplotlib.pyplot as plt

samples_per_wave = 512
amplitude = 511

# Sine wave
x = np.arange(samples_per_wave)
sine_wave = np.round(amplitude * 0.5 * (1 + np.sin(2 * np.pi * x / samples_per_wave)))

# Triangle wave
triangle_wave = np.concatenate([
    np.linspace(0, amplitude, samples_per_wave // 2, endpoint=False),
    np.linspace(amplitude, 0, samples_per_wave // 2, endpoint=False)
])

# Square wave
square_wave = np.concatenate([
    np.full(samples_per_wave // 2, amplitude),
    np.full(samples_per_wave // 2, 0)
])

# Heartbeat wave
heartbeat_wave = np.full(samples_per_wave, 256)
def triangle_pulse(width, height, invert=False):
    x = np.linspace(0, height, width // 2, endpoint=False)
    y = np.linspace(height, 0, width // 2, endpoint=True)
    pulse = np.concatenate((x, y))
    return -pulse if invert else pulse

def apply_pulse(center, offset, pulse):
    start = center + offset
    end = start + len(pulse)
    if 0 <= start and end <= samples_per_wave:
        heartbeat_wave[start:end] += pulse

small_pulse = triangle_pulse(20, 100, invert=True).astype(int)
large_pulse = triangle_pulse(40, 200).astype(int)

for c in [128, 384]:
    apply_pulse(c, -40 - 20, small_pulse)
    apply_pulse(c, -20,        large_pulse)

waveform = np.concatenate([sine_wave, square_wave, triangle_wave, heartbeat_wave])
waveform = waveform.astype(int)


# Write to file
with open('wave.txt', 'w') as f:
    for v in waveform:
        f.write(f'{v:03x}\n')

# # Plot to verify shapes
# plt.plot(waveform[:samples_per_wave], label='Sine')
# plt.plot(waveform[samples_per_wave:2*samples_per_wave], label='Triangle')
# plt.plot(waveform[2*samples_per_wave:3*samples_per_wave], label='Square')
# plt.plot(waveform[3*samples_per_wave:4*samples_per_wave], label='Heartbeat')
# plt.legend()
# plt.show()
