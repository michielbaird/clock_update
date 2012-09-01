from django.http import HttpResponse
from web.ilv import ClockUnit
# Create your views here.

def index(request):
    clock = ClockUnit(("192.168.1.252",10001))
    time = clock.getDateTime()
    return HttpResponse(time.strftime("%Y-%m-%d %H:%M:%s"))

