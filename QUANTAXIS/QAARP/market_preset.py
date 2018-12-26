#


class per_unit():
    def __init__(self):
        self.unit_table = {
            'P': 10,
            'Y': 10,
            'M': 10,
            'A': 10,
            'B': 10,
            'C': 10,
            'L': 5,
            'JD': 10,
            'J': 100,
            'JM': 60,
            'FB': 500,
            'I': 100,
            'PP': 5,
            'BB': 500,
            'V': 5,
            'CS': 10,
            'EG': 10,
            'AL': 5,
            'AU': 1000,
            'CU': 5,
            'RU': 10,
            'FU': 10,
            'RB': 10,
            'WR': 10,
            'ZN': 5,
            'BU': 10,
            'AG': 15,
            'SN': 1,
            'NI': 1,
            'HC': 10,
            'PB': 5,
            'SP': 10,
            'T': 10000,
            'IC': 200,
            'IH': 300,
            'IF': 300,
            'TF': 10000,
            'TS': 20000
        }

    def get(self, code):
        return self.unit_table.get(code[0:-2])


class MARKET_PRESET:

    def __init__(self):
        self.table = {

            ### 大商所 DCE ##########################################
            'P': {'unit_table': 10, 'commission_coeff_peramount': 0, 'commission_coeff_pervol': 2.5, 'commission_coeff_today_peramount': 0, 'commission_coeff_today_pervol': 1.25},  # 棕榈油
            'Y': {'unit_table': 10, 'commission_coeff_peramount': 0, 'commission_coeff_pervol': 2.5, 'commission_coeff_today_peramount': 0, 'commission_coeff_today_pervol': 1.25},  # 豆油
            'M': {'unit_table': 10, 'commission_coeff_peramount': 0, 'commission_coeff_pervol': 1.5, 'commission_coeff_today_peramount': 0, 'commission_coeff_today_pervol': 0.75},  # 豆粕
            'A': {'unit_table': 10, 'commission_coeff_peramount': 0, 'commission_coeff_pervol': 2, 'commission_coeff_today_peramount': 0, 'commission_coeff_today_pervol': 2},  # 豆一
            'B': {'unit_table': 10, 'commission_coeff_peramount': 0, 'commission_coeff_pervol': 1, 'commission_coeff_today_peramount': 0, 'commission_coeff_today_pervol': 1},  # 豆二
            'C': {'unit_table': 10, 'commission_coeff_peramount': 0, 'commission_coeff_pervol': 1.2, 'commission_coeff_today_peramount': 0, 'commission_coeff_today_pervol': 0.6},  # 玉米
            'L': {'unit_table': 5, 'commission_coeff_peramount': 0, 'commission_coeff_pervol': 2, 'commission_coeff_today_peramount': 0, 'commission_coeff_today_pervol': 1},  # 塑料/聚乙烯
            'JD': {'unit_table': 10, 'commission_coeff_peramount': 0.00015, 'commission_coeff_pervol': 0, 'commission_coeff_today_peramount': 0.00015, 'commission_coeff_today_pervol': 0},  # 鸡蛋
            'J': {'unit_table': 100, 'commission_coeff_peramount': 0.00006, 'commission_coeff_pervol': 0, 'commission_coeff_today_peramount': 0.00018, 'commission_coeff_today_pervol': 0},  # 焦炭
            'JM': {'unit_table': 60, 'commission_coeff_peramount': 0.00006, 'commission_coeff_pervol': 0, 'commission_coeff_today_peramount': 0.00018, 'commission_coeff_today_pervol': 0},  # 焦煤
            'FB': {'unit_table': 500, 'commission_coeff_peramount': 0.0001, 'commission_coeff_pervol': 0, 'commission_coeff_today_peramount': 0.00005, 'commission_coeff_today_pervol': 0},  # 纤维板
            'I': {'unit_table': 100, 'commission_coeff_peramount': 0.00006, 'commission_coeff_pervol': 0, 'commission_coeff_today_peramount': 0.00006, 'commission_coeff_today_pervol': 0},  # 铁矿石
            'PP': {'unit_table': 5, 'commission_coeff_peramount': 0.00006, 'commission_coeff_pervol': 0, 'commission_coeff_today_peramount': 0.00003, 'commission_coeff_today_pervol': 0},  # 聚丙烯
            'EG': {'unit_table': 10, 'commission_coeff_peramount': 0, 'commission_coeff_pervol': 4, 'commission_coeff_today_peramount': 0, 'commission_coeff_today_pervol': 2},  # 乙二醇
            'BB': {'unit_table': 500, 'commission_coeff_peramount': 0.0001, 'commission_coeff_pervol': 0, 'commission_coeff_today_peramount': 0.00005, 'commission_coeff_today_pervol': 0},  # 胶合板
            'V': {'unit_table': 5, 'commission_coeff_peramount': 0, 'commission_coeff_pervol': 2, 'commission_coeff_today_peramount': 0, 'commission_coeff_today_pervol': 1},  # 聚氯乙烯
            'CS':  {'unit_table': 10, 'commission_coeff_peramount': 0, 'commission_coeff_pervol': 1.5, 'commission_coeff_today_peramount': 0, 'commission_coeff_today_pervol': 0.75},  # 玉米淀粉
            ### 上期所 SHFE ##########################################
            'AL': 5,
            'AU': 1000,
            'CU': 5,
            'RU': 10,
            'FU': 10,
            'RB': 10,
            'WR': 10,
            'ZN': 5,
            'BU': 10,
            'AG': 15,
            'SN': 1,
            'NI': 1,
            'HC': 10,
            'PB': 5,
            'SP': 10,
            ###  中金所 CFFEX #######################################
            'T': 10000,
            'IC': 200,
            'IH': 300,
            'IF': 300,
            'TF': 10000,
            'TS': 20000,
            #### 郑商所 ZCE  ########################################
            'RI': 20,
            'RO': 5,
            'SR': 10,
            'TA': 5,
            'WS': 10,
            'FG': 20,
            'OI': 10,
            'ZC': 100,
            'CF': 5,
            'WT': 10,
            'RM': 10,
            'PM': 10,
            'SM': 5,
            'SF': 5,
            'LR': 20,
            'MA': 10,
            'JR': 20,
            'RS': 10,
            'CY': 5,
            'AP': 10,

        }

    # 手续费比例
    def get_commission_coeff(self, code, dtype):
        pass

    # 印花税系数
    def get_tax_coeff(self, code, dtype):
        pass

    # 交易时间
    def get_trade_time(self, code, dtype):
        pass

    # 交易日期
    def get_trade_day(self, code, dtype):
        pass

    # 交易规则( t0/sell_open)
    def get_trade_rules(self, code, dtypes):
        pass

    # 交易杠杆
    def get_trade_margin(self, code, dtypes):
        pass
