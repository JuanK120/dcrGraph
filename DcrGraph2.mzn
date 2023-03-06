%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%% Parameters %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Events
enum events;

%Initial Markings
array [events, 1..3] of bool: InitialM;

%Actions
enum Act;


%Condition Relations
% event conditions[i,1] must happen before event conditions[i,2]
int: numConditions;
array[1..numConditions,1..2] of events:conditions; 

%Response Relations
% event responses[i,1] must happen after event responses[i,2]
int: numResponses;
array[1..numResponses,1..2] of events:responses;

%Inclusion Relations
% if event inclusions[i,1] happens,then event inclusions[i,2] is included
int: numInclusions;
array[1..numInclusions,1..2] of events:inclusions;

%Exclusion Relations
% if event exclusions[i,1] happens,then event exclusions[i,2] is excluded
int: numExclusions;
array[1..numExclusions,1..2] of events:exclusions;

%Labeling Function
% l[i] is the label of event i
array [events] of Act: l;

%Maximum Trace Length, Valid traces must be of a length equal to K or less
int:K;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%% Variables %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Marking sequence
% array storing the markings at the I-th moment of the execution
array [1..K+1,events,1..3] of var bool: M; 

%Trace
% trace[i] is the i-th event executed, or 0
array [1..K] of var events:trace;

% the position of the last event of a trace, because a trace can be of a length < K
var int: lastEvent;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%% Predicates and functions %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% PREDICATE is_enabled
% determines if an event is enabled
% an event is enabled to be executed at the i-th moment if the event is included
% and all pre conditions of the event have already been either executed before or 
% excluded at the moment of the execution of the event
% i is the position in the trace we are analyzing
% evnt is the event we want to verirfy if it is enabled
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
predicate is_enabled(var int:i, var events:evnt)= M[i,evnt,2]==true /\ 
                                            forall(j in 1..numConditions where conditions[j,2]==events[evnt])(
                                                    M[i,conditions[j,1],1]==true\/M[i,conditions[j,1],2]==false
                                                   );
                                                   
% FUNCTION is_contained
% determines if a tuple of events is contained in an array of events
% tupl is the tuple of events we want to search
% arr is the array in which we will look for the tuple
function var bool: is_contained(array[1..2] of var events:tupl,array[int,1..2] of events:arr,int:lengthArr)= 
        exists(i in 1..lengthArr)(arr[i,1]==tupl[1] /\ arr[i,2]==tupl[2])     
        ;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%% Constraints %%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% lastEvent is the last event of a trace
%constraint forall(index in 1..K-1)(if trace[index]!=events[1] /\ trace[index+1]==events[1] then lastEvent=index else lastEvent=K endif);
constraint (events[1] in trace /\ trace[lastEvent] != events[1] /\ trace[lastEvent+1]==events[1] /\ lastEvent <= K) \/ (lastEvent == K /\ not(events[1] in trace));


% trace[i] must ve a value of the enum E or 0
constraint forall(index in 1..K)(trace[index] in events);

% if trace[i] is 0 then trace[i+1] is 0
constraint forall(index in 1..K-1)(if trace[index]==events[1] then trace[index+1]==events[1] endif);

% if trace[i] is not 0 then trace[i-1] is not 0
constraint forall(index in 2..K)(if trace[index]!=events[1] then trace[index-1]!=events[1] endif);

% if trace[i] is 0 then M[i+1] matrix is all false
constraint forall(index in 2..K+1)(if trace[index-1]==events[1] then forall(i in events,j in 1..3)(M[index,i,j]==true) endif);

% enabled events, where Event is included and all preconditions have already been executed

constraint forall(indexI in events,indexJ in 1..3)(M[1,indexI,indexJ]==InitialM[indexI,indexJ]);

% for every element of trace[i], 
constraint forall(index in 1..K)(if trace[index] != events[1] then is_enabled(index, events[trace[index]])endif);

%%% marking Transitions %%%


% add responses trigered by executing the i-th event
constraint forall(index in 2..K+1)(if trace[index-1] != events[1] then 
                                    forall(i in 1..numResponses where responses[i,1]==trace[index-1])(
                                           M[index,responses[i,2],3]== true
                                           ) endif);

% execute exclusions trigered by executing the i-th event
constraint forall(index in 2..K+1)(if trace[index-1] != events[1] then 
                                    forall(i in 1..numExclusions where exclusions[i,1]==trace[index-1])
                                          (
                                             if not(is_contained([trace[index-1],exclusions[i,2]],inclusions,numInclusions))
                                             then
                                              M[index,exclusions[i,2],2]== false
                                             endif
                                           )endif);

% 
constraint forall (index in 2..K+1)(if trace[index-1] != events[1] then
                                        M[index,trace[index-1],1]==true
                                    endif);

% execute inclusions trigered by executing the i-th event
constraint forall(index in 2..K+1)(if trace[index-1] != events[1] then 
                                    forall(i in 1..numInclusions where inclusions[i,1]==trace[index-1])
                                          (
                                              M[index,inclusions[i,2],2]== true
                                           )endif);
                                           
% if there is no inclusion, exclusion or response relation, marking is the same as the previous one                                         
constraint forall(index in 2..K+1)(if trace[index-1] != events[1] then 
                                    forall(i in events where 
                                              not(is_contained([trace[index-1],i],inclusions,numInclusions) 
                                                  \/ is_contained([trace[index-1],i],exclusions,numExclusions))
                                           )(
                                               M[index,i,2]==M[index-1,i,2]  
                                           ) endif);

constraint forall(index in 2..K+1)(if trace[index-1] != events[1] then 
                                    forall(i in events where 
                                              not(is_contained([trace[index-1],i],responses,numResponses))
                                           )(
                                               M[index,i,3]=M[index-1,i,3]  
                                           ) endif);
                                           
constraint forall (index in 2..K+1)(if trace[index-1] != events[1] then
                                        forall(e in events where e != trace[index-1])(
                                          M[index,e,1]==M[index-1,e,1]
                                        )
                                    endif);


% Accepting marking
constraint not(exists(index in events)(M[lastEvent+1,index,2]==true /\ M[lastEvent+1,index,3]==true));

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% output [
%     "trace : ", show(trace), " \n m: "] ++ [ show3d(M)] ++ [" LastEvent : ", show(lastEvent),"\n"] 
%         ++ ["%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% \n",
%          "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% \n", 
%          "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% \n"]

output ["k : ", show(lastEvent),"\n"] ++ ["trace : ", show(trace), "\n"]




