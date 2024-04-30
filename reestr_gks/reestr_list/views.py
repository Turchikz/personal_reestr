from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from .models import Register, Pover
from timeit import default_timer
from django.views.generic import TemplateView
from .forms import AddFormSet
from django.urls import reverse_lazy


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

def add_to_register(request: HttpRequest):
    
    context = {
        'registers': Register.objects.all(),
    }
    return render(request, 'reestr_list/add_to_register.html', context=context)

class PostAddView(TemplateView):
    template_name = "reestr_list/add_to_reestr.html"

    def get(self, *args, **kwargs):
        formset = AddFormSet(queryset=Register.objects.none())
        return self.render_to_response({'add_formset': formset})

    # Define method to handle POST request
    def post(self, *args, **kwargs):
        formset = AddFormSet(data=self.request.POST)

        # Check if submitted forms are valid
        if formset.is_valid():
            for form in formset:
                jc = form.save(commit=True)
                jc.id_numb = str(jc.date)
                jc.id_numb = str((Register.objects.filter(date__contains=str(jc.date.year)).count()) + 0) + '-' + \
                             jc.id_numb[2] + jc.id_numb[3]
                jc.save()
            formset.save()
            return redirect(reverse_lazy("post_list"))

        return self.render_to_response({'add_formset': formset})
    
