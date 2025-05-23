
class Bank:
    def __init__(self,name,ac,pin):
        self.name=name
        self.ac=ac
        self.pin=pin
        self.bal=0
    
    def validate(self,ac,pin):
        if self.ac==ac and self.pin==pin:
            return True
        else:
            return False
    
    def deposit(self,amt):
        self.bal+=amt
        print("Amount deposited successfully!")
        print("Your current balance:",self.bal)

    def withdraw(self,amt):
        if self.bal>=amt:
            self.bal-=amt
            print("Amount withdrawn successfully!")
            print("Your current balance:",self.bal)
        else:
            print("Insufficient Balance!")
            print("Your available balance:",self.bal)

    def balance(self):
        print("Your available balance:",self.bal)


Users={}
while True:
    stat=int(input("1.New User or 2.Existing User:"))
    if stat==1:
        print("SET YOUR DETAILS:")
        name=input("Name:")
        ac=input("Account Number:")
        pin=input("Set your pin:")

        Users[ac]=Bank(name,ac,pin)
        print("Account created Successfully")
    elif stat==2:
        print("1.Deposit\n2.Withdraw\n3.Check Balance")
        ch=int(input("Select your service:[1/2/3]:"))

        test_ac=input("Enter your Account Number:")
        test_pin=input("Enter your pin:")
        user=Users.get(test_ac)
        if user and user.validate(test_ac,test_pin):
            if ch==1:
                amt=float(input("Enter the amount:"))
                user.deposit(amt)
            elif ch==2:
                amt=float(input("Enter the amount:"))
                user.withdraw(amt)
            elif ch==3:
                user.balance()
            else:
                print("Inavalid service selected!")
        else:
            print("Incorrect Credentials!")
    
    else:
        print("Invalid choice")
    ch=input("Do you want to continue[y/n]:")
    if ch=='n':
        break

    
