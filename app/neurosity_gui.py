import tkinter as tk
from tkinter import scrolledtext, messagebox
from neurosity_manager import NeurosityManager
from encryption_util import load_key, encrypt_message, decrypt_message
import json
import os

class NeurosityGUI:
    def __init__(self, root):
        self.root = root
        self.manager = NeurosityManager()
        self.create_widgets()
        self.fernet = load_key()
        self.credentials_file = "credentials.enc"
        self.load_credentials()

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

def run_gui():
    root = tk.Tk()
    root.title("Neurosity Data Collector")
    app = NeurosityGUI(root)
    root.mainloop()


if __name__ == '__main__':
    run_gui()
