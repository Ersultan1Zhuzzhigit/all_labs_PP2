class Shape:
    def area(self):
        return 0
class Ractangle():
    def __init__(self,l,w):
        self.l=l
        self.w=w
    def area(self):
        return self.l*self.w
l=float(input("length="))
w=float(input("width="))
area=Ractangle(l,w)
print(area.area())
