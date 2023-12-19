from neurosity import NeurositySDK
from dotenv import load_dotenv
import numpy as np
import os
import csv
import datetime
from pynput import keyboard
from encryption_util import load_key, encrypt_message, decrypt_message
import json
import pygame
import threading
import time

load_dotenv()


class NeurosityManager:
    def __init__(self, gui):
        self.neurosity = NeurositySDK({
            "device_id": os.getenv("NEUROSITY_DEVICE_ID")
        })
        self.brain_data_csv_file = "../data/brain_data.csv"
        self.key_stroke_log_csv_file = '../data/keystrokes_log.csv'
        self.button_log_csv_file = '../data/button_log.csv'
        self.joystick_log_csv_file = '../data/joystick_log.csv'
        self.trigger_log_csv_file = '../data/trigger_log.csv'
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

        # Ensure the directory exists
        directory = os.path.dirname(self.brain_data_csv_file)
        if not os.path.exists(directory):
            os.makedirs(directory)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        # Open the file in append mode
        with open(self.brain_data_csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([data, timestamp])
            print("Wrote line to brain_data.csv")

        # current_time = datetime.datetime.now()
        # num_points = len(data['data'][0])  # Assuming data['data'] is a list of lists
        #
        # Generate timestamps in microseconds
        # timestamps = [current_time + datetime.timedelta(microseconds=i * self.time_step_micros) for i in
        #               range(num_points)]
        #
        # self.data_buffer.append((timestamps, data['data']))
        #
        # if len(self.data_buffer) >= self.buffer_size:
        #     # Process buffer data
        #     avg_timestamps = []
        #     avg_data = [[] for _ in range(len(self.data_buffer[0][1]))]
        #
        #     for timestamps, data_points in self.data_buffer:
        #         avg_timestamps.extend(timestamps)
        #         for i, channel_data in enumerate(data_points):
        #             avg_data[i].extend(channel_data)
        #
        #     self.gui.root.after(0, self.gui.update_plot, avg_timestamps, avg_data)
        #     self.data_buffer = []

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
        self.start_key_logging()
        self.start_controller_logging()

    def stop_brainwaves_collection(self):
        if self.unsubscribe:
            self.unsubscribe()
        self.stop_key_logging()
        self.stop_controller_logging()

    def start_controller_logging(self):
        self.initialize_controller()
        self.controller_logging_running = True
        self.controller_thread = threading.Thread(target=self.controller_logging_loop)
        self.controller_thread.start()

    def stop_controller_logging(self):
        self.controller_logging_running = False
        if self.controller_thread and self.controller_thread.is_alive():
            self.controller_thread.join()
        pygame.quit()

    def controller_logging_loop(self):
        while self.controller_logging_running:
            self.record_controller_input()
            time.sleep(0.01)  # Adjust the sleep time as needed for responsiveness

    def record_controller_input(self):
        pygame.event.pump()  # Process event queue
        for event in pygame.event.get():
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            # if event.type == pygame.JOYAXISMOTION:
            #     # Log joystick movements
            #     with open(self.joystick_log_csv_file, 'a', newline='') as file:
            #         writer = csv.writer(file)
            #         writer.writerow([event.axis, event.value, timestamp])
            if event.type == pygame.JOYAXISMOTION:
                # Check if the axis event is from the triggers
                if event.axis == 4:  # Assuming axis 2 is for L2
                    trigger_label = 'L2'
                    # print("L2 Trigger Value:", event.value)
                    with open(self.trigger_log_csv_file, 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([trigger_label, event.value, timestamp])
                elif event.axis == 5:  # Assuming axis 5 is for R2
                    trigger_label = 'R2'
                    # print("R2 Trigger Value:", event.value)
                    with open(self.trigger_log_csv_file, 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([trigger_label, event.value, timestamp])
                else:
                    # print("Joystick Code:", event.axis, "Value:", event.value)
                    # Log other joystick movements
                    with open(self.joystick_log_csv_file, 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([event.axis, event.value, timestamp])

            elif event.type in [pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP]:
                print("Button Code:", event.button)
                # Log button presses
                button_label = self.get_button_label(event.button)
                if event.type == pygame.JOYBUTTONDOWN:
                    event_label = "Pressed"
                elif event.type == pygame.JOYBUTTONUP:
                    event_label = "Released"
                else:
                    event_label = "Unknown"
                with open(self.button_log_csv_file, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([button_label, event.type, event_label, timestamp])

    def get_button_label(self, button_code):
        # Map the button codes to their respective labels
        button_labels = {
            0: "X",
            1: "Circle",
            2: "Square",
            3: "Triangle",
            4: "Left Options Button",
            5: "PlayStation Button",
            6: "Right Options Button",
            7: "L3",
            8: "R3",
            9: "L1",
            10: "R1",
            11: "UpArrow",
            12: "DownArrow",
            13: "LeftArrow",
            14: "RightArrow",
            15: "Middle Button",
        }
        return button_labels.get(button_code, f"Unknown({button_code})")


    def on_press(self, key):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        with open(self.key_stroke_log_csv_file, 'a') as file:
            writer = csv.writer(file)
            writer.writerow([key, timestamp])

    # Keystroke recording

    def start_key_logging(self):
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def stop_key_logging(self):
        self.listener.stop()

# Game controller recording
    def initialize_controller(self):
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            self.controller_log_csv_file = '../data/controller_log.csv'
        else:
            print("No PS5 DualSense controller found. Please connect the controller.")
