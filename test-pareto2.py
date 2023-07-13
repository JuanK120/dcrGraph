import csv
import os
import ast
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
            with open(os.path.join("Tests/Pareto", "tests.txt"), 'rb') as tests_file:
                count=22
                dataToStore =["k","Events","Feats","Cond","Res","Inc","Exc","numberOfOptimalTraces","supersetPareto","modelsExecutionTime","exploredNodes","paretoExecutionTime","paretoExploredNodes","totalTime","flatTimeModel","flatTimePareto"]
                writer = csv.writer(avgs_file)
                writer.writerow(dataToStore)      
                while count<=40:
                    with open(os.path.join("Tests/Pareto", f"{count}.csv"), 'w', newline='') as csv_file:
                        csvWriter = csv.writer(csv_file)
                        csvWriter.writerow(dataToStore) 
                        print(count, "\n") 
                        count += 1
                        #print("here 1")
                        averages=[0,0,0,0,0,0,0]
                        validGraph=0
                        graphs = ""
                        # Get next line from file
                        line = tests_file.readline()
                        # if line is empty
                        # end of file is reached
                        if not line:
                            break
                        line = line
                        model = eval(line)
                        
                        try :
                            result = pymzn_ExtendedDCrGraph.solveExtendedDcrGraph(model)
                            while (result["hasSolution"] == False): 
                                result = pymzn_ExtendedDCrGraph.solveExtendedDcrGraph(model)  
                            row=[model["K"],len(model["events"]),len(model["feats"]),len(model["conditions"]),len(model["responses"]),len(model["inclusions"]),len(model["exclusions"])]
                            row.append(result["numberOfOptimalTraces"])
                            averages[0]+=result["numberOfOptimalTraces"]
                            row.append(result["supersetPareto"])
                            averages[1]+=result["numberOfOptimalTraces"]
                            row.append(result["modelsExecutionTime"])
                            averages[2]+=result["modelsExecutionTime"]
                            row.append(result["exploredNodes"])
                            averages[3]+=result["exploredNodes"]
                            row.append(result["paretoExecutionTime"]) 
                            averages[4]+=result["paretoExecutionTime"]
                            row.append(result["paretoExploredNodes"]) 
                            averages[5]+=result["paretoExploredNodes"]
                            row.append(result["totalTime"]) 
                            averages[6]+=result["totalTime"]
                            row.append(result["flatTimeModel"]) 
                            row.append(result["flatTimePareto"]) 
                        except:
                            row=[model["K"],len(model["events"]),len(model["feats"]),len(model["conditions"]),len(model["responses"]),len(model["inclusions"]),len(model["exclusions"])]
                            row.append("__")
                            averages[0]+=0
                            row.append("__")
                            averages[1]+=0
                            row.append("__")
                            averages[2]+=0
                            row.append("__")
                            averages[3]+=0
                            row.append("__") 
                            averages[4]+=0
                            row.append("__") 
                            averages[5]+=0
                            row.append("__") 
                            averages[6]+=0
                            row.append("__") 
                            row.append("__") 
                        csvWriter.writerow(row)
                        validGraph+=1  
                        #print(row)    
                        model = ""
                        result = ""
                        csv_file.close()
                tests_file.close()
            avgs_file.close()
    print("instances completed")

test = []

for i in range(30):
    test.append(i)

Run_test(test)