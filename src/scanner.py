import subprocess
import platform
import re
import time

class WiFiScanner:
    def __init__(self):
        self.os_type = platform.system()

    def get_rssi(self):
        """
        Retrieves the Signal Strength (RSSI) in dBm.
        Note: Windows and Linux often provide 'Quality %', 
        which is converted here to an approximate dBm value.
        """
        try:
            match self.os_type:
                case "Darwin":
                    # Using shell=True to support pipe operations for macOS system_profiler
                    cmd = "system_profiler SPAirPortDataType | grep 'Signal / Noise' | head -n 1 | grep -oE '\\-[0-9]+' | head -n 1"
                    output = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
                    return int(output) if output else None
                
                case "Linux":
                    # nmcli provides signal quality as a percentage
                    cmd = ["nmcli", "-f", "IN-USE,SIGNAL", "device", "wifi"]
                    output = subprocess.check_output(cmd).decode("utf-8")
                    for line in output.splitlines():
                        if line.startswith("*"):
                            quality = int(line.split()[1])
                            # Rough conversion: dBm = (Quality / 2) - 100
                            return (quality / 2) - 100
                    return None
                
                case "Windows":
                    cmd = ["netsh", "wlan", "show", "interfaces"]
                    output = subprocess.check_output(cmd).decode("utf-8", errors="ignore")
                    match = re.search(r"(\d+)%", output)
                    if match:
                        quality = int(match.group(1))
                        # Standard Windows signal quality to dBm conversion
                        return (quality / 2) - 100
                    return None
                
                case _:
                    print(f"Unsupported OS: {self.os_type}")
                    return None
        except Exception as e:
            print(f"Error scanning WiFi RSSI: {e}")
            return None
        
    def get_current_ssid(self):
        """
        Retrieves the SSID of the currently connected network.
        """
        try:
            match self.os_type:
                case "Darwin":
                    cmd = "system_profiler SPAirPortDataType | grep -A 20 'Current Network Information:' | grep 'SSID:' | head -n 1 | awk '{print $2}'"
                    output = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
                    return output if output else "eero_Hidden_Node"
                
                case "Linux":
                    cmd = ["nmcli", "-t", "-f", "ACTIVE,SSID", "dev", "wifi"]
                    output = subprocess.check_output(cmd).decode("utf-8")
                    for line in output.splitlines():
                        if line.startswith("yes"):
                            return line.split(":")[1].strip()
                    return None
                
                case "Windows":
                    cmd = ["netsh", "wlan", "show", "interfaces"]
                    output = subprocess.check_output(cmd).decode("utf-8", errors="ignore")
                    # Using multiline regex to find the SSID field
                    match = re.search(r"^\s+SSID\s+:\s+(.+)$", output, re.MULTILINE)
                    return match.group(1).strip() if match else None
                
                case _:
                    return None
        except Exception as e:
            print(f"Error retrieving SSID: {e}")
            return None
        
    def get_latency(self, host="8.8.8.8"):
        """
        Measures network latency (Ping) to a specific host.
        Default host is Google Public DNS (8.8.8.8).
        """
        try:
            # Platform-specific ping parameters:
            # Windows: -n (count), -w (timeout in ms)
            # Unix: -c (count), -t (timeout in seconds)
            if self.os_type == "Windows":
                cmd = ["ping", "-n", "1", "-w", "1000", host]
            else:
                cmd = ["ping", "-c", "1", "-t", "1", host]

            output = subprocess.check_output(cmd).decode("utf-8", errors="ignore")
            
            # Regex to extract the time value from ping output
            match = re.search(r"time[=<](\d+\.?\d*)", output)
            if match:
                return float(match.group(1))
            
            return 999.0  # High value represents timeout/failure
        except Exception:
            return 999.0
        
if __name__ == "__main__":
    scanner = WiFiScanner()
    print(f"--- WiFi QA Scanner Mode (OS: {scanner.os_type}) ---")
    
    # Execution loop for demonstration
    for i in range(5):
        rssi = scanner.get_rssi()
        ssid = scanner.get_current_ssid()
        latency = scanner.get_latency()
        print(f"[{i+1}] SSID: {ssid:<15} | RSSI: {rssi if rssi else 'N/A'} dBm | Latency: {latency} ms")
        time.sleep(1)