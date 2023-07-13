from minizinc import Instance, Model, Solver, Status, Result
import random


### Load Dcr Graph model from file
generatorModel = Model("./Tests/Generator/DcrGenerator.mzn")

### Load MiniZinc solver
gecode = Solver.lookup("gecode")




def generate(k,events,feats,conditions,responses,inclusions,exclusions):
    generatorInstance = Instance(gecode, generatorModel)
    model = {
        "K" : k,
        "feats" : [],
        "events" : ['dummyEv'],
        "InitialM" : [[False,False,False]],
        "Act" : ['dummyAct'],
        "conditions" : [],
        "responses" : [],
        "inclusions" : [],
        "exclusions" : [],
        "l" : ['dummyAct'],
        "agg" : [],
        "cost" : []
    }
    for i in range(events):
        eventName = "evnt" + str(i)
        ActName = "act" + str(i)
        model["events"].append(eventName)
        model["Act"].append(ActName)
        marking=[False,True,randBool()]
        model["InitialM"].append(marking)

    for i in range(feats):
        featName = "feat" + str(i)
        model["feats"].append(featName)
        model["agg"].append(randAgg())
        
    generatorInstance["events"]=model["events"]
    generatorInstance["Act"]=model["Act"]
    generatorInstance["numConditions"]=conditions
    generatorInstance["numResponses"]=responses
    generatorInstance["numInclusions"]=inclusions
    generatorInstance["numExclusions"]=exclusions
    generatedDcr:Result = generatorInstance.solve()
    	
    model["conditions"]=generatedDcr["conditions"]
    model["responses"]=generatedDcr["responses"]
    model["inclusions"]=generatedDcr["inclusions"]
    model["exclusions"]=generatedDcr["exclusions"]
    model["l"]=generatedDcr["l"]
    
    for i in range(events+1):
        actCost=[]
        for j in range(feats):
            if j == 0 :
                actCost.append(0)
            else:
                actCost.append(randCost())
        model["cost"].append(actCost)
    
    
    return model
    
def randBool() :
    if (random.randrange(0,1)==0) :
        return False
    else:
        return True
    
def randAgg() :
    if (random.randrange(0,1)==0) :
        return 'sumVal'
    else:
        return 'lenght'
    
def randCost() :
    return random.randrange(1,100)
