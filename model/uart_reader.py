import serial
import serial.tools.list_ports
import time
from datetime import datetime

class UARTReader:
    def __init__(self, baudrate=115200):
        self.baudrate = baudrate
        self.serial_port = None
        
    def list_available_ports(self):
        """แสดงรายการพอร์ตที่สามารถใช้ได้"""
        ports = list(serial.tools.list_ports.comports())
        if not ports:
            print("No serial ports found!")
            return []
        
        print("\nAvailable ports:")
        for idx, port in enumerate(ports):
            print(f"{idx}: {port.device} - {port.description}")
        return ports
    
    def connect(self, port_index=None):
        """เชื่อมต่อพอร์ตที่เลือก"""
        ports = list(serial.tools.list_ports.comports())
        
        if not ports:
            raise Exception("No serial ports available!")
            
        if port_index is None:
            selected_port = ports[3].device  # ใช้พอร์ตตัวแรก
        else:
            try:
                selected_port = ports[port_index].device
            except IndexError:
                raise Exception(f"Invalid port index: {port_index}")
        
        try:
            self.serial_port = serial.Serial(
                port=selected_port,
                baudrate=self.baudrate,
                timeout=1
            )
            print(f"\nConnected to {selected_port} at {self.baudrate} baud")
        except serial.SerialException as e:
            raise Exception(f"Failed to connect to {selected_port}: {str(e)}")
    
    def read_data(self):
        """อ่านข้อมูลจาก UART"""
        if not self.serial_port:
            raise Exception("Not connected to any port!")
            
        try:
            while True:
                if self.serial_port.in_waiting > 0:
                    print(f"Bytes waiting: {self.serial_port.in_waiting}")
                    line = self.serial_port.readline()
                    print(f"Raw received: {line}")  # Debugging line
                    
                    try:
                        decoded_line = line.decode('utf-8').strip()
                        if decoded_line:
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                            print(f"[{timestamp}] {decoded_line}")
                    except UnicodeDecodeError:
                        print("Received non-UTF-8 data")
                time.sleep(0.1)  # ลดโหลด CPU
                
        except KeyboardInterrupt:
            print("\nStopping UART reader...")
        except Exception as e:
            print(f"Error reading data: {str(e)}")
        finally:
            self.disconnect()
    
    def disconnect(self):
        """ปิดการเชื่อมต่อพอร์ต"""
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            print("Disconnected from serial port")

def main():
    reader = UARTReader(baudrate=115200)
    
    try:
        ports = reader.list_available_ports()
        if not ports:
            return
        
        port_index = int(input("Enter the port index to connect: "))
        reader.connect(port_index=port_index)
        
        print("\nReading data from UART... (Press Ctrl+C to stop)")
        reader.read_data()
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
