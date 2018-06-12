#
#from scrapy import project, signals


#import scrapy
'''
copy the from scrapy from the environment
just for easy run by IDE for debug purpose!

'''
import re
import sys

from scrapy.cmdline import execute


if __name__ == '__main__':

    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.argv.append('crawl')
    sys.argv.append('zjlx')

    sys.exit(execute())