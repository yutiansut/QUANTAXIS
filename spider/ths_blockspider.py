import requests
from lxml import etree


url_list=['gn','dy','thshy','zjhhy']



for item in url_list:
    tree=etree.HTML(requests.get('http://q.10jqka.com.cn/{}/'.format(item)).text)
    gn=tree.xpath('/html/body/div/div/div/div/div/a/text()')
    gpath=tree.xpath('/html/body/div/div/div/div/div/a/@href')

    for _i in range(len(gn)):

        for i in range(1,15):

               # print('http://q.10jqka.com.cn/{}/detail/order/desc/page/{}/ajax/1/code/{}'.format(item,i,gpath[_i].split('/')[-2]))
                data=etree.HTML(requests.get('http://q.10jqka.com.cn/{}/detail/order/desc/page/{}/ajax/1/code/{}'.format(item,i,gpath[_i].split('/')[-2])).text)
                name=data.xpath('/html/body/table/tbody/tr/td[3]/a/text()')
                code=data.xpath('/html/body/table/tbody/tr/td[3]/a/@href')
                for i_ in range(len(name)):
                    
                    print('{}-{}-{}-{}-{}-{}'.format(item,gn[_i],gpath[_i].split('/')[-2],name[i_],code[i_].split('/')[-1],code[i_]))
