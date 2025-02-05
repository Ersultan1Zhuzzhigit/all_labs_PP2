
def spy_game(lists):
    filter=[num for num in lists if num==0 or num==7]
    if len(filter)>=3 and filter[0]==0 and filter[1]==0 and filter[2]==7:
        return True
    else :
        return False

print(spy_game([1,2,4,0,0,7,5]))
print(spy_game([1,0,2,4,0,5,7]))
print(spy_game([1,7,2,0,4,5,0]))
