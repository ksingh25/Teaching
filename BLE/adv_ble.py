import ubinascii
from network import Bluetooth
from time import sleep

bluetooth = Bluetooth()
bluetooth.init()

#stop scanning if scanning is active
if bluetooth.isscanning():
    bluetooth.stop_scan()

bluetooth.set_advertisement(name="Machine a Cafe", manufacturer_data="Pret a lemploi")

bluetooth.advertise(True)