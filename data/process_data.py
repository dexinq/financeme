#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/12 15:31
# @Author  : dx
# @File    : process_data.py


class ProcessData(object):
    """
    this is parent class, for process origin data and put into mysql
    """

    def __init__(self, filter_nan):
        self.filter_nan = filter_nan

    def _data_source(self):
        # get data from data_source indicate by type
        pass

    def get_data(self):
        return [{}]

    def process_data(self):
        raise NotImplementedError

    def _init_code_list(self):
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        pass


class CorrelationData(ProcessData):
    """
    to calculate Correlation between different stock set
    """

    def __init__(self, filter_nan=True):
        super(CorrelationData, self).__init__(filter_nan)

    def process_data(self):
        data_to_process = self.get_data()
        pass

    def _init_code_list(self):
        pass
