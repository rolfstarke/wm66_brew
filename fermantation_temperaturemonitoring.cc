#include <Wire.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <InfluxDbClient.h>
#include <InfluxDbCloud.h>
#include <WiFiMulti.h>
  WiFiMulti wifiMulti;
#define DEVICE "ESP32"

const int SensorDataPin = 4;   
OneWire oneWire(SensorDataPin);
DallasTemperature sensors(&oneWire);

float temperature_Celsius;
float temperature_Fahrenheit;

#define WIFI_SSID " "
#define WIFI_PASSWORD " "
#define INFLUXDB_URL " "
#define INFLUXDB_TOKEN " "
#define INFLUXDB_ORG " "
#define INFLUXDB_BUCKET " "

#define TZ_INFO "CET-1CEST,M3.5.0,M10.5.0/3"

InfluxDBClient client(INFLUXDB_URL, INFLUXDB_ORG, INFLUXDB_BUCKET, INFLUXDB_TOKEN, InfluxDbCloud2CACert);

Point sensor("measurements");



void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  wifiMulti.addAP(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to wifi");
  while (wifiMulti.run() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();

 sensors.begin();
 
  // Add tags
  sensor.addTag("device", DEVICE);
  sensor.addTag("SSID", WiFi.SSID());
  
  timeSync(TZ_INFO, "pool.ntp.org", "time.nis.gov");
  
  if (client.validateConnection()) {
    Serial.print("Connected to InfluxDB: ");
    Serial.println(client.getServerUrl());
  } else {
    Serial.print("InfluxDB connection failed: ");
    Serial.println(client.getLastErrorMessage());
  }
}



void loop() {
  
  sensor.clearFields();

  sensors.requestTemperatures(); 
  temperature_Celsius = sensors.getTempCByIndex(0);
  temperature_Fahrenheit = sensors.getTempFByIndex(0);
  
  sensor.addField("Temperature Celsius",temperature_Celsius);
  sensor.addField("Temperature Fahrenheit",temperature_Fahrenheit);
  
  Serial.print("Writing: ");
  Serial.println(client.pointToLineProtocol(sensor));

  // If no Wifi signal, try to reconnect it
  if (wifiMulti.run() != WL_CONNECTED) {
    Serial.println("Wifi connection lost");
  }
  // Write point
  if (!client.writePoint(sensor)) {
    Serial.print("InfluxDB write failed for temperature: ");
    Serial.println(client.getLastErrorMessage());
  }
  Serial.println("");
  Serial.println("Delay 10s");
  delay(10000);
}
