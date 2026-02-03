# SIDE-CHANNEL
SIDE-CHANNEL PRIVACY LEAK DETECTION SYSTEM
usage-----
A. Initializing Monitoring
   1. Click the "Start Monitoring" button.
   2. Calibration Phase (Automated): For the first 6-10 seconds, the status will show "CALIBRATING...". During this time, the system uses Machine
      Learning to learn your hardware's "normal" baseline behavior.
   3. Active State: Once calibration is finished, the status changes to "REAL-TIME ML ANALYSIS ACTIVE" (Green).

  B. Visualizing Signals
  The dashboard displays three real-time graphs representing indirect information sources:
   * Power Proxy: Displays fluctuations in CPU usage (simulating power consumption).
   * Exec Time: Displays variations in system execution timing.
   * Cache/Mem: Displays memory usage patterns.

  C. Testing Detection (Simulated Attack)
  To verify that the Machine Learning model is detecting leaks:
   1. Click "Simulate Side-Channel Attack".
   2. The system will inject anomalous statistical spikes into the data stream.
   3. The UI will immediately trigger a RED ALERT status: "PRIVACY LEAK DETECTED!".
   4. An alert entry will appear in the "System Logs" box at the bottom.

  5. Forensic Reports & Logs
  The system automatically generates forensic evidence for every detected anomaly. You can find these files in the project folder:

   * System Event Log: SideChannelDetector/data/logs/system.log (General activity tracking).
   * Forensic Alert Log: SideChannelDetector/data/logs/alerts.csv (Detailed spreadsheet containing timestamps, anomaly scores, and leak types for
     further analysis).

  6. Stopping the System
   1. Click "Stop Monitoring" to halt the data collection.
   2. Close the window to safely shut down all background analysis threads.
