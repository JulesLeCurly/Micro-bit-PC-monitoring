import pc_side.other.All_basic_function as All_basic_functions
import serial
import time

class ConnectionManager:
    def __init__(self):
        self.connected = False

        Config = All_basic_functions.read_yml("config/config.yml")
        self.microbit_port = Config['microbit_port']
        self.baud_rate = Config['baud_rate']
        self.update_interval = Config['UPDATE_INTERVAL']
        self.retry_timeout = Config['Retray_timeout']

        self.ser = None
    
    def Get_connection(self):
        try:
            self.ser = serial.Serial(self.microbit_port, self.baud_rate, timeout=1)
            self.connected = True
        except:
            self.connected = False
        
    def wait_for_connection(self):
        self.Get_connection()
        while not self.connected:
            time.sleep(self.retry_timeout)
            self.Get_connection()
    
    def send_data_with_serial(self, data):
        try:
            self.ser.write(data.encode("utf-8"))
        except Exception as e:
            print(f"Error sending data: {e}")
            self.connected = False
        time.sleep(self.update_interval)
    
    def send_data(self, Page, data):
        data = f"{Page}:{data}" # Add the Page
        if self.connected:
            self.send_data_with_serial(data)
    
    def recev_data(self):
        try:
            line = self.ser.read().decode('utf-8').strip()
            return line
        except Exception as e:
            print(f"Error receiving data: {e}")
            self.connected = False
        return None