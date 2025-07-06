import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- Hampel Filter that Ignores Zeros ---
def hampel_filter_ignore_zeros(df, window_size=5, n=3):
    filtered_df = df.copy()
    k = 1.4826  # scale factor for Gaussian distribution

    for col in df.columns:
        series = df[col]
        new_series = series.copy()

        for i in range(window_size, len(series) - window_size):
            window = series[i - window_size:i + window_size + 1]
            window_nonzero = window[window != 0]

            if len(window_nonzero) < 3:
                continue  # not enough valid points to filter

            median = window_nonzero.median()
            mad = k * np.median(np.abs(window_nonzero - median))

            # Ignore filtering if the current value is zero (assume invalid)
            if series.iloc[i] == 0:
                continue

            # Apply Hampel filtering only to non-zero values
            if np.abs(series.iloc[i] - median) > n * mad:
                new_series.iloc[i] = median

        filtered_df[col] = new_series

    return filtered_df

# Load the CSI CSV file
df = pd.read_csv("csi_data3.csv")

# Extract timestamps and amplitudes
timestamps = df.iloc[:, 0]
amplitudes = df.iloc[:, 1:]

# Normalize timestamps (optional)
time_relative = (timestamps - timestamps.min()) / 1e3  # convert µs to seconds

# Apply Hampel filter (ignoring zeros)
filtered_amplitudes = hampel_filter_ignore_zeros(amplitudes, window_size=5, n=3)

# Create heatmap data
heatmap_data = pd.DataFrame(
    filtered_amplitudes.values,
    index=time_relative,
    columns=[f'SC_{i}' for i in range(filtered_amplitudes.shape[1])]
)

# Plot heatmap
plt.figure(figsize=(14, 6))
sns.heatmap(heatmap_data.T, cmap='viridis', cbar_kws={'label': 'Amplitude (Filtered)'})
plt.xlabel("Time (s)")
plt.ylabel("Subcarrier Index")
plt.title("CSI Amplitude vs Time Heatmap (Hampel Filtered, Ignoring Zeros)")
plt.tight_layout()
plt.show()
