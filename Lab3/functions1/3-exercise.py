
def solve(numheads,numlegs):
    R=numheads-1
    C=1
    while(R*4+C*2!=numlegs):
        C+=1
        R-=1
    return f"Rabbits{R}\n"  f" Chicken{C}"
h=int(input("head="))
l=int(input("leg="))
print(solve(h,l))
