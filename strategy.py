# -*- coding: utf-8 -*-
import numpy as np
import logging
from utils import date_minus


class Strategy:
    
    def __init__(self, init_cash):
        self.init_cash = init_cash
        self.cash = self.init_cash
        self.wealth = self.cash
        self.holds = {}     # {code: detail}, detail: (avg_price, latest_price, volume, [(buy_date, buy_price, buy_volume), ...])
        self.all_assets, self.all_dates = [], []
        self.trade_times = 0
        self.win_times = 0
        self.start_date = ''
        self.end_date = ''
        self.first_trade_date = ''
        self.last_trade_date = ''
    
    def update_wealth(self):
        self.wealth = self.cash
        for code, detail in self.holds.items():
            latest_price = detail[1]
            vol = detail[2]
            self.wealth += (vol * latest_price)

    def compute_max_drawdown(self):
        assert len(self.all_assets) > 1 and len(self.all_assets) == len(self.all_dates)

        date_return_rates = []
        for i in range(1, len(self.all_assets)):
            return_rate = self.all_assets[i] / self.all_assets[i - 1]
            date_return_rates.append((self.all_dates[i], return_rate))

        min_prods = []
        starts = []
        for i, n in enumerate(date_return_rates):
            # n: [date, return_rate]
            if i == 0:
                min_prods.append(n[1])
                starts.append(i)
                continue
            if n[1] * min_prods[-1] < n[1]:
                min_prods.append(n[1] * min_prods[-1])
                starts.append(starts[-1])
            else:
                min_prods.append(n[1])
                starts.append(i)
        min_idx = np.argmin(min_prods)
        start_idx = starts[min_idx]

        return date_return_rates[start_idx: min_idx + 1]

    def summary(self):
        logging.info(f"\nstart date: {self.start_date}\n"
                     f"end date: {self.end_date}\n"
                     f"n_days: {date_minus(self.end_date,  self.start_date)}\n")

        return_date = (self.wealth - self.init_cash) / self.init_cash * 100
        y = date_minus(self.end_date, self.start_date) / 365
        yrr = (np.power((self.wealth / self.init_cash), 1 / y) - 1) * 100

        logging.info(f"init cash: {self.init_cash}\n"
                     f"final assets: {self.wealth}\n"
                     f"return rate: {round(return_date, 2)}%\n"
                     f"year return rate: {round(yrr, 2)}%\n")

        logging.info(f"trade times: {self.trade_times}\n"
                     f"win times: {self.win_times}\n"
                     f"win rate: {round(self.win_times / self.trade_times, 2)}\n")

        date_return_rates = self.compute_max_drawdown()
        logging.info(f"最小收益区间：{date_return_rates[0][0]}~{date_return_rates[-1][0]}\n"
                     f"总收益率为{np.prod([n[1] for n in date_return_rates])}")

    def back_test_in_days(self):
        pass

    def compare_with(self, code):
        pass
    