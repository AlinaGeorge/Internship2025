def Palindrome(word):
    term=word.lower()       #converting string to lower case inorder to compare words irrespective of type
    print("Word: ",term)
    rev=term[::-1]          #reversing the word
    print("Reverse: ",rev)
    #comparing word and its reverse
    if term==rev:
        return True
    else:
        return False
    
word=input("Enter the word: ")

if Palindrome(word):
    print("The word is a Palindrome!")
else:
    print("The word is not a Palindrome!")



    