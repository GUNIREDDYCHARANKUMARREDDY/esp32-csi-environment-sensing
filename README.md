**# esp32-csi-environment-sensing**
CSI-based environment sensing using two ESP32 devices with UDP transmission, Hampel filtering, and 3D/heatmap visualization.


This project demonstrates how to use two ESP32 devices to transmit and receive Wi-Fi signals, extract CSI (Channel State Information) data, and analyze the environment based on CSI amplitude values. It includes real-time UART logging, noise filtering using Hampel filters, and visualizations like heatmaps and 3D surface plots.

---

## 📡 Project Overview

- **Transmitter ESP32:** Sends Wi-Fi UDP packets continuously.
- **Receiver ESP32:** Captures CSI data triggered by incoming packets.
- **PC Logger:** Receives CSI data via UART and saves it to a `.csv` file.
- **Filtering & Analysis:** Applies Hampel filtering to reduce noise/outliers.
- **Visualization:** Generates Heatmaps and 3D plots to observe environmental effects.

---

## 🧪 Experimental Setup

| Scenario               | Description                              |
|------------------------|------------------------------------------|
| No Obstruction         | ESP32 devices face each other directly   |
| Human Obstruction      | A person stands between the devices      |

> Wi-Fi signals being sinusoidal in nature, any obstruction causes amplitude distortions due to multipath fading and absorption. These effects are visible in the plots.





