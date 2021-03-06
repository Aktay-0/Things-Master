from django.shortcuts import render
from django.shortcuts import redirect
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout
from . import mqtt
import time

# Create your views here.

def get_config(data):
    conf = {}
    dt = data.split(',')
    for i in dt:
        bf = i.split('|')
        conf[bf[1]] = bf[2]
    return conf

def auth(operation):
    def check_auth(request):
        if not request.user == None:
            if request.user.is_authenticated:
                return operation(request)
            else:
                return redirect('/login')
        else:
            return redirect('/login')
    return check_auth

def go_to_index(operation):
    def go_index(request):
        if not request.user == None:
            if request.user.is_authenticated:
                return redirect('/')
            else:
                return operation(request)
        else:
            return operation(request)
    return go_index

@auth
def index(request):
    devices = Device.objects.filter(user = request.user)
    return render(request, 'manager/index.html', { 'title': 'GSM Manager', 'devices': devices})

@go_to_index
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            if user is not None:
                if user.is_active:
                    login_user(request, user)
                    return redirect('/')
    form = RegistrationForm()
    return render(request, 'manager/register.html', { 'title': 'Register', 'form': form})

@go_to_index
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login_user(request, user)
                    return redirect('/')
    form = LoginForm()
    return render(request, 'manager/login.html', { 'title': 'Login', 'form': form})

@auth
def logout_user(request):
    logout(request)
    return redirect('/login')

@auth
def device(request):
    if request.method == 'POST':
        serial = request.POST['serial']
        device = Device.objects.get(serial_number=serial)
        form = DeviceEditForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            device.name = name
            device.description = description
            device.save()
            return redirect('/device?serial=' + device.serial_number)
    serial = request.GET['serial']
    device = Device.objects.get(serial_number=serial)
    form = DeviceEditForm({'name': device.name, 'description': device.description})
    config = device.config
    config = get_config(config)
    form_config = DeviceConfigForm(config)
    logs = DeviceLog.objects.filter(device=device).order_by('-date')
    return render(request, 'manager/device.html', { 'title': 'Device', 'device': device, 'form': form, 'logs': logs, 'form_config': form_config})

@auth
def device_register(request):
    if request.method == 'POST':
        form = DeviceRegistrationForm(request.POST)
        if form.is_valid():
            serial_number = form.cleaned_data.get('serial_number')
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            if Device.objects.filter(serial_number=serial_number).count() == 0:
                device = Device.objects.create(user=request.user, serial_number=serial_number, name=name, description=description)
                device.save()
                return redirect('/')
            return redirect('/device-register')
    form = DeviceRegistrationForm()
    return render(request, 'manager/register_device.html', { 'title': 'Device Register', 'form': form})

@auth
def profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            old_password = form.cleaned_data.get('old_password')
            new_password = form.cleaned_data.get('new_password')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            user = authenticate(request, username=request.user.username, password=old_password)
            if user is not None:
                if user.is_active:
                    user.username = username
                    user.set_password(new_password)
                    user.email = email
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                    login_user(request, user)
                    return redirect('/profile')
    user = User.objects.get(username=request.user.username)
    form = UserEditForm({'username': user.username, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name})
    return render(request, 'manager/profile.html', { 'title': 'Profile', 'form': form})

@auth
def save_config(request):
    if request.method == 'POST':
        serial = request.POST['serial']
        form = DeviceConfigForm(request.POST)
        if form.is_valid():
            data = serial + ';'
            conf = form.cleaned_data
            for i in conf:
                data += 'type|' + i + '|' + str(conf[i]) + ','
            data = data[:-1]
            #device = Device.objects.get(serial_number=serial)
            #device.config = data
            #device.save() 
            mqtt.client.publish("device/config", data)
            time.sleep(1)
            return redirect('/device?serial=' + serial)
    return redirect('/')

