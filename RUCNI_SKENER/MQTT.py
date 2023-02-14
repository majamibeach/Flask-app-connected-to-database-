import paho.mqtt.client as mqtt

m=""

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    client.subscribe("/esp32/mass")

def on_message(client, userdata, message):
    print("Received message '" + str(message.payload) + "' on topic '" + message.topic)
    mass = str(message.payload)
    mass = mass.replace('b','')
    global m
    m=mass

def main():
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect('localhost', 1883, 60) 
    # Connect to the MQTT server and process messages in a background thread. 
    mqtt_client.loop_start()
    
def get_mass():
    #c = str(message.payload)
    return m

if __name__ == '__main__':
    
    print('MQTT to InfluxDB bridge')
    main()