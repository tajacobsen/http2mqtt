# http2mqtt

http2mqtt is a small web service that listens for http get requests and publishes mqtt messages.

The service can be run through docker with the command:
```shell
sudo docker run -it -v $HOME/http2mqtt:/config --network host [image id]
```

The config directory ($HOME/http2mqtt in this case) should contain a config.ini file.

Test the server with the command:
```
curl "http://localhost:9090/http2mqtt?topic=topic/topic&payload=payload"
```

## Using with myStrom
The web service was specifically written to translate http messages from a myStrom button to mqtt messages. This is possible with the configuration:
```ini
[mqtt-server]
username = mqtt-server-user
password = mqtt-server-password
host = mqtt.example.com 
port = 8883
client_id = http2mqtt
ca_certs = /etc/ssl/certs/ca-certificates.crt

[http]
port = 9090
allowed_topics = topics/mystorm
allowed_payloads = single;double;long
```

Note that `allowed_topics` and `allowed_payloads` whitlists allowed topics and payloads. All other requests will be ignored to avoid misuse.

The myStrom button should then be configured with the following commands:
```
curl -d "single=get://[hostname of server running http2mqtt]:9090/http2mqtt?topic=topics/mystorm&payload=single" http://[IP address of the button]/api/v1/device/[MAC address of the button]
curl -d "double=get://[hostname of server running http2mqtt]:9090/http2mqtt?topic=topics/mystorm&payload=double" http://[IP address of the button]/api/v1/device/[MAC address of the button]
curl -d "long=get://[hostname of server running http2mqtt]:9090/http2mqtt?topic=topics/mystorm&payload=long" http://[IP address of the button]/api/v1/device/[MAC address of the button]
```
