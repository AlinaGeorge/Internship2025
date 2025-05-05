def addition(a,b):
    return a + b

def subtraction(a,b):
    return a - b

def multiplication(a,b):
    return a * b

def division(a,b):
    if b == 0:
        return "Error! Division by zero."
    return a / b

def calculator(a, b, op):
    if op == '+':
        return addition(a, b)
    elif op == '-':
        return subtraction(a, b)
    elif op == '*':
        return multiplication(a, b)
    elif op == '/':
        return division(a, b)
    else:
        return "Invalid operator!"
    
a=float(input("Enter first number: "))
op=input("Enter operator (+, -, *, /): ")
b=float(input("Enter second number: "))
print("The result of operation ",a,op,b,"=",calculator(a, b, op))