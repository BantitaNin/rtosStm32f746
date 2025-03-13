import serial
import serial.tools.list_ports
import os
import json
import librosa
import numpy as np
import sounddevice as sd
import tensorflow as tf
from tensorflow.keras.models import load_model
from scipy.io.wavfile import write
import time

def find_first_port():
    ports = list(serial.tools.list_ports.comports())
    if ports:
        first_port = ports[0].device  # แก้ให้ถูกต้องเป็น ports[0]
        print(f"Found port: {first_port} - {ports[0].description}")
        return first_port
    return None

# Serial port configuration
BAUD_RATE = 115200
port = find_first_port()
if port is None:
    print("Error: No serial ports found!")
    exit(1)

print(f"Connecting to port: {port}")
try:
    ser = serial.Serial(port, BAUD_RATE, timeout=1)
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit(1)

DATASET_PATH = "dataset"
LABELS = {"Orange": 0, "Coffee": 1, "unknown": 2}

# Load model
model_path = 'test_model3.h5'
try:
    model = load_model(model_path)
except Exception as e:
    print(f"Error loading model: {e}")
    ser.close()
    exit(1)

def extract_features(audio, sr):
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
    return np.mean(mfcc, axis=1)

def predict_audio(model, audio, sr):
    features = extract_features(audio, sr)
    prediction = model.predict(np.array([features]))
    confidence = np.max(prediction)
    confidence_percent = int(confidence * 100)
    
    label = np.argmax(prediction)
    label_name = list(LABELS.keys())[label]
    return label_name, confidence_percent

def record_audio(duration=3, sample_rate=22050):
    print("Recording...")
    try:
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
        sd.wait()
        return audio.flatten(), sample_rate
    except Exception as e:
        print(f"Error recording audio: {e}")
        return None, None

def send_serial_data(data):
    try:
        if ser.is_open:
            # First clear any pending data
            ser.reset_input_buffer()
            
            # Send data with proper encoding
            ser.write(data.encode('utf-8', errors='replace'))
            ser.flush()
            print(f"Sent: {data.strip()}")
            
            # Wait for acknowledgment (optional)
            time.sleep(0.1)
            if ser.in_waiting > 0:
                response = ser.readline().decode('utf-8', errors='replace').strip()
                print(f"Device acknowledged: {response}")
    except serial.SerialException as e:
        print(f"Error sending data: {e}")

def main():
    print(f"Connected to {port}")
    print("Waiting for commands...")
    
    while True:
        try:
            if ser.in_waiting > 0:
                command = ser.readline().decode('utf-8', errors='replace').strip()
                print(f"Received command: {command}")
                
                if command == "START_RECORDING":
                    print("Got recording command")
                    
                    audio, sr = record_audio(duration=2)
                    if audio is not None:
                        predicted_label, confidence_percent = predict_audio(model, audio, sr)
                        
                        result = f"{predicted_label}"
                        send_serial_data(result)
                    else:
                        send_serial_data("ERROR:Recording failed\n")
                        
        except serial.SerialException as e:
            print(f"Serial communication error: {e}")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            continue

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    except Exception as e:
        print(f"Program error: {e}")
    finally:
        print("Closing serial port")
        ser.close()
