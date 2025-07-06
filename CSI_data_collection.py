import serial
import csv
import time

ser = serial.Serial('COM3', 115200)

with open('csi_data4.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp'] + [f'CSI_{i+1}' for i in range(64)])

    while True:
        try:
            line = ser.readline().decode().strip()

            # Only lines that contain numeric CSV (exclude logs)
            if ',' not in line:
                continue

            amplitudes = line.split(',')

            # Check if all are float values
            try:
                float_values = [float(val.strip()) for val in amplitudes]
            except ValueError:
                continue  # Skip non-numeric lines

            timestamp = time.time()
            row = [timestamp] + float_values
            writer.writerow(row)
            print("Saved:", row)

        except Exception as e:
            print("Error:", e)
