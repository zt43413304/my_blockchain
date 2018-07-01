# coding=utf-8
import configparser
import logging
import os
import re
from datetime import datetime, timedelta

from coineal import web_coineal_class

# 第一步，创建一个logger,并设置级别
logger = logging.getLogger("web_coineal_trade.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./logs/web_coineal_trade.log', mode='w')
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


def load_quota():
    # get config information
    curpath = os.getcwd()
    content = open(curpath + '/coineal/web_config.ini').read()
    content = re.sub(r"\xfe\xff", "", content)
    content = re.sub(r"\xff\xfe", "", content)
    content = re.sub(r"\xef\xbb\xbf", "", content)
    open(curpath + '/coineal/web_config.ini', 'w').write(content)

    cf = configparser.ConfigParser()
    cf.read(curpath + '/coineal/web_config.ini')
    ETH_Price = cf.get('info', 'ETH_Price').strip()
    Deal_Quota = cf.get('info', 'Deal_Quota').strip()
    phone = cf.get('info', 'phone').strip()
    password = cf.get('info', 'password').strip()
    return ETH_Price, Deal_Quota, phone, password


def trade_buy_first_with_quota(trader):
    (ETH_Price, Deal_Quota, phone, password) = load_quota()
    trans_quota = float(Deal_Quota) / float(ETH_Price)
    try:
        (avg_price_value, sell_balance, buy_balance, sell01, buy01) = trader.get_price()
        amount = int(trans_quota / float(avg_price_value))

        sell_balance = 10
        # buy_balance = 10
        sell_amount = 1.11
        # buy_amount = 1.12

        # logger.warning("========== sell_amount: " + str(sell_amount) + ", buy_amount: " + str(buy_amount))
        if amount < float(sell_balance) \
                and amount < (float(buy_balance) / float(avg_price_value)) \
                and (sell01 - buy01 > 0.00000005):
            code = trader.buy(amount)
            if code == 0:
                logger.warning("<<<<<<<<<< 买入成功！")
            else:
                logger.warning("<<<<<<<<<< 买入失败！")

            code = trader.sell(amount)
            if code == 0:
                logger.warning(">>>>>>>>>> 卖出成功！")
            else:
                logger.warning(">>>>>>>>>> 卖出失败！")
        # else:
        #     res = trader.cancel_order()
        #     if res == 0:
        #         logger.warning("<<<<<<<<<< 撤销买入订单成功！")
        #     else:
        #         logger.warning("<<<<<<<<<< 撤销买入订单失败！")
        #     (avg_price_value, sell_balance, buy_balance) = trader.get_price()
        #     if float(buy_balance) < 0.2:
        #         code = trader.sell(str(10000))
        #         if code == 0:
        #             logger.warning(">>>>>>>>>> 二次卖出成功！")
        #         else:
        #             logger.warning(">>>>>>>>>> 二次卖出失败！")

    except Exception as e:
        print(e)

# start from here ......
day = 0
hour = 0
min = 0
second = 20

(ETH_Price, Deal_Quota, phone, password) = load_quota()
trader = web_coineal_class.trader_class()
res = trader.login(phone, password)
trader.load_coin()

trade_buy_first_with_quota(trader)

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
            trade_buy_first_with_quota(trader)
            # logger.warning("trade done.")
            # Get next iteration time
            iter_time = iter_now + period
            strnext_time = iter_time.strftime('%Y-%m-%d %H:%M:%S')
            logger.warning("********** Next_run: " + strnext_time)
            # Continue next iteration
            continue
