import time
import sys
import argparse
import csv
from datetime import datetime
import os
from src.scanner import WiFiScanner
from src.analyzer import NetworkAnalyzer
from src.reporter import NetworkReporter

def save_raw_data(rssi_history, latency_history, folder="data"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(folder, f"raw_data_{timestamp}.csv")
    
    with open(filepath, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Sample_Index", "RSSI_dBm", "Latency_ms"])
        for i, (r, l) in enumerate(zip(rssi_history, latency_history)):
            writer.writerow([i, r, l])
    
    print(f"💾 Raw data saved to: {filepath}")

def run_interactive_monitor(interval=2, duration=60):
    scanner = WiFiScanner()
    analyzer = NetworkAnalyzer()
    reporter = NetworkReporter()

    start_time = time.time()
    end_time = start_time + duration

    print(f"\n🚀 Network Side Project: WiFi Stability Monitor")
    print(f"📡 Target SSID: {scanner.get_current_ssid() or 'N/A'}")
    print(f"⏱  Duration: {duration}s | Interval: {interval}s")
    print("-" * 50)

    try:
        while time.time() < end_time:
            rssi = scanner.get_rssi()
            latency = scanner.get_latency()

            analyzer.add_record(rssi, latency)

            report = analyzer.get_stability_report()

            status_color = "\033[92m" if report['overall_status'] == "PASS" else "\033[91m"
            reset_color = "\033[0m"

            sys.stdout.write(
                f"\r📊 [{time.strftime('%H:%M:%S')}] "
                f"RSSI: {rssi if rssi else '??'} dBm | "
                f"Lat: {latency}ms | "
                f"Jitter: {report['jitter_ms']}ms | "
                f"Status: {status_color}{report['overall_status']}{reset_color}   "
            )
            sys.stdout.flush()
            
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n\n🛑 Monitor stopped by user.")

    # After network test - Final Report
    print("\n" + "="*50)
    print("📋 FINAL TEST REPORT")
    final_report = analyzer.get_stability_report()
    for key, value in final_report.items():
        print(f" - {key.replace('_', ' ').title()}: {value}")

    reporter.generate_report(analyzer.rssi_history, analyzer.latency_history)
    print("="*50)
    save_raw_data(analyzer.rssi_history, analyzer.latency_history)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WiFi Performance Interactive Monitor")
    parser.add_argument("--interval", type=int, default=2, help="Interval between scans (seconds)")
    parser.add_argument("--duration", type=int, default=60, help="Total test duration (seconds)")
    
    args = parser.parse_args()
    run_interactive_monitor(interval=args.interval, duration=args.duration)