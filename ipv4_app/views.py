from django.shortcuts import render
from .forms import IndexForm

# Create your views here.


def index(request):
    form = IndexForm()
    return render(request, 'index.html', {'form': form})


data = {}


def result(request):
    global data
    if request.method == 'POST':
        form = IndexForm(request.POST)
        if form.is_valid():
            data['ip'] = form.cleaned_data.get('ip_address')
            data['qtd'] = form.cleaned_data.get('quantity')
            data['opt'] = form.cleaned_data.get('option')
        else:
            data = {'form': form}
            return render(request, 'index.html', data)
    if data['opt'] == 'hosts':
        data['opt_inv'] = 'subnets'
    else:
        data['opt_inv'] = 'hosts'
    return render(request, 'result.html', data)
