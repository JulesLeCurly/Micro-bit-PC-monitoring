"""
Micro:bit PC Monitoring - Main Application
Monitors system metrics and sends them to a micro:bit via serial connection.
"""

import pc_side.core.connection_manager as connection_manager
import pc_side.core.system_monitor as system_monitor
import pc_side.ui.system_tray as system_tray_icon
import threading
import time
import sys

# Global variables
current_page = "Monitoring"
running = True
conn_manager = None
sys_monitor = None

def monitoring_loop():
    """
    Main monitoring loop that collects system metrics and sends them to micro:bit.
    Runs in a separate thread.
    """
    global conn_manager, sys_monitor, running, current_page
    
    print("Starting monitoring loop...")
    
    # Initialize connection manager and system monitor
    conn_manager = connection_manager.ConnectionManager()
    sys_monitor = system_monitor.SystemMonitor()
    
    # Wait for micro:bit connection
    print("Waiting for micro:bit connection...")
    conn_manager.wait_for_connection()
    print("✓ Connected to micro:bit!")
    
    while running:
        try:
            if not conn_manager.connected:
                print("Connection lost. Reconnecting...")
                conn_manager.wait_for_connection()
                print("✓ Reconnected to micro:bit!")
            
            # Collect data based on current page
            if current_page == "Monitoring":
                # Get system metrics
                cpu_data = sys_monitor.get_cpu_usage()
                memory_data = sys_monitor.get_memory_usage()
                gpu_data = sys_monitor.get_gpu_metrics()
                
                # Format data for micro:bit
                cpu_usage = cpu_data.get("usage", 0)
                ram_usage = memory_data.get("usage", 0)
                
                if "error" in gpu_data:
                    # No GPU available
                    data_str = f"CPU:{cpu_usage:.1f},RAM:{ram_usage:.1f}"
                else:
                    gpu_usage = gpu_data.get("usage", 0)
                    gpu_temp = gpu_data.get("temperature", 0)
                    vram = gpu_data.get("vram", 0)
                    fan_speed = gpu_data.get("fan_speed", 0)
                    data_str = f"CPU:{cpu_usage:.1f},RAM:{ram_usage:.1f},GPU:{gpu_usage},TEMP:{gpu_temp},FAN:{fan_speed}"
                
                # Send data to micro:bit
                conn_manager.send_data(current_page, data_str)
                
                # Debug output
                print(f"[{current_page}] Sent: {data_str}")
            
            elif current_page == "WLED":
                # TODO: Implement WLED control
                data_str = "STATUS:OK"
                conn_manager.send_data(current_page, data_str)
                print(f"[{current_page}] WLED control not yet implemented")
            
            elif current_page == "Temperature":
                # TODO: Implement room temperature monitoring
                data_str = "TEMP:22"
                conn_manager.send_data(current_page, data_str)
                print(f"[{current_page}] Temperature monitoring not yet implemented")
            
            else:
                print(f"Unknown page: {current_page}")
            
            # Small delay between updates (defined in config)
            time.sleep(conn_manager.update_interval)
            
        except KeyboardInterrupt:
            print("\nStopping monitoring loop...")
            running = False
            break
        except Exception as e:
            print(f"Error in monitoring loop: {e}")
            time.sleep(1)  # Wait a bit before retrying

def change_page(new_page):
    """Change the current display page on the micro:bit."""
    global current_page
    if new_page in ["Monitoring", "WLED", "Temperature"]:
        current_page = new_page
        print(f"Switched to page: {current_page}")
    else:
        print(f"Invalid page: {new_page}")

def quit_application():
    """Cleanly quit the application."""
    global running
    print("Quitting application...")
    running = False
    sys.exit(0)

def main():
    """Main entry point of the application."""
    print("=" * 50)
    print("  Micro:bit PC Monitoring System")
    print("=" * 50)
    print()
    
    # Start monitoring loop in a separate thread
    monitoring_thread = threading.Thread(target=monitoring_loop, daemon=True)
    monitoring_thread.start()
    
    # TODO: Start system tray icon
    # The system tray icon should run in the main thread
    # For now, just keep the main thread alive
    print("\nApplication running. Press Ctrl+C to quit.")
    print("=" * 50)
    
    try:
        # Keep main thread alive
        while running:
            time.sleep(0.5)
    except KeyboardInterrupt:
        quit_application()

if __name__ == "__main__":
    main()