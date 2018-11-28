from django.shortcuts import render

# Create your views here.
def showmap(request):
    location = [[37.5018216, 127.0355291],[37.50329,127.0414513],[37.5018498,127.0366247],[37.5089909,127.0381735],[37.5019224,127.0372503]]
    return render(request,'map/showmap.html', {'location':location})