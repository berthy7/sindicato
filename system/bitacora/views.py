from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json

# Create your views here.
@login_required
def index(request):
    # return render(request, 'index.html')
    return render(request, 'bitacora/index.html')


@login_required
def list(request):
    dt_list = []

    return JsonResponse(dt_list, safe=False)