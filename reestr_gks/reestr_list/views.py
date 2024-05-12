from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from .models import Register, Pover
from timeit import default_timer
from django.views.generic import TemplateView, CreateView, View
from .forms import Add_to_registerForm, Add_to_registerFormSet
from django.urls import reverse_lazy
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect



class IndexView(View):
    def get(self, requset:HttpRequest) -> HttpResponse:
        context = {
            'time_working': str(int(default_timer()) // 60) + ' минут',
            'users': User.objects.all(),
        }
        return render(self.request, 'index.html', context=context)

def reestr_list(request: HttpRequest):
    
    context = {
        'registers': Register.objects.all(),
        'povers': Pover.objects.all(),
    }
    return render(request, 'reestr_list/list.html', context=context)

class Add_to_reestrView___(CreateView):
    def get(self, requset:HttpRequest) -> HttpResponse:
        context = {
            'registers': Register.objects.all(),
            # 'form': Add_to_register(),
        }
        return render(self.request, 'reestr_list/add_to_register.html', context=context)
    # if request.method == 'POST':

    #     form = Add_to_register(request.POST)
    #     if form.is_valid():
    #         jc = form.save(commit=True)

    #         jc.id_numb = str(jc.date)
    #         jc.id_numb = str((Register.objects.filter(date__contains=str(jc.date.year)).count())+0)+ '-' + jc.id_numb[2] + jc.id_numb[3]
    #         jc.save()
    #         return redirect('reestr')
    #     else:
    #         error = 'форма была неверной'
    # form = Add_to_register()
    # data = {
    #     'form': form,
    #     'error': error
    # }

class Add_to_reestrView(CreateView):
    model =  Register
    success_url = '/reestr/'
    form_class = Add_to_registerForm
    template_name = 'reestr_list/add_to_register.html'


    def get_context_data(self, **kwargs):
        context = super(Add_to_reestrView, self).get_context_data(**kwargs)
        context['formset'] = Add_to_registerFormSet(queryset=Register.objects.none())
        return context

    def form_valid(self, formset):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
        return self.render_to_response({'formset': formset})   
        # return HttpResponseRedirect(self.get_success_url)   
        
    def post(self, request, *args, **kwargs):
        formset = Add_to_registerFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                jc = form.save(commit=True)
                jc.id_numb = str(jc.date)
                jc.id_numb = str((Register.objects.filter(date__contains=str(jc.date.year)).count()) + 0) + '-' + \
                             jc.id_numb[2] + jc.id_numb[3]
                jc.save()
            formset.save()

        return self.render_to_response({'formset': formset})
   