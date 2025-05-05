def Guess(a,b):
    M=int((a+b)/2)
    print("Is your number >",M,":[y/n])")
    guess=input()
    if guess=='y':
        Guess(M,b)
        
    else:
        print("Is your number < ",M,":[y/n])")
        guess=input()
        if guess=='y':
            Guess(a,M)
        else:
            print("Your guess is ",M,"?" )
            return M
            
    

print("Guess the number game!")
print("Firstly, you need to guess a number")
print("Now,Enter a range of numbers containing it:")
a=float(input("Enter the lower limit:"))
b=float(input("Enter the upper limit:"))

Guess(a,b)

