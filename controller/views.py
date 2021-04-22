from django.shortcuts import render
from .models import Tests
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import transaction
import os
from django.shortcuts import HttpResponse
import xlwt
from io import BytesIO
import qrcode
import xlrd
# Create your views here.

def test(request):
    if request.method == "POST" and request.POST:
        s_id = request.POST.get('source_id')
        t_id = request.POST.get('target_id')
        # 创建新的测试对象，存入数据库中
        info = Tests()
        info.source_id = s_id
        info.target_id = t_id
        info.save()
        return render(request, 'home.html')
    return render(request, 'home.html')
