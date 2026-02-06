import tkinter as tk
from modules.data_collection import DataCollector
from modules.preprocessing import Preprocessor
from modules.detection import AnomalyDetector
from modules.reporting import ForensicLogger
from gui.app import App
import sys
import os

# Ensure modules are importable
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

def main():
    # Initialize Backend Modules
    collector = DataCollector()
    preprocessor = Preprocessor()
    detector = AnomalyDetector()
    logger = ForensicLogger()

    # Initialize GUI
    root = tk.Tk()
    app = App(root, collector, preprocessor, detector, logger)
    
    # Handle graceful exit
    def on_closing():
        collector.stop_collection()
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start App
    root.mainloop()

if __name__ == "__main__":
    main()
