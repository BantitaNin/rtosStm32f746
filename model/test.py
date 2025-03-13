import serial
import time
import serial.tools.list_ports

# ค้นหาพอร์ตที่มีอยู่ทั้งหมด
ports = list(serial.tools.list_ports.comports())
if not ports:
    print("No serial ports found.")
    exit()

# เลือกพอร์ตแรกที่พบ
port_name = ports[0].device  # เปลี่ยนจาก ports[2] เป็น ports[0]
print(f"Connecting to {port_name}")

try:
    # กำหนดค่าพอร์ต UART และ baud rate
    ser = serial.Serial(port_name, baudrate=115200, timeout=1)

    def send_uart_message(message):
        """ ส่งข้อความผ่าน UART """
        if ser.is_open:
            ser.write((message + '\n').encode('utf-8'))
            print(f"Sent: {message}")
        else:
            print(f"{port_name} is not open.")

    try:
        while True:
            send_uart_message("Hello UART\n")
            time.sleep(1)  # ส่งข้อความทุก 1 วินาที
    except KeyboardInterrupt:
        print("Stopped by user")
    finally:
        ser.close()  # ปิดพอร์ตเมื่อสิ้นสุดการใช้งาน

except serial.SerialException as e:
    print(f"Failed to open {port_name}: {str(e)}")
