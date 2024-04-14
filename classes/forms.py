from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Class

class ClassForm(ModelForm):
	class Meta:
		model = Class
		fields = ['name', 'prefixed_id']

class ClassNameForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name']

    name = forms.ModelChoiceField(
        queryset=Class.objects.all(),
        to_field_name='name',
        required=True,  
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    