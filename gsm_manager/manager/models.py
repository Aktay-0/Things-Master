from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.


class Device(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    serial_number = models.CharField('Серийный номер', primary_key = True, max_length = 200, null = False)
    name = models.CharField('Название', max_length = 255, null = False)
    description = models.TextField('Описание', blank = True)
    config = models.TextField('Конфигурация устройства', blank = True)

class DeviceLog(models.Model):
    device = models.ForeignKey('Device', on_delete = models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    message = models.TextField('Сообщение', blank = True)
