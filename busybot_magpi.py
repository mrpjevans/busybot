import time
import scrollphathd
import paho.mqtt.client as mqtt

# Change these to suit your needs
broker = '192.168.0.100'
client_name = 'busybot'
topic = 'study/busybot'
brightness = 0.1

current_message = ''


def scroll_message():
    # Original function by Pimoroni x
    global current_message
    while True:

        # No message? Don't do anything.
        if len(current_message) is 0:
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
    global current_message
    print('MQTT Message received')
    current_message = message.payload.decode("utf-8")
    if len(current_message) == 0:
        print('Clearing message')
    else:
        print('Scrolling ' + current_message)


print('Starting')
client = mqtt.Client(client_name)
client.connect(broker)
client.subscribe(topic)
client.on_message = on_message

print('Listening to ' + topic)
client.loop_start()

scrollphathd.set_brightness(brightness)
scroll_message()
