import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
"""
getFeats(folder) get the features associated with tests in Folfer 'foder'
"""
def getFeats(folder):
    keyvals=folder.split(',')
    d={}
    for kv in keyvals:
        if 'k' in kv: 
            d['k']=int(kv.split('k')[1])
        elif 'Ev' in kv:
            d['Ev']=int(kv.split('Ev')[1])
        elif 'Ft' in kv:
            d['Ft']=int(kv.split('Ft')[1])
        elif 'Cnd' in kv:
            d['Cnd']=int(kv.split('Cnd')[1])
        elif 'Res' in kv:
            d['Res']=int(kv.split('Res')[1])
        elif 'In' in kv:
            d['In']=int(kv.split('In')[1])
        else:
            d['Ex']=int(kv.split('Ex')[1])
    return(d)


def getdataset(action):
    d={'i':[],'k':[],'Ev':[],'Ft':[],'Cnd':[],'Res':[],'In':[],'Ex':[],'numTraces':[],'solveTime':[],'nodes':[],'totalTime':[]}
    for folder in os.listdir(action):
        if 'k' in folder:
            F=getFeats(folder)
            lines=open(action+'/'+folder+'/data.csv').readlines()[1:]
            for (i,line) in enumerate(lines):
                vals=map(float, line.split(','))
                d['i'].append(i)
                for k in F:
                    d[k].append(F[k])

                for (k,v) in zip(['numTraces','solveTime','nodes','totalTime'],vals):
                    d[k].append(v)
    return d

def mergedatasets():
    dfCnd=pd.DataFrame.from_dict(getdataset('conditions'))
    dfRes=pd.DataFrame.from_dict(getdataset('responses'))
    dfEv=pd.DataFrame.from_dict(getdataset('events'))
    dfK=pd.DataFrame.from_dict(getdataset('k'))
    dfFts=pd.DataFrame.from_dict(getdataset('feats'))
    dfIn=pd.DataFrame.from_dict(getdataset('inclusions'))
    dfEx=pd.DataFrame.from_dict(getdataset('exclusions'))
    dfs= [dfCnd,dfRes,dfEv,dfK,dfFts,dfIn,dfEx]
    mergedDf = pd.concat(dfs)
    mergedDf.to_csv('mergedData.csv')

"""
getGlobalCSV(action) created the global CSV file associated with the tests in the different subfolders
of the corresponding action. This functions also creates a bar plot summarsing the results.
"""
def getGlobalCSV(action,plotfeat='totalTime',abreviation='k'):
#    d={'i':[],'k':[],'Ev':[],'Ft':[],'Cnd':[],'Res':[],'In':[],'Ex':[],'numTraces':[],'solveTime':[],'nodes':[],'totalTime':[]}
#    for folder in os.listdir(action):
#        if 'k' in folder:
#            F=getFeats(folder)
#            lines=open(action+'/'+folder+'/data.csv').readlines()[1:]
#            for (i,line) in enumerate(lines):
#                vals=map(float, line.split(','))
#                d['i'].append(i)
#                for k in F:
#                    d[k].append(F[k])
#
#                for (k,v) in zip(['numTraces','solveTime','nodes','totalTime'],vals):
#                    d[k].append(v)

    df=pd.DataFrame.from_dict(getdataset(action))#d

    print('k',sorted(set(df['k'])))
    print('Ev',sorted(set(df['Ev'])))
    print('Ft',sorted(set(df['Ft'])))
    print('Cnd',sorted(set(df['Cnd'])))
    print('Res',sorted(set(df['Res'])))
    print('In',sorted(set(df['In'])))
    print('Ex',sorted(set(df['Ex'])))

    if (action == 'k'):
        xLabel = "Length of trace (k)"
    else :
        xLabel = "Number of "+action

    if (plotfeat == 'nodes'):
        yLabel = "Number of nodes explored"
    else :
        yLabel = plotfeat+" (Sec)"


    df.to_csv(action+'.csv')

    conffeat=abreviation
    df=df[df[conffeat].isin(range(15,46,2))]

    plt.figure()

    plt.ylim(0, 280)
    #plt.yscale('log')
    g = sns.boxplot( x=df[conffeat],y=df[plotfeat])
    g.set(ylabel=yLabel, xlabel= xLabel)
    plt.savefig(action+'_'+conffeat+'_'+plotfeat+'.pdf', bbox_inches='tight')



#getGlobalCSV('exclusions', plotfeat='nodes')

#getGlobalCSV('conditions', plotfeat='nodes',abreviation='Cnd')
#getGlobalCSV('conditions', plotfeat='solveTime',abreviation='Cnd')
#getGlobalCSV('conditions', plotfeat='totalTime',abreviation='Cnd')
#getGlobalCSV('responses', plotfeat='nodes',abreviation='Res')
#getGlobalCSV('responses', plotfeat='solveTime',abreviation='Res')
#getGlobalCSV('responses', plotfeat='totalTime',abreviation='Res')

#getGlobalCSV('events', plotfeat='nodes',abreviation='Ev')
#getGlobalCSV('events', plotfeat='solveTime',abreviation='Ev')
#getGlobalCSV('events', plotfeat='totalTime',abreviation='Ev')
#getGlobalCSV('feats', plotfeat='nodes',abreviation='Ft')
#getGlobalCSV('feats', plotfeat='solveTime',abreviation='Ft')
#getGlobalCSV('feats', plotfeat='totalTime',abreviation='Ft')
#getGlobalCSV('k', plotfeat='nodes',abreviation='k')
#getGlobalCSV('k', plotfeat='solveTime',abreviation='k')
#getGlobalCSV('k', plotfeat='totalTime',abreviation='k')
#getGlobalCSV('inclusions', plotfeat='nodes',abreviation='In')
#getGlobalCSV('inclusions', plotfeat='solveTime',abreviation='In')
#getGlobalCSV('inclusions', plotfeat='totalTime',abreviation='In')
#getGlobalCSV('exclusions', plotfeat='nodes',abreviation='Ex')
#getGlobalCSV('exclusions', plotfeat='solveTime',abreviation='Ex')
#getGlobalCSV('exclusions', plotfeat='totalTime',abreviation='Ex')


mergedatasets()