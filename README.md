# Keylogger Project

A Python-based keylogger that records keystrokes, logs geolocation information, and sends log files via email at configurable intervals.  
**Disclaimer**: This project is intended for educational purposes only. Unauthorized or malicious use is strictly prohibited.

---

## Features

- Records all keystrokes.
- Captures system geolocation (IP, city, region, country).
- Sends log files via email at user-defined intervals.
- Provides a GUI for easy configuration of email and settings.

---

## Requirements

Install the required libraries by running:
```bash
pip install -r requirements.txt
```

Dependencies:
- `pynput`
- `python-dotenv`
- `requests`
- `tkinter` (built-in with Python)

---

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd keylogger
```

### 2. Set Up Environment Variables
Create a `.env` file in the root directory with:
```plaintext
EMAIL_ADDRESS=<your_email>
EMAIL_PASSWORD=<your_email_password>
DEFAULT_RECIPIENT_EMAIL=<recipient_email>
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
FILE_PATH=project file path
LOG_FILE=key_log.txt
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Project
```bash
python keylog.py
```

---

## Usage

1. Run the script:
```bash
python keylog.py
```

2. A GUI will prompt you to configure:
   - **Recipient Email**: Email address to receive log files.
   - **Log Time Interval**: Time in seconds between logs.
   - **Number of Logs**: Total number of logs to generate before stopping.

3. The program will:
   - Record keystrokes.
   - Fetch and log geolocation data.
   - Email log files at the specified intervals.

---

## File Structure

```plaintext
keylogger/
├── keylog.py          # Main script
├── .env               # Environment variables
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

---

## Important Notes

- This tool is for **educational purposes only**.
- Use a dedicated or disposable email account for testing.
- Be aware of privacy and security laws in your region.
- Avoid using personal or sensitive credentials in the `.env` file.

---
