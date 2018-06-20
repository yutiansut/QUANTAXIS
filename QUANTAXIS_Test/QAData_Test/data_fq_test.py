import unittest

class QAData_fq_test(unittest.TestCase):

    '''
    wind 复权算法

    定点复权公司
    Pt’= P0* ( P1/ f1(P0))* ( P2/ f2(P1))*...*( Pt-1/ ft-1(Pt-2))*(Pt/ ft(Pt-1))

    Pt’:t 点复权价
    Pt:t 点交易价
    ft(Pt-1):昨收盘价

    当天交易价格/前一天的交易价格

    假设 股价 序列
    p[0:10] = [1.1,0.6,0.7,0.8,0.8,1.0,0.5,0.6,0.7,0.8]
    t=1 1转1股
    t=5 1转1股

    '''
    def fq_test(self):
        print("测试复权")
        pass
    pass