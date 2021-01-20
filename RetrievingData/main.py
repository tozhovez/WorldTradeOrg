#!/usr/bin/env python3

import time
import json
from tornado import httpclient, ioloop
from tornado.web import HTTPError
from itertools import groupby
import operator
import statistics


async def get_data_from_url(url=None):
    response = None
    try:
        response = await httpclient.AsyncHTTPClient().fetch(url)
    except HTTPError as e:
        print("Error: %s" % e)
    html = response.body.decode(errors="ignore")
    return json.loads(html)



def get_transport(data):
    for line in data:
        if "Transport" in line["ProductOrSector"]:
            yield line["Period"], line["Value"]


def get_travel(data):
    for line in data:
        if "Travel" in line["ProductOrSector"]:
            yield line["Year"], line["Value"]


def get_category(data):
    for line in data:
        yield line["ProductOrSector"], line["Value"]


def get_consistent_increase_category(data):
    for line in data:
        if "Telecommunications, computer, and information" in line["ProductOrSector"]:
            yield line["PeriodCode"], line["Year"], line["Period"], line["Value"]


def query_1(data):
    transport = list(get_transport(data))
    transport = sorted(transport, key=operator.itemgetter(0))
    avg_max = None
    for k, g in groupby(transport, key=operator.itemgetter(0)):
        avg = statistics.fmean(d[1] for d in g)
        if avg_max:
            if avg > avg_max[1]:
                avg_max = (k, avg)
        else:
            avg_max = (k, avg)
    print("\nq1\tOn what quarter, on average, is the largest import of Transport services?")
    print(f"\nRESULT: quarter={avg_max[0]}  (on average={avg_max[1]} is the largest import of Transport services)")



def query_2(data):
    travel = list(get_travel(data))
    travel = sorted(travel, key=operator.itemgetter(0))
    year_max = None
    for k, g in groupby(travel, key=operator.itemgetter(0)):
        arr = sum(d[1] for d in g)
        if year_max:
            if arr > year_max[1]:
                year_max = (k, arr)
        else:
            year_max = (k, arr)
    print("\nq2\tOn what year was the largest import of Travel services?")
    print(f"\nRESULT: year={year_max[0]}  (max import of Travel services={year_max[1]})")



def query_3(data):
    category = list(get_category(data))
    category = sorted(category, key=operator.itemgetter(0))
    min_stdev = None
    for k, g in groupby(category, key=operator.itemgetter(0)):
        ssd = statistics.stdev((d[1] for d in g))
        if min_stdev:
            if 0 < ssd < min_stdev[1]:
                min_stdev = (k, ssd)
        else:
            if 0 < ssd:
                min_stdev = (k, ssd)
    print("\nq3\tWhat is the import category with the lowest standard deviation?")
    print(f"\nRESULT: import category={min_stdev[0]}(stdev={min_stdev[1]})")


def query_4(data):
    cons_inc_category = list(get_consistent_increase_category(data))
    cons_inc = sorted(cons_inc_category, key=operator.itemgetter(1, 0))
    consistent_increase = []
    i, c, s  = 1, 0, 0
    while i < len(cons_inc):
        if cons_inc[i-1][3] > cons_inc[i][3]:
            if c >= 3:
                consistent_increase.append(f"From {cons_inc[s][2]} {cons_inc[s][1]} to {cons_inc[i][2]} {cons_inc[i][1]} - consistent increase {c} quarters")
            s = i
            c = 0
        c += 1
        i += 1
    if c >= 3:
        consistent_increase.append(f"From {cons_inc[s][2]} {cons_inc[s][1]} to {cons_inc[i][2]} {cons_inc[i][1]} - consistent increase {c} quarters")
    print("\nq4\tWhen was a consistent increase (of consecutive 3 quarters) in import of ”Telecommunications, computer, and information” services?")
    print("\nRESULT:\n\n%s" % ("\n".join(consistent_increase)))
    

async def main():
    start = time.time()
    data = dict()
    url = "https://api.wto.org/timeseries/v1/data?i=ITS_CS_QM&r=376&p=000&ps=2005-2020&fmt=json&mode=full&lang=1&meta=true&subscription-key=c7eb2391404a459ba0e76d0e4f2631b3"
    try:
        data = await get_data_from_url(url)
    except Exception as e:
        print("Exception: %s" % (e,))

    query_1(data['Dataset'])
    query_2(data['Dataset'])
    query_3(data['Dataset'])
    query_4(data['Dataset'])
    
    print("\n\nDone in %d seconds, fetched %s URL." % (time.time() - start, len(data)))


if __name__ == "__main__":
    io_loop = ioloop.IOLoop.current()
    io_loop.run_sync(main)


