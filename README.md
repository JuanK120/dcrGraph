
  # Pareto-Optimal Trace Generation from Declarative Process Models 

  ## Description

  This is the repository containing the extended version of the article "Pareto-Optimal Trace Generation from Declarative Process Models" 
  submitted for the 11th International Workshop on DEClarative, DECision, and Hybrid approaches to processes 
  
  ## Index ##
  
  - [Contents](#Contents)
    
  - [Instalation](#Instalation)
  
  - [Usage](#Usage)
  
  - [Credits](#Credits)

  ## Contents

  This repository is structured in the following manner, first, we have the pdf file of the article submitted for the conference, then we have the source folder,
  containing the source code for the solution implemented for the article.

  inside the source folder we have different subfiles: 
  - DcrGraph : a folder containing the model used for the implementation in minizinc of the constraint model of a DCR graph.
  - pareto : a folder containing a constraint model created to implement the Pareto sorting used to solve the problem described in the article.
  - Tests : a folder containing the DCR graph generator used to generate DCR graphs to test the performance of the tool, and all tests, datafiles,
     and scripts used while testing the performance of the tool.
  - pymzn_MultiObj_AsFunct.py: contains the code of the implementation of our tool combining the DCR graph constraint model and implementing both
    the branch and bound algorithm and the pareto sorting to compute the Pareto front of a DCR graph 

  ## Instalation

  To install this tool it is necessary to have installed :
  - Python version 3.9.5
  - MiniZinc version 2.6.2
  - Gecode Solver version 6.3.0
  - Python-minzinc library version 0.9.0.

  Then, it is only needed to clone the repository and import the pymzn_MultiObj_AsFunct.py in a new Python file or script.
  
  ## Usage

  To use the tool, once istalled, the user has to make a call to the method solveExtendedDcrGraph(extendedGraph), where 
  extendedGraph is a python dict (dictionary) containing the following keys and values:

  - "K" : maximum value of the traces we are looking for.
  - "feats" : array of strings defining the features we are analizying
  - "events" : array of strings containing the names of the events in the graph 
  - "InitialM" : inititial markings of the graph
  - "Act" : array of strings containing the names of the actions in the graph 
  - "conditions" : bidimentional array of pairs containing events that represent the condition relations in the graph, in
    which the first event of the event is the trigering event, and the second is the target event, meaning that for a pair
    in the array, for example ["eventA", "eventB"], then eventA must happen before eventB
  - "responses" :  bidimentional array of pairs containing events that represent the response relations in the graph, in
    which the first event of the event is the trigering event, and the second is the target event, meaning that for a pair
    in the array, for example ["eventA", "eventB"], then if eventA where to be executed then eventB would be marked as pending
  - "inclutions" :  bidimentional array of pairs containing events that represent the inclution relations in the graph, in
    which the first event of the event is the trigering event, and the second is the target event, meaning that for a pair
    in the array, for example ["eventA", "eventB"], then if eventA where to be executed then eventB would be marked as included
  - "exclutions" :  bidimentional array of pairs containing events that represent the exclution relations in the graph, in
    which the first event of the event is the trigering event, and the second is the target event, meaning that for a pair
    in the array, for example ["eventA", "eventB"], then if eventA where to be executed then eventB would be marked as excluded
  - "l" : array of Strings that relate each even with an action in the graph
  - "agg" : array of String that indicates the agregation method of each feature, at the moment it can be 'sumVal' to indicate a sum
    of the values, or 'lenght', that the value is the lenght of the trace
  - "cost" : M x N array in wich M represents an action, and N a feature, to that cost[m,n]  represents the value of the feature n
    for the event m.

  then the output of the toll is a python dict containing the next keys and values :

  - "hasSolution": boolean value indicating if the given DCR graph has or not a valid solution
  - "numberOfOptimalTraces": indicates the number of optimal traces for the given DCR graph
  - "paretoOptimalTraces": an array containing the optimal traces for the given DCR graph
  - "actionsOfTrace": an array containing the actions associated with each optimal trace of the DCR graph
  - "costOfTrace": an array containing the cost associated with each optimal trace of the DCR graph
  - "modelsExecutionTime": the time the minizinc solver took to run the model.
  - "exploredNodes": the number of nodes of the search tree generated by the minizinc solver explored to generate the solutions
  - "tracesBeforePareto": the number of traces generated in the superset of the Pareto frontier generated before applying the Pareto filter
  - "CostsBerforePareto": an array containing the cost associated with each trace of the superset of the Pareto frontier
  - "paretoExecutionTime": the time taken by the Pareto filter to identify the Pareto frontier from the superset 
  - "supersetPareto": the number of traces present in the superset of the Pareto frontier
  - "flatTimeModel": the flattening time taken by minizinc to convert the entry into a minizinc datafile to run 
  - "totalTime": the total time taken by the tool to finish running.

  ## Credits

  Juan F. Diaz - juanfco.diaz@correounivalle.edu.co
  Hugo A. López - hulo@dtu.dk
  Luis Quesada - luis.quesada@insight-centre.org
  Juan C. Rosero - juan.camilo.rosero@correounivalle.edu.co

  
  
