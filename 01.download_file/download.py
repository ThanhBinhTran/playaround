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
		
def get_web_data_from_link(link):
    return soup_site(link)





# this function will list all links as posible of a website
link = 'http://hdgsnn.gov.vn/files/'

print ("Geting infomation from: " + link)

all_links = []
all_links.append(link)
for cur_link in all_links:
    # check if current link is a file. 
    if cur_link[-1] == '/':   # process if current link is folder, skip if it's a file
        soup = get_web_data_from_link(cur_link);
        if soup != -1:  # handle if data is responded
            hyperlink_tags = soup.find_all('a')
            for hyperlinks in hyperlink_tags:
                hyperlink = hyperlinks.get('href')
                if hyperlink.find('http') != -1:  # full link
                    downlink = hyperlink
                    print ("full link: " + downlink)
                elif hyperlink.find('../') != -1:  # parents
                    
                    downlink = cur_link.rsplit('/', 2)[0]
                    downlink = downlink + '/'
                    print ("parents: " + downlink)
                else:
                    downlink = cur_link + hyperlink
                    print ("downlink: " + downlink)
                
                #if hyperlink.find('/') != -1:     # if hyperlink contains /  then check duplicate in path
                #    path = hyperlink.rsplit('/', 1)[0]            # get the first part from last /
                #    if cur_link.find(path) != -1:      # found overlap between links and hyperlink
                #                                    # then remove overlap
                #        downlink = downlink.replace(path, '',1)
                #        print ("downlink overlap: " + downlink)
                if downlink not in all_links: # not exist in list, then add into it
                    all_links.append(downlink)
                    print("Added: " + downlink)
import urllib.request
import os
download_path = 'download\\'
# mode 
mode = 0o666
# check if download folder is exist
isdir = os.path.isdir(download_path)
if  not isdir:  # if not create new one
    os.mkdir(download_path, mode) 

#for item in all_info:
#    print('Downloading: ' + item[0])
#    urllib.request.urlretrieve(item[0], "download\\" +item[1])

for line_link in all_links:
    if line_link[-1] != '/':   # just download files, skip folder
        temp_name = line_link.replace('//','/')
        temp_name = temp_name.replace('http:/hdgsnn.gov.vn/files/','')
        temp_name = temp_name.replace('/','_')
        #print('Downloading: ' + line_link + " save name: " + temp_name)
        urllib.request.urlretrieve(line_link, download_path + temp_name)
    else:
        print ("skip: " + line_link)