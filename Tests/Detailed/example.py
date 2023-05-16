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

"""
getGlobalCSV(action) created the global CSV file associated with the tests in the different subfolders
of the corresponding action. This functions also creates a bar plot summarsing the results.
"""
def getGlobalCSV(action):
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

    df=pd.DataFrame.from_dict(d)

    print('k',sorted(set(df['k'])))
    print('Ev',sorted(set(df['Ev'])))
    print('Ft',sorted(set(df['Ft'])))
    print('Cnd',sorted(set(df['Cnd'])))
    print('Res',sorted(set(df['Res'])))
    print('In',sorted(set(df['In'])))
    print('Ex',sorted(set(df['Ex'])))


    df.to_csv(action+'.csv')

    conffeat='Ex'
    df=df[df[conffeat].isin(range(15,114,3))]
    plt.figure()
    sns.boxplot( x=df[conffeat],y=df['totalTime'])
    plt.savefig(action+'_'+conffeat+'.pdf', bbox_inches='tight')



getGlobalCSV('exclusions')