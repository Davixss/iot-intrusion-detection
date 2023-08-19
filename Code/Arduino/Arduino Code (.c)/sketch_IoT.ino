#include <SoftwareSerial.h>

#define PIR 2
#define GreenLED 4
#define RedLED 5
#define buzzer 9
#define button 7  

#define WAIT_PIR_PREPARE 60000 //ms

SoftwareSerial mySerial(10, 11); // RX, TX

bool deviceIsReady = false;
bool alarmEnabled = true;
bool alarmTriggered = false;

void setup()
{
    mySerial.begin(9600);
    Serial.begin(9600);
    pinMode(RedLED, OUTPUT);
    pinMode(GreenLED, OUTPUT);
    pinMode(buzzer, OUTPUT);
    pinMode(PIR, INPUT);
    pinMode(button, INPUT); 
}

void loop()
{
    if(deviceIsReady)
    {
        if(alarmEnabled)
        {
            // Detecting the motion through PIR sensor
            int motionValue = digitalRead(PIR);

            // If a movement is detected return 1 otherwise return 0
            if(motionValue == HIGH)
            {
                if(alarmTriggered == false)
                {
                    // Send movement value through second port
                    mySerial.println(1);
                    Serial.println(1);
                    startAlarm();
                }
            }
            else
            {
                // Send movement value through second port
                mySerial.println(0);
                Serial.println(0);
            }
        }

        MQTT_checkMessages();
        checkButtonStatus();
        delay(1000);
    }
    else
    {
        // Waiting 1 minute for the PIR preparing
        LedBlinking();
    }
}

void checkButtonStatus()
{
    if(digitalRead(button) == HIGH)
    {
        if(alarmEnabled)
        {
            alarmEnabled = false;
            digitalWrite(GreenLED, LOW);
            Serial.println(">> Alarm disabled");
        }
        else 
        {
            alarmEnabled = true;
            digitalWrite(GreenLED, HIGH);
            Serial.println(">> Alarm enabled");
        }

        delay(1500);
    }
}

void changeSystemStatus(int status)
{
    if(status == 1)
    {
        if(alarmEnabled == false)
        {
            alarmEnabled = true;
            digitalWrite(GreenLED, HIGH);
            Serial.println(">> ALARM ENABLED");
        }
    }
    else 
    {
        if(alarmEnabled)
        {
            alarmEnabled = false;
            digitalWrite(GreenLED, LOW);
            Serial.println(">> ALARM DISABLED");
        }
    }
}

void startAlarm()
{
    if(alarmEnabled && alarmTriggered == false)
    {
        alarmTriggered = true;
        digitalWrite(RedLED, HIGH);
        for(int i=0; i<25; i++)
        {
            MQTT_checkMessages();
            checkButtonStatus();
            if(alarmTriggered && alarmEnabled)
            {
                tone(buzzer, 700);
                delay(200);
                noTone(buzzer);
                delay(200);
            }
            else break;
        }
        digitalWrite(RedLED, LOW);
        stopAlarm();
    }
}

void stopAlarm()
{
    if(alarmTriggered)
    {
        alarmTriggered = false;
        digitalWrite(RedLED, LOW);
        noTone(buzzer);
    }
}

void LedBlinking()
{
    // Alternate blinking LEDs for 1 minute
    unsigned long startTime = millis();
    while (millis() - startTime < WAIT_PIR_PREPARE)
    {
        digitalWrite(GreenLED, HIGH);
        digitalWrite(RedLED, LOW);
        delay(300);
        digitalWrite(GreenLED, LOW);
        digitalWrite(RedLED, HIGH);
        delay(300);
    }

    // Turn off the LEDs after 1 minute
    digitalWrite(GreenLED, HIGH);
    digitalWrite(RedLED, LOW);

    deviceIsReady = true;
}

void MQTT_checkMessages()
{
    if(Serial.available() > 0)
    {
        String message = readSerialMessage();

        // Process the message
        if(message.length() > 0)
        {
            // Perform some action based on the message content
            if(message.equals("ENABLE_ALARM"))
            {
                changeSystemStatus(1);
            }
            else if(message.equals("DISABLE_ALARM"))
            {
                changeSystemStatus(0);
            }
            else if(message.equals("START_ALARM"))
            {
                startAlarm();
            }
            else if(message.equals("STOP_ALARM"))
            {
                stopAlarm();
            }
        }
    }
}

String readSerialMessage()
{
    String message = "";
    char incomingChar;

    while (Serial.available() > 0)
    {
        incomingChar = Serial.read();

        // Read characters until the newline character is received
        if (incomingChar == '\n')
        {
            break; // Exit the loop when newline is received
        }

        // Append the character to the message
        message += incomingChar;
    }

    // Remove any leading or trailing whitespaces from the message
    message.trim();

    return message;
}
