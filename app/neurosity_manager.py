from neurosity import NeurositySDK
from dotenv import load_dotenv
import numpy as np
import os
import csv
import datetime
from pynput import keyboard
from encryption_util import load_key, encrypt_message, decrypt_message
import json

load_dotenv()


class NeurosityManager:
    def __init__(self, gui):
        self.neurosity = NeurositySDK({
            "device_id": os.getenv("NEUROSITY_DEVICE_ID")
        })
        self.brain_data_csv_file = "../data/brain_data.csv"
        self.key_stroke_log_csv_file = '../data/keystrokes_log.csv'
        self.gui = gui
        self.data_buffer = []
        self.buffer_size = 10  # Buffer size, adjust as needed
        self.time_step_ms = 3.90625  # Example value for 256 Hz, adjust based on your device's frequency
        self.time_step_micros = int(self.time_step_ms * 1000)  # Convert time step to microseconds

    def login(self, email, password):
        self.neurosity.login({
            "email": email,
            "password": password
        })

    def get_info(self):
        return self.neurosity.get_info()

    def brainwaves_callback(self, data):
        if data is None:
            print("Received data is None")
            return
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        with open(self.brain_data_csv_file, 'a') as file:
            writer = csv.writer(file)
            writer.writerow([data, timestamp])

        current_time = datetime.datetime.now()
        num_points = len(data['data'][0])  # Assuming data['data'] is a list of lists

        # Generate timestamps in microseconds
        timestamps = [current_time + datetime.timedelta(microseconds=i * self.time_step_micros) for i in
                      range(num_points)]

        self.data_buffer.append((timestamps, data['data']))

        if len(self.data_buffer) >= self.buffer_size:
            # Process buffer data
            avg_timestamps = []
            avg_data = [[] for _ in range(len(self.data_buffer[0][1]))]

            for timestamps, data_points in self.data_buffer:
                avg_timestamps.extend(timestamps)
                for i, channel_data in enumerate(data_points):
                    avg_data[i].extend(channel_data)

            self.gui.root.after(0, self.gui.update_plot, avg_timestamps, avg_data)
            self.data_buffer = []

    def update_plot(self, eeg_data):
        # Assuming eeg_data is a list of lists of EEG values
        # Clear the previous plot
        self.gui.ax.clear()

        # Plot each channel's data
        for channel_data in eeg_data:
            self.gui.ax.plot(channel_data)

        self.gui.canvas.draw()

    def start_brainwaves_collection(self):
        self.unsubscribe = self.neurosity.brainwaves_raw(self.brainwaves_callback)

    def stop_brainwaves_collection(self):
        self.unsubscribe()

    def on_press(self, key):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        with open(self.key_stroke_log_csv_file, 'a') as file:
            writer = csv.writer(file)
            writer.writerow([key, timestamp])

    def start_key_logging(self):
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def stop_key_logging(self):
        self.listener.stop()
