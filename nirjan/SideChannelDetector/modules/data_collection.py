import time
import psutil
import numpy as np
import threading

class DataCollector:
    def __init__(self):
        self.running = False
        self.data_buffer = []
        self._lock = threading.Lock()
        self.simulating_attack = False

    def start_collection(self):
        self.running = True
        # In a real scenario, this might connect to a DAQ device or read /proc/stat
        pass

    def stop_collection(self):
        self.running = False

    def trigger_attack_simulation(self, state=True):
        self.simulating_attack = state

    def get_realtime_data(self):
        """
        Simulate collecting side-channel data.
        We use system metrics as proxies for:
        - Power Consumption (approximated by CPU Usage)
        - Execution Time (approximated by User/System CPU times)
        - Cache/Memory behavior (approximated by Memory Usage)
        """
        try:
            # CPU times as proxy for execution time variations
            cpu_times = psutil.cpu_times()
            user_time = cpu_times.user
            system_time = cpu_times.system
            
            # CPU Percent as proxy for Power Consumption
            cpu_percent = psutil.cpu_percent(interval=None)
            
            # Virtual Memory as proxy for Cache/Sensor load
            mem = psutil.virtual_memory()
            mem_percent = mem.percent
            
            # Inject subtle noise to simulate sensor noise
            noise = np.random.normal(0, 0.5)

            # Attack Simulation: Inject large spikes
            if self.simulating_attack:
                cpu_percent += np.random.uniform(50, 100) # Fake power spike
                mem_percent += np.random.uniform(20, 50)  # Fake memory leak
                noise += 10 # High noise
            
            return {
                'timestamp': time.time(),
                'power_proxy': cpu_percent + noise,
                'exec_time_proxy': user_time + system_time,
                'memory_proxy': mem_percent
            }
        except Exception as e:
            print(f"Error collecting data: {e}")
            return None
