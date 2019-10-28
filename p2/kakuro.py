from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ortools.sat.python import cp_model

inputFile = open("kakuro_input.txt", "r")

model = cp_model.CpModel()

# Creates the variables.
num_vals = 10
x1 = model.NewIntVar(1, num_vals - 1, 'x1')
x2 = model.NewIntVar(1, num_vals - 1, 'x2')
x3 = model.NewIntVar(1, num_vals - 1, 'x3')
y1 = model.NewIntVar(1, num_vals - 1, 'y1')
y2 = model.NewIntVar(1, num_vals - 1, 'y2')
y3 = model.NewIntVar(1, num_vals - 1, 'y3')
z1 = model.NewIntVar(1, num_vals - 1, 'z1')
z2 = model.NewIntVar(1, num_vals - 1, 'z2')
z3 = model.NewIntVar(1, num_vals - 1, 'z3')

# Creates the constraints.
model.Add(x1 != x2)
model.Add(x1 != x3)
model.Add(x2 != x3)
model.Add(y1 != y2)
model.Add(y1 != y3)
model.Add(y2 != y3)
model.Add(z1 != z2)
model.Add(z2 != z3)
model.Add(z1 != z3)
model.Add(x1 != y1)
model.Add(y1 != z1)
model.Add(x1 != z1)
model.Add(x2 != y2)
model.Add(x2 != z2)
model.Add(y2 != z2)
model.Add(x3 != y3)
model.Add(x3 != z3)
model.Add(y3 != z3)

liste = {}
i = 0
for line in inputFile:
    lineArray = line.split(", ")
    if "\n" in lineArray[2]:
        lineArray[2] = lineArray[2][:-1]
    liste[i] = lineArray
    i = i + 1
print(liste)
print(liste[0][0])

model.Add(x1 + x2 + x3 == int(liste[1][0]))
model.Add(y1 + y2 + y3 == int(liste[1][1]))
model.Add(z1 + z2 + z3 == int(liste[1][2]))

model.Add(x1 + y1 + z1 == int(liste[0][0]))
model.Add(x2 + y2 + z2 == int(liste[0][1]))
model.Add(x3 + y3 + z3 == int(liste[0][2]))
# Creates a solver and solves the model.
solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.FEASIBLE:
    fileOutput=open("koutput.txt", "w+")
    fileOutput.write("x, {0}, {1}, {2}\n".format(liste[0][0],liste[0][1],liste[0][2]))
    fileOutput.write("{0}, {1}, {2}, {3}\n".format(liste[1][0],solver.Value(x1),solver.Value(x2),solver.Value(x3)))
    fileOutput.write("{0}, {1}, {2}, {3}\n".format(liste[1][1],solver.Value(y1),solver.Value(y2),solver.Value(y3)))
    fileOutput.write("{0}, {1}, {2}, {3}".format(liste[1][2],solver.Value(z1),solver.Value(z2),solver.Value(z3)))
    fileOutput.close()


