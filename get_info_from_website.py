#Run with Python 3

import pandas as pd
import numpy as np
import urllib.request
import shutil
import re
import os
import pathlib
import argparse
import pdb
import threading
from bs4 import BeautifulSoup

def site_open(site):
    '''Makes connection and opens up target website. Returns a website object.'''
    try:
        #sets up request object
        req = urllib.request.Request(site)

        #adds User-Agent info to request object
        req.add_header("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) \
         AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5")

        #opens up site
        website = urllib.request.urlopen(req)

        return website
    except urllib.request.URLError:
#            print('Could not connect to '+ site + '!')
           pass
    
def soup_site(site):
    '''opens site and turns it into a format to easily parse the DOM. Returns a Soup Object'''
    try:
        website = site_open(site)
#         return BeautifulSoup(website, "html5lib")
        return BeautifulSoup(website, "lxml")
    except Exception as e:
        print(e)
        return -1


def generate_ID():
    partIDs = range (1, 20, 1)
    fullIDs =[]
    for item in partIDs:
        fullIDs.append( "2209337{0:04d}".format(item))
        
    return pd.Series(fullIDs)

IDs = generate_ID()

IDs
links = "http://capnuoctrungan.vn/Main/Home/TraCuuTienNuoc?danhbo=" + IDs;

links


def get_info_from_link(link):
    soup = soup_site(link)
    data =[]
    # check if content is present, if yes then parse and get info
    if soup != -1:
        information = soup.findAll("div", {"class" : "info_label"})
        for info in information:
            field = info.label  		# get all contents of <table> tag
            data_temp = info.b			# get all contents of <b> tag
            data_temp = data_temp.string  # get payload of contents
            print (field.string, data_temp)
            data.append(data_temp)
        print( data)
    else:
        print ("Not found {0}". format(link))
    return data
	

# write to csv file
import csv
f = open("water.csv", 'w', newline='', encoding="utf-8")
writer = csv.writer(f, delimiter=",")
writer.writerow(["Số Danh Bộ", "Tên Khách Hàng", "Số điện thoại", "Địa Chỉ", "Tình trạng đồng hồ"])
for link in links:
    print (link)
    writer.writerow(get_info_from_link(link))

f.close()