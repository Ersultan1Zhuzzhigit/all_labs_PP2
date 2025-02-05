import math
class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def show(self):
        return f"Cordinata:{self.x}{self.y}"
    def move(self,x1,y1):
        self.x=x1
        self.y=y1
    def dist(self,point2):
        dx=self.x-point2.x
        dy=self.y-point2.y
        distance=math.sqrt(dx**2+dy**2)
a=float(input("x:"))
b=float(input("y:"))
point1=Point(a,b)
point2=Point(a,b)
point1.show()
k=float(input("x1:"))
p=float(input("y1:"))

point1.move(k,p)
point1.show() 

distance = point1.dist(point2)
print(f"Distance between point1 and point2: {distance}")