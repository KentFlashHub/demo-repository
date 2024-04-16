from django.shortcuts import render, redirect, HttpResponse
import random
import csv
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import Class, Enrollment

@login_required
def enroll(request):
    if request.method == 'POST':
        form = ClassNameForm(request.POST)
        # print(f"The ID is: {form['name'].value()}")
        # print(f"The user is: {request.user}")

        class_instance = Class.objects.get(pk=form['name'].value())

        enroll = Enrollment(course_id = class_instance, user_id = request.user)
        enroll.save()

        return redirect('/courses/' + form['name'].value())
    else:
        context = {'form': ClassNameForm}
        return render(request, 'classes/enroll.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Course {form.cleaned_data.get("prefixed_id")} created.')
            return render(request, 'classes/create.html', {'form': form})
    else:
        return render(request, 'classes/create.html', {'form': ClassForm})

@login_required
def view(request, id):
    course = Class.objects.get(pk=id)
    context = {'course':course}
    return render(request, 'classes/course.html', context)
