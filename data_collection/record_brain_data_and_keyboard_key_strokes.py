from neurosity import NeurositySDK
from dotenv import load_dotenv
import os
import csv
import datetime
from pynput import keyboard

load_dotenv()

neurosity = NeurositySDK({
    "device_id": os.getenv("NEUROSITY_DEVICE_ID")
})

neurosity.login({
    "email": os.getenv("NEUROSITY_EMAIL"),
    "password": os.getenv("NEUROSITY_PASSWORD")
})

info = neurosity.get_info()
print(info)


def callback(data):
    print("data", data)
    brain_data_csv_file = "../data/brain_data.csv"
    # Save data to a csv file with a timestamp with milliseconds
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    # timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(brain_data_csv_file, mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([data, timestamp])


unsubscribe = neurosity.brainwaves_raw(callback)

key_stroke_log_csv_file = '../data/keystrokes_log.csv'


def on_press(key):
    # Log the pressed key and the current time with milliseconds
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    with open(key_stroke_log_csv_file, mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([key, timestamp])


# Create a listener for keyboard events
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

if __name__ == '__main__':
    # Run the listener in a non-blocking fashion:
    listener.start()
    # Break the listener by pressing Ctrl + C
