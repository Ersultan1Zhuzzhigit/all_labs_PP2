
def is_prime(n):
    if n<2:
        return False
    for i in range(2,int(n**0.5)+1):
        if n%i == 0:
            return False
    return True
def filter_prime(numbers):
    num_list=list(map(int,numbers.split()))
    return [num for num in num_list if is_prime(num)]
numbers=input("list numbers=")
print(filter_prime(numbers))
