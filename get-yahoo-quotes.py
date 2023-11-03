#!/usr/bin/env python

"""
get-yahoo-quotes.py:  Script to download Yahoo historical quotes using the new cookie authenticated site.
 Usage: get-yahoo-quotes SYMBOL
 History
 06-03-2017 : Created script
"""

__author__ = "Brad Luicas"
__copyright__ = "Copyright 2017, Brad Lucas"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Brad Lucas"
__email__ = "brad@beaconhill.com"
__status__ = "Production"


import re
import sys
import time
import datetime
import requests
import calendar


def split_crumb_store(v):
    return v.split(':')[2].strip('"')


def find_crumb_store(lines):
    # Looking for
    # ,"CrumbStore":{"crumb":"9q.A4D1c.b9
    for l in lines:
        if re.findall(r'CrumbStore', l):
            return l
    print("Did not find CrumbStore")


def get_cookie_value(r):
    return {'B': r.cookies['B']}


def get_page_data(symbol):
    url = "https://finance.yahoo.com/quote/%s/?p=%s" % (symbol, symbol)
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:74.0) Gecko/20100101 Firefox/74.0'}
    r = requests.get(url,headers=headers)
    cookie = get_cookie_value(r)

    # Code to replace possible \u002F value
    # ,"CrumbStore":{"crumb":"FWP\u002F5EFll3U"
    # FWP\u002F5EFll3U
    lines = r.content.decode('unicode-escape').strip(). replace('}', '\n')
    return cookie, lines.split('\n')


def get_cookie_crumb(symbol):
    cookie, lines = get_page_data(symbol)
    crumb = split_crumb_store(find_crumb_store(lines))
    return cookie, crumb


def get_data(symbol, start_date, end_date, cookie, crumb):
    filename = '%s.csv' % (symbol)
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:74.0) Gecko/20100101 Firefox/74.0'}
    url = "https://query1.finance.yahoo.com/v7/finance/download/%s?period1=%s&period2=%s&interval=1d&events=history&crumb=%s" % (symbol, start_date, end_date, crumb)
    response = requests.get(url, cookies=cookie, headers=headers)
    with open (filename, 'wb') as handle:
        for block in response.iter_content(1024):
            handle.write(block)


def get_now_epoch():
    # @see https://www.linuxquestions.org/questions/programming-9/python-datetime-to-epoch-4175520007/#post5244109
    return int(time.time())

	
def get_time_epoch(iso_time):
    return calendar.timegm(time.strptime(iso_time, '%Y-%m-%d'))

	
def download_quotes(symbol, start_date, end_date):
    cookie, crumb = get_cookie_crumb(symbol)
    get_data(symbol, start_date, end_date, cookie, crumb)


def main():
    # If we have at least one parameter go ahead and loop overa all the parameters assuming they are symbols
    start_date = get_time_epoch('1970-01-01')
    end_date = get_now_epoch()

    if len(sys.argv) == 1:
        print("\nUsage: get-yahoo-quotes.py SYMBOL [optional yyyy-mm-dd]START_DATE [optional yyyy-mm-dd]END_DATE\n\n")
        return
    
    symbol = sys.argv[1]    
    if len(sys.argv) > 2:
        start_date = get_time_epoch(sys.argv[2])
    
    if len(sys.argv) > 3:
        end_date = get_time_epoch(sys.argv[3])
    
    print("Downloading %s to %s.csv" % (symbol, symbol))
    download_quotes(symbol, start_date, end_date)    


if __name__ == '__main__':
    main()

print("--------------------------------------------------")
