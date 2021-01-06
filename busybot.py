import time
import scrollphathd
import paho.mqtt.client as mqtt

broker = "192.168.0.100"
topic = "study/busybot"

def scroll_message(message):
    print('Scrolling ' + message)
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
  scroll_message(message.payload.decode("utf-8"))

client = mqtt.Client("busybot")
client.connect(broker)
client.subscribe("study/busybot")
client.on_message = on_message
client.loop_start()

while True:
  pass
