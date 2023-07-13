%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%% Parameters %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Events set
enum events;

% Actions set
enum Act;

% K
% Maximum Trace Length, Valid traces must be 
% of a length equal to K or less
int: K;

% numberOfSolutions
% is the total number of traces we are analyzing to get the pareto front.
int: numberOfSolutions;

% numberOfFeats
% is the total number of different features associated with each trace.
int: numberOfFeats;

% Traces
% the possible solutions we want to analyze to obtain the pareto front.
array [1..numberOfSolutions, 1..K] of events: traces;
array [1..numberOfSolutions, 1..numberOfFeats] of int: alphas;

% Labeling Function
% l[i] is the label of event i
array [events] of Act: l;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%% Variables %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Trace pertaining to the pareto frontier
array [1..numberOfSolutions] of var bool: paretoOptimalTraces;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%% Constraints %%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Function to check if one array dominates another array
function var bool: dominates(array[1..numberOfFeats] of int : array1,array[1..numberOfFeats] of int :  array2) =
  forall(i in 1..numberOfFeats) (
    array1[i] >= array2[i]
  );

constraint exists(i in 1..numberOfSolutions)(paretoOptimalTraces[i]);

% Finding Pareto optimal traces
constraint
  forall(i in 1..numberOfSolutions) (
    let {
      var bool: is_pareto_optimal = true;
    } in
    forall(j in 1..numberOfSolutions) (
      if i != j /\ dominates(alphas[i, 1..numberOfFeats], alphas[j, 1..numberOfFeats]) then
        is_pareto_optimal = false
      endif
    )
    /\ is_pareto_optimal -> paretoOptimalTraces[i]
  );

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%% Solve %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

solve satisfy;