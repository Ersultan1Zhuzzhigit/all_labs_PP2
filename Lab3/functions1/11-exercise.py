def polindrom(a):
        if a==a[::-1]:
            return True
        return False
a=input("a=")
print(polindrom(a))