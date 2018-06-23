# coding=utf-8


import logging
import random
from datetime import datetime, timedelta

from onechain import Appium_class

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("Appium_trade.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/Appium_trade.log', mode='w')
fh.setLevel(logging.WARNING)  # 输出到file的log等级的开关
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)  # 输出到console的log等级的开关
# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# 第四步，将logger添加到handler里面
logger.addHandler(fh)
logger.addHandler(ch)


def trade_with_condition(trader):
    trans_quota = 1000/6.49
    try:
        (sell01, sell_balance, buy01, buy_balance) = trader.get_price()
        # 买入价(buy01) < 卖出价(sell01) x (1 + 0.04%)
        if float(buy01) <= float(sell01) * (1 + 0.0004):
            buy_amount = round(trans_quota/float(buy01), 4)
            sell_amount = round(trans_quota/float(sell01), 4)
            logger.warning("========== sell_amount: " + str(sell_amount) + ", buy_amount: " + str(buy_amount))
            if sell_amount<float(sell_balance) and buy_amount<(float(buy_balance)/float(buy01)):
                code = trader.buy(buy01, str(buy_amount))
                if code == 0:
                    logger.warning("<<<<<<<<<< 买入成功！")
                else:
                    logger.warning("<<<<<<<<<< 买入失败！")


                code = trader.sell(sell01, str(sell_amount))
                if code == 0:
                    logger.warning(">>>>>>>>>> 卖出成功！")
                else:
                    logger.warning(">>>>>>>>>> 卖出失败！")
    except Exception as e:
        print(e)

def trade_buy_first(trader):
    ETH = 3365
    trans_quota = 500/ETH
    try:
        (avg_price_value, sell_balance, buy_balance) = trader.get_price()
        # 买入价(buy01) < 卖出价(sell01) x (1 + 0.04%)
        # if float(buy01) <= float(sell01) * (1 + 0.0004):
        buy_amount = round(trans_quota/float(avg_price_value), 4)
        sell_amount = round(trans_quota/float(avg_price_value), 4)
        logger.warning("========== sell_amount: " + str(sell_amount) + ", buy_amount: " + str(buy_amount))
        if sell_amount<float(sell_balance) and buy_amount<(float(buy_balance)/float(avg_price_value)):
            code = trader.buy(str(buy_amount))
            if code == 0:
                logger.warning("<<<<<<<<<< 买入成功！")
            else:
                logger.warning("<<<<<<<<<< 买入失败！")


            code = trader.sell(str(sell_amount))
            if code == 0:
                logger.warning(">>>>>>>>>> 卖出成功！")
            else:
                logger.warning(">>>>>>>>>> 卖出失败！")
    except Exception as e:
        print(e)

def trade_sell_first(trader):
    ETH = 3200
    trans_quota = random.randint(200,300)/ETH
    try:
        (avg_price_value, sell_balance, buy_balance) = trader.get_price()
        # 买入价(buy01) < 卖出价(sell01) x (1 + 0.04%)
        # if float(buy01) <= float(sell01) * (1 + 0.0004):
        buy_amount = round(trans_quota/float(avg_price_value), 4)
        sell_amount = round(trans_quota/float(avg_price_value), 4)
        logger.warning("========== sell_amount: " + str(sell_amount) + ", buy_amount: " + str(buy_amount))
        if sell_amount<float(sell_balance) and buy_amount<(float(buy_balance)/float(avg_price_value)):
            code = trader.sell(str(sell_amount))
            if code == 0:
                logger.warning(">>>>>>>>>> 卖出成功！")
            else:
                logger.warning(">>>>>>>>>> 卖出失败！")

            code = trader.buy(str(buy_amount))
            if code == 0:
                logger.warning("<<<<<<<<<< 买入成功！")
            else:
                logger.warning("<<<<<<<<<< 买入失败！")


    except Exception as e:
        print(e)


def trade01(trader):
    try:
        (sell01, sell_balance, buy01, buy_balance) = trader.get_price()
        logger.warning("Test......")
        pass
    except Exception as e:
        print(e)

day = 0
hour = 0
min = 1
second = 45

trader = Appium_class.trader_class()
res = trader.one_login()
# trade_sell_first(trader)

if res == 0:
    now = datetime.now()
    strnow = now.strftime('%Y-%m-%d %H:%M:%S')
    logger.warning("********** Now: " + strnow)
    # First next run time
    period = timedelta(days=day, hours=hour, minutes=min, seconds=second)
    next_time = now + period
    strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
    logger.warning("********** Next_run: " + strnext_time)
    while True:
        # Get system current time
        iter_now = datetime.now()
        iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')
        if str(iter_now_time) == str(strnext_time):
            # Get every start work time
            # logger.warning("start trade: " +iter_now_time)
            # Call task func
            trade_sell_first(trader)
            # logger.warning("trade done.")
            # Get next iteration time
            iter_time = iter_now + period
            strnext_time = iter_time.strftime('%Y-%m-%d %H:%M:%S')
            logger.warning("********** Next_run: " + strnext_time)
            # Continue next iteration
            continue
