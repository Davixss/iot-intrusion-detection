import serial
import time
import json
import threading
from Config import *
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# Alarm triggered
alarm_triggered = '0'

# Serial port config
serial_port = 'COM10'
baud_rate = 9600
ser = serial.Serial(serial_port, baud_rate)

# MQTT topic
sub_topic = "ArduinoSensors/sub"
pub_topic = "ArduinoSensors/pub"


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
                my_mqtt_client.publish(pub_topic, json.dumps(sensor_data), 0)
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
    my_mqtt_client.subscribe(sub_topic, 0, readMessages)
    print(">> Client subscribed to ArduinoSensors topic")

    # To loop message broadcasting
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    # Program interrupt when is pressed CTRL+C
    my_mqtt_client.disconnect()
    ser.close()
    print("\nDisconnected from broker AWS IoT.")
