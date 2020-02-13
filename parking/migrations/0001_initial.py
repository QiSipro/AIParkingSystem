# Generated by Django 2.0.8 on 2020-02-13 17:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_plate', models.CharField(max_length=50, verbose_name='车牌号')),
                ('parking_status', models.CharField(choices=[('in', '停车中'), ('out', '已离开')], default='in', max_length=10, verbose_name='停车状态')),
                ('order_no', models.BigIntegerField(blank=True, null=True, verbose_name='订单号')),
                ('in_time', models.DateField(default=datetime.datetime.now, verbose_name='进入时间')),
                ('out_time', models.DateField(verbose_name='离开时间')),
                ('create_time', models.DateField(default=datetime.datetime.now, verbose_name='创建时间')),
                ('update_time', models.DateField(verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '停车记录',
                'verbose_name_plural': '停车记录',
            },
        ),
    ]
