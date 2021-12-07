import numpy as np
from typing import List
from enum import Enum


from colorama import init
from termcolor import colored
 
init()

MAX_ITER = 100

class MINMAX(Enum):
    Maximize = 1
    Minimize = 2

class linsolve:

    def __init__(self, A: List[List[float]], b: List[float], c: List[float]):
        """
        A: mxn matrix of inequality constraint coefficients.
        b: nx1 vector for constraints.
        c: nx1 vector, cost associated to each variable.
        obj: objective, 1 for maximize, 2 for minimize

        if maximize is set the method expects the problem in standard form -> Ax <= b, x >= 0
        if minimize is set the method expects the problem in standard form -> Ax >= b, x >= 0

        default objective is maximize
        """
        self.A = np.array(A, dtype=np.float64)
        self.b = np.array(b, dtype=np.float64)
        self.c = np.array(c, dtype=np.float64)
        self.obj = 1

        # state boolean variables
        self.optimal = False
        self.feasible = True
        self.bounded = False
        self.transform = False
        self.v = False

        # solution variables
        self.x = [float(0)] * len(c)
        self.optimalValue = None

    def setA(self, A):
        self.A = A
        
    def setb(self, b):
        self.b = b
        
    def setc(self, c):
        self.c = c

    # default is minimize
    def setobj(self, m):
        if m == MINMAX.Minimize.value or m == MINMAX.Maximize.value:
            self.obj = m
        else:
            print("Invalid objective.")
        self.transform = False

    def printObj(self):
        print("Objective:",MINMAX(self.obj).name,"\n")

    def isMin(self):
        return (self.obj == MINMAX.Minimize.value)
            
    def setVerbose(self, v):
        self.v = v

    def getChar(self, tableau, j):
        if j in range(0, len(self.c)):
            return("x_" + str(j))
        if j >= len(self.c):
            return("s_" + str(j-len(self.c)))
        
    def colorElem(self, text, h, e):
        print(colored(text, 'white', h), end = e)

    def printSolutions(self):
        if(self.feasible):
            if(self.bounded):
                print("##################################")
                print()
                print("Coefficients: ")
                k = 0
                for i in self.x:
                    print("x_", k," = ", i)
                    k += 1
                print("Optimal value: ")
                self.colorElem(self.optimalValue, 'on_green', '\n')
            else:
                print("Problem Unbounded => No Solution")
        else:
            print("Problem Infeasible => No Solution")
        

    def printTableauP(self, tableau, r, n):
        print("TAB \t\t", end = "")
        for j in range(0, len(self.c)):
            print("x_" + str(j), end = "\t")
        for j in range(0, (len(tableau[0]) - len(self.c) - 2)):
            print("s_" + str(j), end = "\t")
        
        print()
        print("------------", end="")
        for i in range(0, len(tableau[0])):
            print("-------", end="")
        print("")
        for j in range(0, len(tableau)):
            for i in range(0, len(tableau[0])):
                if not np.isnan(tableau[j, i]):
                    if i == 0:
                        print(int(tableau[j, i]), end = "\t")
                    elif j == r and i == n:
                        self.colorElem(round(tableau[j, i], 2), 'on_red', '\t')
                    else:
                        print(round(tableau[j, i], 2), end = "\t")
                        if(j==0 and i==len(tableau[0])-1):
                            print()
                            print("------------", end="")
                            for i in range(0, len(tableau[0])):
                                print("-------", end="")
                            print("")
                else:
                    print(end = "\t")
            print()
                    
    def printTableau(self, tableau):
        print("TAB \t\t", end = "")
        for j in range(0, len(self.c)):
            print("x_" + str(j), end = "\t")
        for j in range(0, (len(tableau[0]) - len(self.c) - 2)):
            print("s_" + str(j), end = "\t")
        
        print()
        print("------------", end="")
        for i in range(0, len(tableau[0])):
            print("-------", end="")
        print("")
        for j in range(0, len(tableau)):
            for i in range(0, len(tableau[0])):
                if not np.isnan(tableau[j, i]):
                    if i == 0:
                        print(int(tableau[j, i]), end = "\t")
                    else:
                        print(round(tableau[j, i], 2), end = "\t")
                        if(j==0 and i==len(tableau[0])-1):
                            print()
                            print("------------", end="")
                            for i in range(0, len(tableau[0])):
                                print("-------", end="")
                            print("")
                else:
                    print(end = "\t")
            print()

    def minRatio(self, tableau, n):
        minimum = 99999
        r = -1
        for i in range(1, len(tableau)): 
            if tableau[i, n] > 0:
                val = tableau[i, 1]/tableau[i, n]
                if val<minimum: 
                    minimum = val 
                    r = i
        return r

    def getN(self, tableau):
        if self.isMin():
                return tableau[0, 2:].tolist().index(np.amin(tableau[0, 2:])) + 2        
        return tableau[0, 2:].tolist().index(np.amax(tableau[0, 2:])) + 2

    def get_tableau(self):
        if self.isMin():
            self.A = np.transpose(self.A)
            tmp = self.c
            self.c = self.b
            self.b = tmp
            self.setobj(1)
            self.transform = True
        nVar = len(self.c)
        nSlack = len(self.A)
        
        l1 = np.hstack(([None], [0], self.c, [0] * nSlack))
        
        basis = np.array([0] * nSlack)
        
        for i in range(0, len(basis)):
            basis[i] = nVar + i
        
        A = self.A
        
        if((nSlack + nVar) != len(self.A[0])):
            B = np.identity(nSlack)
            A = np.hstack((self.A, B))
            
        l2 = np.hstack((np.transpose([basis]), np.transpose([self.b]), A))
        
        tableau = np.vstack((l1, l2))
        
        tableau = np.array(tableau, dtype ='float')

        return tableau

    def pivot(self, tableau, r, n):      
        # divide the pivot row with the pivot element 
        tableau[r, 1:] = tableau[r, 1:] / tableau[r, n] 
            
        # pivot other rows
        for i in range(0, len(tableau)): 
            if i != r:
                const = tableau[i, n] / tableau[r, n]
                tableau[i, 1:] = tableau[i, 1:] - const * tableau[r, 1:]
                
        return tableau

    def simplex(self, tableau):
        if self.v:
            if self.transform:
                print("Starting Dual Tableau:")
            else:
                print("Starting Tableau:")
            self.printTableau(tableau)
            
        #assume initial basis is not optimal, problem is feasible, and problem is bounded
        optimal = False
        feasible = True
        bounded = True
        
        # keep track of iterations for display
        iter = 1
        while(iter <= MAX_ITER):
                
            if self.isMin():
                for cost in tableau[0, 2:]:
                    if cost < 0:
                        optimal = False
                        break
                    optimal = True
            else:
                for profit in tableau[0, 2:]:
                    if profit > 0:
                        optimal = False
                        break
                    optimal = True
                    
            #if all directions result in decreased profit or increased cost
            if optimal == True: 
                 break
            
            # nth variable enters basis, minimum ratio test, rth variable leaves basis
            n = self.getN(tableau)
            r = self.minRatio(tableau, n)
            
            pivotElement = tableau[r, n]

            if self.v:
                print("##################################")
                print()
                print("Iteration :", iter)
                self.printTableauP(tableau, r, n)
            
            if self.v:
                print()
                print("Pivot Column:", n)
                print("Pivot Row:", r)
                self.colorElem("Pivot Element: " + str(round(pivotElement,2)), 'on_red', '')
                print()
                print("Variable Leaving Basis: " + str(int(tableau[r, 0])) + " (" + self.getChar(tableau, int(tableau[r, 0])) +")")
                print("Variable Entering Basis: " + self.getChar(tableau, n-2))
                print()
            
            for element in tableau[1:, n]:
                if element != 0:
                    self.bounded = True
            
            if not(self.bounded):
                print("Problem Unbounded => No solution feasible")
                return

            # pivoting on selected element
            tableau = self.pivot(tableau, r, n)
            
            # basis update 
            tableau[r, 0] = n - 2
            
            
            iter += 1
            
        
        if(self.v == True):
            print("##################################")
            print()
            print("Final Tableau reached in", iter, "iterations")
            self.printTableau(tableau)
        else:
            print("Solved")
            
        return tableau

    def optimize(self):        
        tableau = self.get_tableau()
        
        tableau = self.simplex(tableau)

        if not self.bounded:
            return
        
        # save coefficients
        if self.transform == False:
            for key in range(1, (len(tableau))):
                if(tableau[key, 0] < len(self.c)):
                    self.x[int(tableau[key, 0])] = round(tableau[key, 1],3)
        else:
            i=0
            for key in range(len(self.c)+2, (len(tableau[0]))):
                self.x[i] = -1*round(tableau[0, key],3)
                i+=1
                    
        self.optimalValue = -1 * round(tableau[0,1],3)
