import pytest
from src.analyzer import NetworkAnalyzer

def test_perfect_connection():
    """Test: A stable network environment should return PASS"""
    analyzer = NetworkAnalyzer()
    # Simulate 5 stable, low-latency data points
    for _ in range(5):
        analyzer.add_record(rssi=-40, latency=15.0)
    
    report = analyzer.get_stability_report()
    assert report["overall_status"] == "PASS"
    assert report["jitter_ms"] < 5.0

def test_high_jitter_failure():
    """Test: High latency variance should return FAIL"""
    analyzer = NetworkAnalyzer()
    # Simulate severe latency spikes (10ms -> 200ms -> 15ms)
    latencies = [10.0, 200.0, 15.0, 180.0, 20.0]
    for lat in latencies:
        analyzer.add_record(rssi=-50, latency=lat)
    
    report = analyzer.get_stability_report()
    assert report["overall_status"] == "FAIL"
    assert report["jitter_ms"] > 30.0

def test_packet_loss():
    """Test: Response when packet loss (999ms) occurs"""
    analyzer = NetworkAnalyzer()
    # Simulate 4 normal pings and 1 timeout (20% loss rate)
    for lat in [20.0, 20.0, 999.0, 20.0, 20.0]:
        analyzer.add_record(rssi=-50, latency=lat)
    
    report = analyzer.get_stability_report()
    assert report["overall_status"] == "FAIL"
    assert report["packet_loss_rate"] == "20.0%"

def test_empty_data():
    """Test: Boundary condition with no data collected"""
    analyzer = NetworkAnalyzer()
    report = analyzer.get_stability_report()
    assert report["overall_status"] == "NO_DATA"