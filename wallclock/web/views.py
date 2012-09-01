from django.http import HttpResponse
from django.shortcuts import render_to_response,redirect
from web.ilv import ClockUnit
from datetime import datetime
import time
# Create your views here.

def index(request):
    clock = ClockUnit(("192.168.1.252",10001))
    time = clock.getDateTime()
    d = {'current_time':time.strftime("%Y-%m-%d %H:%M:%S")}
    return render_to_response('index.html', d)
def set_time(request):
    clock = ClockUnit(("192.168.1.252",10001))
    clock.setDateTime(datetime.now())
    time.sleep(2)
    return redirect('web.views.index')

