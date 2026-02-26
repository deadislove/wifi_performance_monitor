# WiFi Performance Monitor

## 📌 Project Overview
This project is an automated diagnostic tool designed to evaluate Wi-Fi stability. It simulates the data collection workflow of a QA Engineer by monitoring Signal Strength (RSSI), Latency, and Jitter in real-time. It is built to help identify network performance bottlenecks, such as interference or node handoff issues.

*Technical Highlight*: This tool features a robust workaround for macOS (Sonoma/Sequoia) privacy restrictions (<redacted> SSID/RSSI info) by utilizing system_profiler and advanced Regex parsing, ensuring reliable data extraction without requiring root privileges.

## 📂 Project Structure

```
wifi-performance-monitor/
├── src/
│   ├── __init__.py
│   ├── scanner.py          # OS-specific command wrapper (handles macOS privacy)
│   ├── analyzer.py         # Analysis engine: Jitter, Mean, and Status logic
│   └── reporter.py         # Visualization module (Dual-axis charts)
├── tests/
│   └── test_analyzer.py    # Unit tests for analysis accuracy
├── data/                   # Directory for CSV logs and PNG reports
├── requirements.txt        # Dependencies (matplotlib, pandas, numpy, etc.)
├── run_monitor.py          # Main CLI entry point
└── README.md               # Documentation
```

## 🛠 Feature List

1. Core Monitoring

- Real-time RSSI Tracking: Monitors Wi-Fi signal strength (dBm) to detect physical layer degradation.
- Multi-node Latency Testing: Pings Gateway (eero) and external DNS (Google) simultaneously to isolate LAN vs. WAN issues.
- Packet Loss Statistics: Automatically tracks drops during the test duration.

2. QA Automation & Analysis

- Threshold-based Evaluation: Automatically classifies network health based on industry standards (e.g., RSSI > -60 dBm is Excellent).
- Jitter Analysis: Calculates the variance in latency, a critical metric for VoIP and streaming stability.
- Anomaly Detection: Captures and logs latency spikes (e.g., >3x the moving average).

3. Reporting & Visualization

- Performance Trends: Generates dual-axis line charts comparing RSSI and Latency over time using matplotlib.
- Data Persistence: Saves raw data in CSV format for regression testing and historical comparison.

## 🚀 Getting Started

### Build Development Environment

```
# Create virtual environment
python3 -m venv venv

# Activate virtual environment (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Library Dependencies

- numpy: For statistical calculations (Jitter/Mean).
- pandas: For data structuring.
- matplotlib: For visual reporting.
- pytest: For running unit tests.

### Run the Monitor

```
# Execute monitoring (Default: 5s interval, 60s duration)
python run_monitor.py --interval 5 --duration 60
```

## 🧪 Technical Challenges & Solutions

1. macOS Privacy Workaround (<redacted> Issue)

In recent macOS versions, system tools like wdutil and airport often hide SSID and RSSI information under <redacted> for privacy.

- Solution: Implemented a fallback mechanism using system_profiler SPAirPortDataType. By applying a specific Regex pattern (\-[0-9]+), the tool successfully extracts signal strength even when the SSID is masked by the OS.

2. Filtering Noise in Jitter Calculation

High Jitter was detected even with strong RSSI (-48 dBm).

- Solution: The analyzer module filters out "Timeout" values (999ms) from Jitter calculations to prevent skewed data, providing a more accurate representation of actual packet transmission stability.

📈 Sample Output

```
📊 [00:33:20] RSSI: -48 dBm | Lat: 13.84ms | Jitter: 41.64ms | Status: FAIL
==================================================
📋 FINAL TEST REPORT
 - Avg Latency: 35.19 ms
 - Jitter: 41.64 ms (High fluctuation detected)
 - Packet Loss: 0.0%
 - Overall Status: FAIL
==================================================
```

### 👨‍💻 Author

[Da-Wei Lin](https://github.com/deadislove) - QA Automation Engineer focused on Wireless Networking and System Stability.

### 📝 Final Note for Git

Before you upload, here is a .gitignore to keep your repo clean:

```
# .gitignore
venv/
__pycache__/
*.pyc
data/*.csv
data/*.png
.pytest_cache/
.DS_Store
```
