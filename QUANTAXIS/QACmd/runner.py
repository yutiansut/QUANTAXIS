# coding=utf-8
"""
QACmd runner - 策略/脚本运行入口

qarun 入口点，用于运行策略或启动主CLI。
"""
import sys


def run():
    """qarun 入口：启动 QUANTAXIS 主 CLI"""
    from QUANTAXIS.QACmd import QA_cmd
    QA_cmd()
