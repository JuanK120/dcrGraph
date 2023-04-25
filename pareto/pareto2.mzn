%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%% Parameters %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Events set
enum events;

%Actions set
enum Act;

%K
% Maximum Trace Length, Valid traces must be 
% of a length equal to K or less
int:K;

%numberOfSolutions
%is the total number of traces we are analyzing to get the pareto front.
int:numberOfSolutions;

%numberOfFeats
%is the total number of different features associated with each trace.
int:numberOfFeats;

%Traces
% the posible solutions we want to analyze to obtain the pareto front.
array [1..numberOfSolutions,1..K] of events:traces;
array [1..numberOfSolutions,1..numberOfFeats] of int:alphas;

%Labeling Function
% l[i] is the label of event i
array [events] of Act: l;



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%% Variables %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Trace pertaining to the pareto frontier
array [1..numberOfSolutions] of var bool:paretoOptimalTraces;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%% Constraints %%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%constraint is_in_alphas(alphas,paretoOptimalAlpha,traces,paretoOptimalTrace); 

% Constraint to ensure at least one solution is marked as Pareto optimal
constraint exists(i in 1..numberOfSolutions)(paretoOptimalTraces[i]);

% For each pair of solutions in the array
constraint (forall(i in 1..numberOfSolutions where paretoOptimalTraces[i]=true,
                  j in 1..numberOfSolutions where i!=j)(
  % Implement Pareto dominance relation
   forall(k in 1..numberOfFeats) (
    alphas[i,k] <= alphas[j,k]
  ) /\ exists(k in 1..numberOfFeats) (
    alphas[i,k] < alphas[j,k]
  )
)) \/ forall(k in 1..numberOfFeats)((exists(i in 1..numberOfSolutions where paretoOptimalTraces[i]=true,
                  j in 1..numberOfSolutions where i!=j)(
  % Implement Pareto dominance relation
   alphas[i,k]>=alphas[j,k]
)));

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

solve satisfy;
