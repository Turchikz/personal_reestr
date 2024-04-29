from .models import Register
from django.forms import ModelForm, TextInput, DateInput, Select, ModelChoiceField, CheckboxSelectMultiple
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    date_of_birth = forms.DateField(required=True, help_text='Дата рождения')


class ExtendedRegisterForm(UserCreationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    date_of_birth = forms.DateField(required=True, help_text='Дата рождения')




class RegisterForm(ModelForm):
    # Type_mod = forms.ModelMultipleChoiceField(queryset=Approved.objects.filter())

    class Meta:
        model = Register

        fields = ['kind', 'descr', 'modif', 'date', 'until', 'owner', 'place',
                  'number', 'povername', 'number', 'etalons', 'temp_val', 'temp_kind', 'press_val', 'others',
                  'hum_val', 'd_min', 'd_max', 'ed_izm', 'pogr_val', 'pogr_kind', 'impl_name',
                  ]

        widgets = {
            'kind': Select(attrs={
                'class': 'form-control',
            }),
            'descr': Select(attrs={
                'class': 'form-control',
            }),
            'modif': Select(attrs={
                'class': 'form-control',
            }),
            'date': DateInput(attrs={
                'class': 'date',
            }),
            'until': DateInput(attrs={
                'class': 'date',
            }),
            'owner': Select(attrs={
                'class': 'form-control',
            }),
            'place': Select(attrs={
                'class': 'form-control',
            }),
            'number': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заводской номер',
            }),
            'povername': Select(attrs={
                'class': 'form-control',
            }),
            'etalons': CheckboxSelectMultiple(attrs={
                'class': 'form-control',
            }),
            'temp_val': TextInput(attrs={
                'class': 'form-control',
            }),
            'press_val': TextInput(attrs={
                'type': 'form-control'
            }),
            'hum_val': TextInput(attrs={
                'class': 'form-control',
            }),
            'others': DateInput(attrs={
                'type': 'form-control'
            }),
            'd_min': TextInput(attrs={
                'class': 'form-control',
            }),
            'd_max': TextInput(attrs={
                'class': 'form-control',
            }),
            'ed_izm': TextInput(attrs={
                'class': 'form-control',
            }),
            'pogr_val': TextInput(attrs={
                'class': 'form-control',
            }),
            'pogr_kind': Select(attrs={
                'class': 'form-control',
            }),
            'impl_name': Select(attrs={
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['etalons'] = ModelChoiceField(queryset=Register.objects.all(), empty_label="Choose a countries", )


class RegisterAllForm(forms.Form):
    class Meta:
        model = Register

        fields = ['kind', 'date', 'apr_mpi', 'until', 'name', 'modif', 'owner',
                  'povername', 'place', 'descr', 'number', 'apr_method', 'etalons', 'temp_val', 'temp_kind',
                  'press_val', 'press_kind', 'hum_val', 'hum_kind', 'others', 'd_min', 'd_max', 'impl_name'
                  ]


AddFormSet = modelformset_factory(
    Register, extra=1, fields='__all__', form=RegisterForm,
)
