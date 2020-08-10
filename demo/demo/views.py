from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from . import model


def index(req):
    tips = model.get_tips()
    return render(req, 'index1.html',{'tips':tips})


def get_kgdata(request):
    key=request.GET.get('key')
    kgdata=model.get_data(key)
    return JsonResponse({'kgdata':kgdata})
