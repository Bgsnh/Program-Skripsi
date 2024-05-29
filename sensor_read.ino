#include <DHT.h>
#define DHT_SENSOR_PIN  21 // ESP32 pin GPIO21 connected to DHT22 sensor
#define DHT_SENSOR_TYPE DHT22

DHT dht_sensor(DHT_SENSOR_PIN, DHT_SENSOR_TYPE);

int V3 = 34; // MQ3 connected to ADC1 CH6
int V4 = 35; // MQ4 connected to ADC1 CH7
int V5 = 32; // MQ5 connected to ADC1 CH4
int V135 = 33; // MQ135 connected to ADC1 CH5

void setup() {
  Serial.begin(115200);           // setup serial communication
  dht_sensor.begin();             // initialize the DHT sensor
  Serial.println("Humidity (%) , Temp (°C) , MQ3 , MQ4 , MQ5 , MQ135 ");
}

void loop() {
  // Read humidity and temperature from DHT22
  float humi = dht_sensor.readHumidity();
  float tempC = dht_sensor.readTemperature();

  // Check if the readings from DHT22 are successful
  if (isnan(humi) || isnan(tempC)) {
    Serial.println("Failed to read from DHT sensor!");
  } else {
    Serial.print(humi);
    Serial.print(" , ");
    Serial.print(tempC);
    Serial.print(" , ");
  }

  // Variables to store ADC values
  int val_MQ3 = 0;
  int val_MQ4 = 0;
  int val_MQ5 = 0;
  int val_MQ135 = 0;

  // Take multiple readings and average them
  for (int i = 0; i < 24; i++) {  
    val_MQ3 += analogRead(V3);
    delay(5);
    val_MQ4 += analogRead(V4);
    delay(5);
    val_MQ5 += analogRead(V5);
    delay(5);
    val_MQ135 += analogRead(V135);
    delay(5);
  }

  // Calculate the average of the readings
  val_MQ3 /= 24;
  val_MQ4 /= 24;
  val_MQ5 /= 24;
  val_MQ135 /= 24;

  // Print the averaged sensor values
  Serial.print(val_MQ3);          
  Serial.print(" , ");
  Serial.print(val_MQ4);          
  Serial.print(" , ");
  Serial.print(val_MQ5);          
  Serial.print(" , ");
  Serial.println(val_MQ135);

  delay(2000); // Wait for 2 seconds before the next loop
}