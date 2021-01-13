# path for window
from pathlib import Path

# import input/output handling
import io

searchdir = Path(r"C:\Users\Binh Tran\OneDrive - hcmut.edu.vn\01.TechingHCMUT")
tex_file_lists = [str(pp) for pp in searchdir.glob("**/*ABET*")]

for texfile in tex_file_lists:
    print (texfile)
            
# log the result
with io.open("result_file.txt", 'w', encoding='utf8') as f:
    for filename in tex_file_lists:
            f.write(filename + "\n")
f.close()
