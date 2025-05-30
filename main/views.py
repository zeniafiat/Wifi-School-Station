from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import DATT
from .forms import sencorIDform

def index(request):
    context = {
        'title': 'School'
    }
    return render(request, 'main\index.html',context=context)

def docs(request):
    return render(request, 'main\docks.html')

@login_required
def info(request):
    user = request.user
    if request.method == "POST":
        form = sencorIDform(request.POST)
        sensor_id = request.POST['sensor_id']
        profile = user.userprofile
        profile.sensor_id = sensor_id 
    else:
        form = sencorIDform()
    if user.username == 'root':
        context = {
        'dat':DATT.objects.all(),
        'form': form,
        }
        return render(request, 'main/info.html', context)
    else:
        try:
            profile = user.userprofile 
            sensor_id = profile.sensor_id
            print(sensor_id)
            context = {
            'dat':DATT.objects.filter(addr=sensor_id),
            'form': form,
            }
            return render(request, 'main/info.html', context)
        except: 
            return render(request, 'main/index.html', context)
    



