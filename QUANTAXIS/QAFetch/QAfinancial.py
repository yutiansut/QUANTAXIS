# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2018 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sys
import requests
import pandas as pd
from pytdx.reader.history_financial_reader import HistoryFinancialReader
from pytdx.crawler.history_financial_crawler import HistoryFinancialCrawler
from QUANTAXIS.QAUtil.QAFile import QA_util_file_md5
from QUANTAXIS.QASetting.QALocalize import qa_path, download_path
"""
参见PYTDX 1.65
"""

FINANCIAL_URL = 'http://down.tdx.com.cn:8001/fin/gpcw.txt'


class QAHistoryFinancialCrawler(HistoryFinancialCrawler):

    def to_df(self, data):
        if len(data) == 0:
            return None

        total_lengh = len(data[0])
        col = ['code', 'report_date']

        length = total_lengh - 2
        for i in range(0, length):
            col.append('00{}'.format(str(i + 1))[-3:])

        df = pd.DataFrame(data=data, columns=col)
        df.set_index('code', inplace=True)
        return df


class QAHistoryFinancialReader(HistoryFinancialReader):

    def get_df(self, data_file):
        """
        读取历史财务数据文件，并返回pandas结果 ， 类似gpcw20171231.zip格式，具体字段含义参考

        https://github.com/rainx/pytdx/issues/133

        :param data_file: 数据文件地址， 数据文件类型可以为 .zip 文件，也可以为解压后的 .dat
        :return: pandas DataFrame格式的历史财务数据
        """

        crawler = QAHistoryFinancialCrawler()

        with open(data_file, 'rb') as df:
            data = crawler.parse(download_file=df)

        return crawler.to_df(data)


def get_filename():
    """
    get_filename
    """
    return [(l[0],l[1]) for l in [line.strip().split(",") for line in requests.get(FINANCIAL_URL).text.strip().split('\n')]]



def get_md5():
    return [l[1] for l in [line.strip().split(",") for line in requests.get(FINANCIAL_URL).text.strip().split('\n')]]

def download_financialzip():
    """
    会创建一个download/文件夹
    """
    result = get_filename()
    res = []
    for item, md5 in result:
        if item in os.listdir(download_path) and md5==QA_util_file_md5('{}{}{}'.format(download_path,os.sep,item)):
            
            print('FILE {} is already in {}'.format(item, download_path))
        else:
            print('CURRENTLY GET/UPDATE {}'.format(item[0:12]))
            r = requests.get('http://down.tdx.com.cn:8001/fin/{}'.format(item))

            file = '{}{}{}'.format(download_path, os.sep, item)

            with open(file, "wb") as code:
                code.write(r.content)
            res.append(item)
    return res


def get_and_parse(filename):
    return QAHistoryFinancialReader().get_df(filename)


def parse_filelist(filelist):

    return pd.concat([get_and_parse('{}{}{}'.format(download_path, os.sep, item)) for item in filelist])


def parse_all():
    """
    解析目录下的所有文件
    """
    #filepath = '{}{}{}{}'.format(qa_path, os.sep, 'downloads', os.sep)
    filename = os.listdir(download_path)

    return parse_filelist(filename)


financialmeans = ['基本每股收益',
                  '扣除非经常性损益每股收益',
                  '每股未分配利润',
                  '每股净资产',
                  '每股资本公积金',
                  '净资产收益率',
                  '每股经营现金流量',
                  '货币资金',
                  '交易性金融资产',
                  '应收票据',
                  '应收账款',
                  '预付款项',
                  '其他应收款',
                  '应收关联公司款',
                  '应收利息',
                  '应收股利',
                  '存货',
                  '其中：消耗性生物资产',
                  '一年内到期的非流动资产',
                  '其他流动资产',
                  '流动资产合计',
                  '可供出售金融资产',
                  '持有至到期投资',
                  '长期应收款',
                  '长期股权投资',
                  '投资性房地产',
                  '固定资产',
                  '在建工程',
                  '工程物资',
                  '固定资产清理',
                  '生产性生物资产',
                  '油气资产',
                  '无形资产',
                  '开发支出',
                  '商誉',
                  '长期待摊费用',
                  '递延所得税资产',
                  '其他非流动资产',
                  '非流动资产合计',
                  '资产总计',
                  '短期借款',
                  '交易性金融负债',
                  '应付票据',
                  '应付账款',
                  '预收款项',
                  '应付职工薪酬',
                  '应交税费',
                  '应付利息',
                  '应付股利',
                  '其他应付款',
                  '应付关联公司款',
                  '一年内到期的非流动负债',
                  '其他流动负债',
                  '流动负债合计',
                  '长期借款',
                  '应付债券',
                  '长期应付款',
                  '专项应付款',
                  '预计负债',
                  '递延所得税负债',
                  '其他非流动负债',
                  '非流动负债合计',
                  '负债合计',
                  '实收资本（或股本）',
                  '资本公积',
                  '盈余公积',
                  '减：库存股',
                  '未分配利润',
                  '少数股东权益',
                  '外币报表折算价差',
                  '非正常经营项目收益调整',
                  '所有者权益（或股东权益）合计',
                  '负债和所有者（或股东权益）合计',
                  '其中：营业收入',
                  '其中：营业成本',
                  '营业税金及附加',
                  '销售费用',
                  '管理费用',
                  '堪探费用',
                  '财务费用',
                  '资产减值损失',
                  '加：公允价值变动净收益',
                  '投资收益',
                  '其中：对联营企业和合营企业的投资收益',
                  '影响营业利润的其他科目',
                  '三、营业利润',
                  '加：补贴收入',
                  '营业外收入',
                  '减：营业外支出',
                  '其中：非流动资产处置净损失',
                  '加：影响利润总额的其他科目',
                  '四、利润总额',
                  '减：所得税',
                  '加：影响净利润的其他科目',
                  '五、净利润',
                  '归属于母公司所有者的净利润',
                  '少数股东损益',
                  '销售商品、提供劳务收到的现金',
                  '收到的税费返还',
                  '收到其他与经营活动有关的现金',
                  '经营活动现金流入小计',
                  '购买商品、接受劳务支付的现金',
                  '支付给职工以及为职工支付的现金',
                  '支付的各项税费',
                  '支付其他与经营活动有关的现金',
                  '经营活动现金流出小计',
                  '经营活动产生的现金流量净额',
                  '收回投资收到的现金',
                  '取得投资收益收到的现金',
                  '处置固定资产、无形资产和其他长期资产收回的现金净额',
                  '处置子公司及其他营业单位收到的现金净额',
                  '收到其他与投资活动有关的现金',
                  '投资活动现金流入小计',
                  '购建固定资产、无形资产和其他长期资产支付的现金',
                  '投资支付的现金',
                  '取得子公司及其他营业单位支付的现金净额',
                  '支付其他与投资活动有关的现金',
                  '投资活动现金流出小计',
                  '投资活动产生的现金流量净额',
                  '吸收投资收到的现金',
                  '取得借款收到的现金',
                  '收到其他与筹资活动有关的现金',
                  '筹资活动现金流入小计',
                  '偿还债务支付的现金',
                  '分配股利、利润或偿付利息支付的现金',
                  '支付其他与筹资活动有关的现金',
                  '筹资活动现金流出小计',
                  '筹资活动产生的现金流量净额',
                  '四、汇率变动对现金的影响',
                  '四(2)、其他原因对现金的影响',
                  '五、现金及现金等价物净增加额',
                  '期初现金及现金等价物余额',
                  '期末现金及现金等价物余额',
                  '净利润',
                  '加：资产减值准备',
                  '固定资产折旧、油气资产折耗、生产性生物资产折旧',
                  '无形资产摊销',
                  '长期待摊费用摊销',
                  '处置固定资产、无形资产和其他长期资产的损失',
                  '固定资产报废损失',
                  '公允价值变动损失',
                  '财务费用',
                  '投资损失',
                  '递延所得税资产减少',
                  '递延所得税负债增加',
                  '存货的减少',
                  '经营性应收项目的减少',
                  '经营性应付项目的增加',
                  '其他',
                  '经营活动产生的现金流量净额2',
                  '债务转为资本',
                  '一年内到期的可转换公司债券',
                  '融资租入固定资产',
                  '现金的期末余额',
                  '减：现金的期初余额',
                  '加：现金等价物的期末余额',
                  '减：现金等价物的期初余额',
                  '现金及现金等价物净增加额',
                  '流动比率',
                  '速动比率',
                  '现金比率(%)',
                  '利息保障倍数',
                  '非流动负债比率(%)',
                  '流动负债比率(%)',
                  '现金到期债务比率(%)',
                  '有形资产净值债务率(%)',
                  '权益乘数(%)',
                  '股东的权益/负债合计(%)',
                  '有形资产/负债合计(%)',
                  '经营活动产生的现金流量净额/负债合计(%)',
                  'EBITDA/负债合计(%)',
                  '应收帐款周转率',
                  '存货周转率',
                  '运营资金周转率',
                  '总资产周转率',
                  '固定资产周转率',
                  '应收帐款周转天数',
                  '存货周转天数',
                  '流动资产周转率',
                  '流动资产周转天数',
                  '总资产周转天数',
                  '股东权益周转率',
                  '营业收入增长率(%)',
                  '净利润增长率(%)',
                  '净资产增长率(%)',
                  '固定资产增长率(%)',
                  '总资产增长率(%)',
                  '投资收益增长率(%)',
                  '营业利润增长率(%)',
                  '暂无',
                  '暂无',
                  '暂无',
                  '成本费用利润率(%)',
                  '营业利润率',
                  '营业税金率',
                  '营业成本率',
                  '净资产收益率',
                  '投资收益率',
                  '销售净利率(%)',
                  '总资产报酬率',
                  '净利润率',
                  '销售毛利率(%)',
                  '三费比重',
                  '管理费用率',
                  '财务费用率',
                  '扣除非经常性损益后的净利润',
                  '息税前利润(EBIT)',
                  '息税折旧摊销前利润(EBITDA)',
                  'EBITDA/营业总收入(%)',
                  '资产负债率(%)',
                  '流动资产比率',
                  '货币资金比率',
                  '存货比率',
                  '固定资产比率',
                  '负债结构比',
                  '归属于母公司股东权益/全部投入资本(%)',
                  '股东的权益/带息债务(%)',
                  '有形资产/净债务(%)',
                  '每股经营性现金流(元)',
                  '营业收入现金含量(%)',
                  '经营活动产生的现金流量净额/经营活动净收益(%)',
                  '销售商品提供劳务收到的现金/营业收入(%)',
                  '经营活动产生的现金流量净额/营业收入',
                  '资本支出/折旧和摊销',
                  '每股现金流量净额(元)',
                  '经营净现金比率（短期债务）',
                  '经营净现金比率（全部债务）',
                  '经营活动现金净流量与净利润比率',
                  '全部资产现金回收率',
                  '营业收入',
                  '营业利润',
                  '归属于母公司所有者的净利润',
                  '扣除非经常性损益后的净利润',
                  '经营活动产生的现金流量净额',
                  '投资活动产生的现金流量净额',
                  '筹资活动产生的现金流量净额',
                  '现金及现金等价物净增加额',
                  '总股本',
                  '已上市流通A股',
                  '已上市流通B股',
                  '已上市流通H股',
                  '股东人数(户)',
                  '第一大股东的持股数量',
                  '十大流通股东持股数量合计(股)',
                  '十大股东持股数量合计(股)',
                  '机构总量（家）',
                  '机构持股总量(股)',
                  'QFII机构数',
                  'QFII持股量',
                  '券商机构数',
                  '券商持股量',
                  '保险机构数',
                  '保险持股量',
                  '基金机构数',
                  '基金持股量',
                  '社保机构数',
                  '社保持股量',
                  '私募机构数',
                  '私募持股量',
                  '财务公司机构数',
                  '财务公司持股量',
                  '年金机构数',
                  '年金持股量',
                  '十大流通股东中持有A股合计(股)',
                  '第一大流通股东持股量(股)',
                  '自由流通股(股)',
                  '受限流通A股(股)',
                  '一般风险准备(金融类)',
                  '其他综合收益(利润表)',
                  '综合收益总额(利润表)',
                  '归属于母公司股东权益(资产负债表)',
                  '银行机构数(家)(机构持股)',
                  '银行持股量(股)(机构持股)',
                  '一般法人机构数(家)(机构持股)',
                  '一般法人持股量(股)(机构持股)',
                  '近一年净利润(元)']
if __name__ == '__main__':
    # download()
    parse_all()
