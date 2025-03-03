'''
boot.py

ESP32  /ESP8266

'''

from machine import Pin, I2C
import BME280
import network
import urequests

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'Deine_SSID'
password = 'Dein_PASSWORT'

api_key = 'Deine_IFTTT_API_KEY'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Verbindung erfolgreich')
print(station.ifconfig())

# ESP32 - Pinbelegung
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=10000)
# ESP8266 - Pinbelegung
#i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000)

try:
  bme = BME280.BME280(i2c=i2c)
  temp = bme.temperature
  hum = bme.humidity
  pres = bme.pressure

  # Fahrenheit
  #temp = (bme.read_temperature()/100) * (9/5) + 32
  #temp = str(round(temp, 2)) + 'F'

  sensor_readings = {'value1':temp, 'value2':hum, 'value3':pres}
  print(sensor_readings)

  request_headers = {'Content-Type': 'application/json'}

  request = urequests.post(
    'http://maker.ifttt.com/trigger/bme280/with/key/' + api_key,
    json=sensor_readings,
    headers=request_headers)
  print(request.text)
  request.close()

except OSError as e:
  print('Fehler beim Lesen/Veröffentlichen von Sensormesswerten.')
