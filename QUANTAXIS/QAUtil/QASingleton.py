# -*- coding: utf-8 -*-

def singleton(cls):

    instances = {}

    def _wrapper(*args, **kwargs):

        if cls not in instances:

            instances[cls] = cls(*args, **kwargs)

        return instances[cls]

    return _wrapper