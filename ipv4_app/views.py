from django.shortcuts import render
from .forms import IndexForm
from math import log, ceil

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


def bin_octets(ip_mask):
    octets = split_octets(ip_mask)
    octet1 = dec_to_bin(int(octets[0])).rjust(8, '0')
    octet2 = dec_to_bin(int(octets[1])).rjust(8, '0')
    octet3 = dec_to_bin(int(octets[2])).rjust(8, '0')
    octet4 = dec_to_bin(int(octets[3])).rjust(8, '0')
    ip_mask = octet1 + '.' + octet2 + '.' + octet3 + '.' + octet4
    return ip_mask


def dec_octets(ip_mask):
    octets = split_octets(ip_mask)
    octet1 = str(bin_to_dec(octets[0]))
    octet2 = str(bin_to_dec(octets[1]))
    octet3 = str(bin_to_dec(octets[2]))
    octet4 = str(bin_to_dec(octets[3]))
    ip_mask = octet1 + '.' + octet2 + '.' + octet3 + '.' + octet4
    return ip_mask


def dec_mask(ip_class):
    if ip_class == 'A':
        dec_mask = '255.0.0.0'
    elif ip_class == 'B':
        dec_mask = '255.255.0.0'
    elif ip_class == 'C':
        dec_mask = '255.255.255.0'
    return dec_mask


def dec_wildcard(ip_class):
    if ip_class == 'A':
        dec_wildcard = '0.255.255.255'
    elif ip_class == 'B':
        dec_wildcard = '0.255.255.255'
    elif ip_class == 'C':
        dec_wildcard = '0.255.255.255'
    return dec_wildcard


def bits_opt(opt, qty):
    if opt == 'subnets':
        aux = log(int(qty), 2)
        bits_opt = int(ceil(aux))
    elif opt == 'hosts':
        aux = log((int(qty)+2), 2)
        bits_opt = int(ceil(aux))
    return bits_opt


def bits_inv_opt(ip_class, opt, qty):
    if ip_class == 'A':
        bits_inv_opt = 24 - bits_opt(opt, qty)
    elif ip_class == 'B':
        bits_inv_opt = 16 - bits_opt(opt, qty)
    elif ip_class == 'C':
        bits_inv_opt = 8 - bits_opt(opt, qty)
    return bits_inv_opt


def qty_opt(opt, qty):
    aux = pow(2, bits_opt(opt, qty))
    if opt == 'subnets':
        qty_opt = int(aux)
    elif opt == 'hosts':
        qty_opt = int(aux - 2)
    return qty_opt


def qty_inv_opt(ip_class, opt, inv_opt, qty):
    aux = pow(2, bits_inv_opt(ip_class, opt, qty))
    if inv_opt == 'subnets':
        qty_inv_opt = int(aux)
    elif inv_opt == 'hosts':
        qty_inv_opt = int(aux - 2)
    return qty_inv_opt


def new_bin_mask(ip_class, opt, qty, bin_mask):
    if opt == 'subnets':
        bits = bits_opt(opt, qty)
    elif opt == 'hosts':
        bits = bits_inv_opt(ip_class, opt, qty)
    new_bin_mask = bin_mask.replace('0', '1', bits)
    return new_bin_mask


def cidr_notation(mask):
    cidr = 0
    aux = mask.replace('.', '')
    for i in range(len(aux)):
        if aux[i] == '1':
            cidr += 1
        else:
            break
    return cidr


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
    data['bin_ip'] = bin_octets(data['ip'])
    data['dec_mask'] = dec_mask(data['class'])
    data['bin_mask'] = bin_octets(data['dec_mask'])
    data['dec_wildcard'] = dec_wildcard(data['class'])
    data['bin_wildcard'] = bin_octets(data['dec_wildcard'])
    data['bits_opt'] = bits_opt(data['opt'], data['qty'])
    data['bits_inv_opt'] = bits_inv_opt(
        data['class'], data['opt'], data['qty'])
    data['qty_opt'] = qty_opt(data['opt'], data['qty'])
    data['qty_inv_opt'] = qty_inv_opt(
        data['class'], data['opt'], data['inv_opt'], data['qty'])
    data['new_bin_mask'] = new_bin_mask(
        data['class'], data['opt'], data['qty'], data['bin_mask'])
    data['new_dec_mask'] = dec_octets(data['new_bin_mask'])
    data['cidr'] = cidr_notation(data['new_bin_mask'])

    return render(request, 'result.html', data)
