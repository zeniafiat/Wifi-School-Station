from django.shortcuts import render
from .models import DATT


def index(request):
    context = {
        'title': 'School'
    }
    return render(request, 'main\index.html',context=context)

def docs(request):
    return render(request, 'main\docks.html')

def info(request):
    context = {
        'dat':DATT.objects.all(),
    }
    return render(request, 'main\info.html', context)



