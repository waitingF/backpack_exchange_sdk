# -*- coding: utf-8 -*-
from grid_data import RunBetData
import time

from backpack_exchange_sdk.authenticated import AuthenticationClient
from backpack_exchange_sdk.public import PublicClient
from config import key, secret

runbet = RunBetData()


SOL_USDC = "SOL_USDC"
client = AuthenticationClient()
client.setup(key, secret)

def get_price():
    tick = PublicClient().get_ticker(SOL_USDC)
    return float(tick['lastPrice'])
    # print(PublicClient().get_markets())



class Run_Main():

    def __init__(self):
        self.coinType = runbet.get_cointype()  # 交易币种
        pass

    def loop_run(self):
        while True:
            cur_market_price = get_price() # 当前交易对市价
            grid_buy_price = runbet.get_buy_price()  # 当前网格买入价格
            grid_sell_price = runbet.get_sell_price() # 当前网格卖出价格
            quantity = runbet.get_quantity()   # 买入量
            step = runbet.get_step() # 当前步数

            if grid_buy_price >= cur_market_price:   # 是否满足买入价
                # res = msg.buy_limit_msg(self.coinType, quantity, grid_buy_price)
                res = client.execute_order("Limit", "Bid", SOL_USDC, quantity=quantity, price=str(grid_buy_price))
                print("以价格 %s 买入 %s" % (grid_buy_price, quantity), res)
                if res['id']: # 挂单成功
                    runbet.modify_price(grid_buy_price, step+1) #修改data.json中价格、当前步数
                    time.sleep(60) # 挂单后，停止运行1分钟
                else:
                    break

            elif grid_sell_price < cur_market_price:  # 是否满足卖出价
                if step==0: # setp=0 防止踏空，跟随价格上涨
                    runbet.modify_price(grid_sell_price,step)
                else:
                    # res = msg.sell_limit_msg(self.coinType, runbet.get_quantity(False), grid_sell_price)
                    res = client.execute_order("Limit", "Ask", SOL_USDC, quantity=quantity, price=str(grid_sell_price))
                    print("以价格 %s 卖出 %s" % (grid_sell_price, quantity), res)
                    if res['id']:
                        runbet.modify_price(grid_sell_price, step - 1)
                        time.sleep(60)  # 挂单后，停止运行1分钟
                    else:
                        break
            else:
                print("当前市价：{market_price}。未能满足交易,继续运行".format(market_price = cur_market_price))
                time.sleep(1)


if __name__ == "__main__":
    instance = Run_Main()
    try:
        instance.loop_run()
    except Exception as e:
        error_info = "报警：币种 {coin},服务停止.错误原因 {info}".format(coin=instance.coinType,info=str(e))
        print(error_info)

# 调试看报错运行下面，正式运行用上面
# if __name__ == "__main__":
    # instance = Run_Main()
    # instance.loop_run()