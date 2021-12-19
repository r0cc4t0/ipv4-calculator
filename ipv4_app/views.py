from django.shortcuts import render
from .forms import IndexForm
from math import log, ceil
from io import BytesIO
from django.http import FileResponse
from reportlab.pdfgen.canvas import Canvas

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


def new_bin_wildcard(new_bin_mask):
    one = 0
    zero = 0
    for i in range(len(new_bin_mask)):
        if new_bin_mask[i] == '1':
            one += 1
        elif new_bin_mask[i] == '0':
            zero += 1
    new_bin_wildcard = new_bin_mask.replace(
        '0', '1', zero).replace('1', '0', one)
    return new_bin_wildcard


def effective_quantity(ip_class):
    if ip_class == 'A':
        effective_quantity = 8388608
    elif ip_class == 'B':
        effective_quantity = 32768
    elif ip_class == 'C':
        effective_quantity = 128
    return effective_quantity


def calculate_subnets(ip, ip_class, cidr):
    ip_octets = split_octets(ip)
    aux = ''

    if ip_class == 'A':
        bits = int(cidr) - 8
    elif ip_class == 'B':
        bits = int(cidr) - 16
    elif ip_class == 'C':
        bits = int(cidr) - 24

    aux = '1' * bits
    bin_size = len(aux)
    dec_size = int(aux, 2) + 1
    network = []
    broadcast = []
    subnet_number = 1
    subnets = []

    for i in range(dec_size):
        network.append(bin(i)[2:].rjust(bin_size, '0').ljust(8, '0'))
        broadcast.append(bin(i)[2:].rjust(bin_size, '0').ljust(8, '1'))

        if ip_class == 'A':
            network[i] = network[i][:8] + '.' + \
                network[i][8:16].ljust(8, '0') + '.' + \
                network[i][16:].ljust(8, '0')
            broadcast[i] = broadcast[i][:8] + '.' + \
                broadcast[i][8:16].ljust(
                    8, '1') + '.' + broadcast[i][16:].ljust(8, '1')
            subnets.append({
                'number': subnet_number,
                'dec_network': dec_octets(ip_octets[0] + '.' + network[i]),
                'bin_network': ip_octets[0] + '.' + network[i],
                'dec_broadcast': dec_octets(ip_octets[0] + '.' + broadcast[i]),
                'bin_broadcast': ip_octets[0] + '.' + broadcast[i]
            })

        if ip_class == 'B':
            network[i] = network[i][:8] + '.' + network[i][8:].ljust(8, '0')
            broadcast[i] = broadcast[i][:8] + \
                '.' + broadcast[i][8:].ljust(8, '1')
            subnets.append({
                'number': subnet_number,
                'dec_network': dec_octets(ip_octets[0] + '.' + ip_octets[1] + '.' + network[i]),
                'bin_network': ip_octets[0] + '.' + ip_octets[1] + '.' + network[i],
                'dec_broadcast': dec_octets(ip_octets[0] + '.' + ip_octets[1] + '.' + broadcast[i]),
                'bin_broadcast': ip_octets[0] + '.' + ip_octets[1] + '.' + broadcast[i]
            })

        if ip_class == 'C':
            subnets.append({
                'number': subnet_number,
                'dec_network': dec_octets(ip_octets[0] + '.' + ip_octets[1] + '.' + ip_octets[2] + '.' + network[i]),
                'bin_network': ip_octets[0] + '.' + ip_octets[1] + '.' + ip_octets[2] + '.' + network[i],
                'dec_broadcast': dec_octets(ip_octets[0] + '.' + ip_octets[1] + '.' + ip_octets[2] + '.' + broadcast[i]),
                'bin_broadcast': ip_octets[0] + '.' + ip_octets[1] + '.' + ip_octets[2] + '.' + broadcast[i]
            })

        subnet_number += 1
    return subnets


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
    data['new_bin_wildcard'] = new_bin_wildcard(data['new_bin_mask'])
    data['new_dec_wildcard'] = dec_octets(data['new_bin_wildcard'])
    data['effective_subnets'] = effective_quantity(data['class'])
    data['effective_hosts'] = effective_quantity(data['class']) - 2
    data['subnets'] = calculate_subnets(
        data['bin_ip'], data['class'], data['cidr'])

    return render(request, 'result.html', data)


def generate_pdf(request):
    buffer = BytesIO()
    pdf = Canvas(buffer)
    pdf.setTitle('IPv4 Subnets Calculator')
    width = 595
    height = 842
    margin = 85

    pdf.drawCentredString(width / 2, height - margin,
                          'IPv4 Subnets Calculator')
    pdf.drawString(margin, 672, 'Decimal IP Address: ' + data['ip'])
    pdf.drawString(margin, 647, 'Chosen Option: ' + data['opt'])
    pdf.drawString(margin, 622, 'Requested Quantity: {:d}'.format(data['qty']))
    pdf.drawString(margin, 597, 'IP Class: ' + data['class'])
    pdf.drawString(margin, 572, 'IP Type: ' + data['type'])
    pdf.drawString(margin, 547, 'Binary IP Address: ' + data['bin_ip'])
    pdf.drawString(
        margin, 522, 'Decimal Default Subnet Mask: ' + data['dec_mask'])
    pdf.drawString(
        margin, 497, 'Binary Default Subnet Mask: ' + data['bin_mask'])
    pdf.drawString(
        margin, 472, 'Decimal Default Wildcard Mask: ' + data['dec_wildcard'])
    pdf.drawString(
        margin, 447, 'Binary Default Wildcard Mask: ' + data['bin_wildcard'])
    pdf.drawString(margin, 422, 'Number of bits used for {}: {:d}'.format(
        data['opt'], data['bits_opt']))
    pdf.drawString(margin, 397, 'Valid number of {} with {:d} bits: {:d}'.format(
        data['opt'], data['bits_opt'], data['qty_opt']))
    pdf.drawString(margin, 372, 'Number of bits used for {}: {:d}'.format(
        data['inv_opt'], data['bits_inv_opt']))
    pdf.drawString(margin, 347, 'Valid number of {} with {:d} bits: {:d}'.format(
        data['inv_opt'], data['bits_inv_opt'], data['qty_inv_opt']))
    pdf.drawString(margin, 322, 'Binary New Subnet Mask: ' +
                   data['new_bin_mask'])
    pdf.drawString(margin, 297, 'Decimal New Subnet Mask: ' +
                   data['new_dec_mask'])
    pdf.drawString(margin, 272, 'CIDR Notation: /{:d}'.format(data['cidr']))
    pdf.drawString(margin, 247, 'Binary New Wildcard Mask: ' +
                   data['new_bin_wildcard'])
    pdf.drawString(margin, 222, 'Decimal New Wildcard Mask: ' +
                   data['new_dec_wildcard'])
    pdf.drawString(margin, 197, 'Maximum subnets for class {}: {:d}'.format(
        data['class'], data['effective_subnets']))
    pdf.drawString(margin, 172, 'Maximum hosts per subnet for class {}: {:d}'.format(
        data['class'], data['effective_hosts']))

    pdf.showPage()

    count = 0
    y = height - margin
    for i in range(len(data['subnets'])):
        pdf.drawString(margin, y, 'Subnet: {}'.format(
            data['subnets'][i]['number']))
        pdf.drawString(
            margin, y - 25, 'Decimal Network Address: {}'.format(data['subnets'][i]['dec_network']))
        pdf.drawString(
            margin, y - 50, 'Binary Network Address: {}'.format(data['subnets'][i]['bin_network']))
        pdf.drawString(
            margin, y - 75, 'Decimal Broadcast Address: {}'.format(data['subnets'][i]['dec_broadcast']))
        pdf.drawString(
            margin, y - 100, 'Binary Broadcast Address: {}'.format(data['subnets'][i]['bin_broadcast']))
        count += 1
        y -= 100 + margin
        if count % 4 == 0:
            pdf.showPage()
            y = height - margin

    pdf.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='ipv4.pdf')
