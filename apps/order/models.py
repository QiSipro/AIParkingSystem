# coding:utf-8
from django.db import models
from datetime import datetime


# Create your models here.

class Order(models.Model):
    """
    订单表
    """
    order_no = models.BigIntegerField(null=True, blank=True, verbose_name='订单号')
    car_plate = models.CharField(max_length=50, null=False, blank=False,
                                 verbose_name="车牌号")
    order_status = models.CharField(max_length=10, default='0',
                                    verbose_name='订单状态',
                                    choices=(('1', '已支付'), ('0', '未支付')))
    payment = models.DecimalField(max_digits=10, decimal_places=2,
                                  verbose_name='支付金额')
    payment_type = models.CharField(max_length=10, default='0',
                                    choices=(('1', '支付宝'),
                                             ('2', '微信'),
                                             ('0', '未支付')),
                                    verbose_name='支付类型')
    payment_time = models.DateTimeField(null=True, blank=True,
                                        verbose_name='支付时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(null=True, blank=True, auto_now=True,
                                       verbose_name='更新时间')

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_no)


class Charge(models.Model):
    charge_name = models.CharField(max_length=50, null=False, blank=False,
                                   verbose_name="收费标准名")
    pay_level_1 = models.IntegerField(verbose_name='第一时段1-5小时')
    pay_level_2 = models.IntegerField(verbose_name='第二时段5-12小时')
    pay_level_3 = models.IntegerField(verbose_name='第三时段12-24小时')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(null=True, blank=True, auto_now=True,
                                       verbose_name='更新时间')

    class Meta:
        verbose_name = '收费标准'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.charge_name


class Discount(models.Model):
    discount_name = models.CharField(max_length=50, null=False, blank=False,
                                     verbose_name="活动名")
    discount = models.IntegerField(verbose_name='折扣')
    start_time = models.DateTimeField(null=True, blank=True,
                                      verbose_name='开始时间')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(null=True, blank=True, auto_now=True,
                                       verbose_name='更新时间')

    class Meta:
        verbose_name = '折扣'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.discount_name
