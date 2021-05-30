from .models import *

def set_log(msg):
    mes = msg.payload.decode("utf-8")
    mes = mes.split(';')
    device = Device.objects.get(serial_number=mes[0])
    device_log = DeviceLog.objects.create(device = device, message = mes[1])
    device_log.save()
    

def set_config(msg):
    mes = msg.payload.decode("utf-8")
    ms = mes.split(';')
    device = Device.objects.get(serial_number=ms[0])
    device.config = mes
    device.save()
