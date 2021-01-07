
# Parallelizing using Pool.apply()
import csv
from multiprocessing import Pool, Process, Pipe, Queue
import multiprocessing as mp
import time
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

IDstart = 700
IDend = 0
Threshold = 10

# get all range
inputrange = range(IDstart, IDstart + 100, Threshold)

#inputrange = range(IDstart, 4*Threshold, Threshold)

Baselink = 'http://capnuoctrungan.vn/Main/Home/TraCuuTienNuoc?danhbo='

def generate_allIDs(IDstart, IDend):
    partIDs = range (IDstart, IDend, 1)
    fullIDs =[]
    for item in partIDs:
        fullIDs.append( "2209337{0:04d}".format(item))
    return fullIDs
    
def generate_IDs(IDbegin):
    partIDs = range (IDbegin, IDbegin + Threshold, 1)
    fullIDs =[]
    for item in partIDs:
        fullIDs.append( "2209337{0:04d}".format(item))
    return fullIDs

#for i in inputrange:
#    print ("range", i)
#    IDs = generate_IDs(i)
#    print (IDs)

def format_data(buffer):
    return BeautifulSoup(buffer, "lxml")

def get_water_use(data):
    water_records = []
    total = 0
    month_use = 0
    water_meter = 0
    # check if content is present, if yes then parse and get info
    if data != -1:
        information = data.findAll("table", {"class" : "table_tiennuoc"})
        for info in information:
            data_rows = info.findAll('tr')
            for data_row in data_rows:
                #print ("row-------------------------------------------------")
                data_items = data_row.findAll('td')
                if len(data_items)  > 7:
                    
                    water_row = []
                    try:
                        total_int = int(data_items[7].text.replace(',',''))
                        water_use_int = int(data_items[3].text)
                        water_row.append(data_items[0].text.strip()) # date
                        water_row.append(water_use_int) # water use
                        water_row.append(total_int) # subtotal
                        
                        month_use = month_use + 1
                        total = total + total_int
                        water_meter = water_meter + water_use_int 
                        water_records.append(water_row)
                        
                    except ValueError:
                        print('invalid integer')
                    
                #for data_item in data_items:
                #    water_row.append(data_item.text.strip())
                #print (water_row)
                #if len(water_row) != 0:
                #    water_records.append(water_row)
    else:
        print ("Null data")
    return [water_records, total, month_use, water_meter]

def get_personal_info(data):
    personal_info = []
    
    # check if content is present, if yes then parse and get info
    if data != -1:
        information = data.findAll("div", {"class" : "info_label"})
        for info in information:
            data_temp = info.b       # get all contents of <b> tag
            data_temp = data_temp.string.strip()  # get payload of contents
            personal_info.append(data_temp)
        #print( data)
    else:
        print ("Null data")
    return personal_info

def store_data(body, waterID):
    data = format_data(body)
    personal_info = get_personal_info(data)
    #print (personal_info)
    total= 0
    month_use = 0
    water_meter = 0
    if len(personal_info) != 0:
        [water_use, total, month_use, water_meter] = get_water_use(data)
        #print (water_use)
        
        # log file
        f = open(waterID + ".csv", 'w', newline='', encoding="utf-8")
        writer = csv.writer(f, delimiter=",")

        writer.writerow(['ID', 'Name', 'phone number', 'address', 'water meter status'])
        writer.writerow(personal_info)
        
        writer.writerow(['Total', '#water meter','#month use', '#water meter mean','Total mean',])
        writer.writerow([total, water_meter, month_use, int(water_meter/month_use), int(total/month_use)])

        
        writer.writerow(['Kỳ', 'Tieu thu', 'Tong tien'])
        for water_use_item in water_use:
            writer.writerow(water_use_item)
        f.close()
    return [personal_info, total, month_use, water_meter]

def get_data(waterID):
    buffer = BytesIO()
    #print(waterID)
    link = Baselink + waterID
    
    c = pycurl.Curl()
    c.setopt(c.URL, link)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    
    return buffer.getvalue().decode()
    
def get_data_parallel(IDrange_start):
    info = []
    IDs = generate_IDs(IDrange_start)
    for waterid in IDs:
        body = get_data(waterid)
        info.append(store_data(body, waterid))
    return info
    
def pipe_child_task(child_conn, waterID): # get data from website
    body = get_data(waterID)
    child_conn.send(body)
    child_conn.close()

def pipe_parent_task(parent_conn,waterID):         # parse info from responded  data
    store_data(parent_conn.recv(), waterID)




if __name__ == '__main__':
    print ("Parents[{0:05d}]->START".format(os.getpid()))
else:
    print ("+--child[{0:05d}]-->START".format(os.getpid()))

# pipeline
#if __name__ == '__main__':
#    IDs = generate_allIDs(IDend, IDstart)
#    for waterid in IDs:
#        parent_conn, child_conn = Pipe()
#        p = Process(target=pipe_child_task, args=(child_conn, waterid))
#
#        p.start()
#        pipe_parent_task(parent_conn, waterid)
#        p.join()

# parallelism by executing in multiple processors 
if __name__ == '__main__':
    with Pool(mp.cpu_count()) as p:
        results = p.map(get_data_parallel, inputrange )
        
        #log file
        fname = "summary{0:05d}_{1:05d}.csv".format(inputrange[0],inputrange[-1] + Threshold -1)
        f = open(fname, 'w', newline='', encoding="utf-8")
        writer = csv.writer(f, delimiter=",")
        writer.writerow(['ID', 'Name', 'phone number', 'address', 'total', 'month_use', 'water_meter'])
        for bunch_results in results:
            for result in bunch_results:
                temp_info = result
                writer.writerow([temp_info[0],temp_info[1],temp_info[2],temp_info[3],result[1], result[2], result[2]])
        f.close()

if __name__ == '__main__':
    print ("Parents[{0:05d}]-.DONE".format(os.getpid()))
else:
    print ("+--child[{0:05d}]--.DONE".format(os.getpid()))