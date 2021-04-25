from django.db import models
from django.conf import settings

# Create your models here.


class Device(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    serial_number = models.CharField('Серийный номер', primary_key = True, max_length = 200, null = False)
    name = models.CharField('Название', max_length = 255, null = False)
    description = models.TextField('Описание', blank = True)
