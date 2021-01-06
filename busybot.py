import time
import scrollphathd
import paho.mqtt.client as mqtt

# Chnage these to suit your needs
broker = "192.168.0.100"
client_name = "busybot"
topic = "study/busybot"


# Original function by Pimoroni x
def scroll_message(message):
    print('Scrolling "' + message + '"')
    # Clear the display and reset scrolling to (0, 0)
    scrollphathd.clear()
    length = scrollphathd.write_string(message)  # Write out your message
    scrollphathd.show()                          # Show the result
    # Initial delay before scrolling
    time.sleep(0.5)

    length -= scrollphathd.width

    # Now for the scrolling loop...
    while length > 0:
        # Scroll the buffer one place to the left
        scrollphathd.scroll(1)
        scrollphathd.show()                      # Show the result
        length -= 1
        # Delay for each scrolling step
        time.sleep(0.02)

    # Delay at the end of scrolling
    time.sleep(0.5)


def on_message(client, userdata, message):
  print('MQTT Message received')
  scrollphathd.clear()
  length = scrollphathd.write_string(message.payload.decode("utf-8"))  # Write out your message
  scrollphathd.show()                          # Show the result
  print('Displayed ' + message.payload.decode("utf-8"))

print('Starting')
client = mqtt.Client(client_name)
client.connect(broker)
client.subscribe(topic)
client.on_message = on_message

print('Listening to ' + topic)
client.loop_forever()
