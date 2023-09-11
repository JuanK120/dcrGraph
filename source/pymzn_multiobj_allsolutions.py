from minizinc import Instance, Model, Solver, Status, Result
from datetime import datetime
from pareto.pareto2 import cull,dominates
import os
import sys

# Solves an Extended DCR graph and return all pareto optimal traces
# For a given graph. 
# Input
# extendedGraph : object containing all required data to run the Extended DCR Graph,
#                 with the following :
#        - K : maximum value of the traces we are looking for.
#        - feats : array of strings defining the features we are analizying
#        - events : array of strings containing the names of the events in the graph 
#        - InitialM : inititial markings of the graph
#        - Act : array of strings containing the names of the actions in the graph 
#        - conditions : bidimentional array of pairs containing events that represent the
#                       condition relations in the graph
#        - responses :  bidimentional array of pairs containing events that represent the
#                       response relations in the graph
#        - inclutions :  bidimentional array of pairs containing events that represent the
#                        inclution relations in the graph
#        - exclutions :  bidimentional array of pairs containing events that represent the
#                        exclution relations in the graph
#        - l : array of Strings that relate each even with an action in the graph
#        - agg : array of String that indicates the agregation method of each feature
#        - cost : M x N array in wich M represents an action, and N a feature, to that cost[m,n]
#                 represents the value of the feature n for the event m. 
# Output 
def solveExtendedDcrGraph(extendedGraph):
    ### Load Dcr Graph model from file
    DcrModel = Model("./DcrGraph/DcrGraph_Extended.mzn")

    # Load pareto optimization for Dcr graphs model from file
    paretoModel = Model("./pareto/pareto2.mzn")

    #### Load .dzn file for the Dcr graph model
    #dznFile = sys.argv[1]
    #if os.path.exists(dznFile):
    #    DcrModel.add_file(dznFile)
    #    #  "./minizinc/examples/DcrGraph_Ex1.dzn"

    ### Load MiniZinc solver
    gecode = Solver.lookup("gecode")

    ### Create an Instance for the Dcr Graph
    dcrInstance = Instance(gecode, DcrModel)
    #dcrInstance["K"]=int(sys.argv[2])

    dcrInstance["K"]=extendedGraph["K"]
    dcrInstance["feats"]=extendedGraph["feats"]
    dcrInstance["events"]=extendedGraph["events"]
    dcrInstance["InitialM"]=extendedGraph["InitialM"]
    dcrInstance["Act"]=extendedGraph["Act"]
    dcrInstance["conditions"]=extendedGraph["conditions"]
    dcrInstance["numConditions"]=len(extendedGraph["conditions"])
    dcrInstance["responses"]=extendedGraph["responses"]
    dcrInstance["numResponses"]=len(extendedGraph["responses"])
    dcrInstance["inclusions"]=extendedGraph["inclusions"]
    dcrInstance["numInclusions"]=len(extendedGraph["inclusions"])
    dcrInstance["exclusions"]=extendedGraph["exclusions"]
    dcrInstance["numExclusions"]=len(extendedGraph["exclusions"])
    dcrInstance["l"]=extendedGraph["l"]
    dcrInstance["agg"]=extendedGraph["agg"]
    dcrInstance["cost"]=extendedGraph["cost"]

    ### performanceMeasures
    modelsExecutionTime = 0
    exploredNodes = 0
    totalTimeStart = datetime.now()
    paretoModelExecutionTime = 0
    paretoExploredNodes = 0

    ### run instance

    solution = {}

    #print("executing DCR with minizinc model")
    dcrResult: Result = dcrInstance.solve()
    if (dcrResult.status != Status.SATISFIED) :
        solution["hasSolution"] = False
        return solution
    fts = extendedGraph["feats"]
    traces = []
    alphas=[]
    actsOfTrace=[]
    count=1
    while dcrResult.status == Status.SATISFIED and count < 5250:
        modelsExecutionTime += dcrResult.statistics["solveTime"].total_seconds()
        modelsflatTime = dcrResult.statistics["flatTime"].total_seconds()
        exploredNodes += dcrResult.statistics["nodes"]
        traces.append(dcrResult["trace"])
        #print(dcrResult["trace"])
        actsOfTrace.append(dcrResult["ActsOfTrace"])
        #print("Acts : ", dcrResult["ActsOfTrace"])
        alphas.append(dcrResult["alpha"]) 
        print(count)
        count=count+1   
        print(dcrResult["alpha"])    
        with dcrInstance.branch() as child:
            #print(fts[0],"  < ")
            #print(dcrResult["alpha"])

            #constraintBetterFeat = f"constraint (alpha[{fts[0]}] < {dcrResult['alpha'][0]})"
            #for i in range(len(fts)-1):
            #    constraintBetterFeat += f" \/ (alpha[{fts[i+1]}] < {dcrResult['alpha'][i+1]})"                
            #constraintBetterFeat += ";\n "
            #child.add_string(constraintBetterFeat)
            child.add_string(f"constraint trace != {dcrResult['trace']}; \n")
            dcrResult = child.solve()
            if dcrResult.solution is not None:
                dcrInstance = child
            #print (dcrResult.statistics["solveTime"])

    ### Create an Instance for the Pareto model
    paretoInstance = Instance(gecode, paretoModel)

    ### Add data to pareto model
    paretoInstance["events"]=extendedGraph["events"]
    paretoInstance["Act"]=extendedGraph["Act"]
    paretoInstance["K"]=extendedGraph["K"]
    paretoInstance["numberOfSolutions"]=len(traces)
    paretoInstance["numberOfFeats"]=len(fts)
    paretoInstance["traces"]=traces
    paretoInstance["alphas"]=alphas
    paretoInstance["l"]=extendedGraph["l"]

    dictret = {}
    dictret["events"]=extendedGraph["events"]
    dictret["Act"]=extendedGraph["Act"]
    dictret["K"]=extendedGraph["K"]
    dictret["numberOfSolutions"]=len(traces)
    dictret["numberOfFeats"]=len(fts)
    dictret["traces"]=traces
    dictret["alphas"]=alphas
    dictret["l"]=extendedGraph["l"]


    #print("Calculating Pareto Front with minizinc model")
    ### Solving pareto model
    paretoSolution = paretoInstance.solve()
    supersetPareto = len(traces)
    paretoModelExecutionTime = paretoSolution.statistics["solveTime"].total_seconds()
    paretoExploredNodes = paretoSolution.statistics["nodes"]
    paretoflatTime = paretoSolution.statistics["flatTime"].total_seconds()

    modelsExecutionTime += paretoSolution.statistics["solveTime"].total_seconds()
    exploredNodes += paretoSolution.statistics["nodes"]

    ### output
    #print("traces : ", paretoSolution["paretoOptimalTraces"])
    #print("alphas : ", alphas) 
    paretoOptimalTraces = []
    actionsOfTrace = []
    costOfTrace=[]

    
    for i in range(len(traces)):
        if paretoSolution["paretoOptimalTraces"][i] == True:
            paretoOptimalTraces.append(traces[i])
            #print("Trace "+ str(i) + " : ", traces[i])
            actionsOfTrace.append(actsOfTrace[i])
            #print("Actions of trace : ", actsOfTrace[i])
            costOfTrace.append(alphas[i])
            #print("Cost of trace : ", alphas[i])

    solution["hasSolution"] = True
    solution["numberOfOptimalTraces"]=len(paretoOptimalTraces)
    solution["paretoOptimalTraces"] = paretoOptimalTraces
    solution["actionsOfTrace"] = actionsOfTrace
    solution["costOfTrace"] = costOfTrace
    solution["modelsExecutionTime"] = modelsExecutionTime
    solution["exploredNodes"] = exploredNodes   
    solution["tracesBeforePareto"] = traces
    solution["CostsBerforePareto"] = alphas
    solution["paretoExecutionTime"] = paretoModelExecutionTime
    solution["paretoExploredNodes"] = paretoExploredNodes
    solution["supersetPareto"] = supersetPareto
    solution["totalTime"] = (datetime.now()-totalTimeStart).total_seconds() 
    solution["flatTimeModel"] = modelsflatTime 
    solution["flatTimePareto"] = paretoflatTime

    return solution           
