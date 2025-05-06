def celsius(F):
    C=(F-32)/(9/5)      #conversion from fahrenheit to celsius
    return C

def fahrenheit(C):
    F=(C*(9/5))+32      #conversion from celsius to fahrenheit
    return F

print("Temperature Convertor")

print("1.Celsius to Fahrenheit")
print("2.Fahrenheit to Celsius")
print("Select the suitable option:[1/2]")      #Selecting the conversion as user's choice

opt=int(input())
#calling the appropriate function according to user's choice
if opt==1:
    C=float(input("Enter temperature in Celsius: "))
    F=fahrenheit(C)     #return equivalent fahrenheit value
    print("The temperature in Fahrenheit: ",F,"*F")
if opt==2:
    F=float(input("Enter temperature in Fahrenheit: "))
    C=celsius(F)        #return equivalent celsius value
    print("The temperature in Celsius: ",C,"*C")