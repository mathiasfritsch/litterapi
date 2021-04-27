import sys
import network
import utime
import urequests
import machine
import ntptime
from machine import Pin, ADC
import ujson

def setleds(leds):
  print(leds)
  for binIndex in range(4):
      utime.sleep_ms(100)
      pinData.value(leds[binIndex])
      utime.sleep_ms(100)
      pinClock.value(1)
      utime.sleep_ms(100)
      pinClock.value(0)
try:
  utime.sleep_ms(1000 * 10 )

  battery = ADC(Pin(32))
  battery.atten(ADC.ATTN_11DB)  #Full range: 3.3v
  battery_value = battery.read()
  battery_voltage = (battery_value/4095.) * 2 * 3.3
  print(battery_voltage )

  wifi_ssid = ""
  wifi_password = ""

  station = network.WLAN(network.STA_IF)
  station.active(True)
  station.connect(wifi_ssid, wifi_password)
  maxloop = 10
  utime.sleep_ms(3000)
  print(station.isconnected() )

  while not station.isconnected() and maxloop > 0:
      maxloop -= 1
      print(maxloop)
      utime.sleep_ms(3000)

  bins = ["green","red","blue", "yellow"]
  results =  [0, 0, 0, 0]

  post_data = ujson.dumps({ 'voltage': battery_voltage })
  print(post_data)

  r = urequests.post("https://litterapi.azurewebsites.net/api/Battery",
    headers = {'content-type': 'application/json'},
    data=post_data)

  r.close()

  for binIndex in range(4):
    r = urequests.get("https://litterapi.azurewebsites.net/api/LitterDate/" + bins[binIndex] )
    if r.text == "1":
      results[binIndex] = 1
    r.close()

  print(results)

  pinClock = Pin(2, Pin.OUT) 
  pinData = Pin(4, Pin.OUT) 

  pinClock.value(0) 
  pinData.value(0) 

  setleds( [0, 0, 0, 0])
  setleds( [1, 1, 1, 1])
  setleds(results)

  utime.sleep_ms(1000 * 2 )

  setleds( [0, 0, 0, 0])
  setleds( [1, 1, 1, 1])
  setleds(results)

  utime.sleep_ms(1000 * 2 )

  setleds( [0, 0, 0, 0])
  setleds( [1, 1, 1, 1])
  setleds(results)

  utime.sleep_ms(1000 * 10 )

finally:
  print('ok')
  machine.deepsleep(1000 * 60 * 60 )
