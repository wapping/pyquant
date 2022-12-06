# -*- coding: utf-8 -*-
import os
import akshare as ak
from tqdm import tqdm


def download_a_list():
    data_path = ""
    a_list = ak.stock_zh_a_spot_em()
    a_list.to_csv(data_path)


def download_all_a_hist():
    """下载A股历史数据"""
    
    save_dir = ""
    os.makedirs(save_dir, exist_ok=True)

    a_list = ak.stock_zh_a_spot_em()
    
    with tqdm(range(a_list.__len__())) as t:
        for i in t:
            row = a_list.iloc[i]
            code = row['代码']
            t.set_postfix(code=code)
            hist = ak.stock_zh_a_hist(code)
            hist.to_csv(os.path.join(save_dir, code + ".csv"))

