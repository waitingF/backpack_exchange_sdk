# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import queue
import threading
import time

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
            time.sleep(1)

    def close(self):
        self.shut_down = True


if __name__ == "__main__":
    #
    # # Get all supported assets
    # assets = public_client.get_assets()
    # print(assets)
    #
    # # Get ticker information for a specific symbol

    tickers = TickerThread()
    tickers.start()



    client = AuthenticationClient()
    client.setup(key, secret)


    # Get account balances
    balances = client.get_balances()
    print(balances)
    orders = client.get_order_history(SOL_USDC)
    for order in orders:
        print(order)
    print(client.get_open_orders(SOL_USDC))
    # print(client.execute_order("Limit", "Bid", SOL_USDC, quantity="0.01", price="152.2"))


    # Request a withdrawal
    # response = client.request_withdrawal('xxxxaddress', 'Solana', '0,1', 'Sol')
    # print(response)

    # public_client = PublicClient()
    #
    # # Get all supported assets
    # assets = public_client.get_assets()
    # print(assets)
    #
    # # Get ticker information for a specific symbol
    # ticker = public_client.get_ticker('SOL_USDC')
    # print(ticker)

    # print(PublicClient().get_klines(SOL_USDC, "1m"))


    # while True:
    #     tick = tick_queue.get()
    #     print(datetime.datetime.now(), tick)

    tickers.close()