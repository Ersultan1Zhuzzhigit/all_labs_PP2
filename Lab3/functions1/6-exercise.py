
def return_string(str):
    return ' '.join(str.split() [::-1])
str=input("Your string=")
print (return_string(str))
