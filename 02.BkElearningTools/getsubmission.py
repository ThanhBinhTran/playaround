# import input/output handling
import io

# import os for handling OS operation
import os

# importing pandas as pd 
import pandas as pd 
  
# importing re for regular expressions 
import re 

# path for window
from pathlib import Path

# execute process for OS
import subprocess

# date time
import datetime

#submission = "W2"
#submission = "W3"
#submission = "W4"
#submission = "W5"
submission = "W8"
#submission = "Assignment"
win_path = r"C:\Users\Binh Tran\Downloads\KTMT" + submission

submit_dir = Path(win_path)


rar_list = [str(pp) for pp in submit_dir.glob("**/*.rar")]
zip_list = [str(pp) for pp in submit_dir.glob("**/*.zip")]
archived_paths = rar_list + zip_list


archived_dirs = []

for path in archived_paths:
    archived_dirs.append(os.path.dirname(path))
    
for path in archived_paths:
    print (path)

# extract all archived files
cmd_app = "C:\Program Files\WinRAR\WinRAR.exe"
cmd_options = " x "
quote  = '\"'
space = ' ' 
cmds = []

for i in range(len(archived_paths)):
    cmds.append ( quote  + cmd_app + quote  + 
                 cmd_options +
                 quote  + archived_paths[i] +quote  + space + 
                 quote+archived_dirs[i] +quote
                ) 
#for cmd in cmds:
#    print(cmd)

# extract archived files
for cmd in cmds:
    subprocess.call(cmd, shell=True)
print("DONE " + str(datetime.datetime.now()))

# get all submited folders
import glob
submit_paths = [str(pp) for pp in glob.glob(win_path + "\**")]

for path in submit_paths:
    print (path)
print("DONE " + str(datetime.datetime.now()))

# remove "_xxxx_assignsubmission_file_" in submission folder by REN cmd in window
src_paths = []
dst_paths = []
for path in submit_paths:
    src_paths.append(path)
    if path.find('_') != -1:
        temp = path.split('_', 1)
        dst_paths.append(temp[0])
    else:
        dst_paths.append(path)

for path in dst_paths:
    print (path)

# rename execution
for i in range(len(src_paths)):
    os.rename(src_paths[i],dst_paths[i])
print("DONE " + str(datetime.datetime.now()))

# write csv file for studentID and student name
# write to csv file
studentID = []
studentName = []
#get student ID and student NAME
for path in dst_paths:
    temp = path.rsplit('\\',1)
    temp = temp[1]
    studentID.append(temp.split('-',1)[0])
    studentName.append(temp.split('-',1)[1])
    
for i in range(len(studentID)):
    print (studentID[i], studentName[i])
    
import csv
f = open(submission + "_submision.csv", 'w', newline='', encoding="utf-8")
writer = csv.writer(f, delimiter=",")
writer.writerow(["StudentID", "StudentName"])
for i in range(len(studentID)):
    writer.writerow([studentID[i], studentName[i]])
f.close()
print("DONE " + str(datetime.datetime.now()))

# get all files, dirs
asm_lists = [str(pp) for pp in submit_dir.glob("**/*.asm")]
all_paths = [str(pp) for pp in submit_dir.glob("**/*")]

#log all paths
with io.open(submission + "_all_paths.txt",'w',encoding='utf8') as f:
    for i in range(len(all_paths)):
            f.write(all_paths[i] + "\n")
f.close()

# log all files
with io.open(submission + "_all_files.txt",'w',encoding='utf8') as f:
    for i in range(len(all_paths)):
        if os.path.isfile(all_paths[i]):
            f.write(all_paths[i] + "\n")
f.close()

# log all dirs
with io.open(submission + "_all_dirs.txt",'w',encoding='utf8') as f:
    for i in range(len(all_paths)):
        if os.path.isdir(all_paths[i]):
            f.write(all_paths[i] + "\n")
f.close()

#log all asm files
with io.open(submission + "_all_asm_files.txt",'w',encoding='utf8') as f:
    for item in asm_lists:
            f.write(item + "\n")
f.close()
print("DONE " + str(datetime.datetime.now()))

# Creating the Series 
sr = pd.Series(all_paths) 
  
# the letter 'i' follwed by any small alphabet. 
result = sr.str.contains(pat = '.asm|.ASM|.Asm|.RAR|.rar|.Rar|.zip|.ZIP|.Zip|.pdf|.PDF', regex = True) 
 
with io.open(submission + "_no_extension.txt",'w',encoding='utf8') as f:
    for i in range(len(all_paths)):
        if result[i] == False and os.path.isfile(all_paths[i]):
            f.write(all_paths[i] + "\n")
f.close()
print("DONE")

