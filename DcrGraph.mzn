%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Dcr Graph %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%% Variables and Parameters %%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Events
enum e;
int: lenE;

%Initial Markings
array [1..3,1..lenE] of var bool: InitialM;

%Marking transitions
array [1..K+1,1..3,1..lenE] of var bool: M; 

%Actions
enum Act;
int: lenAct;

%Condition Relations
% event conditions[i,1] must happen before event conditions[i,2]
int: numConditions;
array[1..numConditions,1..2] of int:conditions;

%Response Relations
% event responses[i,1] must happen after event responses[i,2]
int: numResponses;
array[1..numResponses,1..2] of int:responses;

%Inclusion Relations
% if event inclusions[i,1] happens,then event inclusions[i,2] is included
int: numInclusions;
array[1..numInclusions,1..2] of int:inclusions;

%Exclusion Relations
% if event exclusions[i,1] happens,then event exclusions[i,2] is excluded
int: numExclusions;
array[1..numExclusions,1..2] of int:exclusions;

%Labeling Function
% l[i] is the label of event i
array [1..lenE] of int: l;
%Maximum Trace Length
int:K;

%Trace
% trace[i] is the i-th event executed, or 0
array [1..K] of var int:trace;
% the position of the last element of a trace, because a trace can be of a length < K
var int: lastEvent;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%% Constraints %%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% lastEvent is the last event of a trace
constraint forall(index in 1..K-1)(if trace[index]!=0 /\ trace[index+1]=0 then lastEvent=index else lastEvent=K endif);

% trace[i] must ve a value of the enum E or 0
constraint forall(index in 1..K)(trace[index]>=0 /\ trace[index]<=lenE);

% if trace[i] is 0 then trace[i+1] is 0
constraint forall(index in 1..K-1)(if trace[index]=0 then trace[index+1]=0 endif);

% enabled events, where Event is included and all preconditions have already been executed
constraint forall(indexI in 1..3,indexJ in 1..lenE)(M[1,indexI,indexJ]=InitialM[indexI,indexJ]);

constraint forall(index in 1..K)(if trace[index] != 0 then M[index,2,trace[index]]== true /\ 
                                    forall(i in 1..numConditions where conditions[i,2]==M[index,2,trace[index]])(
                                           M[index,1,i]== true
                                           ) endif);
% marking Transitions


% Accepting marking
constraint forall(index in 1..lenE)(not(M[lastEvent,2,index]==true /\ M[lastEvent,3,index]==true));








