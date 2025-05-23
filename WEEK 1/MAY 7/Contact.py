f=open('Contacts.txt','a+')
contact={}      #initializing dictionary

#user inputting contacts into dictionary
name=input("Enter the name: ")
phone=input("Enter the phone number: ")

contact[name]=phone        #appends to the dictionary
print("Successfully saved contact!")
 
# Format: Name:Phone
f.write(f"{name}:{phone}\n")  # Append to the file

print("Saved Contacts:")        #displaying the saved contacts
f.seek(0)                       #moving the cursor back to begin to print
for contact in f:
    print(contact)

f.close()