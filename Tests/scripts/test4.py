import csv
import os
import threading
import concurrent.futures
import pymzn_MultiObj_AsFunct as pymzn_ExtendedDCrGraph
import DcrInstancesGenerator2 as dcrGenerator

def Run_test(tests):
                
    # Conditions
    for m in tests:
        j=45;l=10;i=10;n=10;o=10;p=10
        newDir = "k"+str(i)+", Ev"+str(j)+", Ft"+str(l)+", Cnd"+str(m)+", Res"+str(n)+", In"+str(o)+", Ex"+str(p)
        print(newDir)
        if not os.path.exists(os.path.join("Tests/Detailed/conditions",newDir)):
            os.mkdir(os.path.join("Tests/Detailed/conditions",newDir))
        csv_file_path = os.path.join("Tests/Detailed/conditions", newDir, "data.csv")
        dataToStore =["numberOfOptimalTraces","modelsExecutionTime","exploredNodes","totalTime"]
        with open(os.path.join("Tests/Detailed/conditions", "avgs.csv"), 'w', newline='') as avgs_file:
            with open(csv_file_path, 'w', newline='') as csv_file:
                writer = csv.writer(avgs_file)
                writer.writerow(dataToStore)
                csvWriter = csv.writer(csv_file)
                validGraph=0
                csvWriter.writerow(dataToStore)
                with open(os.path.join("Tests/Detailed/conditions",newDir, "tests.txt"), 'w', newline='') as tests_file:
                    graphs = ""
                    while (validGraph<15):
                        model =  dcrGenerator.generate(i,j,l,m,n,o,p)
                        #print(model)
                        result = pymzn_ExtendedDCrGraph.solveExtendedDcrGraph(model)
                        #print(result["hasSolution"])
                        if (result["hasSolution"] == True):
                            print(validGraph)
                            print(model)
                            graphs += f"{model} \n"
                            #print(result["numberOfOptimalTraces"])
                            row=[]
                            row.append(result["numberOfOptimalTraces"])
                            row.append(result["modelsExecutionTime"])
                            row.append(result["exploredNodes"])
                            row.append(result["totalTime"]) 
                            csvWriter.writerow(row)
                            validGraph+=1 
                    tests_file.writelines(graphs)
                tests_file.close()      
            csv_file.close()
        avgs_file.close()
        print("instances of" + newDir + "completed")
                

test = []

for i in range(15):
    test.append(15+2*i)

Run_test(test)