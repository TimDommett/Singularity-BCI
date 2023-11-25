from neurosity import NeurositySDK
from dotenv import load_dotenv
import os
import csv
import datetime
from pynput import keyboard
from encryption_util import load_key, encrypt_message, decrypt_message
import json

load_dotenv()

class NeurosityManager:
    def __init__(self):
        self.neurosity = NeurositySDK({
            "device_id": os.getenv("NEUROSITY_DEVICE_ID")
        })
        self.brain_data_csv_file = "../data/brain_data.csv"
        self.key_stroke_log_csv_file = '../data/keystrokes_log.csv'

    def login(self, email, password):
        self.neurosity.login({
            "email": email,
            "password": password
        })

    def get_info(self):
        return self.neurosity.get_info()

    def brainwaves_callback(self, data):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        with open(self.brain_data_csv_file, 'a') as file:
            writer = csv.writer(file)
            writer.writerow([data, timestamp])

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
