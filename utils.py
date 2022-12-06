import math
import numpy as np
from datetime import datetime
from pyecharts import options as opts
from pyecharts.charts import Kline, Line


def date_minus(day1, day2):
    d1 = datetime.strptime(day1, '%Y-%m-%d')
    d2 = datetime.strptime(day2, '%Y-%m-%d')
    return (d1 - d2).days


def min_gain_rate(gain_rates):
    assert len(gain_rates) > 0
    min_prods = []
    starts = []
    for i, n in enumerate(gain_rates):
        # n: [start_date, end_date, gain_rate]
        if i == 0:
            min_prods.append(n[2])
            starts.append(i)
            continue
        if n[2] * min_prods[-1] < n[2]:
            min_prods.append(n[2] * min_prods[-1])
            starts.append(starts[-1])
        else:
            min_prods.append(n[2])
            starts.append(i)
    min_idx = np.argmin(min_prods)
    start_idx = starts[min_idx]

    return gain_rates[start_idx: min_idx + 1]


def draw_line(x, y, save_path):
    line = (
        Line()
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        )
        .add_xaxis(xaxis_data=x)
        .add_yaxis(
            series_name="累计收益",
            y_axis=y,
            symbol="emptyCircle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
    )
    line.render(save_path)


def draw_lines(x, ys, names, save_path):
    line = Line()
    line.set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        )
    line.add_xaxis(xaxis_data=x)
    for y, name in zip(ys, names):
        line.add_yaxis(
            series_name=name,
            y_axis=y,
            symbol="emptyCircle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False),
        )

    line.render(save_path)


def compute_grid_interval_v2(price, base, grow_rate):
    assert grow_rate > 1.

    if price >= base:
        min_n = int(math.ceil((math.log10(price / base)) / (math.log10(grow_rate))))
        low_line = base * np.power(grow_rate, min_n - 1)
        high_line = base * np.power(grow_rate, min_n)
        return [low_line, high_line]
    else:
        max_n = int(math.ceil((math.log10(base / price)) / (math.log10(grow_rate))))
        low_line = base * np.power(1 / grow_rate, max_n)
        high_line = base * np.power(1 / grow_rate, max_n - 1)
        return [low_line, high_line]


def compute_kdj(hist, pre_k, pre_d):
    high = hist['high'].max()
    low = hist['low'].min()
    close = hist.iloc[-1]['close']
    rsv = (close - low) / (high - low) * 100
    k = 2 / 3 * pre_k + 1 / 3 * rsv
    d = 2 / 3 * pre_d + 1 / 3 * k
    j = 3 * k - 2 * d
    return k, d, j
