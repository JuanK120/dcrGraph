import random


def generate(k,events,feats,conditions,responses,inclusions,exclusions):
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
        marking=[True]
        for i in range(2):
            marking.append(randBool())
        model["InitialM"].append(marking)

    for i in range(feats):
        featName = "feat" + str(i)
        model["feats"].append(featName)
        model["agg"].append(randAgg())
        

    for i in range(conditions):
        condition = []
        condition.append(model["events"][random.randrange(1,events+1)])
        condition.append(model["events"][random.randrange(1,events+1)])
        while condition[0]==condition[1]:
            condition[0]=model["events"][random.randrange(1,events+1)]
            condition[1]=model["events"][random.randrange(1,events+1)]
        model["conditions"].append(condition)

    for i in range(responses):
        response = []
        response.append(model["events"][random.randrange(1,events+1)])
        response.append(model["events"][random.randrange(1,events+1)])
        while response[0]==response[1]:
            response[0]=model["events"][random.randrange(1,events+1)]
            response[1]=model["events"][random.randrange(1,events+1)]
        model["responses"].append(response)

    for i in range(inclusions):
        inclusion = []
        inclusion.append(model["events"][random.randrange(1,events+1)])
        inclusion.append(model["events"][random.randrange(1,events+1)])
        model["inclusions"].append(inclusion)
    for i in range(exclusions):
        exclusion = []
        exclusion.append(model["events"][random.randrange(1,events+1)])
        exclusion.append(model["events"][random.randrange(1,events+1)])
        model["exclusions"].append(exclusion)

    for i in range(events):
        model["l"].append(model["Act"][random.randrange(1,events+1)])
    
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
    return random.randrange(1,1000)

