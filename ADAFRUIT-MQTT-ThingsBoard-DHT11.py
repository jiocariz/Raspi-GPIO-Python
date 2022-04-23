import os
import time
import sys
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import json
import board
import adafruit_dht
import psutil

THINGSBOARD_HOST = 'localhost'
ACCESS_TOKEN = 'DHT11_DEMO_TOKEN'
try:
    #Inicializamos la lectura del sensor
    sensor = adafruit_dht.DHT11(board.D27)
    #Inicializamos la estructura de datos
    sensor_data = {'temperatura': 0, 'humedad': 0}

    client = mqtt.Client()
    # Set access token
    client.username_pw_set("DHT11_DEMO_TOKEN")
    # Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
    client.connect("localhost", 1883, 60)
    client.loop_start()


    while True:
        try:
            sensor_data['temperatura'] = sensor.temperature
            sensor_data['humedad'] = sensor.humidity
            print("LECTURA DHT11: Temperature: {}*C   Humidity: {}% ".format(sensor_data['temperatura'], sensor_data['humedad']))
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:            
            raise error
        #Publicamos el mensaje al broker
        client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)

        time.sleep(0.5) #no tengo claro si pongo menos que el keepalive si se desconectaría
            
except KeyboardInterrupt:
    print("Ctrl+C pulsado")
except Exception as error:
    print("Se ha producido un error: " + error.args[0])
finally:
    print("Deshacemos gentilmente todo")
    sensor.exit()
    client.loop_stop()
    client.disconnect()
