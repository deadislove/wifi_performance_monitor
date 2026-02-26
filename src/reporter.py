import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import datetime

class NetworkReporter:
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_report(self, rssi_history, latency_history):
        """
        Transforms scanned network data into a visual trend chart.
        """
        if not rssi_history:
            print("❌ No data available to generate report.")
            return

        # 1. Data Cleaning: Replace timeouts (999ms) with None to create 
        # visual breaks in the chart instead of spikes.
        clean_latency = [l if l < 999 else None for l in latency_history]
        
        # 2. Create DataFrame for plotting
        df = pd.DataFrame({
            'Sample': range(len(rssi_history)),
            'RSSI': rssi_history,
            'Latency': clean_latency
        })

        # 3. Plotting Configuration
        fig, ax1 = plt.subplots(figsize=(12, 6))
        plt.title(f"eero Connectivity Analysis Report\nGenerated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Primary Axis: RSSI (Signal Strength)
        color_rssi = 'tab:blue'
        ax1.set_xlabel('Timeline (Samples)')
        ax1.set_ylabel('Signal Strength (RSSI dBm)', color=color_rssi)
        ax1.plot(df['Sample'], df['RSSI'], color=color_rssi, marker='o', label='RSSI (dBm)', linewidth=2)
        ax1.tick_params(axis='y', labelcolor=color_rssi)
        ax1.grid(True, which='both', linestyle='--', alpha=0.5)

        # Secondary Axis: Latency
        ax2 = ax1.twinx()
        color_lat = 'tab:red'
        ax2.set_ylabel('Latency (ms)', color=color_lat)
        ax2.plot(df['Sample'], df['Latency'], color=color_lat, marker='x', label='Latency (ms)', linestyle='-.')
        ax2.tick_params(axis='y', labelcolor=color_lat)

        # Combine legends from both axes
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

        # Save the report with a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.output_dir, f"stability_report_{timestamp}.png")
        plt.savefig(filename)
        plt.close()
        
        print(f"\n✅ [Reporter] Professional chart saved to: {filename}")
        return filename