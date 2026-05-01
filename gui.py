import tkinter as tk
from tkinter import filedialog
import threading
import os
from datetime import datetime
from scanner import scan_folder


class AntivirusUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Antivirus Simulation")
        self.root.geometry("900x550")
        self.root.configure(bg="#0f172a")

        self.scan_results = []
        self.folder_path = os.path.abspath("test_files")

        # ---------------- HEADER ----------------
        tk.Label(root, text="🛡 Antivirus",
                 bg="#0f172a", fg="#22c55e",
                 font=("Arial", 20, "bold")).pack(pady=10)

        # ---------------- STATUS ----------------
        self.status = tk.Label(root, text="Status: Idle",
                               bg="#0f172a", fg="#facc15",
                               font=("Arial", 12))
        self.status.pack()

        # ---------------- BUTTON FRAME ----------------
        self.btn_frame = tk.Frame(root, bg="#0f172a")
        self.btn_frame.pack(pady=10)

        tk.Button(self.btn_frame, text="Select Folder",
                  command=self.select_folder,
                  bg="#1e293b", fg="white", width=15).grid(row=0, column=0, padx=10)

        tk.Button(self.btn_frame, text="Start Scan",
                  command=self.start_scan,
                  bg="#22c55e", fg="black", width=15).grid(row=0, column=1, padx=10)

        tk.Button(self.btn_frame, text="Export Report",
                  command=self.export_report,
                  bg="#3b82f6", fg="white", width=15).grid(row=0, column=2, padx=10)

        # ---------------- STATS ----------------
        stats_frame = tk.Frame(root, bg="#0f172a")
        stats_frame.pack(pady=10)

        self.total_label = tk.Label(stats_frame, text="Files: 0",
                                    bg="#0f172a", fg="white")
        self.total_label.grid(row=0, column=0, padx=20)

        self.threat_label = tk.Label(stats_frame, text="Threats: 0",
                                     bg="#0f172a", fg="#ef4444")
        self.threat_label.grid(row=0, column=1, padx=20)

        # ---------------- OUTPUT BOX ----------------
        self.output = tk.Text(root,
                              bg="#020617",
                              fg="#38bdf8",
                              insertbackground="white")
        self.output.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(self.output)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.output.yview)

        self.output.insert(tk.END, f"[AUTO] Default folder: {self.folder_path}\n")

        self.setup_tags()

    # ---------------- SELECT FOLDER ----------------
    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path = folder
            self.write_output(f"[INFO] Selected: {folder}")

    # ---------------- START SCAN ----------------
    def start_scan(self):
        if not self.folder_path:
            self.write_output("[ERROR] No folder selected", "error")
            return

        threading.Thread(target=self.run_scan).start()

    # ---------------- RUN SCAN ----------------
    def run_scan(self):
        self.status.config(text="Status: Scanning...", fg="#facc15")

        self.clear_output()
        self.scan_results.clear()

        total, threats = scan_folder(self.folder_path, self.handle_output)

        self.total_label.config(text=f"Files: {total}")
        self.threat_label.config(text=f"Threats: {threats}")

        self.status.config(text="Status: Completed", fg="#22c55e")

    # ---------------- HANDLE OUTPUT ----------------
    def handle_output(self, message):
        self.scan_results.append(message)

        if "[MALWARE]" in message:
            self.write_output(message, "malware")
        elif "[SAFE]" in message:
            self.write_output(message, "safe")
        else:
            self.write_output(message, "normal")

    # ---------------- WRITE OUTPUT ----------------
    def write_output(self, message, tag="normal"):
        self.output.insert(tk.END, message + "\n", tag)
        self.output.see(tk.END)

    # ---------------- CLEAR OUTPUT ----------------
    def clear_output(self):
        self.output.delete(1.0, tk.END)

    # ---------------- EXPORT REPORT ----------------
    def export_report(self):
        if not self.scan_results:
            self.write_output("[ERROR] No scan data to export", "error")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            title="Save Report"
        )

        if not file_path:
            return

        try:
            with open(file_path, "w") as f:
                f.write("Antivirus Scan Report\n")
                f.write("=" * 30 + "\n\n")

                f.write(f"{self.total_label.cget('text')}\n")
                f.write(f"{self.threat_label.cget('text')}\n\n")

                f.write("Details:\n")
                f.write("-" * 30 + "\n")

                for line in self.scan_results:
                    f.write(line + "\n")

                f.write("\nGenerated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            self.write_output("[INFO] Report saved successfully")

        except Exception as e:
            self.write_output(f"[ERROR] Failed to save report: {e}", "error")

    # ---------------- TAG COLORS ----------------
    def setup_tags(self):
        self.output.tag_config("safe", foreground="#22c55e")
        self.output.tag_config("malware", foreground="#ef4444")
        self.output.tag_config("error", foreground="orange")
        self.output.tag_config("normal", foreground="#38bdf8")