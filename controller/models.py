from django.db import models

# Create your models here.
# models用于和数据库交互，Django提供ORM，无须自行编写sql语句
# Create your models here

# 单次模型训练的参数结果需要存储至数据库中，保存为一个result对象
class Tests(models.Model):
    # 训练模型
    model_id = models.CharField(max_length=50, default='None')
    # 训练源域数据集
    source_id = models.CharField(max_length=50, default='None')
    # 训练目标域数据集
    target_id = models.CharField(max_length=50, default='None')
    # 源域训练数据准确率
    source_acc = models.CharField(max_length=50, default='None')
    # 目标域训练数据准确率
    target_acc = models.CharField(max_length=50, default='None')
    # 源域训练数据时长
    source_time = models.CharField(max_length=50, default='None')
    # 目标域训练数据时长
    target_time = models.CharField(max_length=50, default='None')

