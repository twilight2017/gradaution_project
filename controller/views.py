from django.shortcuts import render
from .models import Tests
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import transaction
import os
import charts
import echarts
import subprocess
import webbrowser
from subprocess import Popen, PIPE
from django.shortcuts import HttpResponse
import xlwt
from io import BytesIO
import qrcode
import xlrd
# Create your views here.

def algorithm(request):
    if request.method == "POST" and request.POST:
        # 读取前端页面上传的数据
        m_id = request.POST.get('model')
        s_id = request.POST.get('source')
        t_id = request.POST.get('target')
        #判断调用的模型是DSN模型还是上次迁移学习结果的模型
        if m_id == 'DSN':
            outfile = open('test.txt', 'w')  # same with "w" or "a" as opening mode
            res = subprocess.Popen('python D:\study\graduation_project\grdaution_project\instru_identify\\train.py',stdout=outfile)
            res.communicate()
            file = open('D:\study\graduation_project\grdaution_project\\test.txt',encoding='utf-8')
            # 按行读取运行结果文件，并存入数组中进行保存
        else:
            outfile = open('test.txt', 'w')  # same with "w" or "a" as opening mode
            res = subprocess.Popen('python D:\study\graduation_project\grdaution_project\instru_identify\\train_l.py',
                                   stdout=outfile)
            res.communicate()
            file = open('D:\study\graduation_project\grdaution_project\\test.txt', encoding='utf-8')
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

def line(request):
    print('line_success')
    # 获取当前数据库中所有tests()对象
    dis = Tests.objects.filter()
    LIST = []
    count = 0  # count记录当前的迭代总次数
    for i in dis:
        LIST.append(i)
        count += 1
    # 获取所有的源数据集准确率对象
    s_acc = []
    for li in LIST:
        s_acc.append(li.source_acc)
    # 获取当前所有的目标数据集准确率对象
    t_acc = []
    for lin in LIST:
        t_acc.append(lin.target_acc)
    charts.paint(count, s_acc, t_acc)
    webbrowser.open('D:\study\graduation_project\grdaution_project\\templates\line.html')
    return render(request,'identify.html')

def bar(request):
    # 获取当前数据库中所有tests()对象
    dis = Tests.objects.filter()
    LIST = []
    count = 0  # count记录当前的迭代总次数
    for i in dis:
        LIST.append(i)
        count += 1
    # 获取所有的源数据集训练时长对象
    s_time = []
    for li in LIST:
        s_time.append(li.source_time)
    # 获取当前所有的目标数据集训练时长对象
    t_time = []
    for lin in LIST:
        t_time.append(lin.target_time)
    echarts.paint(count, s_time, t_time)
    webbrowser.open('D:\study\graduation_project\grdaution_project\\templates\\bar.html')
    return render(request, 'identify.html')