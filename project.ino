#include "DHT.h"
#include "DFRobot_MICS.h"
#include "BluetoothSerial.h"

String device_name = "ESP32-Plant-Logger";

// Check if Bluetooth is available
#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

// Check SerialBT Port Profile
#if !defined(CONFIG_BT_SPP_ENABLED)
#error SerialBT Port Profile for Bluetooth is not available or not enabled. It is only available for the ESP32 chip.
#endif

BluetoothSerial SerialBT;


//temp and humid
#define DHTPIN 15
#define DHTTYPE DHT22     // Digital pin connected to the DHT sensor
#define SOILPIN 34
#define PUMP 23
DHT dht(DHTPIN, DHTTYPE);

 //gas sensor
#define CALIBRATION_TIME   3    // Default calibration time is three minutes for gas
#define ADC_PIN            35   // Analog pin connected to the gas sensor's analog output
#define POWER_PIN          33    // Digital pin to enable the gas sensor

DFRobot_MICS_ADC mics(ADC_PIN, POWER_PIN);

#define lightPin 32
int lightLevel = 0;

int soilMoist = 0;



void setup() {
  
  SerialBT.begin(115200);
  SerialBT.begin(device_name);  //Bluetooth device name
  //SerialBT.deleteAllBondedDevices(); // Uncomment this to delete paired devices; Must be called after begin
  SerialBT.printf("The device with name \"%s\" is started.\nNow you can pair it with Bluetooth!\n", device_name.c_str());

  pinMode(SOILPIN, INPUT);
  pinMode(PUMP, OUTPUT);

  dht.begin();

  // setup gas sensor
  if(!mics.begin())
  {
    SerialBT.println("Gas sensor not found! Please check the connections.");
  }
  else
  {
    // Check the current power state of the sensor
    uint8_t mode = mics.getPowerState();
  if (mode == SLEEP_MODE) {
    mics.wakeUpMode();
    SerialBT.println("Sensor woken up successfully!");
  } else {
    SerialBT.println("Sensor is already in wake-up mode.");
  }
  }
}

void loop() {
  // Wait a few seconds between measurements.
  delay(2000);

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();


  SerialBT.print(F("Humidity: "));
  SerialBT.print(h);
  SerialBT.print(F("%  Temperature: "));
  SerialBT.print(t);
  SerialBT.print(F("°C\n"));

soilMoist = analogRead(SOILPIN);

// Map the raw sensor value to percentage (0% = dry, 100% = wet)
int moisturePercent = map(soilMoist, 4095, 1161, 0, 100);

// Constrain to 0-100% to avoid going out of range
moisturePercent = constrain(moisturePercent, 0, 100);

SerialBT.print("Soil Moisture: ");
SerialBT.print(moisturePercent);
SerialBT.println("%");

if(moisturePercent < 50)
{
  digitalWrite(PUMP, HIGH);
  
}
else
{
  digitalWrite(PUMP, LOW);
  delay(50);
}

lightLevel = analogRead(lightPin);

int lightPercent = map(lightLevel, 4095, 1300, 0, 100);

// Constrain to 0-100% to avoid going out of range
lightPercent = constrain(lightPercent, 0, 100);

SerialBT.print("Light intensity ");
SerialBT.print(lightPercent);
SerialBT.print("%\n");

if (!mics.warmUpTime(CALIBRATION_TIME)) {
    SerialBT.println("GAS Sensor is in Waming Up!");
    delay(1000);
  }
  else
  {
  // Read gas data from the sensor
  float coConcentration = mics.getGasData(CO);
  float ch4Concentration = mics.getGasData(CH4);
  float c2h5ohConcentration = mics.getGasData(C2H5OH);
  float h2Concentration = mics.getGasData(H2);
  float nh3Concentration = mics.getGasData(NH3);
  float no2Concentration = mics.getGasData(NO2);
 
  // Print the gas concentrations to the serialBT monitor
  SerialBT.print("CO (Carbon ): ");
  SerialBT.print(coConcentration, 1);
  SerialBT.println(" PPM");
 
  SerialBT.print("CH4 (Methane): ");
  SerialBT.print(ch4Concentration, 1);
  SerialBT.println(" PPM");
 
  SerialBT.print("C2H5OH (Ethanol): ");
  SerialBT.print(c2h5ohConcentration, 1);
  SerialBT.println(" PPM");
 
  SerialBT.print("H2 (Hydrogen): ");
  SerialBT.print(h2Concentration, 1);
  SerialBT.println(" PPM");
 
  SerialBT.print("NH3 (Ammonia): ");
  SerialBT.print(nh3Concentration, 1);
  SerialBT.println(" PPM");
 
  SerialBT.print("NO2 (Nitrogen Dioxide): ");
  SerialBT.print(no2Concentration, 1);
  SerialBT.println(" PPM");
  SerialBT.println();
 
  delay(1000); // Wait for 1 second before the next reading
  
  }
  
}

