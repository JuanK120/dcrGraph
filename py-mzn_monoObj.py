from minizinc import Instance, Model, Solver, Status, Result
from pareto.pareto2 import cull,dominates
import os
import sys



# Load Dcr Graph model from file
DcrModel = Model("./DcrGraph/DcrGraph_Extended2.mzn")

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

#run instance
dcrResult: Result = dcrInstance.solve()
print(dcrResult)
 
events = dcrResult["events"]
Act = dcrResult["Act"]
l = dcrResult["l"]
Kmax = dcrResult["K"]
lastEvent = dcrResult["lastEvent"]
traces = []
feats=dcrResult["feats"] 
alphas=[]
while dcrResult.status == Status.SATISFIED:
    
    traces.append(dcrResult["trace"])
    print("trace : ", dcrResult["trace"])
    alphas.append(dcrResult["alpha"])    
    print("alpha : ", dcrResult["alpha"])
    with dcrInstance.branch() as child:
        child.add_string(f"constraint weigthedSum < {dcrResult['weigthedSum']};")
        dcrResult = child.solve()
        if dcrResult.solution is not None:
            print(dcrResult.solution)

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



 