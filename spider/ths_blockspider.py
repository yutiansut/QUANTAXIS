import requests
from lxml import etree


def QA_Mod_ths_blockspider():
    url_list = ['gn', 'dy', 'thshy', 'zjhhy']  # 概念/地域/同花顺板块/证监会板块
    data = []
    for item in url_list:
        tree = etree.HTML(requests.get(
            'http://q.10jqka.com.cn/{}/'.format(item)).text)
        gn = tree.xpath('/html/body/div/div/div/div/div/a/text()')
        gpath = tree.xpath('/html/body/div/div/div/div/div/a/@href')
        for _i in range(len(gn)):
            for i in range(1, 15):
                _data = etree.HTML(requests.get(
                    'http://q.10jqka.com.cn/{}/detail/order/desc/page/{}/ajax/1/code/{}'.format(item, i, gpath[_i].split('/')[-2])).text)
                name = _data.xpath('/html/body/table/tbody/tr/td[3]/a/text()')
                code = _data.xpath('/html/body/table/tbody/tr/td[3]/a/@href')
                for i_ in range(len(name)):
                    print('{}-{}-{}-{}-{}-{}'.format(item, gn[_i], gpath[_i].split(
                        '/')[-2], name[i_], code[i_].split('/')[-1], code[i_]))
                    data.append([item, gn[_i], gpath[_i].split(
                        '/')[-2], name[i_], code[i_].split('/')[-1], code[i_]])

    return data
