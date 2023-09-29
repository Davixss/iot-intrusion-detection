import serial
import requests
import time
import json
import threading
import random
import datetime
from Config import *
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from influxdb_client_3 import InfluxDBClient3, Point

# Alarm triggered
alarm_triggered = '0'

# Serial port config
serial_port = 'COM10'
baud_rate = 9600
ser = serial.Serial(serial_port, baud_rate)

# MQTT topic
sub_topic = "ArduinoSensors/sub"
pub_topic = "ArduinoSensors/pub"

# InfluxDB Connection
client = InfluxDBClient3(host=Config.host_influx, token=Config.token_influx, org=Config.org_influx)


def readArduinoValues():
    while True:
        # Receiving Arduino data
        if ser.in_waiting > 0:
            alarm_triggered = ser.readline().decode().strip()
            if alarm_triggered == '1':
                # Publishing sensor data
                sensor_data = {
                    "message": "intrusion detected"
                }
                # Convert payload in JSON format
                my_mqtt_client.publish(pub_topic, json.dumps(sensor_data), 1)

                # Simulating other sensors
                types = ["Movement", "Noise", "Camera"]
                sensortype = random.choice(types)

                # Saving data into InfluxDB
                data_influx = {
                    "data": {
                        "Intrusion": "True",
                        "SensorType": sensortype
                    }
                }

                for key in data_influx:
                    point = (
                        Point("ArduinoData")
                        .tag("Intrusion", data_influx[key]["Intrusion"])
                        .field("SensorType", data_influx[key]["SensorType"])
                    )
                client.write(database=Config.bucket, record=point)

                # Sending email to the admins
                current_time = datetime.datetime.now()
                today = current_time.strftime('%d/%m/%Y %H:%M')
                emailBody = f"An intrusion was detected by the {sensortype} sensor at {today}"
                sendEmail(emailBody)

                print(f"System status: INTRUSION DETECTED!")
            else:
                print(f"System status: no events detected")
        time.sleep(1)


def readMessages(client, userdata, message):
    # Function called when a message is received
    payload = json.loads(message.payload)
    received_message = payload["message"]
    print(f">> MQTT Received Message: {received_message}")
    if received_message == "ENABLE_ALARM" or received_message == "DISABLE_ALARM" or received_message == "START_ALARM" or received_message == "STOP_ALARM":
        # Sending a welcome message to the board
        ser.write(received_message.encode())


def sendEmail(body):
    receivers = ",".join(Config.emails)
    url = f'{Config.altervista_host}/iot/sendEmail.php?receivers={receivers}&subject={Config.subject}&body={body}<br><br>'
    response = requests.get(url)
    if response.status_code == 200:
        print(">> [Email] Intrusion notification via email successfully sent")
    else:
        print(response.text)


thread = threading.Thread(target=readArduinoValues)
thread.start()


try:
    # Create a MQTT client
    my_mqtt_client = AWSIoTMQTTClient(Config.client_id)
    my_mqtt_client.configureEndpoint(Config.endpoint, 8883)
    my_mqtt_client.configureCredentials(Config.root_ca, Config.private_key, Config.certificate)

    # Broker AWS IoT connection
    my_mqtt_client.connect()
    print(">> MQTT broker connected")

    # Topic subscription
    my_mqtt_client.subscribe(sub_topic, 1, readMessages)
    print(">> Client subscribed to ArduinoSensors topic")

    # To loop message broadcasting
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    # Program interrupt when is pressed CTRL+C
    my_mqtt_client.disconnect()
    ser.close()
    print("\nDisconnected from broker AWS IoT.")
