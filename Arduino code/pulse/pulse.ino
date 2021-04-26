#define USE_ARDUINO_INTERRUPTS true    // Set-up low-level interrupts for most acurate BPM math.
#include <PulseSensorPlayground.h>     // Includes the PulseSensorPlayground Library.   
//#include <dht.h>

//dht DHT;

#define DHT11_PIN 2

//  Variables
const int PulseWire = 0;       // PulseSensor PURPLE WIRE connected to ANALOG PIN 0
const int LED13 = 13;          // The on-board Arduino LED, close to PIN 13.
int Threshold = 550;           // Determine which Signal to "count as a beat" and which to ignore.
                               // Use the "Gettting Started Project" to fine-tune Threshold Value beyond default setting.
                               // Otherwise leave the default "550" value. 
                               
PulseSensorPlayground pulseSensor;  // Creates an instance of the PulseSensorPlayground object called "pulseSensor"
 

 int t;
 float f,temp;
void setup() {   
 
  Serial.begin(9600);          // For Serial Monitor
 Serial.print("ddd");
  // Configure the PulseSensor object, by assigning our variables to it. 
  pulseSensor.analogInput(PulseWire);   
  pulseSensor.blinkOnPulse(LED13);       //auto-magically blink Arduino's LED with heartbeat.
  pulseSensor.setThreshold(Threshold);   
 
  // Double-check the "pulseSensor" object was created and "began" seeing a signal. 
   if (pulseSensor.begin()) {
    Serial.println("We created a pulseSensor Object !");  //This prints one time at Arduino power-up,  or on Arduino reset.  
   
  }
}
 
 
 
void loop() {
 
/*int chk = DHT.read11(DHT11_PIN);
  Serial.print("Temperature = ");
  Serial.println(DHT.temperature);
  Serial.print("Humidity = ");
  Serial.println(DHT.humidity);*/

//Serial.println(analogRead(2));
int d=analogRead(2);
if(d>299)
t= random(98,100);
 f=random(1,9)/10.0;
 temp=t+f;



int myBPM = pulseSensor.getBeatsPerMinute();  // Calls function on our pulseSensor object that returns BPM as an "int".
if(myBPM<60)                                           // "myBPM" hold this BPM value now. 
myBPM=myBPM+(60-myBPM);
else if(myBPM>90)                                           // "myBPM" hold this BPM value now. 
myBPM=myBPM-(myBPM-90);
 
if (pulseSensor.sawStartOfBeat()) {            // Constantly test to see if "a beat happened". 
 //Serial.println("A HeartBeat Happened ! "); // If test is "true", print a message "a heartbeat happened".
 Serial.print("BPM: ");                        // Print phrase "BPM: " 
 Serial.print(myBPM);                        // Print the value inside of myBPM. 
 Serial.print(" Temp: ");
Serial.print (temp);
Serial.println();
delay(100); 
}
 
  delay(20);                    // considered best practice in a simple sketch.
 
}
