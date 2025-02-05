
import random
a=str(input("What is your name?:"))
b=random.randint(1,20)
c=0
num=1
while num>0:
    d=int(input("Choose the number:"))
    c+=1
    if d==b:
        print("Good job, ",a,"! You guessed my number in ",c," guesses!")
        break
    else:
        print("Wrong choose")
