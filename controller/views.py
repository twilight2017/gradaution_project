from django.shortcuts import render
from .models import Tests
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import transaction
import os
import subprocess
from subprocess import Popen, PIPE
from django.shortcuts import HttpResponse
import xlwt
from io import BytesIO
import qrcode
import xlrd
# Create your views here.
global cout

def test(request):
    return render(request, 'home.html')

def algorithm(request):
    if request.method == "POST" and request.POST:
        # 读取前端页面上传的数据
        m_id = request.POST.get('model')
        s_id = request.POST.get('source')
        t_id = request.POST.get('target')
        outfile = open('test.txt', 'w')  # same with "w" or "a" as opening mode
        res = subprocess.Popen('python D:\study\graduation_project\grdaution_project\instru_identify\\train.py',stdout=outfile)
        res.communicate()
        file = open('D:\study\graduation_project\grdaution_project\\test.txt',encoding='utf-8')
        # 按行读取运行结果文件，并存入数组中进行保存
        dit, i= {}, 1
        for line in file:
            line = line.strip('\n')
            dit[i] = line
            i += 1
            dit.update(dit)
        # print('dit:',dit)
        # 创建新的测试对象，存入数据库中
        info = Tests()
        info.model_id = m_id
        info.source_id = s_id
        info.target_id = t_id
        info.source_acc = dit[1]
        info.target_acc = dit[2]
        info.source_time = dit[3]
        info.target_time = dit[4]
        info.save()
        # 列表存储返回前端的结果
        # 获取展示队列
        display = Tests.objects.get(target_acc=dit[2])
        return render(request, 'identify.html',{'test_list':display})
    return render(request,'identify.html')
