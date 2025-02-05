class stringmethods:
    def getstring(self):
        self.string=input("Your string:")
    def printstring(self):
        print("Print with upper case"+self.string.upper())
str=stringmethods()
str.getstring()
str.printstring()