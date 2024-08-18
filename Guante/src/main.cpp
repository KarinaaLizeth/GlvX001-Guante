#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

// Definir pines
#define FLEX1_PIN 34
#define FLEX2_PIN 35
#define FLEX3_PIN 32
#define FLEX4_PIN 36
#define FLEX5_PIN 39
#define BUTTON_PIN 18

Adafruit_MPU6050 mpu;
bool capturing = false;
bool lastButtonState = HIGH; // Estado anterior del botón

void setup() {
  Serial.begin(115200);
  
  // Configurar pines de flexores como entradase
  pinMode(FLEX1_PIN, INPUT);
  pinMode(FLEX2_PIN, INPUT);
  pinMode(FLEX3_PIN, INPUT);
  pinMode(FLEX4_PIN, INPUT);
  pinMode(FLEX5_PIN, INPUT);
  
  // Configurar pin de botón como entrada con pull-up interno
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  // Iniciar el MPU6050
  if (!mpu.begin()) {
    Serial.println("No se pudo encontrar el MPU6050, verifica las conexiones!");
    while (1);
  }

  // Configuración del MPU6050
  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
  mpu.setGyroRange(MPU6050_RANGE_250_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
}

void loop() {
  // Leer los valores de los flexores
  int flex1Value = analogRead(FLEX1_PIN);
  int flex2Value = analogRead(FLEX2_PIN);
  int flex3Value = analogRead(FLEX3_PIN);
  int flex4Value = analogRead(FLEX4_PIN);
  int flex5Value = analogRead(FLEX5_PIN);

  // Leer el estado del botón
  bool buttonState = digitalRead(BUTTON_PIN);

  // Detectar cambio de estado en el botón
  if (buttonState == LOW && lastButtonState == HIGH) {
    capturing = !capturing; // Cambiar el estado de captura
    if (capturing) {
      Serial.println("###CAPTURE_START###");
    } else {
      Serial.println("###CAPTURE_COMPLETE###");
    }
  }
  lastButtonState = buttonState; // Actualizar el estado anterior del botón

  if (capturing) {
    // Leer los datos del MPU6050
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    // Enviar datos por serial
    Serial.print("DATA,");
    Serial.print(flex1Value); Serial.print(",");
    Serial.print(flex2Value); Serial.print(",");
    Serial.print(flex3Value); Serial.print(",");
    Serial.print(flex4Value); Serial.print(",");
    Serial.print(flex5Value); Serial.print(",");
    Serial.print(a.acceleration.x); Serial.print(",");
    Serial.print(a.acceleration.y); Serial.print(",");
    Serial.print(a.acceleration.z); Serial.print(",");
    Serial.print(g.gyro.x); Serial.print(",");
    Serial.println(g.gyro.y);  
  }

  delay(100); 
}
