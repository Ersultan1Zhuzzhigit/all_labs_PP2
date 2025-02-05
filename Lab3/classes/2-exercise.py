
class Shape:
    def area(self):
        return 0
class Square(Shape):
    def __init__(self,length):
        self.length=length
    def area(self):
        return self.length ** 2
n=float(input("n="))
myshape=Shape()
mysquare=Square(n)
print("Square Area: ",mysquare.area())
print("Other: ",myshape.area())
