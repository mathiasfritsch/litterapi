import sys
import network
import utime
import urequests
import machine

wifi_ssid = ""
wifi_password = ""

station = network.WLAN(network.STA_IF)
station.active(True)

while not station.isconnected():
    station.connect(wifi_ssid, wifi_password)
    utime.sleep_ms(300)

bins = ["red", "green", "yellow","blue"]
results =  [False, False, False,False]
for binIndex in range(4):
  r = urequests.get("https://litterapi.azurewebsites.net/api/LitterDate/" + bins[binIndex] )
  print(r.text)
  if r.text == "1":
    results[binIndex] = True
print(results)

r.close()