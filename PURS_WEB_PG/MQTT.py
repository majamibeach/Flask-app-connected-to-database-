import paho.mqtt.client as mqtt
import re
import time

Broker = '192.168.137.15'
last_called = 0
msg_ = ""

def mqttpodaci(msg):
    main.mqttpodaci(msg)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    client.subscribe("/DataToServer")

def on_message(client, userdata, message):
    #print("Received message '" + str(message.payload) + "' on topic '" + message.topic)
    #global 
    msg = str(message.payload)
    msg = msg.replace('b','')
    msg = msg.replace("'",'')
    #print(msg)

    match = re.match(r'([A-Za-z]+)(#.+)-(\d+)\+(\d+)', msg)

    if match:
        substring = match.groups()

    global last_called
    current_time = time.time()
    if current_time - last_called > 2:
        import main
        main.parsingFun(substring)
        last_called = current_time

def on_disconnect(client, userdata, message):
    client.loop_stop(force=False)
    if message != 0:
        print("Unexpected disconnection.")
    else:
        print("Disconnected")

def main():
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.on_disconnect = on_disconnect

    #mqtt_client.connect('localhost', 1883, 60) Broker = '192.168.137.15'
    mqtt_client.connect(Broker, 1883, 60)
    # Connect to the MQTT server and process messages in a background thread. 
    mqtt_client.loop_start()

if __name__ == '__main__':
    
    print('MQTT to InfluxDB bridge')
  