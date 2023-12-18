import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np  # Make sure to import numpy
from tkinter import scrolledtext, ttk
from neurosity_manager import NeurosityManager
from encryption_util import load_key, encrypt_message, decrypt_message
import json
import os
import mne


class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        # Set background color
        self.scrollable_frame.configure(bg='#2b2b2b')


class NeurosityGUI:
    def __init__(self, root):
        self.figure = None
        self.canvas = None
        self.ax = None
        self.lines = None
        self.device_id_entry = None
        self.email_entry = None
        self.password_entry = None
        self.root = root
        self.manager = NeurosityManager(self)
        # Define colors
        self.bg_color = '#2b2b2b'
        self.fg_color = '#a9b7c6'
        self.entry_bg_color = '#3c3f41'
        self.entry_fg_color = '#a9b7c6'
        self.button_bg_color = '#3c3f41'
        self.button_fg_color = '#a9b7c6'
        self.topomap_canvas = None  # Initialize the attribute
        # Create a Scrollable Frame
        self.scrollable_frame = ScrollableFrame(root)
        self.scrollable_frame.pack(fill='both', expand=True)
        self.scrollable_frame.scrollable_frame.columnconfigure(0, weight=1)  # Make the column expandable
        self.scrollable_frame.scrollable_frame.rowconfigure(0, weight=1)  # Make the row expandable

        # Configure ttk style for entry and button widgets
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TEntry', background=self.entry_bg_color, foreground=self.entry_fg_color,
                        fieldbackground=self.entry_bg_color, borderwidth=0)
        style.configure('TButton', background=self.button_bg_color, foreground=self.button_fg_color, borderwidth=2,
                        relief='raised')
        self.create_widgets()
        self.fernet = load_key()
        self.credentials_file = "credentials.enc"
        self.load_credentials()
        # Create the plot
        # self.create_plot()
        # Color scheme variables
        self.is_collecting = False  # State variable to track collection state
        self.toggle_collection_button = ttk.Button(self.root, text="Start Collection", command=self.toggle_collection)
        self.toggle_collection_button.pack(pady=5)

    def toggle_collection(self):
        if self.is_collecting:
            self.stop_collection()
            self.toggle_collection_button.config(text="Start Collection")
            self.is_collecting = False
        else:
            self.start_collection()
            self.toggle_collection_button.config(text="Stop Collection")
            self.is_collecting = True

    def load_credentials(self):
        if os.path.exists(self.credentials_file):
            with open(self.credentials_file, 'rb') as file:
                encrypted_data = file.read()
                decrypted_data = decrypt_message(encrypted_data, self.fernet)
                credentials = json.loads(decrypted_data)
                self.device_id_entry.insert(0, credentials.get("device_id", ""))
                self.email_entry.insert(0, credentials.get("email", ""))
                self.password_entry.insert(0, credentials.get("password", ""))
                # Automatically log in if credentials are loaded
                self.login(credentials.get("device_id", ""), credentials.get("email", ""),
                           credentials.get("password", ""))

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
        main_frame = tk.Frame(self.scrollable_frame.scrollable_frame, bg=self.bg_color)
        main_frame.grid(sticky='nsew')  # Make the main_frame expandable
        main_frame.columnconfigure(0, weight=1)  # Center the frame
        main_frame.columnconfigure(2, weight=1)  # Center the frame

        login_frame = tk.Frame(main_frame, bg=self.bg_color)
        login_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)  # Centered in the main frame
        login_frame.columnconfigure(1, weight=1)  # Make the second column of login_frame expandable

        # Device ID Label and Entry
        tk.Label(login_frame, text="Device ID:", bg=self.bg_color, fg=self.fg_color).grid(row=0, column=0, sticky='e')
        self.device_id_entry = ttk.Entry(login_frame)
        self.device_id_entry.grid(row=0, column=1, sticky='nsew', padx=5)

        # Email Label and Entry
        tk.Label(login_frame, text="Email:", bg=self.bg_color, fg=self.fg_color).grid(row=1, column=0, sticky='e')
        self.email_entry = ttk.Entry(login_frame)
        self.email_entry.grid(row=1, column=1, sticky='nsew', padx=5)

        # Password Label and Entry
        tk.Label(login_frame, text="Password:", bg=self.bg_color, fg=self.fg_color).grid(row=2, column=0, sticky='e')
        self.password_entry = ttk.Entry(login_frame, show="*")
        self.password_entry.grid(row=2, column=1, sticky='nsew', padx=5)

        # Login Button
        login_button = ttk.Button(login_frame, text="Login", command=self.login)
        login_button.grid(row=3, column=0, columnspan=2, pady=10)

    # def create_plot(self):
    #     plot_frame = tk.Frame(self.scrollable_frame.scrollable_frame, bg=self.bg_color)
    #     plot_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
    #     plot_frame.columnconfigure(0, weight=1)  # Make the plot frame expandable
    #     plot_frame.rowconfigure(0, weight=1)
    #
    #     # Change to 2x4 grid
    #     self.fig, self.axes = plt.subplots(2, 4, figsize=(20, 10))  # Adjust the figsize as needed
    #     self.fig.subplots_adjust(hspace=0.5, wspace=0.5)
    #
    #     self.fig.patch.set_facecolor(self.bg_color)
    #     for ax in self.axes.flatten()[:8]:  # Iterate through the first 8 axes
    #         ax.set_facecolor(self.bg_color)
    #         ax.set_title('EEG Channel Data', color=self.fg_color)
    #         ax.set_xlabel('Time (s)', color=self.fg_color)
    #         ax.set_ylabel('Amplitude', color=self.fg_color)
    #         ax.tick_params(axis='x', colors=self.fg_color)
    #         ax.tick_params(axis='y', colors=self.fg_color)
    #         for spine in ax.spines.values():
    #             spine.set_color(self.fg_color)
    #
    #     self.canvas = FigureCanvasTkAgg(self.fig, plot_frame)
    #     self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
    #     self.topomap_canvas = None

    def login(self, device_id=None, email=None, password=None):
        # Use parameters if provided, else get from entry widgets
        device_id = device_id or self.device_id_entry.get()
        email = email or self.email_entry.get()
        password = password or self.password_entry.get()
        self.manager.login(email, password)
        # Save credentials even if manually entered
        self.save_credentials(device_id, email, password)
        print("Logged in")

    def start_collection(self):
        self.manager.start_brainwaves_collection()
        self.manager.start_key_logging()

    def stop_collection(self):
        self.manager.stop_brainwaves_collection()
        self.manager.stop_key_logging()

    # def update_plot(self, timestamps, eeg_data):
    #     # Assuming eeg_data is a list of arrays, with each array representing data from one channel
    #
    #     # Update line plots
    #     unix_timestamps = [timestamp.timestamp() for timestamp in timestamps]
    #
    #     for ax, channel_data, color in zip(self.axes, eeg_data, self.colors):
    #         if ax.lines:  # If there are existing lines in the plot
    #             line = ax.lines[0]
    #             x_data, y_data = line.get_data()
    #             x_data = np.append(x_data, unix_timestamps)
    #             y_data = np.append(y_data, channel_data)
    #         else:  # If no lines, initialize them
    #             x_data = unix_timestamps
    #             y_data = channel_data
    #             ax.plot(x_data, y_data, color=color)
    #
    #         if len(x_data) > 200:  # Limit to last 200 data points
    #             x_data = x_data[-200:]
    #             y_data = y_data[-200:]
    #
    #         ax.set_xlim([min(x_data), max(x_data)])
    #         ax.set_ylim([min(y_data), max(y_data)])
    #         if ax.lines:
    #             ax.lines[0].set_data(x_data, y_data)
    #
    #     # Update scalp topography
    #     ch_names = ['CP3', 'C3', 'F5', 'PO3', 'PO4', 'F6', 'C4', 'CP4']
    #     ch_types = ['eeg'] * len(ch_names)
    #     sfreq = 256  # Replace with your actual sampling frequency
    #     montage = mne.channels.make_standard_montage('standard_1020')
    #
    #     info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)
    #     info.set_montage(montage)
    #
    #     raw = mne.io.RawArray(np.array(eeg_data), info)
    #
    #     # Define the time point for topomap
    #     time_point = raw.times[-1]
    #
    #     # Create topomap figure
    #     fig, ax = plt.subplots()
    #     mne.viz.plot_topomap(raw.copy().pick('eeg').get_data()[:, int(time_point * sfreq)], info, axes=ax, show=False)
    #
    #     # In the update_plot method
    #     if self.topomap_canvas is None:
    #         self.topomap_canvas = FigureCanvasTkAgg(fig, self.scrollable_frame.scrollable_frame)
    #         self.topomap_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    #     else:
    #         self.topomap_canvas.figure = fig
    #         self.topomap_canvas.draw()
    #
    #     self.canvas.draw()


def run_gui():
    root = tk.Tk()
    root.title("Singularity Brain Recorder")

    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set the window size as a percentage of screen size
    window_width = int(screen_width * 0.8)  # 80% of the screen width
    window_height = int(screen_height * 0.8)  # 80% of the screen height

    # Calculate position to center the window on the screen
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    # Set the dimensions and position
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')

    app = NeurosityGUI(root)
    root.mainloop()


if __name__ == '__main__':
    run_gui()
