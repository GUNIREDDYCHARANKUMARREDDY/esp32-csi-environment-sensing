import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- Hampel Filter that Ignores Zeros ---
def hampel_filter_ignore_zeros_2d(data, window_size=5, n=3):
    filtered = data.copy()
    k = 1.4826  # Scale factor for Gaussian distribution

    for col in range(data.shape[1]):  # Loop over subcarriers (columns)
        series = data[:, col]

        for i in range(window_size, len(series) - window_size):
            window = series[i - window_size:i + window_size + 1]
            window_nonzero = window[window != 0]

            if len(window_nonzero) < 3:
                continue

            median = np.median(window_nonzero)
            mad = k * np.median(np.abs(window_nonzero - median))

            if series[i] != 0 and np.abs(series[i] - median) > n * mad:
                filtered[i, col] = median

    return filtered

# Load the CSV file
df = pd.read_csv("csi_data4.csv")

# Extract timestamps and amplitude matrix
timestamps = df.iloc[:, 0].values  # Time
amplitudes = df.iloc[:, 1:].values  # Subcarrier amplitudes

# Normalize time
timestamps = (timestamps - timestamps.min()) / 1e3  # optional: convert µs to seconds

# Apply Hampel filter (row-wise: time over each subcarrier)
amplitudes_filtered = hampel_filter_ignore_zeros_2d(amplitudes, window_size=5, n=3)

# Prepare meshgrid for 3D plot
time_grid, sc_grid = np.meshgrid(timestamps, np.arange(amplitudes.shape[1]))
amp_grid = amplitudes_filtered.T  # Shape: (subcarriers, time)

# Create 3D surface plot
fig = plt.figure(figsize=(16, 8))
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(time_grid, sc_grid, amp_grid, cmap='viridis')

ax.set_xlabel("Time (s)")
ax.set_ylabel("Subcarrier Index")
ax.set_zlabel("Amplitude")
ax.set_title("3D Plot: CSI Amplitude vs Time vs Subcarrier (Filtered)")

fig.colorbar(surf, shrink=0.5, aspect=10, label='Amplitude')
plt.tight_layout()
plt.show()
