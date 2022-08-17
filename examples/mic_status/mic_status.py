#!/usr/bin/env python3

# _____________________________________________________________________.
#/                                                                     |
#|     Author:    Young-Jae Cho                                        |
#|     Version:   0.1                                                  |
#|     Purpose:   Visualize mic mute status in the statusbar.          |
#|                Status is set via mqtt message.                      |
#|                                                                     |
#|_____________________________________________________________________|


import paho.mqtt.client as mqtt
import random
import threading

import rumps

rumps.debug_mode(False)

@rumps.clicked('Icon', 'On')
def mute(_):
    app.icon = 'mic_mute.png'

@rumps.clicked('Icon', 'Off')
def unmute(_):
    app.icon = 'mic_unmute.png'

app = rumps.App('', quit_button=rumps.MenuItem('Quit', key='q'))

class MqttTemplate():
    TPMENUTEXT = "statusbar/muted"

    def __init__(self, name, host = "localhost", port = 1883):
        self.name = name.replace(" ","") + f"-{str(random.randint(0, 10000))}"
        self.mqtt_host = host
        self.mqtt_port = port
        print("trying to connect to: " + host + ":" + str(port))
        self.client  = mqtt.Client(self.name)
        self.client.on_connect=self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.mqtt_host, self.mqtt_port)
        print("init done...")

        print("will loop the mqtt loop...")
        threading.Thread(target=self.client.loop_forever).start()
        mute("")

    def on_connect(self, client, userdata, flags, rc):
        print(self.name + " connected to MQTT broker: " + self.mqtt_host + ":" + str(self.mqtt_port))
        self.client.subscribe(self.TPMENUTEXT)

    def send_msg(self, msg):
        print(msg)
        self.client.publish(self.TPMENUTEXT, msg)

    def on_message(self, client, userdata, message):
        if self.TPMENUTEXT in message.topic:
            muted = message.payload.decode('utf-8')
#            print(f"received muted status: {muted}")
            if muted == "1":
                mute("")
            else:
                unmute("")

mqtt = MqttTemplate('statusbar')

app.run()

