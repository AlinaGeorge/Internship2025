f=open('NewFile','w+')      # Open file for reading and writing

data=input("Enter the data to store in the file:")  #storing data as user input
f.write(data)               #writing the stored data into the created file

f.seek(0)                   #moving the cursor back to begin to print
print("The file contains:",f.read())

f.close()