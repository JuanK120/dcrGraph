import pymzn_multiobj_allsolutions as pyAllSolVer
import pymzn_MultiObj_AsFunct as pyShortVer

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plotSolutions(DCRgraph,xlabel,ylabel,name,title) :

  allSols= pyAllSolVer.solveExtendedDcrGraph(DCRgraph)
  print("\n\n ----------------------------------------------------------------- \n\n")
  ShortSols= pyShortVer.solveExtendedDcrGraph(DCRgraph)

  data1 = pd.DataFrame({'X1': [row[0] for row in allSols["CostsBerforePareto"]], 'Y1': [row[1] for row in allSols["CostsBerforePareto"]]})
  data2 = pd.DataFrame({'X2': [row[0] for row in ShortSols["CostsBerforePareto"]], 'Y2': [row[1] for row in ShortSols["CostsBerforePareto"]]})
  data3 = pd.DataFrame({'X3': [row[0] for row in ShortSols["costOfTrace"]], 'Y3': [row[1] for row in ShortSols["costOfTrace"]]})

  plt.figure(figsize=(8, 6))

  sns.scatterplot(data=data1, x='X1', y='Y1', label='All possible solutions', alpha=1,s=180 ,marker='D')
  sns.scatterplot(data=data3, x='X3', y='Y3', label='Pareto Optimal Solutions', alpha=1,marker='X', s=180)
  sns.scatterplot(data=data2, x='X2', y='Y2', label='Solutions found using the B&B algorithm', alpha=1, s=160, marker='.')


  plt.title(f'Scatter Plot showing the costs of solutions found for the {name} graph')
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.legend()
  save_path = f'./scatter_plot_{title}.png'
  plt.savefig(save_path, format='png')
    

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

exampleBig = {
  'K': 20, 
  'feats': ['costs', 'Time'], 
  'events': ['dummyEv','Evnt1','Evnt2',
             'Evnt3','Evnt4','Evnt5',
             'Evnt6','Evnt7','Evnt8',
             'Evnt9','Evnt10','Evnt11',
             'Evnt12','Evnt13','Evnt14',
             'Evnt15','Evnt16','Evnt17',
             'Evnt18','Evnt19','Evnt20',
             'Evnt21','Evnt22','Evnt23',
             'Evnt24','Evnt25','Evnt26',
             'Evnt27','Evnt28','Evnt29',
             'Evnt30','Evnt31'], 
  'cost': [
    [0, 0],[100, 10],[28, 5],
    [180, 45],[28, 5],[28, 5],
    [150, 23],[80, 30],[80, 30],
    [120, 60],[290, 150],[200, 35],
    [28, 5],[45, 10],[105, 50],
    [120, 60],[155, 60],[28, 5],
    [28, 50],[28, 5],[60, 18],
    [10, 27],[277, 136],[74, 43],
    [32, 12],[240, 350],[80, 30],
    [28, 5],[95, 27],[30, 40],
    [120, 60],[60, 30]
    ],
  'InitialM': [
               [False, False, False],[False, True, False],[False, True, False],
               [False, True, False],[False, True, False],[False, True, False], 
               [False, True, False],[False, True, False],[False, True, False],
               [False, True, False],[False, True, False],[False, True, False],
               [False, True, False],[False, True, False],[False, True, False],
               [False, True, False],[False, True, False],[False, True, False],
               [False, True, False],[False, True, False],[False, True, False],
               [False, True, False],[False, True, False],[False, True, False],
               [False, True, False],[False, True, False],[False, True, False],
               [False, True, False],[False, True, False],[False, True, False],
               [False, True, False],[False, True, False] 
              ], 
  'Act': ['dummyAct','PaymentCompleted','ChangePhaseToPayout',
         'ApplicantJustifiesRelevance','ChangePhaseToPreparation','ChangePhaseToEndReport',
         'FirstPayment','InformApplicantOfApproval','InformApplicationOfBoardReview',
         'Approve','ArchitectReview','ExecuteAbandon',
         'ChangePhaseToComplete','RecieveEndReport','ScreenAplication',
         'RoundApproved','Review','ChangePhaseToReview',
         'ChangePhaseToBoardMeeting','ChangePhaseToAbandon','RoundEnds',
         'RegisterDecision','LawyerReview','Reject',
         'AccountNumberChanged','FillOutApplication','ApplicantInformed',
         'ChangePhaseToAbort','ExecutePreDecision','ScreeningReject',
         'ApprovedToBoard','SetToPreApproved'], 
  'conditions': [
      ['Evnt1', 'Evnt5'],
      ['Evnt5', 'Evnt12'],
      ['Evnt1', 'Evnt12'],
      ['Evnt6', 'Evnt12'],
      ['Evnt6', 'Evnt1'],
      ['Evnt13', 'Evnt12'],
      ['Evnt15', 'Evnt13'],
      ['Evnt20', 'Evnt13'],
      ['Evnt22', 'Evnt13'],
      ['Evnt25', 'Evnt15'],
      ['Evnt25', 'Evnt24'],
      ['Evnt2', 'Evnt6'],
      ['Evnt2', 'Evnt13'],
      ['Evnt7', 'Evnt2'],
      ['Evnt3', 'Evnt2'],
      ['Evnt8', 'Evnt7'],
      ['Evnt8', 'Evnt3'],
      ['Evnt4', 'Evnt3'],
      ['Evnt4', 'Evnt7'],
      ['Evnt9', 'Evnt4'],
      ['Evnt18', 'Evnt9'],
      ['Evnt8', 'Evnt14'],
      ['Evnt8', 'Evnt11'],
      ['Evnt17', 'Evnt8'],
      ['Evnt11', 'Evnt19'],
      ['Evnt18', 'Evnt11'],
      ['Evnt18', 'Evnt14'],
      ['Evnt14', 'Evnt13'],
      ['Evnt10', 'Evnt13'],
      ['Evnt17', 'Evnt10'],
      ['Evnt17', 'Evnt16'],
      ['Evnt16', 'Evnt13'],
      ['Evnt21', 'Evnt18'],
      ['Evnt18', 'Evnt23'],
      ['Evnt17', 'Evnt21'],
      ['Evnt26', 'Evnt27'],
      ['Evnt25', 'Evnt26'],
      ['Evnt25', 'Evnt20'],
      ['Evnt25', 'Evnt29']
    ], 
  'responses': [
      ['Evnt1', 'Evnt5'], 
      ['Evnt12', 'Evnt15'],
      ['Evnt24', 'Evnt15'],
      ['Evnt13', 'Evnt1'],
      ['Evnt13', 'Evnt6'],
      ['Evnt13', 'Evnt25'],
      ['Evnt13', 'Evnt12'],
      ['Evnt3', 'Evnt2'],
      ['Evnt11', 'Evnt19'],
      ['Evnt21', 'Evnt18'],
      ['Evnt23', 'Evnt26'],
      ['Evnt26', 'Evnt27']
    ], 
  'inclusions': [
      ['Evnt1', 'Evnt5'], 
      ['Evnt5', 'Evnt12'],
      ['Evnt20', 'Evnt13'],
    ], 
  'exclusions': [
      ['Evnt1', 'Evnt1'],
      ['Evnt2', 'Evnt2'],
      ['Evnt6', 'Evnt6'],
      ['Evnt5', 'Evnt5'],
      ['Evnt13', 'Evnt13'],
      ['Evnt12', 'Evnt12'],
      ['Evnt17', 'Evnt17'],
      ['Evnt14', 'Evnt14']
    ], 
  'l': ['dummyAct','PaymentCompleted','ChangePhaseToPayout',
         'ApplicantJustifiesRelevance','ChangePhaseToPreparation','ChangePhaseToEndReport',
         'FirstPayment','InformApplicantOfApproval','InformApplicationOfBoardReview',
         'Approve','ArchitectReview','ExecuteAbandon',
         'ChangePhaseToComplete','RecieveEndReport','ScreenAplication',
         'RoundApproved','Review','ChangePhaseToReview',
         'ChangePhaseToBoardMeeting','ChangePhaseToAbandon','RoundEnds',
         'RegisterDecision','LawyerReview','Reject',
         'AccountNumberChanged','FillOutApplication','ApplicantInformed',
         'ChangePhaseToAbort','ExecutePreDecision','ScreeningReject',
         'ApprovedToBoard','SetToPreApproved'], 
  'agg': ['sumVal', 'sumVal']
}

#for the flights DCR graph

print("\n test 1 : \n")

#plotSolutions(exampleFlights, 'Cost (Eur)', 'Time (Minutes)', 'fligths selection', 'fligths')

#for the big sample DCR graph

print("\n test 2 : \n")

#plotSolutions(exampleManySolutions, 'Cost (Eur)', 'Time (Minutes)', 'sample DCR', 'sample')

#For the big example #2

print("\n test 3 : \n")

plotSolutions(exampleBig, 'Cost (Eur)', 'Time (Minutes)', 'Dreyer Foundation Case', 'Dreyer')






