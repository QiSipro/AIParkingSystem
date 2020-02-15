# Generated by Django 2.0.8 on 2020-02-15 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20200215_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_type',
            field=models.CharField(choices=[('1', '支付宝'), ('2', '微信'), ('0', '未支付')], default='0', max_length=10, verbose_name='支付类型'),
        ),
    ]
