from minizinc import Instance, Model, Solver, Status, Result
from pareto.pareto2 import cull,dominates
import os
import sys

## Example 1
#fts=["costs","time","scales"]

#Example 2
fts=["costs","time","steps"]



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
dcrInstance["feats"]=fts

#run instance

print("executing DCR with minizinc model")

dcrResult: Result = dcrInstance.solve()
events=dcrResult["events"]
Act=dcrResult["Act"]
l=dcrResult["l"]
Kmax = dcrResult["K"]
lastEvent = dcrResult["lastEvent"]
traces = []
feats=dcrResult["feats"] 
alphas=[]

while dcrResult.status == Status.SATISFIED:
    traces.append(dcrResult["trace"])
    print(dcrResult["trace"])
    alphas.append(dcrResult["alpha"])    
    print(dcrResult["alpha"])    
    with dcrInstance.branch() as child:
        constraintBetterFeat = f"constraint (alpha[{fts[0]}] < {dcrResult['alpha'][0]})"
        for i in range(len(fts)-1):
            constraintBetterFeat += f"\/ (alpha[{fts[i+1]}] < {dcrResult['alpha'][i+1]})"                
        constraintBetterFeat += ";\n "
        child.add_string(constraintBetterFeat)
        child.add_string(f"constraint trace != {dcrResult['trace']}; \n")
        dcrResult = child.solve()
        if dcrResult.solution is not None:
            dcrInstance = child

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


#output
print("traces : ", paretoSolution["paretoOptimalTraces"])
print("alphas : ", alphas)

print("Calculating Pareto Front with pyhon code")

print(cull(alphas, dominates)[0])   

