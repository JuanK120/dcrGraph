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
array [1..K] of var events:paretoOptimalTrace;

array [1..numberOfFeats] of var int:paretoOptimalAlpha;

array [1..K] of var Act:ActsOfTrace;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%% Predicates and functions %%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% PREDICATE is_in_alphas
% determines if an alpha is in the given array of alphas,
% also makes sure that its corresponding trace is also assigned
% on the given array.
% -- alphas is the array of alphas we ant to search
% -- alpha is the given alpha we want to analize
% -- traces is the given array of traces associated with each alpha
% -- trace is the the trace in which we want to allocate the alpha's
%    associated trace
predicate is_in_alphas(array [1..numberOfSolutions,1..numberOfFeats] of int:alphas,
                       array [1..numberOfFeats] of var int:alpha,
                       array [1..numberOfSolutions,1..K] of events:traces, 
                       array [1..K] of var events:trace)=
       exists(i in 1..numberOfSolutions)(
        forall(j in 1..numberOfFeats)(alphas[i,j]=alpha[j]) /\ 
         forall(n in 1..K)(traces[i,n]=trace[n])
          
       );

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%% Constraints %%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%constraint is_in_alphas(alphas,paretoOptimalAlpha,traces,paretoOptimalTrace);
constraint exists(i in 1.. numberOfSolutions)(
    forall(j in 1..numberOfFeats)(paretoOptimalAlpha[j]=alphas[i,j])
  );

% For each pair of solutions in the array
constraint forall(i in 1..numberOfSolutions)(
  % Implement Pareto dominance relation
   forall(k in 1..numberOfFeats) (
    paretoOptimalAlpha[k] >= alphas[i,k]
  ) /\ exists(k in 1..numberOfFeats) (
    paretoOptimalAlpha[k] > alphas[i,k]
  )
);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

solve satisfy;
