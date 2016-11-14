import math
import sys
def prim(num):
    for i in range(2,num):
        if((num%i) == 0):
            break
    else:
        return True
    return False

for i in range(10):
    if(prim(i)):
        print("%d is prime",i)
    else:
        print("%d is not prim",i)

def showargs(*arggs,**allwords):
    """
    i have a doc!!
    """
    print arggs
    print allwords
    for arg in arggs:
        print(arg)
    for k in allwords:
        print k +": "+allwords[k]

showargs(2,3,5,7,"abc",j="a",k="b",st="444")
print showargs.__doc__
l = lambda x: x*3
sigmoid = lambda x:1/(1+math.exp(-x))
print(sigmoid(5))
print(sigmoid(-5))

a = [1,2,3,5]
b = a.reverse()
print(a)
print(b)
class Toy:
    name = "Toy"
    kind = "playing thing"
    friends = []
    def setName(selff,name):
        selff.name = name
    def __init__(self,name="hahaha"):
        self.name = name
    def hello(self,toast="hello world"):
        print toast
    def who(self):
        return "Toy"
    __who = who
class Gun(Toy):
    pass
    def who(self):
        return "Gun" + Toy.who(self)

    
toy = Toy("Tank")
tank = Toy("T90")
print type(Toy)
toy.setName("Barby")
print toy.name
print Toy.name
print tank.name
tank.age = 12
print(tank.age)
tank.hello("everybody")
say = Toy.hello
say(toy,"nobody")
print(toy.kind)
toy.kind = "changing thing"
toy.friends.append("toys")
tank.friends.append("tanks")
print(toy.kind)
print(tank.kind)
print(tank.friends)
print(toy.friends)
print(toy.__class__)

print(toy.who())

gun = Gun()
print(gun.who())
print(gun._Toy__who())
print(isinstance(gun,Toy))
print(issubclass(Toy,Gun))

for c in "hello world":
    print c

if __name__ == "__main__":
    print(sys.path)
    print(sys.argv)
    print(sys.ps1)