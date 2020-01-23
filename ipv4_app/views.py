from django.shortcuts import render
from .forms import IndexForm

# Create your views here.


def index(request):
    form = IndexForm()
    return render(request, 'index.html', {'form': form})


def dec_to_bin(decimal):
    return bin(decimal)[2:]


def bin_to_dec(binary):
    return int(binary, 2)


def split_octets(ip):
    octets = []
    octets = ip.split('.')
    return octets


def ip_class(ip):
    ip_class = ''
    octet = int(split_octets(ip)[0])
    if 1 <= octet <= 126:
        ip_class = 'A'
    elif 128 <= octet <= 191:
        ip_class = 'B'
    elif 192 <= octet <= 223:
        ip_class = 'C'
    return ip_class


def ip_type(ip):
    ip_type = ''
    octet1 = int(split_octets(ip)[0])
    octet2 = int(split_octets(ip)[1])
    if octet1 == 10:
        ip_type = 'Private'
    elif octet1 == 172 and 16 <= octet2 <= 31:
        ip_type = 'Private'
    elif octet1 == 192 and octet2 == 168:
        ip_type = 'Private'
    else:
        ip_type = 'Public'
    return ip_type


data = {}


def result(request):
    global data
    if request.method == 'POST':
        form = IndexForm(request.POST)
        if form.is_valid():
            data['ip'] = form.cleaned_data.get('ip_address')
            data['qty'] = form.cleaned_data.get('quantity')
            data['opt'] = form.cleaned_data.get('option')
        else:
            data = {'form': form}
            return render(request, 'index.html', data)
    if data['opt'] == 'hosts':
        data['inv_opt'] = 'subnets'
    else:
        data['inv_opt'] = 'hosts'
    data['class'] = ip_class(data['ip'])
    data['type'] = ip_type(data['ip'])
    return render(request, 'result.html', data)
