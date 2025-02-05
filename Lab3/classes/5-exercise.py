
class Bank():
    def __init__(self, account, money):
        self.money = money
        self.account = account

    def balance(self):
        return self.money
    
    def owner(self):
        return self.account
    
    def deposit(self, money):
        self.money+=money

        return f"You are deposit {money} money"
    
    def withdraw(self, money):
        if self.money - money < 0:
            return "insufficient funds"
        else:
            self.money-=money

            return f"you're balance: {self.money},  and you take {money}"
        
        
bank = Bank("Bekzat", 1000)

print(bank.balance())

print(bank.owner())

print(bank.deposit(1000))

print(bank.withdraw(3000))

print(bank.withdraw(2000))
