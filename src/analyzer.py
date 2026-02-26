import numpy as np

class NetworkAnalyzer:
    def __init__(self):
        self.rssi_history = []
        self.latency_history = []

    def add_record(self, rssi: int, latency: float):
        if rssi is not None:
            self.rssi_history.append(rssi)
        if latency is not None:
            self.latency_history.append(latency)

    def calculate_jitter(self) -> float:
        # Filter out timeout values (999.0) for jitter calculation
        valid_data = [l for l in self.latency_history if l < 999.0]
        
        if len(valid_data) < 2:
            return 0.0
        
        if np:
            diffs = np.abs(np.diff(valid_data))
            return float(np.mean(diffs))
        return 0.0
    
    def get_stability_report(self):
        # Handle the edge case where no data has been collected yet
        if not self.latency_history:
            return {
                "avg_latency_ms": 0,
                "jitter_ms": 0,
                "packet_loss_rate": "0%",
                "overall_status": "NO_DATA"
            }
            
        # Filter out 999.0 to isolate valid latency samples
        valid_latencies = [l for l in self.latency_history if l < 999.0]
        
        # Handle the case where all packets were lost (No Connection)
        if not valid_latencies:
            return {
                "avg_latency_ms": 0,
                "jitter_ms": 0,
                "packet_loss_rate": "100%",
                "overall_status": "FAIL (No Connection)"
            }

        # Calculate average latency based on valid samples
        avg_latency = sum(valid_latencies) / len(valid_latencies)
        
        # Calculate Jitter (average variance between consecutive valid samples)
        if len(valid_latencies) > 1 and np:
            diffs = np.abs(np.diff(valid_latencies))
            jitter = float(np.mean(diffs))
        else:
            jitter = 0.0
            
        # Calculate Packet Loss Rate
        loss_rate = (self.latency_history.count(999.0) / len(self.latency_history)) * 100
        
        # Define PASS/FAIL criteria (Thresholds: Loss < 1%, Jitter < 30ms, Latency < 100ms)
        status = "PASS" if (loss_rate < 1.0 and jitter < 30.0 and avg_latency < 100) else "FAIL"

        return {
            "avg_latency_ms": round(avg_latency, 2),
            "jitter_ms": round(jitter, 2),
            "packet_loss_rate": f"{round(loss_rate, 2)}%",
            "overall_status": status
        }
    
if __name__ == "__main__":
    # Test Analysis Logic
    analyzer = NetworkAnalyzer()
    # Mock latency data with some fluctuations
    test_data = [20.5, 22.1, 100.5, 19.8, 25.3] 
    for d in test_data:
        analyzer.add_record(-50, d)
    
    print("Stability Analysis Report:", analyzer.get_stability_report())