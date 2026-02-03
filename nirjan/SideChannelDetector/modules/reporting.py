import logging
import os
from datetime import datetime
import csv

class ForensicLogger:
    def __init__(self, log_dir="data/logs"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Setup General Logger
        self.logger = logging.getLogger("SideChannelDetector")
        self.logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        file_handler = logging.FileHandler(os.path.join(self.log_dir, "system.log"))
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # CSV Alert Log
        self.alert_csv = os.path.join(self.log_dir, "alerts.csv")
        if not os.path.exists(self.alert_csv):
            with open(self.alert_csv, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Type", "Confidence", "Details"])

    def log_system_event(self, message):
        self.logger.info(message)

    def log_alert(self, alert_type, confidence, details):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Log to text file
        self.logger.warning(f"ALERT: {alert_type} (Conf: {confidence}) - {details}")
        
        # Log to CSV for reporting
        with open(self.alert_csv, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, alert_type, confidence, details])
