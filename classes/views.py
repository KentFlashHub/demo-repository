from django.shortcuts import render, redirect, HttpResponse
import random
import csv
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

def enroll(request):
    return render(request, 'classes/base.html')