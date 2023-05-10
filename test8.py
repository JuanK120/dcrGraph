import csv
import os
import threading
import concurrent.futures
import pymzn_MultiObj_AsFunct as pymzn_ExtendedDCrGraph
import DcrInstancesGenerator2 as dcrGenerator

def Run_test(tests):

    #events
    for j in tests:
        i=10;l=10;m=10;n=10;o=10;p=10
        newDir = "k"+str(i)+", Ev"+str(j)+", Ft"+str(l)+", Cnd"+str(m)+", Res"+str(n)+", In"+str(o)+", Ex"+str(p)
        print(newDir)
        if not os.path.exists(os.path.join("Tests/Detailed/k",newDir)):
            os.mkdir(os.path.join("Tests/Detailed/k",newDir))
        csv_file_path = os.path.join("Tests/Detailed/k", newDir, "data.csv")
        dataToStore =["numberOfOptimalTraces","modelsExecutionTime","exploredNodes","totalTime"]
        averages=[0,0,0,0]
        try:
            with open(csv_file_path, 'w', newline='') as csv_file:
                csvWriter = csv.writer(csv_file)
                validGraph = 0
                print("here")
                csvWriter.writerow(dataToStore)
        except Exception as e:
            print("An error occurred:", str(e))
        with open(csv_file_path, 'w', newline='') as csv_file:
            csvWriter = csv.writer(csv_file)
            validGraph=0
            print("here")
            csvWriter.writerow(dataToStore)
            while (validGraph<50):                
                model =  dcrGenerator.generate(i,j,l,m,n,o,p)
                #print(model)
                result = pymzn_ExtendedDCrGraph.solveExtendedDcrGraph(model)
                #print(result["hasSolution"])
                if (result["hasSolution"] == True):
                    print(validGraph)
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
        csv_file.close()
        with open(os.path.join("Tests/Detailed/k", "avgs.csv"), 'w', newline='') as avgs_file:
            writer = csv.writer(avgs_file)       
            writer.writerow(dataToStore)
            writer.writerow([a / 50 for a in averages])
        avgs_file.close() 
        print("instances of" + newDir + "completed")
         
    # Feats
    for l in tests:
        j=15;i=10;m=10;n=10;o=10;p=10
        newDir = "k"+str(i)+", Ev"+str(j)+", Ft"+str(l)+", Cnd"+str(m)+", Res"+str(n)+", In"+str(o)+", Ex"+str(p)
        print(newDir)
        if not os.path.exists(os.path.join("Tests/Detailed/k",newDir)):
            os.mkdir(os.path.join("Tests/Detailed/k",newDir))
        csv_file_path = os.path.join("Tests/Detailed/k", newDir, "data.csv")
        dataToStore =["numberOfOptimalTraces","modelsExecutionTime","exploredNodes","totalTime"]
        averages=[0,0,0,0]
        try:
            with open(csv_file_path, 'w', newline='') as csv_file:
                csvWriter = csv.writer(csv_file)
                validGraph = 0
                print("here")
                csvWriter.writerow(dataToStore)
        except Exception as e:
            print("An error occurred:", str(e))
        with open(csv_file_path, 'w', newline='') as csv_file:
            csvWriter = csv.writer(csv_file)
            validGraph=0
            print("here")
            csvWriter.writerow(dataToStore)
            while (validGraph<50):                
                model =  dcrGenerator.generate(i,j,l,m,n,o,p)
                #print(model)
                result = pymzn_ExtendedDCrGraph.solveExtendedDcrGraph(model)
                #print(result["hasSolution"])
                if (result["hasSolution"] == True):
                    print(validGraph)
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
        csv_file.close()
        with open(os.path.join("Tests/Detailed/k", "avgs.csv"), 'w', newline='') as avgs_file:
            writer = csv.writer(avgs_file)       
            writer.writerow(dataToStore)
            writer.writerow([a / 50 for a in averages])
        avgs_file.close() 
        print("instances of" + newDir + "completed")
                
    # Conditions
    for m in tests:
        j=2*m;l=10;i=10;n=10;o=10;p=10
        newDir = "k"+str(i)+", Ev"+str(j)+", Ft"+str(l)+", Cnd"+str(m)+", Res"+str(n)+", In"+str(o)+", Ex"+str(p)
        print(newDir)
        if not os.path.exists(os.path.join("Tests/Detailed/k",newDir)):
            os.mkdir(os.path.join("Tests/Detailed/k",newDir))
        csv_file_path = os.path.join("Tests/Detailed/k", newDir, "data.csv")
        dataToStore =["numberOfOptimalTraces","modelsExecutionTime","exploredNodes","totalTime"]
        averages=[0,0,0,0]
        try:
            with open(csv_file_path, 'w', newline='') as csv_file:
                csvWriter = csv.writer(csv_file)
                validGraph = 0
                print("here")
                csvWriter.writerow(dataToStore)
        except Exception as e:
            print("An error occurred:", str(e))
        with open(csv_file_path, 'w', newline='') as csv_file:
            csvWriter = csv.writer(csv_file)
            validGraph=0
            print("here")
            csvWriter.writerow(dataToStore)
            while (validGraph<50):                
                model =  dcrGenerator.generate(i,j,l,m,n,o,p)
                #print(model)
                result = pymzn_ExtendedDCrGraph.solveExtendedDcrGraph(model)
                #print(result["hasSolution"])
                if (result["hasSolution"] == True):
                    print(validGraph)
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
        csv_file.close()
        with open(os.path.join("Tests/Detailed/k", "avgs.csv"), 'w', newline='') as avgs_file:
            writer = csv.writer(avgs_file)       
            writer.writerow(dataToStore)
            writer.writerow([a / 50 for a in averages])
        avgs_file.close() 
        print("instances of" + newDir + "completed")


    #Responses
    for n in tests:
        j=15;l=10;m=10;i=10;o=10;p=10
        newDir = "k"+str(i)+", Ev"+str(j)+", Ft"+str(l)+", Cnd"+str(m)+", Res"+str(n)+", In"+str(o)+", Ex"+str(p)
        print(newDir)
        if not os.path.exists(os.path.join("Tests/Detailed/k",newDir)):
            os.mkdir(os.path.join("Tests/Detailed/k",newDir))
        csv_file_path = os.path.join("Tests/Detailed/k", newDir, "data.csv")
        dataToStore =["numberOfOptimalTraces","modelsExecutionTime","exploredNodes","totalTime"]
        averages=[0,0,0,0]
        try:
            with open(csv_file_path, 'w', newline='') as csv_file:
                csvWriter = csv.writer(csv_file)
                validGraph = 0
                print("here")
                csvWriter.writerow(dataToStore)
        except Exception as e:
            print("An error occurred:", str(e))
        with open(csv_file_path, 'w', newline='') as csv_file:
            csvWriter = csv.writer(csv_file)
            validGraph=0
            print("here")
            csvWriter.writerow(dataToStore)
            while (validGraph<50):                
                model =  dcrGenerator.generate(i,j,l,m,n,o,p)
                #print(model)
                result = pymzn_ExtendedDCrGraph.solveExtendedDcrGraph(model)
                #print(result["hasSolution"])
                if (result["hasSolution"] == True):
                    print(validGraph)
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
        csv_file.close()
        with open(os.path.join("Tests/Detailed/k", "avgs.csv"), 'w', newline='') as avgs_file:
            writer = csv.writer(avgs_file)       
            writer.writerow(dataToStore)
            writer.writerow([a / 50 for a in averages])
        avgs_file.close() 
        print("instances of" + newDir + "completed")

    #inclusions
    for o in tests:
        j=15;l=10;m=10;n=10;i=10;p=10
        newDir = "k"+str(i)+", Ev"+str(j)+", Ft"+str(l)+", Cnd"+str(m)+", Res"+str(n)+", In"+str(o)+", Ex"+str(p)
        print(newDir)
        if not os.path.exists(os.path.join("Tests/Detailed/k",newDir)):
            os.mkdir(os.path.join("Tests/Detailed/k",newDir))
        csv_file_path = os.path.join("Tests/Detailed/k", newDir, "data.csv")
        dataToStore =["numberOfOptimalTraces","modelsExecutionTime","exploredNodes","totalTime"]
        averages=[0,0,0,0]
        try:
            with open(csv_file_path, 'w', newline='') as csv_file:
                csvWriter = csv.writer(csv_file)
                validGraph = 0
                print("here")
                csvWriter.writerow(dataToStore)
        except Exception as e:
            print("An error occurred:", str(e))
        with open(csv_file_path, 'w', newline='') as csv_file:
            csvWriter = csv.writer(csv_file)
            validGraph=0
            print("here")
            csvWriter.writerow(dataToStore)
            while (validGraph<50):                
                model =  dcrGenerator.generate(i,j,l,m,n,o,p)
                #print(model)
                result = pymzn_ExtendedDCrGraph.solveExtendedDcrGraph(model)
                #print(result["hasSolution"])
                if (result["hasSolution"] == True):
                    print(validGraph)
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
        csv_file.close()
        with open(os.path.join("Tests/Detailed/k", "avgs.csv"), 'w', newline='') as avgs_file:
            writer = csv.writer(avgs_file)       
            writer.writerow(dataToStore)
            writer.writerow([a / 50 for a in averages])
        avgs_file.close() 
        print("instances of" + newDir + "completed")

    #exclusions
    for p in tests:
        j=15;l=10;m=10;n=10;o=10;i=10
        newDir = "k"+str(i)+", Ev"+str(j)+", Ft"+str(l)+", Cnd"+str(m)+", Res"+str(n)+", In"+str(o)+", Ex"+str(p)
        print(newDir)
        if not os.path.exists(os.path.join("Tests/Detailed/k",newDir)):
            os.mkdir(os.path.join("Tests/Detailed/k",newDir))
        csv_file_path = os.path.join("Tests/Detailed/k", newDir, "data.csv")
        dataToStore =["numberOfOptimalTraces","modelsExecutionTime","exploredNodes","totalTime"]
        averages=[0,0,0,0]
        try:
            with open(csv_file_path, 'w', newline='') as csv_file:
                csvWriter = csv.writer(csv_file)
                validGraph = 0
                print("here")
                csvWriter.writerow(dataToStore)
        except Exception as e:
            print("An error occurred:", str(e))
        with open(csv_file_path, 'w', newline='') as csv_file:
            csvWriter = csv.writer(csv_file)
            validGraph=0
            print("here")
            csvWriter.writerow(dataToStore)
            while (validGraph<50):                
                model =  dcrGenerator.generate(i,j,l,m,n,o,p)
                #print(model)
                result = pymzn_ExtendedDCrGraph.solveExtendedDcrGraph(model)
                #print(result["hasSolution"])
                if (result["hasSolution"] == True):
                    print(validGraph)
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
        csv_file.close()
        with open(os.path.join("Tests/Detailed/k", "avgs.csv"), 'w', newline='') as avgs_file:
            writer = csv.writer(avgs_file)       
            writer.writerow(dataToStore)
            writer.writerow([a / 50 for a in averages])
        avgs_file.close() 
        print("instances of" + newDir + "completed")

test = []

for i in range(50):
    test.append(15+2*i)

Run_test(test)
               
                                            


num_threads = 2
threads = []
for i in range(num_threads):
    thread = threading.Thread(target=test)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()