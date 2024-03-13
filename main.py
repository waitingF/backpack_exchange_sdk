# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import queue
import threading
import time
from datetime import datetime

import numpy as np
import bisect

from backpack_exchange_sdk.authenticated import AuthenticationClient
from backpack_exchange_sdk.public import PublicClient
from config import key, secret

SOL_USDC = "SOL_USDC"

tick_queue = queue.Queue()


class TickerThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.public_client = PublicClient()
        self.shut_down = False

    def run(self):
        while not self.shut_down:
            tick = self.public_client.get_ticker(SOL_USDC)
            tick_queue.put(tick)
            time.sleep(2)

    def close(self):
        self.shut_down = True

    # init
    # 2709.89 USDC
if __name__ == "__main__":
    _low = 120
    _high = 160
    grids = [i * 1.0 for i in range(_low, _high + 1, 1)]
    holds = [0.0 for i in range(_low, _high + 1, 1)]
    print(grids, len(grids))

    last_grid = 0

    def find_grid(price: float) -> int:
        res = 0
        for i in range(len(grids)):
            if grids[i] > price:
                break
            else:
                res = i
        return res

    # print(110, find_grid(110), grids[find_grid(110)])
    # print(120, find_grid(120), grids[find_grid(120)])
    # print(121, find_grid(121), grids[find_grid(121)])
    # print(121.1, find_grid(121.1), grids[find_grid(121.1)])
    # print(128.1, find_grid(128.1), grids[find_grid(128.1)])
    # print(160, find_grid(160), grids[find_grid(160)])
    # print(170, find_grid(170), grids[find_grid(170)])

    tickers = TickerThread()
    tickers.start()



    tick_count = 0
    while True:
        tick_count += 1
        tick = tick_queue.get()
        last_price = tick['lastPrice']
        grid_id = find_grid(float(last_price))
        # print(datetime.now(), grid_id, grids[grid_id], last_price)
        quantity = 0.2

        if tick_count % 30 == 0:
            print(datetime.now(), grid_id, grids[grid_id], last_price)

        if last_grid == 0:
            last_grid = grid_id
            print("初始价格 %s 网格id=%s" % (last_price, grid_id))
            continue

        stride = grid_id - last_grid
        if stride == 0: # 同一个网格，不卖出
            pass
        elif stride > 0: # 网格往上走了，卖出

            print("以价格 %s 卖出 %s" % (last_price, quantity * stride))
            pass
        else: # 网格往下走了，买入

            print("以价格 %s 买入 %s" % (last_price, quantity * (-1 * stride)))
            # client.execute_order("Limit", "Bid", SOL_USDC, quantity=quantity, price=str(last_price))
            pass

        last_grid = grid_id



    # Get account balances
    balances = client.get_balances()
    print(balances)
    orders = client.get_order_history(SOL_USDC)
    for order in orders:
        print(order)
    print(client.get_open_orders(SOL_USDC))
    # print(client.execute_order("Limit", "Bid", SOL_USDC, quantity="0.01", price="152.2"))

    # while True:
    #     tick = tick_queue.get()
    #     print(datetime.datetime.now(), tick)

    tickers.close()


    '''
buy
{
  "symbol": "SOL_USDC",
  "side": "Bid",
  "orderType": "Limit",
  "quantity": "1.00",
  "price": "149.50",
  "postOnly": false
}

sell
{
  "symbol": "SOL_USDC",
  "side": "Ask",
  "orderType": "Limit",
  "quantity": "0.01",
  "price": "150.50",
  "postOnly": false
}
    
    
    '''