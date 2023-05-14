import csv
import os
import threading
import concurrent.futures
import pymzn_MultiObj_AsFunct as pymzn_ExtendedDCrGraph
import DcrInstancesGenerator2 as dcrGenerator

def Run_test(tests):


    #Responses
    for n in tests:
        j=45;l=10;m=10;i=10;o=10;p=10
        newDir = "k"+str(i)+", Ev"+str(j)+", Ft"+str(l)+", Cnd"+str(m)+", Res"+str(n)+", In"+str(o)+", Ex"+str(p)
        print(newDir)
        if not os.path.exists(os.path.join("Tests/Detailed/responses",newDir)):
            os.mkdir(os.path.join("Tests/Detailed/responses",newDir))
        csv_file_path = os.path.join("Tests/Detailed/responses", newDir, "data.csv")
        dataToStore =["numberOfOptimalTraces","modelsExecutionTime","exploredNodes","totalTime"]
        #with open(os.path.join("Tests/Detailed/responses", "avgs.csv"), 'w', newline='') as avgs_file:
        with open(csv_file_path, 'w', newline='') as csv_file:
            #writer = csv.writer(avgs_file)
            #writer.writerow(dataToStore)
            averages=[0,0,0,0]
            csvWriter = csv.writer(csv_file)
            validGraph=0
            csvWriter.writerow(dataToStore)
            with open(os.path.join("Tests/Detailed/responses",newDir, "tests.txt"), 'w', newline='') as tests_file:
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
            tests_file.close()      
            #writer.writerow([a / 50 for a in averages])
        csv_file.close()
        #avgs_file.close()
        print("instances of" + newDir + "completed")


test = []

for i in range(1):
    test.append(25+2*i)

Run_test(test)