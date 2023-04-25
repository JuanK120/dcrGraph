from minizinc import Instance, Model, Solver, Status
from pareto.pareto2 import cull,dominates
import os
import sys



# Load Dcr Graph model from file
DcrModel = Model("./DcrGraph/DcrGraph_Extended.mzn")

# Load pareto optimization for Dcr graphs model from file
paretoModel = Model("./pareto/pareto2.mzn")

# Load .dzn file for the Dcr graph model
dznFile = sys.argv[1]
if os.path.exists(dznFile):
    DcrModel.add_file(dznFile)
    #  "./minizinc/examples/DcrGraph_Ex1.dzn"

# Load MiniZinc solver
gecode = Solver.lookup("gecode")

# Create an Instance for the Dcr Graph
dcrInstance = Instance(gecode, DcrModel)
dcrInstance["K"]=int(sys.argv[2])

print(dcrInstance.analyse)

#run instance
dcrResult = dcrInstance.solve(all_solutions=True)

print(dcrResult)

#print solutions
events=dcrResult[0,"events"]
Act=dcrResult[0,"Act"]
l=dcrResult[0,"l"]
Kmax = dcrResult[0,"K"]
lastEvent = dcrResult[0,"lastEvent"]
traces = []
feats=dcrResult[0,"feats"] 
alphas=[]
for i in range(len(dcrResult)):
    traces.append(dcrResult[i,"trace"])
    print("trace : ", dcrResult[i,"trace"])
    alphas.append(dcrResult[i,"alpha"])    
    print("alpha : ", dcrResult[i,"alpha"])

print("executing DCR with minizinc model")

# Create an Instance for the Pareto model
paretoInstance = Instance(gecode, paretoModel)

# Add data to pareto model
paretoInstance["events"]=events
paretoInstance["Act"]=Act
paretoInstance["K"]=Kmax
paretoInstance["numberOfSolutions"]=len(traces)
paretoInstance["numberOfFeats"]=len(feats)
paretoInstance["traces"]=traces
paretoInstance["alphas"]=alphas
paretoInstance["l"]=l

print("Calculating Pareto Front with minizinc model")

# Solving pareto model
paretoSolution = paretoInstance.solve()
print(paretoSolution.status)


#output
print("traces : ", paretoSolution["paretoOptimalTraces"])
print("alphas : ", alphas)

print("Calculating Pareto Front with pyhon code")

print("in python")
print(cull(alphas, dominates)[0])   

