#coding:utf-8
import csv


def QA_util_save_csv(data:list,name:str,location=None):
    assert isinstance(data,list)
    if location==None:
        path='./'+str(name)+'.csv'
    else:
        path=location+str(name)+'.csv'
    with open(path,'w',newline='') as f:
        csvwriter=csv.writer(f)
        for item in data:
            csvwriter.writerow([item])


if __name__=='__main__':
    QA_util_save_csv(['a','v',2,3],'test')