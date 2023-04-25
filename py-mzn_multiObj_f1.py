from minizinc import Instance, Model, Solver, Status, Result
from pareto.pareto2 import cull,dominates
import os
import sys

evs=["dummyEv","evnt1","evnt2","evnt3","evnt4","evnt5","evnt6","evnt7","evnt8","evnt9","evnt10"]
fts=["costs","time","scales"]



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
dcrInstance["events"]=evs
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
    alphas.append(dcrResult["alpha"])    
    count=0
    with dcrInstance.branch() as child:
        constraintBetterFeat = f"constraint"
        for i in range(len(fts)):
            if count==0:
                constraintBetterFeat += f"(alpha[{fts[i]}] < {dcrResult['alpha'][i]})"
                count += 1
            else :
                constraintBetterFeat += f"\/ (alpha[{fts[i]}] < {dcrResult['alpha'][i]})"                
                count += 1
        constraintBetterFeat += ";"
        child.add_string(constraintBetterFeat)
        dcrResult = child.solve()
        if dcrResult.solution is not None:
            print(dcrResult["trace"])
            print(dcrResult["alpha"])

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

print("in python")
print(cull(alphas, dominates)[0])   

