# Generated by Django 3.0.5 on 2021-04-20 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_id', models.CharField(default='None', max_length=50)),
                ('source_id', models.CharField(default='None', max_length=50)),
                ('target_id', models.CharField(default='None', max_length=50)),
                ('source_acc', models.CharField(default='None', max_length=50)),
                ('target_acc', models.CharField(default='None', max_length=50)),
                ('source_time', models.CharField(default='None', max_length=50)),
                ('target_time', models.CharField(default='None', max_length=50)),
            ],
        ),
    ]