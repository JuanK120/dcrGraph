import pymzn_multiobj_allsolutions as pyAllSolVer
import pymzn_MultiObj_AsFunct as pyShortVer

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

exampleFlights = {
    "K" : 10,
    "feats" : ['costs','time'],
    "events" : ['dummyEv', 'evnt1', 'evnt2', 
                'evnt3', 'evnt4', 'evnt5', 
                'evnt6', 'evnt7', 'evnt8', 
                'evnt9', 'evnt10'],
    "InitialM" : [  [False, False, False],
                    [False, True, False],
                    [False, True, False],
                    [False, True, False],
                    [False, True, False],
                    [False, True, False],
                    [False, True, True],
                    [False, True, False],
                    [False, False, True],
                    [False, True, False],
                    [False, False, True]
                 ],
    "Act" : ['dummyAct', 'CphToLhr', 'CphToMad', 
             'MadToLhr', 'LhrToMia', 'LhrToJfk', 
             'MiaToClo', 'MiaToPty', 'PtyToClo', 
             'JfkToBog', 'BogToClo'],
    "conditions" : [['evnt1', 'evnt4'],
                    ['evnt1', 'evnt5'],
                    ['evnt2', 'evnt3'],
                    ['evnt3', 'evnt4'],
                    ['evnt3', 'evnt5'],
                    ['evnt5', 'evnt9'],
                    ['evnt4', 'evnt6'],
                    ['evnt4', 'evnt7'],
                    ['evnt7', 'evnt8'],
                    ['evnt9', 'evnt10']
                   ],
    "responses" : [
                    ['evnt2','evnt6'],
                    ['evnt5','evnt9']         
                  ],
    "inclusions" : [['evnt1', 'evnt4'],
                    ['evnt1', 'evnt5'],
                    ['evnt3', 'evnt4'],
                    ['evnt3', 'evnt5'],
                    ['evnt5', 'evnt9'],
                    ['evnt4', 'evnt6'],
                    ['evnt4', 'evnt7'],
                    ['evnt7', 'evnt8'],
                    ['evnt9', 'evnt10']
                   ],
    "exclusions" : [['evnt1', 'evnt1'],
                    ['evnt2', 'evnt2'],
                    ['evnt3', 'evnt3'],
                    ['evnt4', 'evnt4'],
                    ['evnt5', 'evnt5'],
                    ['evnt6', 'evnt6'],
                    ['evnt7', 'evnt7'],
                    ['evnt8', 'evnt8'],
                    ['evnt9', 'evnt9'],
                    ['evnt10', 'evnt10'],
                    ['evnt1', 'evnt2'],
                    ['evnt2', 'evnt1'],
                    ['evnt1', 'evnt3'],
                    ['evnt4', 'evnt5'],
                    ['evnt5', 'evnt4'],
                    ['evnt5', 'evnt6'],
                    ['evnt5', 'evnt7'],
                    ['evnt4', 'evnt9'],
                    ['evnt6', 'evnt7'],
                    ['evnt7', 'evnt6'],
                    ['evnt6', 'evnt8'],
                    ['evnt8', 'evnt6'],
                    ['evnt6', 'evnt10'],
                    ['evnt10', 'evnt6'],
                    ['evnt8', 'evnt10'],
                    ['evnt10', 'evnt8']
                   ],
    "l" : ['dummyAct','CphToLhr','CphToMad',
           'LhrToMia','LhrToJfk','MadToLhr',
           'MiaToClo','MiaToPty','PtyToClo',
           'BogToClo','JfkToBog'],
    "agg" : ['sumVal','sumVal'],
    "cost" : [[0, 0],
              [227, 12600],
              [325, 19800],
              [151, 10800],
              [424, 46800],
              [613, 68400],
              [280, 17500],
              [350, 7200],
              [447, 5976],
              [452, 21600],
              [77, 4320]
            ]
}

exampleManySolutions = {
    'K': 3, 
    'feats': ['feat0', 'feat1'], 
    'events': ['dummyEv', 'evnt0', 'evnt1', 'evnt2', 'evnt3', 'evnt4', 'evnt5', 'evnt6', 'evnt7', 'evnt8', 'evnt9', 'evnt10', 'evnt11', 'evnt12', 'evnt13', 'evnt14'], 
    'InitialM': [[False, False, False], [False, True, False], [False, True, False], [False, True, False], [False, True, False], [False, True, False], [False, True, False], [False, True, False], [False, True, False], [False, True, False], [False, True, False], [False, True, False], [False, True, False], [False, True, False], [False, True, False], [False, True, False]], 
    'Act': ['dummyAct', 'act0', 'act1', 'act2', 'act3', 'act4', 'act5', 'act6', 'act7', 'act8', 'act9', 'act10', 'act11', 'act12', 'act13', 'act14'], 
    'conditions': [['evnt7', 'evnt3'], ['evnt14', 'evnt11'], ['evnt1', 'evnt9'], ['evnt11', 'evnt9']], 
    'responses': [['evnt7', 'evnt13'], ['evnt5', 'evnt3'], ['evnt5', 'evnt10'], ['evnt3', 'evnt4'], ['evnt4', 'evnt2'], ['evnt8', 'evnt5'], ['evnt10', 'evnt0']], 
    'inclusions': [['evnt1', 'evnt3'], ['evnt14', 'evnt6'], ['evnt12', 'evnt9'], ['evnt4', 'evnt9'], ['evnt14', 'evnt5'], ['evnt9', 'evnt14'], ['evnt10', 'evnt14'], ['evnt11', 'evnt14'], ['evnt1', 'evnt4'], ['evnt0', 'evnt2'], ['evnt11', 'evnt7'], ['evnt13', 'evnt3'], ['evnt10', 'evnt13'], ['evnt9', 'evnt2'], ['evnt8', 'evnt11'], ['evnt3', 'evnt4']], 
    'exclusions': [['evnt12', 'evnt6'], ['evnt7', 'evnt3'], ['evnt1', 'evnt14'], ['evnt7', 'evnt13'], ['evnt7', 'evnt8'], ['evnt4', 'evnt7'], ['evnt0', 'evnt14'], ['evnt8', 'evnt7'], ['evnt9', 'evnt12'], ['evnt13', 'evnt1'], ['evnt9', 'evnt7'], ['evnt13', 'evnt12'], ['evnt3', 'evnt1'], ['evnt14', 'evnt3']], 
    'l': ['dummyAct', 'act1', 'act14', 'act12', 'act10', 'act4', 'act11', 'act11', 'act11', 'act2', 'act3', 'act11', 'act8', 'act0', 'act11', 'act12'], 
    'agg': ['sumVal', 'sumVal'], 
    'cost': [[82, 60], 
             [39, 99], 
             [98, 92], 
             [87, 31], 
             [44, 51], 
             [35, 26], 
             [47, 33], 
             [55, 47], 
             [77, 54], 
             [13, 71], 
             [89, 30], 
             [59, 39], 
             [62, 15], 
             [35, 24], 
             [48, 71], 
             [71, 12]]} 


#for the flights DCR graph

allSolsFlights= pyAllSolVer.solveExtendedDcrGraph(exampleFlights)

ShortSolsFlights= pyShortVer.solveExtendedDcrGraph(exampleFlights)

dataFlights1 = pd.DataFrame({'X1': [row[0] for row in allSolsFlights["CostsBerforePareto"]], 'Y1': [row[1] for row in allSolsFlights["CostsBerforePareto"]]})
dataFlights2 = pd.DataFrame({'X2': [row[0] for row in ShortSolsFlights["CostsBerforePareto"]], 'Y2': [row[1] for row in ShortSolsFlights["CostsBerforePareto"]]})
dataFlights3 = pd.DataFrame({'X3': [row[0] for row in ShortSolsFlights["costOfTrace"]], 'Y3': [row[1] for row in ShortSolsFlights["costOfTrace"]]})

plt.figure(figsize=(8, 6))

sns.scatterplot(data=dataFlights1, x='X1', y='Y1', label='All possible solutions', alpha=1,s=180 ,marker='D')
sns.scatterplot(data=dataFlights3, x='X3', y='Y3', label='Pareto Optimal Solutions', alpha=1,marker='X', s=180)
sns.scatterplot(data=dataFlights2, x='X2', y='Y2', label='Solutions found using the B&B algorithm', alpha=1, s=160, marker='.')


plt.title('Scatter Plot showing the costs of solutions found for the fligths selection DCR graph')
plt.xlabel('Cost (Eur)')
plt.ylabel('Time (Minutes)')
plt.legend()
save_path = './scatter_plot_fligths.png'
plt.savefig(save_path, format='png')


#for the big sample DCR graph

allSolsSampleDCR = pyAllSolVer.solveExtendedDcrGraph(exampleManySolutions)

shortSolsSampleDCR = pyShortVer.solveExtendedDcrGraph(exampleManySolutions)

dataSampleDCR1 = pd.DataFrame({'X1': [row[0] for row in allSolsSampleDCR["CostsBerforePareto"]], 'Y1': [row[1] for row in allSolsSampleDCR["CostsBerforePareto"]]})
dataSampleDCR2 = pd.DataFrame({'X2': [row[0] for row in shortSolsSampleDCR["CostsBerforePareto"]], 'Y2': [row[1] for row in shortSolsSampleDCR["CostsBerforePareto"]]})
dataSampleDCR3 = pd.DataFrame({'X3': [row[0] for row in shortSolsSampleDCR["costOfTrace"]], 'Y3': [row[1] for row in shortSolsSampleDCR["costOfTrace"]]})

plt.figure(figsize=(8, 6))

sns.scatterplot(data=dataSampleDCR1, x='X1', y='Y1', label='All possible solutions', alpha=1,s=180 ,marker='D')
sns.scatterplot(data=dataSampleDCR2, x='X2', y='Y2', label='Solutions found using the B&B algorithm', alpha=1,marker='X', s=180)
sns.scatterplot(data=dataSampleDCR3, x='X3', y='Y3', label='Pareto Optimal Solutions', alpha=1, s=160, marker='.')

plt.title('Scatter Plot showing the costs of solutions found for a sample DCR graph')
plt.xlabel('Feat1')
plt.ylabel('Feat2')
plt.legend()
save_path = './scatter_plot_sample.png'
plt.savefig(save_path, format='png')





