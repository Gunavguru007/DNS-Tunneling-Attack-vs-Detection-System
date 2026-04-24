import os
import tkinter as tk
from tkinter import scrolledtext
from attack import DNSTunnelAttacker
from defense import DNSDefender

os.makedirs("logs", exist_ok=True)

class CyberRangeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DNS Tunneling Cyber Range")
        self.root.geometry("600x500")
        
        self.attacker = DNSTunnelAttacker()
        self.defender = DNSDefender()

        input_frame = tk.Frame(root)
        input_frame.pack(pady=10, padx=10, fill="x")
        
        tk.Label(input_frame, text="Secret Data to Exfiltrate:").pack(side="left")
        self.entry_data = tk.Entry(input_frame, width=40)
        self.entry_data.insert(0, "Confidential_API_KEY_987654321")
        self.entry_data.pack(side="left", padx=10)
        
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        
        tk.Button(btn_frame, text="Send Normal Traffic", command=self.simulate_normal).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Launch Attack", bg="#ffcccc", command=self.simulate_attack).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Clear Console", command=self.clear_console).pack(side="left", padx=5)

        tk.Label(root, text="Defense System Logs:").pack(anchor="w", padx=10)
        self.console = scrolledtext.ScrolledText(root, height=20, width=70, state="disabled")
        self.console.pack(padx=10, pady=5)

    def log_to_gui(self, message: str, status: str):
        self.console.config(state="normal")
        self.console.insert(tk.END, message + "\n", status)
        self.console.tag_config("BLOCKED", foreground="red")
        self.console.tag_config("ALLOWED", foreground="green")
        self.console.see(tk.END)
        self.console.config(state="disabled")

    def process_queries(self, queries: list):
        for query in queries:
            result = self.defender.analyze_query(query)
            log_msg = f"[{result['status']}] {result['query']} (Entropy: {result['entropy']:.2f})"
            self.log_to_gui(log_msg, result['status'])

    def simulate_normal(self):
        queries = self.attacker.generate_normal_queries()
        self.log_to_gui("--- Simulating Normal Traffic ---", "ALLOWED")
        self.process_queries(queries)

    def simulate_attack(self):
        secret = self.entry_data.get()
        if not secret:
            return
        queries = self.attacker.generate_exfiltration_queries(secret)
        self.log_to_gui("--- Launching DNS Exfiltration ---", "BLOCKED")
        self.process_queries(queries)

    def clear_console(self):
        self.console.config(state="normal")
        self.console.delete(1.0, tk.END)
        self.console.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = CyberRangeGUI(root)
    root.mainloop()
