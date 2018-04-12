#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/12 16:12
# @Author  : dx
# @File    : errors.py


class WrongParameterError(Exception):
    """
    wrong parameter type
    """

    def __init__(self, message=''):
        super(Exception, self).__init__()
        self.message = message
