import time
import scrollphathd
import paho.mqtt.client as mqtt
import argparse

parser = argparse.ArgumentParser(
    description="Display messages from an MQTT topic on a Scroll pHAT HD")
parser.add_argument("-b", "--broker", type=str,
                    help="Address of MQTT broker (default 127.0.0.1)", default="127.0.0.1")
parser.add_argument("-c", "--client", type=str,
                    help="Client name (default 'busybot')", default="busybot")
parser.add_argument("-t", "--topic", type=str,
                    help="Topic to subscribe to (default 'busybot')", default="busybot")
parser.add_argument("--brightness", type=float,
                    help="Brightness (0.1 - 1) (default 0.1)", default=0.1)
parser.add_argument("-f", "--flip", action="store_true",
                    help="Flip the display")
args = parser.parse_args()

# Change these to suit your needs
broker = args.broker
client_name = args.client
topic = args.topic
brightness = args.brightness
flip = args.flip

new_message = ''


def scroll_message():
    # Original function by Pimoroni x
    global new_message
    current_message = ''

    while True:

        # If moving to a blank message, clear the display
        if current_message != '' and new_message == '':
            scrollphathd.clear()
            scrollphathd.show()

        # Update our current message
        if current_message != new_message:
            current_message = new_message

        # No message? Don't do anything.
        if current_message == '':
            time.sleep(1)
            continue

        # Clear the display and reset scrolling to (0, 0)
        scrollphathd.clear()
        length = scrollphathd.write_string(current_message)
        scrollphathd.show()
        time.sleep(0.5)

        length -= scrollphathd.width

        # Now for the scrolling loop...
        while length > 0:
            # Scroll the buffer one place to the left
            scrollphathd.scroll(1)
            scrollphathd.show()
            length -= 1
            time.sleep(0.02)

        time.sleep(0.5)


def on_message(client, userdata, message):
    global new_message
    print('MQTT Message received')
    new_message = message.payload.decode("utf-8")
    if len(new_message) == 0:
        print('Clearing current message')
    else:
        print('Scrolling ' + new_message)


print('Starting')
client = mqtt.Client(client_name)
client.connect(broker)
client.subscribe(topic)
client.on_message = on_message

print('Listening to ' + topic)
client.loop_start()

scrollphathd.set_brightness(brightness)
scrollphathd.flip(flip, flip)

scrollphathd.write_string('Ok')
scrollphathd.show()
time.sleep(1)

scroll_message()
