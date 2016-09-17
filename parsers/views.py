from django.http import HttpResponse
from django.shortcuts import render

from . import parser

# Create your views here.
def index(request):
    return render(request, 'index.html')

def search(request):
    tap = parser.tap 
    try:
        link = request.GET.get('link','')
        return HttpResponse("result("+tap.parse(link)+")")
    except:
        return HttpResponse('')
