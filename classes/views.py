from django.shortcuts import render, redirect, HttpResponse
import random
import csv
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import ClassNameForm
from .models import Class

@login_required
def enroll(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        return b'hry'
    else:
        classes = Class.objects.all();
        context = {'classes': classes, 'form': ClassNameForm}
        return render(request, 'classes/enroll.html', context)