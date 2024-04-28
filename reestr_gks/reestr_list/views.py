from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from .models import Register, Pover
from timeit import default_timer


def index(request: HttpRequest):
    
    context = {
        'time_working': str(int(default_timer()) // 60) + ' минут',
        'users': User.objects.all(),
    }
    return render(request, 'index.html', context=context)

def reestr_list(request: HttpRequest):
    
    context = {
        'registers': Register.objects.all(),
        'povers': Pover.objects.all(),
    }
    return render(request, 'reestr_list/list.html', context=context)

def add_to_reestr(request: HttpRequest):
    
    context = {
        'registers': Register.objects.all(),
    }
    return render(request, 'reestr_list/add_to_reestr.html', context=context)

