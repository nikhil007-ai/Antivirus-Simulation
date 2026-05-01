<<<<<<< HEAD
# Antivirus Simulation

## Project Overview

Antivirus Simulation is a Python-based cybersecurity project that demonstrates how signature-based antivirus systems work.
The program scans files, generates SHA-256 hashes, compares them against a malware signature database, and quarantines detected threats.



## bjectives

* Understand signature-based malware detection
* Learn file hashing using SHA-256
* Implement file scanning and quarantine logic
* Build a simple antivirus simulation tool

---

## Features

* Folder scanning (recursive)
* SHA-256 file hashing
* Malware detection using signature database
* Automatic quarantine system
* GUI dashboard (Tkinter)
* Color-coded results (Safe / Malware)
* Scan statistics (files + threats)
* Export scan report (TXT)



## How It Works

1. Select a folder to scan
2. Each file is hashed using SHA-256
3. Hash is compared with malware database
4. If matched → file is marked as malicious
5. Malicious file is moved to quarantine
6. Results are displayed in GUI and can be exported



## Project Structure


AntiVirus_simulation/
├── scanner.py
├── gui.py
├── main.py
├── malware_db.txt
├── test_files/
├── quarantine/
├── logs/
└── README.md




## ▶How to Run

### Option 1: Run using Python

bash
python main.py




## Requirements

* Python 3.10+
* Tkinter (comes with Python)

### Install Tkinter (Linux only)

bash
sudo apt install python3-tk


## No external Python libraries required



## Limitations

* Detects only known malware (signature-based)
* Cannot detect zero-day or unknown threats
* Not a real antivirus system (educational purpose only)



## Author

**Nikhil Verma**
Cybersecurity Intern



## Note

This project is developed for educational purposes to demonstrate core antivirus concepts used in cybersecurity.
=======
# AntiVirus-Simulation
Antivirus Simulation is a Python-based cybersecurity project that demonstrates how signature-based antivirus systems work. The program scans files, generates SHA-256 hashes, compares them against a malware signature database, and quarantines detected threats.
>>>>>>> e523117d53722b10c8b9f9da848822377ea335d0
