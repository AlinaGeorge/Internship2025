def Palindrome(word):
    term=word.lower()
    print("Word: ",term)
    rev=term[::-1]
    print("Reverse: ",rev)
    if term==rev:
        return True
    else:
        return False
    
word=input("Enter the word: ")

if Palindrome(word):
    print("The word is a Palindrome!")
else:
    print("The word is not a Palindrome!")



    