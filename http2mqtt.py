#!/usr/bin/env python3

import cherrypy
import paho.mqtt.client as mqtt
import configparser

class HTTP2MQTT(object):
    def __init__(self, mqtt_client, allowed_topics, allowed_payloads):
        self.mqtt_client = mqtt_client
        self.allowed_topics = allowed_topics
        self.allowed_payloads = allowed_payloads

    @cherrypy.expose
    def index(self):
        return "OK"

    @cherrypy.expose
    def http2mqtt(self, topic=None, payload=""):
        if topic in self.allowed_topics:
            print("Topic: {}".format(topic))
        else:
            return "Invalid topic"

        #if payload.isalnum():
        if payload in self.allowed_payloads:
            print("Payload: {}".format(payload))
        else:
            return "Invalid payload"
        
        self.mqtt_client.publish(topic, payload=payload)

        return "OK"

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")

    username  = config['mqtt-server']['username']
    password  = config['mqtt-server']['password']
    host      = config['mqtt-server']['host']
    port      = int(config['mqtt-server']['port'])
    client_id = config['mqtt-server']['client_id']
    ca_certs  = config['mqtt-server']['ca_certs']

    allowed_topics = config['http']['allowed_topics'].split(';')
    allowed_payloads = config['http']['allowed_payloads'].split(';')

    mqtt_client = mqtt.Client(client_id=client_id)
    mqtt_client.username_pw_set(username, password=password)
    mqtt_client.tls_set(ca_certs=ca_certs)
    mqtt_client.connect(host, port, 60)

    cherrypy.quickstart(
            HTTP2MQTT(
                mqtt_client,
                allowed_topics,
                allowed_payloads
                )
            )

    mqtt_client.disconnect()
