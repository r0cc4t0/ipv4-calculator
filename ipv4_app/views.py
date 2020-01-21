from django.shortcuts import render
from .forms import IndexForm

# Create your views here.


def index(request):
    form = IndexForm()
    return render(request, 'index.html', {'form': form})
