import csv
import os
import threading
import concurrent.futures
import pymzn_MultiObj_AsFunct as pymzn_ExtendedDCrGraph
import DcrInstancesGenerator2 as dcrGenerator
import random
def randnum() :
    return random.randrange(2,20)

def Run_test(tests):

    if not os.path.exists("Tests/Pareto"):
            os.mkdir("Tests/Pareto")
    csv_file_path = os.path.join("Tests/Pareto", "data.csv")
    with open(os.path.join("Tests/Pareto", "avgs.csv"), 'w', newline='') as avgs_file:
        with open(csv_file_path, 'w', newline='') as csv_file:
            with open(os.path.join("Tests/Pareto", "tests.txt"), 'w', newline='') as tests_file:
                dataToStore =["k","Events","Feats","Cond","Res","Inc","Exc","numberOfOptimalTraces","modelsExecutionTime","exploredNodes","paretoExecutionTime","paretoExploredNodes","totalTime"]
                writer = csv.writer(avgs_file)
                writer.writerow(dataToStore)
                csvWriter = csv.writer(csv_file)
                csvWriter.writerow(dataToStore)                 
                for k in tests:
                    i=randnum();j=randnum();l=randnum();m=randnum();n=randnum();o=randnum();p=randnum()
                    print("here 1")
                    averages=[0,0,0,0]
                    validGraph=0
                    graphs = ""
                    model =  dcrGenerator.generate(i,j,l,m,n,o,p)
                    result = pymzn_ExtendedDCrGraph.solveExtendedDcrGraph(model)
                    while (result["hasSolution"] == False): 
                        result = pymzn_ExtendedDCrGraph.solveExtendedDcrGraph(model)
                    print(k)
                    graphs = f"{model} \n"
                    row=[i,j,l,m,n,o,p]
                    row.append(result["numberOfOptimalTraces"])
                    averages[0]+=result["numberOfOptimalTraces"]
                    row.append(result["modelsExecutionTime"])
                    averages[1]+=result["modelsExecutionTime"]
                    row.append(result["exploredNodes"])
                    averages[2]+=result["exploredNodes"]
                    row.append(result["totalTime"]) 
                    averages[3]+=result["totalTime"]
                    csvWriter.writerow(row)
                    validGraph+=1 
                    tests_file.writelines(graphs)  
                    print(row)   
                    writer.writerow([a / len(tests) for a in averages])
                    model = ""
                    result = ""
            tests_file.close() 
        csv_file.close()
    avgs_file.close()
    print("instances completed")

test = []

for i in range(30):
    test.append(i)

Run_test(test)
            

