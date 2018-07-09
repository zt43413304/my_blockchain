# coding=utf-8
import logging
import sys
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


def trade_buy_first_with_quota(trader):
    (ETH_Price, Deal_Quota, phone, password, cancel_order_flag, cancel_order_timeout) = trader.load_quota()
    trans_quota = float(Deal_Quota) / float(ETH_Price)
    try:
        (avg_price_value, sell_balance, buy_balance, sell01, buy01) = trader.get_price()
        amount = int(trans_quota / float(avg_price_value))

        sell_balance = 100000000
        # buy_balance = 10
        sell_amount = 1.11
        # buy_amount = 1.12

        # logger.warning("========== sell_amount: " + str(sell_amount) + ", buy_amount: " + str(buy_amount))
        if amount < float(sell_balance) \
                and amount < (float(buy_balance) / float(avg_price_value)) \
                and (float(sell01) - float(buy01) > 0.00000005):
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


def coineal_trade(trader, pair):
    (ETH_Price, Deal_Quota, phone, password, cancel_order_flag, cancel_order_timeout) = trader.load_quota(pair)
    # trans_quota = float(Deal_Quota) / float(ETH_Price)
    try:
        (avg_price_value, sell_balance, buy_balance, sell01, buy01) = trader.get_price(pair)
        # amount = int(trans_quota / float(avg_price_value))

        # sell_balance = 100000000
        # buy_balance = 10
        # sell_amount = 1.11
        # buy_amount = 1.12

        # if amount < float(sell_balance) \
        #         and amount < (float(buy_balance) / float(avg_price_value)) \
        #         and (float(sell01) - float(buy01) > 0.00000005):
        if (float(buy_balance) / float(avg_price_value)) > float(Deal_Quota):
            code = trader.buy(buy_balance, pair)
            if code == 0:
                logger.warning("<<<<<<<<<< 买入成功！")
            else:
                logger.warning("<<<<<<<<<< 买入失败！")

        if (float(sell_balance)) > float(Deal_Quota):
            code = trader.sell(sell_balance, pair)
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


def loop_coineal_trade(pair):
    day = 0
    hour = 0
    min = 0
    second = 30

    trader = web_coineal_class.trader_class(pair)
    trader.load_coin(pair)
    coineal_trade(trader, pair)

    now = datetime.now()
    logger.warning("========== Now: " + str(now.strftime('%Y-%m-%d %H:%M:%S')))

    period = timedelta(days=day, hours=hour, minutes=min, seconds=second)
    next_time = now + period

    while True:
        # Get system current time
        now = datetime.now()
        if now >= next_time:
            coineal_trade(trader, pair)
            next_time = now + period
            logger.warning("========== Next_run: " + str(next_time.strftime('%Y-%m-%d %H:%M:%S')))
            continue


# start from here ......
loop_coineal_trade(sys.argv[1])
# loop_coineal_trade('ethusdt')

