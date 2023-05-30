
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Base DCR Model %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%% Parameters %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Events set
enum events :: add_to_output;

%States
enum states = {executed,included,pending};

%Initial Markings
array [events, states] of bool: InitialM;

%Actions set
enum Act :: add_to_output;


%Condition Relations
% number of event conditions in the model
int: numConditions;
% event conditions[i,1] must happen at some point before event conditions[i,2]
array[1..numConditions,1..2] of events:conditions; 

%Response Relations
% number of event responses in the model
int: numResponses;
% If event responses[i,1] happens, then event responses[i,2] must happen at some point.
array[1..numResponses,1..2] of events:responses;

%Inclusion Relations
% number of event inclusions in the model
int: numInclusions;
% if event inclusions[i,1] happens,then event inclusions[i,2] is marked as included
% inmediately after in the marking system
array[1..numInclusions,1..2] of events:inclusions;

%Exclusion Relations
% number of event exclusions in the model
int: numExclusions;
% if event exclusions[i,1] happens,then event exclusions[i,2] is marked as excluded 
% inmediately after in the marking system
array[1..numExclusions,1..2] of events:exclusions;

%Labeling Function
% l[i] is the label of event i
array [events] of Act: l :: add_to_output;

%Maximum Trace Length, Valid traces must be of a length equal to K or less
int:K :: add_to_output;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%% Variables %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Marking sequence

% array storing the markings at the I-th moment of the execution,
% being M[1,...,...] the initial marking,M[2,...,...] the marking
% after executing the event trace[1], M[3,...,...] the marking
% after executing the event trace[2], and so on. this marking is
% taken into account to decide which event is executed at the i-th
% moment
array [1..K+1,events,states] of var bool: M; 

%Trace

% the position of the last event of a trace, after which the rest are
% dummy values, because a trace can be of a length < K
var int: lastEvent :: add_to_output;

% trace[i] is the i-th event executed, or dummyEvent in case the
% candidate Trace is of a length less than K
array [1..K] of var events:trace :: add_to_output;

array [1..K] of var Act:ActsOfTrace :: add_to_output;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%% Predicates and functions %%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% PREDICATE is_enabled
% determines if an event is enabled
% an event is enabled to be executed at the i-th moment if the event is included
% and all pre conditions of the event have already been either executed before or 
% excluded at the moment of the execution of the event
% -- i is the position of the trace we are analyzing
% -- evnt is the event we want to verirfy if it is enabled
predicate is_enabled(var int:i, var events:evnt, array [1..K+1,events,states] of var bool: M)= M[i,evnt,included]==true /\ 
                                            forall(j in 1..numConditions where conditions[j,2]==events[evnt])(
                                                    M[i,conditions[j,1],executed]==true\/M[i,conditions[j,1],included]==false
                                                   );
                                                   
% FUNCTION is_contained
% determines if a tuple of events is contained in an array of events
% -- tupl is the tuple of events we want to search
% -- arr is the array in which we will look for the tuple
function var bool: is_contained(array[1..2] of var events:tupl,array[int,1..2] of events:arr,int:lengthArr)= 
        exists(i in 1..lengthArr)(arr[i,1]==tupl[1] /\ arr[i,2]==tupl[2])     
        ;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%% Constraints %%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% lastEvent is the last event of a trace, be it either
% the moment of the trace where the dummy Events start,
% or K in case the trace is of K lenght
constraint (events[1] in trace /\ trace[lastEvent] != events[1] /\ trace[lastEvent+1]==events[1] /\ lastEvent <= K) \/ 
           (lastEvent == K /\ not(events[1] in trace));

% we want the dummy value to fill the rest of the trace
% when we have a candidate solution of length less than
% K, so for that we make it so that the trace is composed
% of values of Events, until either it is of length K, or
% it reaches a dummy value, after which the rest are dummy
% values. for that, then we have:

% if trace[i] is dummyEv then trace[i+1] is dummyEv
constraint forall(index in 1..K-1)(if trace[index]==events[1] then trace[index+1]==events[1] endif);
% if trace[i] is not dummyEv then trace[i-1] is not dummyEv
constraint forall(index in 2..K)(if trace[index]!=events[1] then trace[index-1]!=events[1] endif);

%%% marking Transitions %%%

% M[1,...,...] is the initial marking set of the model.
constraint forall(indexI in events,indexJ in states)(M[1,indexI,indexJ]==InitialM[indexI,indexJ]);

% We create a default value for the marking when the dummy
% values Start
% if trace[i] is dummyEv then M[i+1] matrix is all true
constraint forall(index in 2..K+1)(if trace[index-1]==events[1] then forall(i in events,j in states)(M[index,i,j]==true) endif);


% we mark as executed in M[i+1,...,...] the event executed at the I-th moment
constraint forall (index in 2..K+1)(if trace[index-1] != events[1] then
                                        M[index,trace[index-1],executed]==true
                                    endif);


% we add in M[i+1,...,...] responses trigered by executing the i-th event
constraint forall(index in 2..K+1)(if trace[index-1] != events[1] then 
                                    forall(i in 1..numResponses where responses[i,1]==trace[index-1])(
                                           M[index,responses[i,2],pending]== true
                                           ) endif);

% we mark as excluded in M[i+1,...,...] the events excluded due to executing the i-th event
constraint forall(index in 2..K+1)(if trace[index-1] != events[1] then 
                                    forall(i in 1..numExclusions where exclusions[i,1]==trace[index-1])
                                          (
                                             if not(is_contained([trace[index-1],exclusions[i,2]],inclusions,numInclusions))
                                             then
                                              M[index,exclusions[i,2],included]== false
                                             endif
                                           )endif);

% we mark as included in M[i+1,...,...] the events included due to executing the i-th event
constraint forall(index in 2..K+1)(if trace[index-1] != events[1] then 
                                    forall(i in 1..numInclusions where inclusions[i,1]==trace[index-1])
                                          (
                                              M[index,inclusions[i,2],included]== true
                                           )endif);
                                           
% if there is no inclusion or exclusion relation 
% trigered by executing the event trace[i], then
% the included marking M[i+1,...,...] is the same 
% as the previous one                                         
constraint forall(index in 2..K+1)(if trace[index-1] != events[1] then 
                                    forall(i in events where 
                                              not(is_contained([trace[index-1],i],inclusions,numInclusions) 
                                                  \/ is_contained([trace[index-1],i],exclusions,numExclusions))
                                           )(
                                               M[index,i,included]==M[index-1,i,included]  
                                           ) endif);

% if there is no Response relation trigered by
% executing the event trace[i], then the pending
% marking M[i+1,...,...] is the same as the previous one   
constraint forall (index in 2..K+1)(
  if trace[index-1] != events[1] then
    forall(i in events where not(is_contained([trace[index-1],i], responses, numResponses)))(
      M[index, i, pending] = M[index-1, i, pending] \/ M[index-1, i, included]
    )
  endif
);

% constraint forall(index in 2..K+1)(if trace[index-1] != events[1] then 
%                                     forall(i in events where 
%                                               not(is_contained([trace[index-1],i],responses,numResponses))
%                                            )(
%                                                M[index,i,pending]=M[index-1,i,pending]  
%                                            ) endif);
                         
% for all other events that are not trace[i],
% the executed marking is the same as the previous one                   
constraint forall (index in 2..K+1)(if trace[index-1] != events[1] then
                                        forall(e in events where e != trace[index-1])(
                                          M[index,e,executed]==M[index-1,e,executed]
                                        )
                                    endif);

% for every element of trace[i], they are enabled events at the i-th moment, 
% meaning, the Event is included at the i-th moment, and all preconditions
% have already been executed
constraint forall(index in 1..K)(if trace[index] != events[1] then is_enabled(index, events[trace[index]],M)endif);

% Accepting marking, the condition that must be true for a trace to be valid,
% it must happen that at the end of the trace, there must not be ane event
% that is both pending and included at the same time.
constraint not(exists(index in events)(M[lastEvent+1,index,included]==true /\ M[lastEvent+1,index,pending]==true));


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% DCR Extension %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%% Parameters %%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Features asociated with actions
enum feats :: add_to_output;

% cost[i,j] represents the cost of the action i
% asociated with the feature j
array [Act,feats] of int: cost;


enum functions = {sumVal,avgVal,lenght};
array [feats] of functions: agg;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%% Variables %%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

array[feats] of var int: alpha :: add_to_output;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%% Predicates and functions %%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Aggregation fuctions agg_f

function var int: trace_sum(array [1..K] of var events:trace, feats:feat,
                            array [Act,feats] of int: cost,array [events] of Act: l)= 
                  sum(i in 1..K where trace[i] != events[1])(cost[l[trace[i]],feat])    
                  ;

% function var int: trace_length(array [1..K] of var events:trace, feats:feat,
%                             array [Act,feats] of int: cost,array [events] of Act: l)= 
%                   sum(i in 1..lastEvent)(cost[l[trace[i]],feat])    
%                   ;

function var float: trace_avg(array [1..K] of var events:trace, feats:feat,
                            array [Act,feats] of int: cost,array [events] of Act: l)= 
                  sum(i in 1..lastEvent)(cost[l[trace[i]],feat])/lastEvent
                  ;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%% Constraints %%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

constraint forall (feat in feats)(
          if agg[feat] == sumVal then
            alpha[feat] == trace_sum(trace,feat,cost,l)
          else
            if agg[feat] == avgVal then
              alpha[feat] == trace_avg(trace,feat,cost,l)
            else 
              if agg[feat] == lenght then
                alpha[feat] == lastEvent
              endif 
            endif             
          endif
);

constraint forall(i in 1..K)(ActsOfTrace[i]= l[trace[i]]);

solve satisfy;



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% output [
%     "trace : ", show(trace), " \n m: "] ++ [ show3d(M)] ++ [" LastEvent : ", show(lastEvent),"\n"] 
%         ++ ["%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% \n",
%          "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% \n", 
%          "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% \n"]

% output ["k : ", show(lastEvent),"\n"] ++ ["trace : " ] ++ 
%        [if show(l[e])=="dummyAct" then "" else " " ++ show(l[e])endif|e in trace]
%        ++ ["\n cost : \n"] ++ [show(feat) ++ " : " ++ show(alpha[feat])|feat in feats]



