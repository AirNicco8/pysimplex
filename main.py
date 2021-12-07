import numpy as np
from typing import List
from simplex import linsolve

print("First Problem", end='\n')
first = True
A = list([[3,2], 
          [9,4], 
          [2,10]])
b = list([66,180,200])
c = list([90,75])

s = linsolve(A,b,c)
s.setobj(1)
s.setVerbose(True)

print("A =", end="")
for i in A:
    if first:
        print("",i)
        first = False
    else:
        print("   ",i)
print()
print("b =", b, "\n")
print("c =", c, "\n")
s.printObj()
s.optimize()
print("\n")
s.printSolutions()

print()
print("////////////////////////////////////////////////////")
print()

print("Second Problem", end='\n')

first = True
A = list([[60,60], 
          [12,6], 
          [10,30]])
b = list([300,36,90])
c = list([0.12,0.15])

s = linsolve(A,b,c)
s.setobj(2)
s.setVerbose(True)

#plot1()

print("A =", end="")
for i in A:
    if first:
        print("",i)
        first = False
    else:
        print("   ",i)
print()
print("b =", b, "\n")
print("c =", c, "\n")
s.printObj()
s.optimize()
print("\n")
s.printSolutions()

print()
print("////////////////////////////////////////////////////")
print()

print("Third Problem", end='\n')

first = True
A = list([[6,-5], 
          [2,2],
          [-5,3]])
b = list([30,10,7])
c = list([7,-5])

s = linsolve(A,b,c)
s.setobj(1)
s.setVerbose(True)

#plot1()

print("A =", end="")
for i in A:
    if first:
        print("",i)
        first = False
    else:
        print("   ",i)
print()
print("b =", b, "\n")
print("c =", c, "\n")
s.printObj()
s.optimize()
print("\n")
s.printSolutions()

print()
print("////////////////////////////////////////////////////")
print()

print("Fourth Problem", end='\n')

first = True
A = list([[5,1], 
          [5,3]])
b = list([5,10])
c = list([4,2])

s = linsolve(A,b,c)
s.setobj(2)
s.setVerbose(True)

#plot1()

print("A =", end="")
for i in A:
    if first:
        print("",i)
        first = False
    else:
        print("   ",i)
print()
print("b =", b, "\n")
print("c =", c, "\n")
s.printObj()
s.optimize()
print("\n")
s.printSolutions()
