#!/usr/bin/env python3

import cherrypy
import paho.mqtt.client as mqtt
import configparser

class HTTP2MQTT(object):
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client

    @cherrypy.expose
    def index(self):
        return "OK"

    @cherrypy.expose
    def http2mqtt(self, topic=None, payload=""):
        print("Topic: {}".format(topic))
        print("Payload: {}".format(payload))
        
        self.mqtt_client.publish(topic, payload=payload)

        return "OK"

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")

    username = config['mqtt-server']['username']
    password = config['mqtt-server']['password']
    host     = config['mqtt-server']['host']
    port     = int(config['mqtt-server']['port'])
    ca_certs = config['mqtt-server']['ca_certs']

    mqtt_client = mqtt.Client(client_id="http2mqtt")
    mqtt_client.username_pw_set(username, password=password)
    mqtt_client.tls_set(ca_certs=ca_certs)
    mqtt_client.connect(host, port, 60)

    cherrypy.quickstart(HTTP2MQTT(mqtt_client))

    mqtt_client.disconnect()
