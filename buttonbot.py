#!/usr/bin/env python
import keybow
import paho.mqtt.client as mqtt
import argparse
import time

# Messages to send - customise as needed!
status_messages = [
    'Zooming',
    'Busy',
    'Headphones on'
]
current_message = -1

parser = argparse.ArgumentParser(
    description="Send messages to an MQTT broker from a Keybow")
parser.add_argument("-b", "--broker", type=str,
                    help="Address of MQTT broker (default 127.0.0.1)", default="127.0.0.1")
parser.add_argument("-c", "--client", type=str,
                    help="Client name (default 'buttonbot')", default="buttonbot")
parser.add_argument("-t", "--topic", type=str,
                    help="Topic to subscribe to (default 'busybot')", default="busybot")
args = parser.parse_args()
broker = args.broker
client_name = args.client
topic = args.topic

keybow.setup(keybow.MINI)


@keybow.on()
def handle_key(index, state):
    global current_message, client, topic, status_messages

    if state:
        for i in range(3):
            if i == index:
                if i == current_message:
                    # Cancel
                    current_message = -1
                    keybow.set_led(i, 0, 0, 0)
                    client.publish(topic, " ")
                else:
                    keybow.set_led(i, 255, 0, 0)
                    current_message = index
                    client.publish(topic, status_messages[i])
            else:
                keybow.set_led(i, 0, 0, 0)

        print("Message ID now %s" % current_message)


client = mqtt.Client(client_name)
client.connect(broker)
print("Sending to topic " + topic + " on broker " + broker)

while True:
    keybow.show()
    time.sleep(1.0 / 60.0)
