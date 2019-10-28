from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ortools.sat.python import cp_model

inputFile = open("futoshiki_input.txt", "r")

# Creates the model.
model = cp_model.CpModel()

# Creates the variables.
num_vals = 5
a1 = model.NewIntVar(1, num_vals - 1, 'a1')
a2 = model.NewIntVar(1, num_vals - 1, 'a2')
a3 = model.NewIntVar(1, num_vals - 1, 'a3')
a4 = model.NewIntVar(1, num_vals - 1, 'a4')

b1 = model.NewIntVar(1, num_vals - 1, 'b1')
b2 = model.NewIntVar(1, num_vals - 1, 'b2')
b3 = model.NewIntVar(1, num_vals - 1, 'b3')
b4 = model.NewIntVar(1, num_vals - 1, 'b4')

c1 = model.NewIntVar(1, num_vals - 1, 'c1')
c2 = model.NewIntVar(1, num_vals - 1, 'c2')
c3 = model.NewIntVar(1, num_vals - 1, 'c3')
c4 = model.NewIntVar(1, num_vals - 1, 'c4')

d1 = model.NewIntVar(1, num_vals - 1, 'd1')
d2 = model.NewIntVar(1, num_vals - 1, 'd2')
d3 = model.NewIntVar(1, num_vals - 1, 'd3')
d4 = model.NewIntVar(1, num_vals - 1, 'd4')

# Creates the constraints.
model.Add(a1 != a2)
model.Add(a2 != a3)
model.Add(a3 != a4)
model.Add(a1 != a3)
model.Add(a1 != a4)
model.Add(a2 != a4)
model.Add(b1 != b2)
model.Add(b2 != b3)
model.Add(b3 != b4)
model.Add(b1 != b3)
model.Add(b2 != b4)
model.Add(b1 != b4)
model.Add(c1 != c2)
model.Add(c2 != c3)
model.Add(c3 != c4)
model.Add(c1 != c3)
model.Add(c2 != c4)
model.Add(c1 != c4)
model.Add(d1 != d2)
model.Add(d2 != d3)
model.Add(d3 != d4)
model.Add(d1 != d3)
model.Add(d2 != d4)
model.Add(d1 != d4)
model.Add(a1 != b1)
model.Add(a1 != c1)
model.Add(a1 != d1)
model.Add(b1 != c1)
model.Add(b1 != d1)
model.Add(c1 != d1)
model.Add(a2 != b2)
model.Add(a2 != c2)
model.Add(a2 != d2)
model.Add(b2 != c2)
model.Add(b2 != d2)
model.Add(c2 != d2)
model.Add(a3 != b3)
model.Add(a3 != c3)
model.Add(a3 != d3)
model.Add(b3 != c3)
model.Add(b3 != d3)
model.Add(c3 != d3)
model.Add(a4 != b4)
model.Add(a4 != c4)
model.Add(a4 != d4)
model.Add(b4 != c4)
model.Add(b4 != d4)
model.Add(c4 != d4)

for line in inputFile:
    lineArray = line.split(", ")
    if "\n" in lineArray[1]:
        lineArray[1] = lineArray[1][:-1]
    if lineArray[1].isdigit():
        # exec("%s == %d" % (lineArray[0],int(lineArray[1])))
        model.Add(vars()[lineArray[0]] == int(lineArray[1]))
    else:
        model.Add(vars()[lineArray[0]] > vars()[lineArray[1]])

solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.FEASIBLE:
    fileOutput = open("futoshiki_output.txt", "w+")
    fileOutput.write(
        "{0}, {1}, {2}, {3}\n".format(solver.Value(a1), solver.Value(a2), solver.Value(a3), solver.Value(a4)))
    fileOutput.write(
        "{0}, {1}, {2}, {3}\n".format(solver.Value(b1), solver.Value(b2), solver.Value(b3), solver.Value(b4)))
    fileOutput.write(
        "{0}, {1}, {2}, {3}\n".format(solver.Value(c1), solver.Value(c2), solver.Value(c3), solver.Value(c4)))
    fileOutput.write(
        "{0}, {1}, {2}, {3}".format(solver.Value(d1), solver.Value(d2), solver.Value(d3), solver.Value(d4)))
    fileOutput.close()
