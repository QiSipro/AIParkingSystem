# coding:utf-8

import os
import random
import time
import datetime
import threading
from django.shortcuts import render, redirect
from django.views.generic.base import View
from playsound import playsound

from .models import Parking
from .forms import IdentifyForm

from utils.pay import AliPay
from order.models import Order, Charge, Discount


# Create your views here.

class IdentifyView(View):

    def get(self, request):
        # 判断传入车牌是否为空
        car_plate_form = IdentifyForm(request.GET)
        if car_plate_form.is_valid():
            # 取出POST中car_plate
            car_plate = request.GET.get("car_plate", "")
            # 传入的车牌去数据库进行搜索,找到所有的记录
            all_records = Parking.objects.filter(car_plate=car_plate)
            # 如果有数据,挑选最后一次没有出去的记录的进入支付状态，如果之前的全部都出去了则新插入记录
            if all_records:
                # 调用service服务,in=False : out=True
                for record in all_records:
                    # 同一个车牌停车场内只可能存在一辆车
                    if record.out_time is None:
                        # 出车
                        pay_url = purchase(request, record)
                        if pay_url is None:
                            return render(request, 'show_msg.html',
                                          {'msg': '祝您一路顺风'})
                        # 非空进入支付
                        return redirect(pay_url)
                car_insert(car_plate)
            else:
                # 没有数据,进行插入记录，调用service服务
                car_insert(car_plate)
            # 欢迎光临
            threading.Thread(target=self.play).start()
            return render(request, 'show_msg.html',
                          {'msg': '欢迎光临'})

    def post(self, request):
        pass

    def play(self):
        path = os.path.abspath('resources/welcome.wav')
        print(path)
        playsound(path)


def purchase(request, record):
    # 费用保留两位小数
    parking_fee = round(fee(record), 2)
    # 传入要创建订单的那条停车信息, 并生成订单
    # 取13位时间戳+100内随机数作为订单号
    order_number = int(round(time.time() * 1000)) + random.randint(0, 100)
    Order.objects.create(order_no=order_number, car_plate=record.car_plate,
                         payment=parking_fee)
    # 更新停车信息的订单号
    record.order_no = order_number
    record.parking_status = 'out'
    record.out_time = datetime.datetime.now()
    record.save()
    # 计算停车费，免费时间段内就不支付了
    if parking_fee <= 0:
        Order.objects.filter(order_no=order_number).update(
            order_status='1',
            payment_type='1',
            payment_time=datetime.datetime.now())
        return None

    # 跳转到支付宝支付页面
    # 实例化AliPay
    alipay = AliPay(
        # APPID
        appid="2016080900196363",
        # 支付宝会向这个地址发送post请求
        app_notify_url='http://zhangsiqi.natapp1.cc/check_order/',
        # 支付宝会向这个地址发送get请求
        return_url='http://zhangsiqi.natapp1.cc/show_msg/',
        # 应用私钥
        app_private_key_path='keys/app_private_2048.txt',
        # 支付宝公钥
        alipay_public_key_path='keys/alipay_public_2048.txt',
        debug=True,  # 默认是False
    )

    # 定义请求地址传入的参数
    query_params = alipay.direct_pay(
        subject=str(record.car_plate + "的停车费用"),  # 商品描述
        out_trade_no=order_number,  # 订单号
        total_amount=parking_fee,  # 交易金额(单位是元，保留两位小数)
    )
    # 需要跳转到支付宝的支付页面，所以需要生成跳转的url
    pay_url = 'https://openapi.alipaydev.com/gateway.do?{0}'.format(
        query_params)
    return pay_url


def fee(record):
    """
    收费标准：30m内免费，超过30m小于1h按1h收费。
    停车时间分为三个挡位，
    1-5小时
    5-12小时
    12-24小时
    超过24小时按第三时段收费。

    标准收费：数据库中只有一条，也可以有多条，分大车小车。
    折扣优惠：可以有多条，根据停车进入时间进行判断，在某一活动内则计算折扣。
    由于车牌识别无法识别车型故无大车小车区分。
    :param record:停车记录
    :return: fee :费用
    """
    # 传入停车记录，取出停车时间计算停车费
    now = datetime.datetime.now()
    in_time = record.in_time
    # 相差的小时数与分钟数
    seconds = (now - in_time).seconds
    # 分钟等于总分钟差减去小时所占的分钟，取出分钟零头
    minutes = int(seconds / 60)
    hours = int(minutes / 60)
    minutes -= hours * 60
    # 取出收费标准和判断是否有折扣
    charge = Charge.objects.get(charge_name='标准收费')
    discounts = Discount.objects.filter()
    rate = 1.0
    level_1 = 5 * charge.pay_level_1
    level_2 = 7 * charge.pay_level_2
    level_3 = 12 * charge.pay_level_3
    for discount in discounts:
        if (in_time - discount.start_time).seconds > 0 and (discount.end_time
                                                            - in_time).seconds > 0:
            # 如果进入时在活动区间, 可以多活动叠加 算出所有活动叠加的最终折扣
            rate = rate * discount.discount / 10
    # 半小时内免费
    if hours == 0 and minutes < 30:
        return 0
    elif hours == 0 and minutes >= 30:
        # 按一个小时算, 没活动还是一个小时
        return charge.pay_level_1 * rate
    # 按挡位区间去算
    elif 1 <= hours <= 5:
        return ((hours + 1) * charge.pay_level_1) * rate
    elif 5 < hours <= 12:
        return (level_1 + (hours - 5) * charge.pay_level_2) * rate
    elif 12 < hours <= 24:
        return (level_1 + level_2 + (hours - 12) * charge.pay_level_3) * rate
    elif hours > 24:
        return (level_1 + level_2 + level_3 + (hours - 24) *
                charge.pay_level_3) * rate


def car_insert(car_plate):
    # 原记录全部已出,新插入
    car = Parking()
    car.car_plate = car_plate
    car.save()
