###################################   README    ################################

Title:
IoT-based Smart Intrusion Detection and Notification System for Industry 4.0


———————————————————————————————————————————


Project Description:
The following project aims to develop an intrusion detection system for the Smart Industry, utilizing IoT
technologies, in order to ensure enhanced security within industrial environments. The system will
continuously monitor industrial sensors, detecting intrusions and promptly sending notifications to
operators through various IoT communication systems. Additionally, to provide an extra layer of
prevention and security against Man-In-The-Middle (MITM) attacks, version 5 of the MQTT protocol
has been employed, with authentication through certificates.

The project features are outlined below:

- Intrusion Detection Sensors
- Alarms and Notifications
- MQTT Protocol
- Remote Control
- Data Storage
- System Activity Monitoring


———————————————————————————————————————————


How to Configure, Install Run the Project

Arduino
1. Install Arduino IDE from the following link: https://www.arduino.cc/en/software
2. Connect the Arduino Board, via the USB port, to the Machine
3. Go to this project repository https://github.com/Davixss/iot-intrusion-detection by following
   the path /Code/Arduino/Arduino Code (.c)
5. Copy the code contained within sketch_IoT.ino into the Arduino IDE
6. Compile it and eterxecute it into the Arduino Board
7. Close the Arduino IDE for preventing any kind of conflict with serials communication


AWS
1. Install AWS from the following link: https://aws.amazon.com/it/
2. Login to the account by entering the following credentials:
     - Email: davide.allegra@studenti.unime.it
     - Password: Industrialiot2023!
3. Enter "IoT Core" module
4. Switching the location to Europe (Frankfurt) eu-central-1
5. For project purpose you can use the already existing things, otherwise you are allowed to
   create a new brand custom thing
6. Eventually you can use the MQTT client test


InfluxDB
1. Install InfluxDB from the following link: eu-central-1-1.aws.cloud2.influxdata.com
2. Create an account (you are allowed to create a free account for the duration of one month)
3. Within the Database you can creare a bucket wherein time series data is stored, capable of
   housing multiple measurements, which represent a cohesive classification for time series data
4. In a measurement you can insert multiple tags and fields.
   Since InfluxDB is a time series database, it is equipped of a chronological indicator linked to
   the data, called Timestamp
5. You can replace the InfluxDB configuration within the Config.py file


PyCharm 
1. Install PyCharm IDE from the following link: https://www.jetbrains.com/pycharm/download/
2. Once the installation has completed, create a new project
3. Install all the dependencies needed for the correct project configuration by running the
   following commands on a terminal:
     - pip install pyserial
     - pip install requests
     - pip install AWSIoTPythonSDK
     - pip install influxdb-client
4. Go to this project repository https://github.com/Davixss/iot-intrusion-detection by following
   the path /Code/Arduino/Arduino Reader (.py)
5. Upload the whole folder into the PyCharm Project
6. Run the MQTT.py file ensuring the Arduino Board is still properly connected to the USB port


MQTT - TLS IoT Tool
1. Download and Install TLS IoT Tool from the App Store (iOS) or Google Play Store (Android)
2. Go to settings and set the following parameters:
     - Home Title: Set your own title  
     - MQTT Endpoint: Set the AWS ARN Endpoint
     - Client ID: name of your AWS thing
     - Certificate: insert your own AWS Certificate
     - Private Key: insert your own AWS Private Key
     - Root CA: insert your own AWS Root CA
     - Timestamp Key: no configuration (leave this space blank)
3. Create a button and set the following parameters:
     - Title: Set your own title (command)
     - MQTT Topic: Set your own MQTT Topic path
     - Message: {"message": "set your own message or command"}
