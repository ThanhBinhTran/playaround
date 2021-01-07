
# Parallelizing using Pool.apply()
import csv
from multiprocessing import Pool
import multiprocessing as mp
import os
import pandas as pd
from io import BytesIO
import pycurl
from bs4 import BeautifulSoup

try:
    # python 3
    from urllib.parse import urlencode
except ImportError:
    # python 2
    from urllib import urlencode
	
threshold = 100
def generate_ID(IDbegin):
    partIDs = range (IDbegin, IDbegin + threshold, 1)
    fullIDs =[]
    for item in partIDs:
        fullIDs.append( "01001{0:03d}".format(item))
    return pd.Series(fullIDs)
	
inputrange = range(1,4*threshold, threshold)
#for inpt in inputrange:
#    print (inpt)

link = 'http://diemthi.hcm.edu.vn/Home/Show'
def get_data(sbd):
    buffer = BytesIO()
    print(sbd)
    c = pycurl.Curl()
    c.setopt(c.URL, link)
    c.setopt(c.WRITEDATA, buffer)

    post_data = {'sobaodanh': sbd}
    # Form data must be provided already urlencoded.
    postfields = urlencode(post_data)
    # Sets request method to POST,
    # Content-Type header to application/x-www-form-urlencoded
    # and data to send in request body.
    c.setopt(c.POSTFIELDS, postfields)

    c.perform()
    c.close()
    #print(buffer.getvalue().decode())
    return buffer.getvalue()

def parse_line(body):
    webdata = BeautifulSoup(body, "lxml")
    linestr =[]
    #print(webdata)
    if webdata != -1:
        rows = webdata.find_all('tr')
        if len(rows) == 2:
            Info = rows[1].find_all('td')
            for info in Info:
               linestr.append(info.text.strip())
    #print (linestr)
    return linestr

def get_score_parallel(IDstart):
    IDs = generate_ID(IDstart)
    filename = "result{0:06d}.csv".format(IDstart)
    f = open(filename, 'w', newline='', encoding="utf-8")
    #print (filename)
    writer = csv.writer(f, delimiter=",")
    writer.writerow(['Name','date of birth','results'])
    for sbd in IDs:
        body = get_data(sbd)
        linedata = parse_line(body)
        writer.writerow(linedata)
    f.close()

print ("START", os.getpid())

if __name__ == '__main__':
    with Pool(mp.cpu_count()) as p:
        p.map(get_score_parallel, inputrange)
print ("DONE")