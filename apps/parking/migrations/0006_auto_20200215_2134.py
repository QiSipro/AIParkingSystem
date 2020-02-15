# Generated by Django 2.0.8 on 2020-02-15 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0005_auto_20200215_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parking',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='parking',
            name='in_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='进入时间'),
        ),
        migrations.AlterField(
            model_name='parking',
            name='update_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间'),
        ),
    ]
