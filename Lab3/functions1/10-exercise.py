
def unique(list):
    unique_list=[]
    for i in list:
        if i not in unique_list:
            unique_list.append(i)
    return unique_list
list=[1,2,3,4,5,6,5,3,6]
print(unique(list))
