import sys
import network
import utime
import urequests


wifi_ssid = ""
wifi_password = ""

station = network.WLAN(network.STA_IF)
station.active(True)

while not station.isconnected():
    station.connect(wifi_ssid, wifi_password)
    utime.sleep_ms(300)



r = urequests.get("https://litterapi.azurewebsites.net/api/LitterDate/green")
print(r.text)

r.close()