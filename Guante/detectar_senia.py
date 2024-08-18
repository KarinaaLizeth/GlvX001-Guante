import serial
import time
import numpy as np
import joblib
from collections import deque
import pandas as pd
import pyttsx3

# Cargar el modelo y el scaler
clf = joblib.load('modelo_senias.pkl')
scaler = joblib.load('scaler_senias.pkl')

# Configuración del puerto serial
port = "COM4"
baudrate = 115200

engine = pyttsx3.init()
# Inicializa la conexión serial
ser = serial.Serial(port, baudrate)
time.sleep(2)
print(f"Conexión serial establecida en {port}")
print('Listo para detectar señales...')

window_size = 15 
prediction_buffer = deque(maxlen=3)

column_names = ['flex1', 'flex2', 'flex3', 'flex4', 'flex5', 'ax', 'ay', 'az', 'gx', 'gy']

def extract_features(segment):
    means = np.mean(segment, axis=0)
    stds = np.std(segment, axis=0)
    maxs = np.max(segment, axis=0)
    mins = np.min(segment, axis=0)
    feature_vector = np.concatenate([means, stds, maxs, mins])
    return feature_vector

def classify_movement(model, segment, scaler):
    segment = np.array(segment)
    df = pd.DataFrame(segment, columns=column_names)
    normalized_segment = scaler.transform(df)
    features = extract_features(normalized_segment).reshape(1, -1)
    return model.predict(features)[0]

def get_filtered_prediction(predictions):
    if len(predictions) < prediction_buffer.maxlen:
        return None
    return max(set(predictions), key=predictions.count)

def read_and_classify():
    current_window = deque(maxlen=window_size)
    
    while True:
        try:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line.startswith("DATA,"):
                parts = line.split(",")
                if len(parts) == 11:  # Esperamos 11 valores + "DATA"
                    try:
                        data = [float(value.strip()) for value in parts[1:11]]
                        if len(data) == 10:  # Asegurarse de que tenemos los 10 valores esperados
                            current_window.append(data)
                            if len(current_window) == window_size:
                                prediction = classify_movement(clf, np.array(current_window), scaler)
                                prediction_buffer.append(prediction)
                                
                                filtered_prediction = get_filtered_prediction(prediction_buffer)
                                if filtered_prediction is not None:
                                    print(f"Palabra: {filtered_prediction}")
                                    #engine.say(filtered_prediction)
                                    #engine.runAndWait()
                                    #time.sleep(0.01)
                                else:
                                    print("No se pudo obtener una predicción filtrada")
                            else:
                                print("Esperando más datos para llenar la ventana")
                    except ValueError as e:
                        print(f"Error al convertir los datos: {e}, data: {line}")
                else:
                    print(f"Número incorrecto de partes en la línea: {len(parts)}")
            else:
                print("Línea no comienza con 'DATA,'")
            
        except KeyboardInterrupt:
            break
        except serial.SerialException as e:
            print(f"Error de conexión serial: {e}")
            time.sleep(1)

    ser.close()
    print("Desconectado...")

try:
    read_and_classify()
except KeyboardInterrupt:
    print("Interrupción del usuario")
finally:
    if ser.is_open:
        ser.close()
    print("Desconectado...")