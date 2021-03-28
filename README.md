# BusyBot and Buttonbot

Display any message on a Pimoroni Scroll pHAT HD using MQTT

## Client

### Hardware

For BusyBot (display messages):

- Raspberry Pi Zero W
- Raspberry Pi OS Lite
- Pimoroni Scroll pHAT HD

For ButtonBot (send messages with a single click):

- Raspberry Pi Zero W
- Raspberry Pi OS Lite
- 3-Key Keybow

### Requirements

- MQTT Broker (such as Mosquitto)

Mosquitto will run happily on a Pi Zero, so if you don't have/don't want an MQTT
broker for general use, just install it on BusyBot.

## BusyBot

### Install Dependancies

```
sudo apt -y update && sudo apt -y full-upgrade
sudo apt install git python3-pip
sudo pip3 install paho-mqtt
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

...will start busybot listening to the topic `busybot` on the MQTT server located at `192.168.0.1`

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

## ButtonBot

ButtonBot is a device for sending pre-canned messages to BusyBot with a single
keypress. It is based on a Raspberry Pi Zero W with a Pimoroni 3-Button Keybow.

### Install Dependancies

```
sudo apt -y update && sudo apt -y update
sudo apt install git python3_pip
sudo pip3 install keybow paho-mqtt
```

### Installation

```
cd
git clone https://github.com/mrpjevans/busybot.git
cd busybot
```

You can now do a test run. Check out the options available:

```
python3 buttonbot.py -h
```

For example:

```
python3 buttonbot.py -b 192.168.0.1 -c BB1 -t busybot
```

...will start button publishing to the topic `busybot` on the MQTT server located at `192.168.0.1`

### Usage

The code comes with three messages pre-loaded. Have a look at the code for easy customisation of
the messages.

Having run up buttonbot, press any button to switch its message 'on'. Hopefully it will
start scrolling on BusyBot. Press again to cancel or another button to switch.

### Running as a Service

To have ButtonBot startup at boot time:

```
sudo nano /usr/lib/systemd/buttonbot.service
```

Add the following:

```
[Unit]
Description=buttonbot

[Service]
ExecStart=/usr/bin/python3 /home/pi/busybot/buttonbot.py -b <host> -c <client_id> -t <topic>
Restart=on-failure
User=pi
Group=pi

[Install]
WantedBy=multi-user.target
```

Save and quit, then from the command line:

```
sudo systemctl enable /usr/lib/systemd/buttonbot.service
sudo systemctl start buttonbot
```
