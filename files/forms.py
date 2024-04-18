from django import forms
from files.models import File, Directory

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file', 'visibility']

class DirectoryForm(forms.ModelForm):
    class Meta:
        model = Directory
        fields = ['name', 'visibility']