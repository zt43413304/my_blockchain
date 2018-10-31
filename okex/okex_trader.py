import time

from okex.exchange_okex import Exchange_Okex


class Strategy(object):

    def __init__(self):

        self.okex = Exchange_Okex()
        self.orderbooks = {}
        self.orderbooks['quarter'] = {}
        self.orderbooks['this_week'] = {}

    # 获取季度合约和当周合约的深度
    def get_orderbooks(self, symbol, depth):
        self.orderbooks['quarter'] = self.okex.get_sorted_orderbook(symbol, "quarter", depth)
        self.orderbooks['this_week'] = self.okex.get_sorted_orderbook(symbol, "this_week", depth)

    # 显示深度数据
    def display_orderbooks(self):
        print(self.orderbooks)

    # 做空季度，做多当周
    def quarter_open_short_(self, order_qty):
        self.okex.do_Future_Tx('eos', "quarter", str(self.orderbooks['quarter']['bids'][0][0] * 0.995), order_qty, "2",
                               "0")  # 做空季度
        self.okex.do_Future_Tx('eos', "this_week", str(self.orderbooks['this_week']['asks'][0][0] * 1.005), order_qty,
                               "1", "0")  # 做多当周

    # 季度平空，当周平多
    def quarter_close_short_(self, order_qty):
        self.okex.do_Future_Tx('eos', "quarter", str(self.orderbooks['quarter']['asks'][0][0] * 1.005), order_qty, "4",
                               "0")  # 季度平空
        self.okex.do_Future_Tx('eos', "this_week", str(self.orderbooks['this_week']['bids'][0][0] * 0.995), order_qty,
                               "3", "0")  # 当周平多

    # 做多季度，做空当周
    def quarter_open_long_(self, order_qty):
        self.okex.do_Future_Tx('eos', "quarter", str(self.orderbooks['quarter']['asks'][0][0] * 1.005), order_qty, "1",
                               "0")  # 做多季度
        self.okex.do_Future_Tx('eos', "this_week", str(self.orderbooks['this_week']['bids'][0][0] * 0.995), order_qty,
                               "2", "0")  # 做空当周

    # 季度平多，当周平空
    def quarter_close_long_(self, order_qty):
        self.okex.do_Future_Tx('eos', "quarter", str(self.orderbooks['quarter']['bids'][0][0] * 0.995), order_qty, "3",
                               "0")  # 季度平多
        self.okex.do_Future_Tx('eos', "this_week", str(self.orderbooks['this_week']['asks'][0][0] * 1.005), order_qty,
                               "4", "0")  # 当周平空

    # 主循环
    def main_loop(self):

        self.get_orderbooks(self.symbol, self.depth)
        self.display_orderbooks()

        # 求正向价差
        forward_gap = (self.orderbooks['quarter']['bids'][0][0] - self.orderbooks['this_week']['asks'][0][0])
        # 求反向价差
        rev_gap = (self.orderbooks['quarter']['asks'][0][0] - self.orderbooks['this_week']['bids'][0][0])

        print("forward_gap is: " + str(forward_gap) + "\n")
        print("rev_gap is: " + str(rev_gap) + "\n")

        if rev_gap < self.limits['quarter_close_short'] and self.current_position < 0:
            # 平空(季度)
            self.quarter_close_short_(self.single_order_qty)
            self.current_position += self.single_order_qty

            self.orderbooks = {}
            return

        elif forward_gap > self.limits['quarter_close_long'] and self.current_position > 0:
            # 平多(季度)
            self.quarter_close_long_(self.single_order_qty)
            self.current_position -= self.single_order_qty

            self.orderbooks = {}
            return


        elif forward_gap > self.limits['quarter_open_short'] and self.current_position > -self.max_position:
            # 开空(季度)
            self.quarter_open_short_(self.single_order_qty)
            self.current_position -= self.single_order_qty

            self.orderbooks = {}
            return


        elif rev_gap < self.limits['quarter_open_long'] and self.current_position < self.max_position:
            # 开多(季度)
            self.quarter_open_long_(self.single_order_qty)
            self.current_position += self.single_order_qty

            self.orderbooks = {}
            return
        time.sleep(1)


def main():
    ok_api_key = "afddfc52-daf8-406e-9d00-ab9b293a2809"  # V1 api
    ok_api_secret = "6485D56167103DF339009A20D9F67ADA"

    strategy = Strategy()
    strategy.okex.auth(ok_api_key, ok_api_secret)

    strategy.get_orderbooks('eos', '5')
    strategy.display_orderbooks()

    # 参数设置
    strategy.symbol = "eos"
    strategy.depth = '5'
    strategy.single_order_qty = 1000  # 单次下单数量
    strategy.current_position = 0  # 当前仓位
    strategy.max_position = 100000  # 最大仓位
    strategy.limits = {"quarter_open_short": 0, "quarter_close_short": -0.028, "quarter_open_long": -0.03,
                       "quarter_close_long": 0}  # 开仓/平仓时价差设置
    # quarter_open_short: 季度开空(当周开多)价差
    # quarter_close_short：季度平空(当周平多)价差
    # quarter_open_long： 季度开多(当周开空)价差
    # quarter_close_long： 季度平多(当周平空)价差

    # 循环执行
    while (True):
        strategy.main_loop()


if __name__ == '__main__':
    main()
