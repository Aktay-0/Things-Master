# Generated by Django 3.1.3 on 2021-05-22 17:44

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('message', models.TextField(blank=True, verbose_name='Сообщение')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.device')),
            ],
        ),
    ]
