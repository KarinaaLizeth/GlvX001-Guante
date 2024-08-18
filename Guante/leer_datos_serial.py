import serial
import time
import csv
import keyboard


port = "COM4"
baudrate = 115200
max_samples = 15  # Número máximo de muestras

def capture_data(label):
    csv_filename = f'datos_{label}.csv'
    ser = serial.Serial(port, baudrate)
    time.sleep(2)
    all_data = []
    capturing = False

    while True:
        try:
            line = ser.readline().decode('utf-8', errors='ignore').strip()

            if not capturing and "###CAPTURE_START###" not in line:
                continue  # Si no estamos capturando, no hacer nada con las líneas recibidas

            print(f"Línea recibida: {line}")

            if "###CAPTURE_START###" in line:
                capturing = True
                all_data = []
                print("Iniciando captura...")

            elif "###CAPTURE_COMPLETE###" in line or len(all_data) >= max_samples:
                capturing = False
                print(f"Captura completa. {len(all_data)} muestras capturadas.")
                save_capture = None
                print("Presiona ESPACIO para guardar la captura, o SUPR para descartarla.")

                def on_space():
                    nonlocal save_capture
                    save_capture = True
                    keyboard.unhook_all()

                def on_delete():
                    nonlocal save_capture
                    save_capture = False
                    keyboard.unhook_all()

                keyboard.on_press_key("space", lambda _: on_space())
                keyboard.on_press_key("delete", lambda _: on_delete())

                while save_capture is None:
                    time.sleep(0.1)  # Esperar a que el usuario presione una tecla

                if save_capture:
                    with open(csv_filename, mode='a', newline='') as file:  # Modo 'a' para agregar datos
                        writer = csv.writer(file)
                        if file.tell() == 0:
                            writer.writerow(["flex1", "flex2", "flex3", "flex4", "flex5", "ax", "ay", "az", "gx", "gy", "label"])
                        for data in all_data:
                            writer.writerow(data + [label])
                        writer.writerow([])  
                    print("Datos guardados en el archivo CSV.")
                else:
                    print("Captura descartada.")
                all_data = []  
                break 

            elif capturing and line.startswith("DATA,"):
                parts = line.split(",")
                if len(parts) == 11: 
                    data = parts[1:] 
                    all_data.append(data)
                    print(f"Muestra capturada: {data}")

                else:
                    print(f"Línea de datos incompleta: {line}")

        except ValueError as e:
            print(f"Error al manejar los datos: {e}, data: {line}")
        except KeyboardInterrupt:
            break

    ser.close()
    print("Desconectado...")

def main():
    while True:
        print("Presiona  't' para 'te amo', 'm' para 'comer','e' para 'escuela', 'h' para 'hola', 'b' para 'bien', 'x' para 'mal', 'esc' para salir.")
        key = keyboard.read_event()
        if key.event_type == keyboard.KEY_DOWN and key.name in [ 't', 'm', 'e', 'h', 'b','x','esc']:
            if key.name == 'e':
                print("Capturando datos para 'escuela'")
                capture_data('escuela')
            elif key.name == 't':
                print("Capturando datos para 'te amo'")
                capture_data('te amo')
            elif key.name == 'm':
                print("Capturando datos para 'comer'")
                capture_data('comer')
            elif key.name == 'h':
                print("Capturando datos para 'hola'")
                capture_data('hola')
            elif key.name == 'b':
                print("Capturando datos para 'bien'")
                capture_data('bien')   
            elif key.name == 'x':
                print("Capturando datos para 'mal'")
                capture_data('mal')              
            elif key.name == 'esc':
                print("Saliendo...")
                break
            time.sleep(0.1)

if __name__ == "__main__":
    main()
