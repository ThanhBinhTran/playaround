import psutil
print ("memory summary", psutil.virtual_memory())
import subprocess

array = []
start = 1
MAX = 3
threshold = 1
for i in range(5): 
    cmd = "python water_info.py -s {0} -M {1} -t {2}".format (start, MAX, threshold)
    print (cmd)
    start = start + MAX
    subprocess.Popen(cmd)
    memory_status = psutil.virtual_memory()
    print ("Memory status", memory_status)
    print ("available: ", memory_status.free)
