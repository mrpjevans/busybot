# BusyBot

Display any message on a Pimoroni Scroll pHAT HD using MQTT

## Client

### Hardware

- Raspberry Pi Zero W
- Raspberry Pi OS Lite
- Pimoroni Scroll pHAT HD

### Requirements

- MQTT Broker (such as Mosquitto)

### Install Dependancies

```
sudo apt -y update && sudo apt -y update
sudo apt install git python3_pip
pip install paho-mqtt
curl https://get.pimoroni.com/scrollphathd | bash
sudo pip3 install smbus
```

### Installation

```
cd
git clone https://github.com/mrpjevans/busybot.git
cd busybot
```

You can now do a test run. Check out the options available:

```
python3 busybot.py -h
```

For example:

```
python3 busybot.py -b 192.168.0.1 -c BB1 -t busybot
```

...will start busybot listening to the top `busybot` on the MQTT server located at `192.168.0.1`

### Pushing messages

To display a message on the Scroll pHAT HD, just publish the message to the chosen topic on the MQTT
server. For example using Mosquitto's command line tools:

```
mosquitto_pub -h 192.168.0.1 -t busybot -m "Hello, world"
```

This should cause "Hello, world" to be displayed repeatedly on the display.

To clear the display, send an empty payload:

```
mosquitto_pub -h 192.168.0.1 -t busybot -m ""
```

### Running as a Service

To have BusyBot startup at boot time:

```
sudo nano /usr/lib/systemd/busybot.service
```

Add the following:

```
[Unit]
Description=busybot

[Service]
ExecStart=/usr/bin/python3 /home/pi/busybot/busybot.py -b <host> -c <client_id> -t <topic>
Restart=on-failure
User=pi
Group=pi

[Install]
WantedBy=multi-user.target
```

Save and quit, then from the command line:

```
sudo systemctl enable /usr/lib/systemd/busybot.service
sudo systemctl start busybot
```
