import sys, getopt

# default values
IDstart = 1
Max = 2
Threshold = 3

try:
    opts, args = getopt.getopt(sys.argv[1:],"hs:M:t:", ["startPoint_int=","MAX_SIZE=","Threshold="])
except getopt.GetoptError:
    print ('program -s <startPoint_int> -M <MAX_SIZE> -t <Threshold>')
    sys.exit(2)

print (opts, args)
for opt, arg in opts:
    if opt == '-h':
        print ('program -s <startPoint_int> -M <MAX_SIZE> -t <Threshold>')
        sys.exit()
    elif opt in ("-s", "--startPoint_int"):
        try:
            IDstart = int(arg)
        except ValueError:
            IDstart = 1
            print('invalid startPoint_int')
    elif opt in ("-M", "--MAX_SIZE"):
        try:
            Max = int(arg)
        except ValueError:
            Max = 1
            print('invalid MAX_SIZE')
    elif opt in ("-t", "--Threshold"):
        try:
            Threshold = int(arg)
        except ValueError:
            Threshold = 1
            print('invalid Threshold')

print ('IDstart is ', IDstart)
print ('Max is ', Max)
print ('Threshold is ', Threshold)
