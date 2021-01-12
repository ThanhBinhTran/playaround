# path for window
from pathlib import Path

# import input/output handling
import io



patternStr = "$t3, $zero, loop" 

searchdir = Path(r"C:\Users\Binh Tran\OneDrive - hcmut.edu.vn\01.TechingHCMUT\01.ComputerArchitecture")
tex_file_lists = [str(pp) for pp in searchdir.glob("**/*.tex")]
results = []
for texfile in tex_file_lists:
    f = open(texfile, encoding='utf-8')
    data = f.readlines()
    for line in data:
        if line.find(patternStr) != -1:
            print ("FOUND ", texfile, )
            results.append(texfile)
            break
            
# log the result
with io.open("result_file.txt", 'w', encoding='utf8') as f:
    for filename in results:
            f.write(filename + "\n")
f.close()
