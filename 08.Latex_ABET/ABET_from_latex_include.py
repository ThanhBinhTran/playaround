# copy then paste to this file
working_dir = r"C:\Users\Binh Tran\OneDrive - hcmut.edu.vn\01.TechingHCMUT\01.ComputerArchitecture\02_Exams_Quiz\\"
tex_file = working_dir + "_Final.tex"
answerChar = ['A', 'B','C','D','']  # leave the last items null value which represents "not found"
questioncount = -1    # not count yet
question_abet = []    
answers = []
ansfound = False
chapter_files = []
f = open(tex_file, encoding='utf-8')
data = f.readlines()
for line in data:
    lineStr = line.strip()
    if lineStr[0:1].find('%') != -1: # skip comment line
        continue
    elif lineStr[0:6].find('\\input') != -1:  # detected new question
        #print (lineStr)
        temp_file = lineStr.split("}")
        temp_file = temp_file[0].split("{")
        print (temp_file[1])
        chapter_files.append(temp_file[1].strip())

#print (data)
for chapter_tex in chapter_files:
    f = open(working_dir + chapter_tex, encoding='utf-8')
    data = f.readlines()
    for line in data:
        #print(line)
        lineStr = line.strip()
        if lineStr[0:1].find('%') != -1: # skip comment line
            continue
        elif lineStr[0:9].find('\\question') != -1:  # detected new question
            questioncount = questioncount  + 1
            #print ("Q{0}: {1}".format(questioncount+1,lineStr))
            answers.append(-1)  # initial answer
            question_abet.append('')  
            ansfound = False
            
            if lineStr.find('(') != -1 and lineStr.find(')') != -1:
                temp = lineStr.split('(')
                temp = temp[1].split(')')
                question_abet[questioncount] =temp[0]
            
        elif lineStr[0:7].find('\\choice') != -1 or lineStr[0:7].find('\\fourch') != -1 or lineStr[0:6].find('\\onech') != -1:                   
            #print ("answers landmark: " + lineStr)
            ansfound = True
            ans = -1                   # Not found yet
        elif ansfound:
            ans = ans + 1
            #print ("[{0}]: {1}".format(str(ans),lineStr) )
            
            if lineStr.find("\\answ") != -1:
                #print ("A:" + str(ans) + "___" + lineStr )
                answers[questioncount] = ans
                ansfound = False

print (question_abet)
print (answers)

# write to file
f = open("ABET.txt", "w")
f.write("SUMMARY\n")
print ("SUMMARY")
for i in range (0,4):
    print ("There are {0} answers {1}".format(answers.count(i), answerChar[i]))
    f.write("There are {0} answers {1}\n".format(answers.count(i), answerChar[i]))
    
print ("ABET")
f.write("ABET\n")
for i in range(len(question_abet)):
    print ("Question: {0:02d}, ABET: {1}, Answer: {2}.".format(i+1,question_abet[i], answerChar[answers[i]]))
    f.write("Question: {0:02d}, ABET: {1}, Answer: {2}.\n".format(i+1,question_abet[i], answerChar[answers[i]]))
f.close()