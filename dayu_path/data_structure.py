#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

from collections import namedtuple

# 系列化返回结果定义的namedTuple 结构
SequentialFiles = namedtuple('SequentialFiles', ('filename', 'frames', 'missing'))
