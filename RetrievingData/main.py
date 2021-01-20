#!/usr/bin/env python3

import time
from datetime import timedelta
import json
#from html.parser import HTMLParser
import urllib
import  urllib.error #, urllib.request, urllib.parse, urllib.error,

from tornado import gen, httpclient, ioloop, queues
from tornado.web import HTTPError
from itertools import groupby
import operator
import statistics
#https://api.wto.org/timeseries/v1/data?i=ITS_CS_QM&r=376&p=000&ps=2005-2020&max=1000000&fmt=csv&mode=full&head=H&lang=1&meta=true&subscription-key=c7eb2391404a459ba0e76d0e4f2631b3"
concurrency = 10


async def get_data_from_url(url=None):
    """Download the page at `url`.
    Returned data.
    """
    response = None
    try:
        response = await httpclient.AsyncHTTPClient().fetch(url)
    except HTTPError as e:
        print("Error: %s" % e)
    #print(response)
    #print("fetched %s" % url)
    html = response.body.decode(errors="ignore")
    #print(html)
    return json.loads(html)

def get_transport(data):
    for line in data:
        if "Transport" in line["ProductOrSector"]:
            yield (line["Period"],line["Value"])
            #list(map(print, line.items()))
            #print(f"""line["ProductOrSector"]={line["ProductOrSector"]}""")
            #print(line["Period"],line["Year"],line["Value"])

def get_travel(data):
    for line in data:
        if "Travel" in line["ProductOrSector"]:
            #print(f"""line["ProductOrSector"]={line["ProductOrSector"]}""")
            #print(line["Year"],line["Value"])
            yield (line["Year"],line["Value"])

def get_category(data):
    for line in data:
        # line["Year"], line["PeriodCode"],
        yield (line["ProductOrSector"], line["Value"])

def get_consistent_increase_category(data):
    for line in data:
        list(map(print, line.items()))
        print(f"""line["ProductOrSector"]={line["ProductOrSector"]}""")
        if "Telecommunications, computer, and information" in line["ProductOrSector"]:
            yield (line["Year"], line["PeriodCode"], line["Value"])


def query_1(data):
    transport = list(get_transport(data))
    transport = sorted(transport, key=operator.itemgetter(0))
    print(*transport)
    #transport = sorted(transport, key=lambda x: (x[0],x[1]))
    avg_max = tuple()
    for k, g in groupby(transport, key=lambda x: (x[0])):
        avg = statistics.fmean(d[1] for d in g)
        #print(arr, [sum(arr), len(arr)])
        #avg = sum(arr)/len(arr)
        if avg_max:
          if avg > avg_max[1]:
            avg_max = (k, avg)
        else:
            avg_max = (k, avg)
        #print(avg_max)
    print("On what quarter, on average, is the largest import of Transport services?")
    print(f"RESULT: quarter={avg_max[0]}  (on average={avg_max[1]} is the largest import of Transport services)")

def query_2(data):
    #travel = list(get_travel(data))
    #travel = sorted(travel, key=lambda x: (x[0]))
    travel = list(get_travel(data))
    travel = sorted(travel, key=operator.itemgetter(0))
    print(*travel)
    year_max = tuple()
    for k, g in groupby(travel, key=operator.itemgetter(0)):

        arr = sum(d[1] for d in g)
        if year_max:
            if arr > year_max[1]:
                year_max = (k, arr)
        else:
            year_max = (k, arr)
    print("On what year was the largest import of Travel services?")
    print(f"RESULT: year={year_max[0]}  (max import of Travel services={year_max[1]})")

def query_3(data):
    #category = list(get_category(data))
    #category = sorted(category, key=lambda x: (x[0]))
    category = list(get_category(data))
    category = sorted(category, key=operator.itemgetter(0))
    #print(*category)
    min_stdev = tuple()
    for k, g in groupby(category, key=operator.itemgetter(0)):
        #dg = list(g)
        #print(k)
        #list(map(print, dg))
        ssd = statistics.stdev((d[1] for d in g))

        #print(dg)
        #ssd0 = stddev(tuple(d[1] for d in dg), ddof=0)
        #ssd1 = stddev(arr, ddof=1)
        #print(ssd0,ssd1)
        if min_stdev:
            if 0 < ssd < min_stdev[1]:
                min_stdev = (k, ssd)
        else:
            if 0 < ssd:
                min_stdev = (k, ssd)
    print("What is the import category with the lowest standard deviation?")
    print(f"RESULT: import category={min_stdev[0]}(stdev={min_stdev[1]})")
    #
    #     if ssd_min:
    #       if ssd <  ssd_min[1]:
    #         ssd_min = (k, ssd)
    #     else:
    #         ssd_min = (k, ssd)
    #     #print(avg_max)
    # return f"quarter={avg_max[0]}(average={avg_max[1]})"

def query_4(data):
    cons_inc_category = list(get_consistent_increase_category(data))
    cons_inc_category = sorted(cons_inc_category, key=operator.itemgetter(0))
    print(*cons_inc_category)
    
    consistent_increase = [0,0]
    print("When was a consistent increase (of consecutive 3 quarters) in import of ”Telecommunications, computer, and information” services?")
    print(f"RESULT: consecutive 3 quarter {consistent_increase[0]}, consistent increase={consistent_increase[1]} of consecutive 3 quarter sin in import of ”Telecommunications, computer, and information” services")

async def main():
    start = time.time()
    data = dict()
    url = "https://api.wto.org/timeseries/v1/data?i=ITS_CS_QM&r=376&p=000&ps=2005-2020&fmt=json&mode=full&lang=1&meta=true&subscription-key=c7eb2391404a459ba0e76d0e4f2631b3"
    url_2 = "https://api.wto.org/timeseries/v1/data?i=ITS_CS_QM&r=376&p=000&ps=2005-2020&subscription-key=c7eb2391404a459ba0e76d0e4f2631b3"
    try:
        data = await get_data_from_url(url_2)
    except Exception as e:
        print("Exception: %s" % (e,))

    
    query_1(data['Dataset'])
    query_2(data['Dataset'])
    query_3(data['Dataset'])
    query_4(data['Dataset'])
    
    print("Done in %d seconds, fetched %s URL." % (time.time() - start, len(data)))



if __name__ == "__main__":
    io_loop = ioloop.IOLoop.current()
    io_loop.run_sync(main)


