
class Prime:
    def __init__(self, numbers):
        self.numbers = numbers

    def is_prime(self, num):
        if num < 2:
            return False
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                return False
        return True

    def filter_prime_numbers(self):
        return list(filter(lambda x: self.is_prime(x), self.numbers))

n = int(input("n: "))
mylist = []
for i in range(n):
    number = int(input("number: "))
    mylist.append(number)

prime_filter = Prime(mylist)
print(prime_filter.filter_prime_numbers())
