import os
import hashlib
import shutil
from datetime import datetime

MALWARE_DB = "malware_db.txt"
QUARANTINE_FOLDER = "quarantine"
LOG_FOLDER = "logs"
LOG_FILE = os.path.join(LOG_FOLDER, "scan_log.txt")

os.makedirs(QUARANTINE_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"

    with open(LOG_FILE, "a") as f:
        f.write(log_message + "\n")

    print(log_message)


def generate_hash(file_path):
    hasher = hashlib.sha256()

    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                hasher.update(chunk)
        return hasher.hexdigest()

    except Exception as e:
        log(f"[ERROR] Cannot read file {file_path}: {e}")
        return None


def load_malware_db():
    db = {}

    if not os.path.exists(MALWARE_DB):
        log("[WARNING] Malware database not found!")
        return db

    with open(MALWARE_DB, "r") as f:
        for line in f:
            if not line.strip():
                continue

            parts = line.strip().split("|")

            if len(parts) == 3:
                hash_value = parts[0].strip()
                name = parts[1].strip()
                severity = parts[2].strip()
                db[hash_value] = (name, severity)

    return db


def quarantine_file(file_path):
    try:
        filename = os.path.basename(file_path)
        destination = os.path.join(QUARANTINE_FOLDER, filename)

        shutil.move(file_path, destination)
        log(f"[QUARANTINED] {filename}")

    except Exception as e:
        log(f"[ERROR] Could not move {file_path}: {e}")


def scan_folder(folder_path, ui_callback=None):
    malware_hashes = load_malware_db()

    total_files = 0
    infected_files = 0

    def output(msg):
        if ui_callback:
            ui_callback(msg)
        else:
            print(msg)

    output(f"--- Scanning: {folder_path} ---")

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            total_files += 1

            file_hash = generate_hash(file_path)
            if file_hash is None:
                continue

            if file_hash in malware_hashes:
                name, severity = malware_hashes[file_hash]
                output(f"[THREAT] {file} | Name: {name} | Severity: {severity}")
                quarantine_file(file_path)
                infected_files += 1
            else:
                output(f"[SAFE] {file}")

    output("--- Scan Completed ---")
    return total_files, infected_files



if __name__ == "__main__":
    import tkinter as tk
    from gui import AntivirusUI

    root = tk.Tk()
    app = AntivirusUI(root)
    root.mainloop()