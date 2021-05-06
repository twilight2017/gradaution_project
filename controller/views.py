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
    return render(request, 'home.html')

def algorithm(request):
    if request.method == "POST" and request.POST:
        # 读取前端页面上传的数据
        m_id = request.POST.get('model')
        s_id = request.POST.get('source')
        t_id = request.POST.get('target')
        os.system('python D:\study\graduation_project\grdaution_project\instru_identify\train.py')
        # 创建新的测试对象，存入数据库中
        #info = Tests()
        #info.model_id = m_id
        #info.source_id = s_id
        #info.target_id = t_id
        #info.save()
        print(m_id)

        return render(request, 'home.html')
    return render(request,'identify.html')
