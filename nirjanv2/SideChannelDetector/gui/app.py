import tkinter as tk
from tkinter import ttk, scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import time
import collections
import numpy as np

# Import our modules
# Assuming app.py is run from the root directory or paths are set correctly.
# In main.py we will ensure sys.path is correct.

class App:
    def __init__(self, root, collector, preprocessor, detector, logger):
        self.root = root
        self.root.title("Side-Channel Privacy Leak Detection System")
        self.root.geometry("1200x800")
        
        self.collector = collector
        self.preprocessor = preprocessor
        self.detector = detector
        self.logger = logger
        
        self.monitoring = False
        self.data_history = collections.deque(maxlen=100) # Keep last 100 points for graphing
        self.timestamps = collections.deque(maxlen=100)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Top Frame: Controls
        control_frame = ttk.LabelFrame(self.root, text="Control Panel", padding=10)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        self.btn_start = ttk.Button(control_frame, text="Start Monitoring", command=self.start_monitoring)
        self.btn_start.pack(side=tk.LEFT, padx=5)
        
        self.btn_stop = ttk.Button(control_frame, text="Stop Monitoring", command=self.stop_monitoring, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT, padx=5)
        
        self.btn_attack = ttk.Button(control_frame, text="Simulate Side-Channel Attack", command=self.toggle_attack)
        self.btn_attack.pack(side=tk.LEFT, padx=20)
        
        self.status_label = ttk.Label(control_frame, text="Status: IDLE", font=("Arial", 12, "bold"))
        self.status_label.pack(side=tk.RIGHT, padx=20)

        # Middle Frame: Graphs
        graph_frame = ttk.Frame(self.root)
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.fig = Figure(figsize=(10, 5), dpi=100)
        self.ax1 = self.fig.add_subplot(311)
        self.ax2 = self.fig.add_subplot(312)
        self.ax3 = self.fig.add_subplot(313)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Bottom Frame: Logs
        log_frame = ttk.LabelFrame(self.root, text="System Logs & Alerts", padding=10)
        log_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5, ipady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, state='disabled')
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def log_message(self, msg):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def toggle_attack(self):
        if self.collector.simulating_attack:
            self.collector.trigger_attack_simulation(False)
            self.btn_attack.config(text="Simulate Side-Channel Attack")
            self.log_message("INFO: Attack Simulation STOPPED.")
        else:
            self.collector.trigger_attack_simulation(True)
            self.btn_attack.config(text="STOP Attack Simulation")
            self.log_message("WARNING: Attack Simulation STARTED.")

    def start_monitoring(self):
        self.monitoring = True
        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        self.status_label.config(text="Status: CALIBRATING...", foreground="orange")
        self.log_message("System: Starting Automated Detection Pipeline...")
        self.log_message("System: Performing Statistical Baseline Analysis...")
        
        # Start background thread
        threading.Thread(target=self.monitoring_loop, daemon=True).start()

    def stop_monitoring(self):
        self.monitoring = False
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        self.status_label.config(text="Status: IDLE", foreground="black")
        self.log_message("System: Monitoring stopped. Forensic logs finalized in /data/logs/.")

    def monitoring_loop(self):
        # 1. Calibration Phase
        calibration_data = []
        for _ in range(60): # Collect samples for baseline
            if not self.monitoring: return
            data = self.collector.get_realtime_data()
            if data:
                calibration_data.append(data)
            time.sleep(0.1)
        
        self.preprocessor.fit(calibration_data)
        
        # Prepare data for training detector (Isolation Forest - ML)
        train_features = []
        for d in calibration_data:
            proc = self.preprocessor.process(d)
            train_features.append(proc[0])
        self.detector.train(np.array(train_features))
        
        self.root.after(0, lambda: self.status_label.config(text="Status: REAL-TIME ML ANALYSIS ACTIVE", foreground="green"))
        self.root.after(0, lambda: self.log_message("System: ML Model (Isolation Forest) & Statistical filters online."))

        # 2. Monitoring Phase
        while self.monitoring:
            data = self.collector.get_realtime_data()
            if data:
                # Store for plotting
                self.timestamps.append(datetime.fromtimestamp(data['timestamp']).strftime('%H:%M:%S'))
                self.data_history.append(data)
                
                # Analysis
                features = self.preprocessor.process(data)
                is_anomaly = self.detector.predict(features) # -1 is anomaly
                
                # UI Updates (must be on main thread)
                self.root.after(0, self.update_plots)
                
                if is_anomaly == -1:
                    score = self.detector.decision_function(features)
                    self.root.after(0, lambda: self.handle_alert(score))
                else:
                     self.root.after(0, lambda: self.status_label.config(text="Status: MONITORING ACTIVE", foreground="green"))

            time.sleep(0.5) # Sampling rate

    def handle_alert(self, score):
        self.status_label.config(text="ALERT: PRIVACY LEAK DETECTED!", foreground="red")
        msg = f"ANOMALY DETECTED! Score: {score:.4f} - Potential Side-Channel Leak"
        self.log_message(msg)
        self.logger.log_alert("SideChannelLeak", f"{score:.4f}", "Abnormal signal pattern detected")

    def update_plots(self):
        if not self.data_history:
            return
            
        power = [d['power_proxy'] for d in self.data_history]
        exec_time = [d['exec_time_proxy'] for d in self.data_history]
        memory = [d['memory_proxy'] for d in self.data_history]
        t = range(len(power))
        
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        
        self.ax1.plot(t, power, 'r-', label='Power (CPU %)')
        self.ax1.legend(loc='upper right')
        self.ax1.set_ylabel('Power')
        
        self.ax2.plot(t, exec_time, 'b-', label='Exec Time (CPU Times)')
        self.ax2.legend(loc='upper right')
        self.ax2.set_ylabel('Time')

        self.ax3.plot(t, memory, 'g-', label='Cache/Mem (RAM %)')
        self.ax3.legend(loc='upper right')
        self.ax3.set_ylabel('Memory')
        
        self.canvas.draw()

from datetime import datetime
