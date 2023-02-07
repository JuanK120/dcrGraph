%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%% Dcr Graphs %%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%Events
enum e;
int: lenE;

%Marquings
array [1..3,1..lenE] of var bool: M; 

%Actions
enum Act;
int: lenAct;

%Condition Relations
int: numConditions;
array[1..numConditions,1..2] of int:conditions;

%Response Relations
int: numResponses;
array[1..numResponses,1..2] of int:responses;

%Inclusion Relations
int: numInclusions;
array[1..numInclusions,1..2] of int:inclusions;

%Exclusion Relations
int: numExclusions;
array[1..numExclusions,1..2] of int:exclusions;

%Marking Function
array [1..lenE,1..2] of int: l;

%Maximum Trace Length
int:K;

%Trace
array [1..K] of int:trace;

%Valid State
constraint forall(index in 1..lenE)(not(M[2,index]==true /\ M[3,index]==true));







