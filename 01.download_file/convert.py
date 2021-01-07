from ftfy import fix_encoding
import unicodedata
import urllib 

with open('test.txt') as f:
	read_data = f.read()
print (read_data)
print(read_data.replace('%20', '_') )
#print (read_data.encode("latin1").decode("utf-8", "ignore") )