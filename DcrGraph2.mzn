%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%% Parameters %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Events
enum e;

%Initial Markings
array [e, 1..3] of bool: InitialM;

%Actions
enum Act;


%Condition Relations
% event conditions[i,1] must happen before event conditions[i,2]
int: numConditions;
array[1..numConditions,1..2] of e:conditions;

%Response Relations
% event responses[i,1] must happen after event responses[i,2]
int: numResponses;
array[1..numResponses,1..2] of e:responses;

%Inclusion Relations
% if event inclusions[i,1] happens,then event inclusions[i,2] is included
int: numInclusions;
array[1..numInclusions,1..2] of e:inclusions;

%Exclusion Relations
% if event exclusions[i,1] happens,then event exclusions[i,2] is excluded
int: numExclusions;
array[1..numExclusions,1..2] of e:exclusions;

%Labeling Function
% l[i] is the label of event i
array [e] of Act: l;

%Maximum Trace Length, Valid traces must be of a length equal to K or less
int:K;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%% Variables %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Marking transitions
% array storing the marking at the I-th moment of the execution, made of 
array [1..K+1,e,1..3] of var bool: M; 

%Trace
% trace[i] is the i-th event executed, or 0
array [1..K] of var e:trace;

% the position of the last event of a trace, because a trace can be of a length < K
var int: lastEvent;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%% Constraints %%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% lastEvent is the last event of a trace
constraint forall(index in 1..K-1)(if trace[index]!=0 /\ trace[index+1]==0 then lastEvent==index else lastEvent==K endif);

% trace[i] must ve a value of the enum E or 0
constraint forall(index in 1..K)(trace[index]==0 \/ trace[index] in e);

% if trace[i] is 0 then trace[i+1] is 0
constraint forall(index in 1..K-1)(if trace[index]==0 then trace[index+1]==0 endif);

% if trace[i] is not 0 then trace[i-1] is not 0
constraint forall(index in 2..K+1)(if trace[index]!=0 then trace[index-1]!=0 endif);

% if trace[i] is 0 then M[i+1] matrix is all false
constraint forall(index in 1..K+1)(if trace[index]==0 then forall(i in e,j in 1..3)(M[index,i,j]==false) endif);

% enabled events, where Event is included and all preconditions have already been executed
constraint forall(indexI in e,indexJ in 1..3)(M[1,indexI,indexJ]=InitialM[indexI,indexJ]);

constraint forall(index in 1..K)(if trace[index] != 0 then M[index,trace[index],2]== true /\ 
                                    forall(i in 1..numConditions where conditions[i,2]==M[index,trace[index],2])(
                                           M[index,conditions[i,1],1]== true
                                           ) endif);
%%% marking Transitions %%%

%add i-th executed event to executed events on marking M[i]
constraint forall(i in 2..K+1)(if trace[i] !=0 then M[i,trace[i-1],1] == true endif);

%add responses trigered by executing the i-th event
constraint forall(index in 2..K+1)(if trace[index] != 0 then 
                                    forall(i in 1..numResponses where responses[i,1]==trace[index-1])(
                                           M[index,responses[i,2],3]== true
                                           ) endif);

%add exclusions trigered by executing the i-th event
constraint forall(index in 2..K+1)(if trace[index] != 0 then 
                                    forall(i in 1..numExclusions where exclusions[i,1]==trace[index-1])(
                                           M[index,exclusions[i,2],2]== false
                                           ) endif);

%add inclusions trigered by executing the i-th event
constraint forall(index in 2..K+1)(if trace[index] != 0 then 
                                    forall(i in 1..numInclusions where inclusions[i,1]==trace[index-1])(
                                           M[index,inclusions[i,2],2]== true
                                           ) endif);                                         

% Accepting marking
constraint forall(index in e)(not(M[lastEvent,index,2]==true /\ M[lastEvent,index,3]==true));




%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

output [
    "trace : ", show(trace)
]





