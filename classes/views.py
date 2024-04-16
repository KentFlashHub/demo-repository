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
        form = ClassNameForm(request.POST, Class.objects.all())
        # print(f"The ID is: {form['name'].value()}")
        # print(f"The user is: {request.user}")

        class_instance = Class.objects.get(pk=form['name'].value())

        enroll = Enrollment(course_id = class_instance, user_id = request.user)
        enroll.save()

        return redirect('/courses/' + form['name'].value())
    else:
        enrollments = Enrollment.objects.filter(user_id = request.user)
        filter_courses = []
        for enrollment in enrollments:
            if enrollment.user_id == request.user:
                filter_courses.append(enrollment.course_id)
        queryset = [x for x in Class.objects.all() if x not in filter_courses]
        queryset = [x.pk for x in queryset]
        print(queryset)
        queryset = Class.objects.filter(pk__in=queryset)
        context = {'form': ClassNameForm(queryset=queryset)}
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

@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(user_id=request.user)
    courses = []
    for course in enrollments:
        courses.append(course.course_id)
    return render(request, 'classes/my_courses.html', {'course_list': courses})