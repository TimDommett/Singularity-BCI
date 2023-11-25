import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np  # Make sure to import numpy
from tkinter import scrolledtext, messagebox
from neurosity_manager import NeurosityManager
from encryption_util import load_key, encrypt_message, decrypt_message
import json
import os


class NeurosityGUI:
    def __init__(self, root):
        self.figure = None
        self.canvas = None
        self.ax = None
        self.lines = None
        self.log_area = None
        self.log_area_scroll = None
        self.device_id_entry = None
        self.email_entry = None
        self.password_entry = None
        self.root = root
        self.manager = NeurosityManager(self)
        self.create_widgets()
        self.fernet = load_key()
        self.credentials_file = "credentials.enc"
        self.load_credentials()
        # Create the plot
        self.create_plot()

    def load_credentials(self):
        if os.path.exists(self.credentials_file):
            with open(self.credentials_file, 'rb') as file:
                encrypted_data = file.read()
                decrypted_data = decrypt_message(encrypted_data, self.fernet)
                credentials = json.loads(decrypted_data)
                self.device_id_entry.insert(0, credentials.get("device_id", ""))
                self.email_entry.insert(0, credentials.get("email", ""))
                self.password_entry.insert(0, credentials.get("password", ""))

    def save_credentials(self, device_id, email, password):
        credentials = {
            "device_id": device_id,
            "email": email,
            "password": password
        }
        encrypted_data = encrypt_message(json.dumps(credentials), self.fernet)
        with open(self.credentials_file, 'wb') as file:
            file.write(encrypted_data)

    def create_widgets(self):
        # Login frame
        login_frame = tk.Frame(self.root)
        login_frame.pack(padx=10, pady=10)

        # Device ID, Email, and Password labels and entries
        tk.Label(login_frame, text="Device ID:").grid(row=0, column=0)
        self.device_id_entry = tk.Entry(login_frame)
        self.device_id_entry.grid(row=0, column=1)

        tk.Label(login_frame, text="Email:").grid(row=1, column=0)
        self.email_entry = tk.Entry(login_frame)
        self.email_entry.grid(row=1, column=1)

        tk.Label(login_frame, text="Password:").grid(row=2, column=0)
        self.password_entry = tk.Entry(login_frame, show="*")
        self.password_entry.grid(row=2, column=1)

        # Login button
        login_button = tk.Button(login_frame, text="Login", command=self.login)
        login_button.grid(row=3, columnspan=2)

        # Start and Stop collection buttons
        start_button = tk.Button(self.root, text="Start Collection", command=self.start_collection)
        start_button.pack(pady=10)

        stop_button = tk.Button(self.root, text="Stop Collection", command=self.stop_collection)
        stop_button.pack(pady=10)

        # Log area
        self.log_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=10)
        self.log_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def login(self):
        # Assuming device_id is not required for login but to initialize NeurositySDK
        device_id = self.device_id_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        self.manager.login(email, password)
        info = self.manager.get_info()
        self.log_area.insert(tk.END, f"Info: {info}\n")
        self.save_credentials(self.device_id_entry.get(), self.email_entry.get(), self.password_entry.get())

    def start_collection(self):
        self.log_area.insert(tk.END, "Starting data collection...\n")
        self.manager.start_brainwaves_collection()
        self.manager.start_key_logging()
        self.log_area.insert(tk.END, "Data collection started.\n")

    def stop_collection(self):
        self.log_area.insert(tk.END, "Stopping data collection...\n")
        self.manager.stop_brainwaves_collection()
        self.manager.stop_key_logging()
        self.log_area.insert(tk.END, "Data collection stopped.\n")

    def create_plot(self):
        self.fig, self.axes = plt.subplots(8, 1, figsize=(6, 10))  # 8 subplots for 8 channels
        self.fig.subplots_adjust(hspace=0.5)  # Adjust the space between plots
        self.colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange']  # Different colors for each line
        for ax, color in zip(self.axes, self.colors):
            ax.set_title('EEG Channel Data')
            ax.set_prop_cycle('color', [color])
            ax.set_xlabel('Time (s)')  # Set x-axis label
            ax.set_ylabel('Amplitude')  # Set y-axis label
        self.canvas = FigureCanvasTkAgg(self.fig, self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_plot(self, timestamps, eeg_data):
        # Convert datetime objects to UNIX timestamps
        unix_timestamps = [timestamp.timestamp() for timestamp in timestamps]

        for ax, channel_data, color in zip(self.axes, eeg_data, self.colors):
            if ax.lines:  # If there are existing lines in the plot
                line = ax.lines[0]
                x_data, y_data = line.get_data()
                x_data = np.append(x_data, unix_timestamps)
                y_data = np.append(y_data, channel_data)
            else:  # If no lines, initialize them
                x_data = unix_timestamps
                y_data = channel_data
                ax.plot(x_data, y_data, color=color)

            if len(x_data) > 200:  # Limit to last 200 data points
                x_data = x_data[-200:]
                y_data = y_data[-200:]

            ax.set_xlim([min(x_data), max(x_data)])
            ax.set_ylim([min(y_data), max(y_data)])
            if ax.lines:
                ax.lines[0].set_data(x_data, y_data)

        self.canvas.draw()


def run_gui():
    root = tk.Tk()
    root.title("Neurosity Data Collector")
    app = NeurosityGUI(root)
    root.mainloop()


if __name__ == '__main__':
    run_gui()
