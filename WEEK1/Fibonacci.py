
def fibonacci(n):
    fib=[]
    '''fib[0]=0
    fib[1]=1'''
    fib.append(0)
    fib.append(1)
    for i in range(2,n):
        term=fib[i-1]+fib[i-2]
        fib.append(term)
    
    print("The fibonacci series of ",n,"terms:")
    print(fib)


n=int(input("Enter the number of terms:"))
fibonacci(n)
