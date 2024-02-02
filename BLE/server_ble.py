from network import Bluetooth
from machine import Timer
import socket
import time
import binascii
import pycom


from pysense import Pysense
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2, ALTITUDE, PRESSURE

py = Pysense()
si = SI7006A20(py)
lt = LTR329ALS01(py)
li = LIS2HH12(py)

# Disable heartbeat LED
pycom.heartbeat(False)


luminosity = 25
update = False

def conn_cb(chr):
    events = chr.events()
    global update
    if events & Bluetooth.CLIENT_CONNECTED:
        print('client connected')
        update = True
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        print('client disconnected')
        update = False

def chr1_handler(chr, data):
    global luminosity
    global update
    events = chr.events()
    print("events: ",events)
    if events & (Bluetooth.CHAR_READ_EVENT | Bluetooth.CHAR_SUBSCRIBE_EVENT):
        chr.value(str(luminosity))
        print("transmitted :", luminosity)
        if (events & Bluetooth.CHAR_SUBSCRIBE_EVENT):
            update = True

bluetooth = Bluetooth()
bluetooth.set_advertisement(name='TP', manufacturer_data="Pycom", service_uuid=0xec00)

bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=conn_cb)
bluetooth.advertise(True)

srv1 = bluetooth.service(uuid=0xec00, isprimary=True,nbr_chars=1)

chr1 = srv1.characteristic(uuid=0xec0e, value='read_from_here') #client reads from here

chr1.callback(trigger=(Bluetooth.CHAR_READ_EVENT | Bluetooth.CHAR_SUBSCRIBE_EVENT), handler=chr1_handler)
print('Start BLE service')
def update_handler(update_alarm):
    global luminosity
    global update
    luminosity = lt.light()[0]
    if update:
        chr1.value(str(luminosity))
        print(luminosity)

update_alarm = Timer.Alarm(update_handler, 5, periodic=True)
