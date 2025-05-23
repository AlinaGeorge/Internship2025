

def login(username,pssd):
    print("Login:")
    #storing the input username and password
    test_name=input("Enter the username: ")       
    test_pssd=input("Enter the password:")

    #implenting the try/except blocks to handle invalid logins
    try:
        if(username==test_name and pssd==test_pssd):
            print("login successful!")
        else:
            raise ValueError("Invalid username or incorrect password.")  #raising tthe error intentionally
    except ValueError as ve:
        print("Login failed:", ve)
    except Exception as e:
        print("An unexpected error occurred during login:", e)


print("1.Register your email and password:")
#Registering details of the user
username=input("Enter the username: ")
pssd=input("Enter the password:")
print("Your details have been successfully registered")

#calling the login function using stored username and password
login(username,pssd)
