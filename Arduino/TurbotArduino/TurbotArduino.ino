#include <Wire.h>

#include "freeram.h"

#include "mpu.h"
#include "I2Cdev.h"

// Télémètre ultrasons
#include "HC_SR04.h"

// Lidar
#include "VL53L0X.h"

// Analog input pin du télémètre infrarouge
# define IR_ANALOG_PIN 0

// Initialisation du télémètre ultrasons
#define TRIG_PIN 7
#define ECHO_PIN 2
#define ECHO_INT 0

HC_SR04 telemetre(TRIG_PIN, ECHO_PIN, ECHO_INT);

VL53L0X lidar;

int ret;
void setup() {
    // Port série
    Serial.begin(115200);
    Serial.println("Port serie initialise");

    // Initialise I2C
    Fastwire::setup(400,0);

    // Télémètre
    telemetre.begin();
    
    // Lidar
    lidar.init();
    lidar.setTimeout(500);
    lidar.setMeasurementTimingBudget(38000);
    lidar.setSignalRateLimit(0.30);
    
    lidar.startContinuous();
    
    Serial.print("Lidar timing budget: "); Serial.println(lidar.getMeasurementTimingBudget());
    Serial.print("Lidar signal rate limit: "); Serial.println(lidar.getSignalRateLimit());
    
    // Le reste
    ret = mympu_open(200);
    Serial.print("MPU init: "); Serial.println(ret);
    Serial.print("Free mem: "); Serial.println(freeRam());

    telemetre.start();	
}

unsigned int c = 0; //cumulative number of successful MPU/DMP reads
unsigned int np = 0; //cumulative number of MPU/DMP reads that brought no packet back
unsigned int err_c = 0; //cumulative number of MPU/DMP reads that brought corrupted packet
unsigned int err_o = 0; //cumulative number of MPU/DMP reads that had overflow bit set

unsigned long last_time = 0;  // horloge lors de la dernière mesure du télémètre IR

void loop() {
  
    // Lecture du télémètre IR
    unsigned long current_time = millis();
    if ( (current_time - last_time) > 5 ) {
      last_time = current_time;
      Serial.println("~");
      Serial.println(analogRead(IR_ANALOG_PIN));
    }
    
    // Lecture du gyro
    ret = mympu_update();

    switch (ret) {
	case 0: c++; break;
	case 1: np++; return;
	case 2: err_o++; return;
	case 3: err_c++; return; 
	default: 
		Serial.print("READ ERROR!  ");
		Serial.println(ret);
		return;
    }
    
    // Lecture du télémètre
    if (telemetre.isFinished()) {
       Serial.println("#");
       Serial.println(telemetre.getRange());
       telemetre.start();	
    }

    // Ecriture des résultats du lidar et du gyro
    if (!(c%8)) {  // Toutes les 8 mesures de gyro
            // Lecture du lidar
            Serial.println("{");
            Serial.println(lidar.readRangeContinuousMillimeters());
	    //Serial.print(np); Serial.print("  "); Serial.print(err_c); Serial.print(" "); Serial.print(err_o);
	    //Serial.print(" Y: "); Serial.print(mympu.ypr[0]);
	    //Serial.print(" P: "); Serial.print(mympu.ypr[1]);
	    //Serial.print(" R: "); Serial.print(mympu.ypr[2]);
	    //Serial.print("\tgy: "); Serial.print(mympu.gyro[0]);
	    //Serial.print(" gp: "); Serial.print(mympu.gyro[1]);
	    //Serial.print(" gr: "); Serial.println(mympu.gyro[2]);
            // Ecriture des résultats du gyro
            Serial.println("@");
            Serial.println(mympu.ypr[0]);
            Serial.println(mympu.ypr[1]);
            Serial.println(mympu.ypr[2]);
    }
}

