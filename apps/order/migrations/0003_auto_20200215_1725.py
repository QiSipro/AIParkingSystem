# Generated by Django 2.0.8 on 2020-02-15 17:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20200215_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='支付时间'),
        ),
        migrations.AlterField(
            model_name='order',
            name='update_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='更新时间'),
        ),
    ]
