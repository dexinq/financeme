#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/12 15:31
# @Author  : dx
# @File    : process_data.py

import pandas as pd
import tushare as ts

from errors import WrongParameterError


class ProcessData(object):
    """
    this is parent class, for process origin data and put into mysql
    """

    def __init__(self, filter_nan):
        self.filter_nan = filter_nan
        self.code_list = list()
        self.start = ''
        self.end = ''

    def _data_source(self):
        # get data from data_source indicate by type
        pass

    def get_data(self, fetch_data_func=None):
        res_dt = pd.DataFrame()
        if not fetch_data_func:
            fetch_data_func = ts.get_hist_data
            for code in self.code_list:
                # print code, self.start, self.end
                temp_d = fetch_data_func(code=code, start=self.start, end=self.end)
                if temp_d is not None:
                    td = temp_d['price_change']
                    res_dt[code] = td
        if self.filter_nan:
            res_dt.dropna(axis=1, how='any')

        return res_dt

    def process_data(self):
        raise NotImplementedError

    def init_code_list(self, code_list=list()):
        pass

    def __call__(self, *args, **kwargs):
        return self.init_code_list(code_list=kwargs.get('code_list', []))


class CorrelationData(ProcessData):
    """
    to calculate Correlation between different stock set
    """

    def __init__(self, filter_nan=True, start='', end=''):
        super(CorrelationData, self).__init__(filter_nan)
        self.start = start
        self.end = end

    def process_data(self):
        data_to_process = self.get_data()
        corr = data_to_process.corr()
        f_res = list()
        for code in self.code_list:
            co = corr.get(code, None)
            if co is None:
                continue
            max_corr = co.sort_values(ascending=False)
            corr_code = max_corr.index[1]
            corr_value = max_corr.values[1]
            f_res.append((code, corr_code, corr_value))
        return f_res

    def init_code_list(self, code_list=list()):
        if not isinstance(code_list, list):
            raise WrongParameterError(message="parameter code list is expected list type")

        self.code_list = code_list
        return self.process_data()


if __name__ == "__main__":
    cd = CorrelationData(start='2018-01-01', end='2018-04-11')
    code = ts.get_hs300s()['code'].tolist()
    # d = cd(code_list=code)
    # print len(d)
