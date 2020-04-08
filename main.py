import sys
import network
import utime
import urequests
import machine
import ntptime
from machine import Pin

wifi_ssid = ""
wifi_password = ""

station = network.WLAN(network.STA_IF)
station.active(True)

while not station.isconnected():
    station.connect(wifi_ssid, wifi_password)
    utime.sleep_ms(300)

ntptime.settime()
rtc = machine.RTC()
date = rtc.datetime()
utcOffset = 1
time = date[4] + utcOffset

bins = ["red", "green", "yellow","blue"]
results =  [0, 0, 0, 0]

allwaysRequestData = False
allwaysRequestData = True

if time > 16 and time < 20 or time > 6 and time < 9 or allwaysRequestData:
  for binIndex in range(4):
    r = urequests.get("https://litterapi.azurewebsites.net/api/LitterDate/" + bins[binIndex] )
    print(r.text)
    if r.text == "1":
      results[binIndex] = 1
    r.close()

print(results)

pinClock = Pin(2, Pin.OUT) 
pinData = Pin(4, Pin.OUT) 

pinClock.value(0) 
pinData.value(0) 

for binIndex in range(4):
    utime.sleep_ms(100)
    pinData.value(results[binIndex])
    utime.sleep_ms(100)
    pinClock.value(1)
    utime.sleep_ms(100)
    pinClock.value(0)