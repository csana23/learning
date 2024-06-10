def factorial(n):
    result = 1
    for i in range(1,n+1):
        result = result * i

    print(result)

def fibonacci(n):
    array = [0, 1]

    for i in range(1, n-1):
        array.append(array[i] + array[i-1])

    print(array)

fibonacci(5)