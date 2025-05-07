# opening textfile named MyFile
f=open('MyFile.txt','r')        # r mode to read only

#print(f.read())                 # prints the entire file
'''
count=0
for i in f:
    count+=1                    #counts only the number of lines
print(count)'''

file=f.read()                   # storing the data in file temporarily
text=file.split()               # stores the words of file into an array
print(text)
print("The word frequency is:",len(text))   #the length of array returns the word frequency