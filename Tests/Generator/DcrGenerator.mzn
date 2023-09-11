enum events;
enum Act;

int: numConditions;
int: numResponses;
int: numInclusions;
int: numExclusions;

array [1..numConditions,1..2] of var events:conditions;
array [1..numResponses,1..2] of var events:responses;
array [1..numInclusions,1..2] of var events:inclusions;
array [1..numExclusions,1..2] of var events:exclusions;
array [events] of var Act: l;




constraint forall(i in 1..numConditions)(conditions[i,1]!=conditions[i,2]);

constraint forall(i in 1..numResponses)(responses[i,1]!=responses[i,2]);

constraint forall(i in 1..numConditions)(conditions[i,1]!=events[1] /\ conditions[i,2]!=events[1]);
constraint forall(i in 1..numResponses)(responses[i,1]!=events[1] /\ responses[i,2]!=events[1]);
constraint forall(i in 1..numInclusions)(inclusions[i,1]!=events[1] /\ inclusions[i,2]!=events[1]);
constraint forall(i in 1..numExclusions)(exclusions[i,1]!=events[1] /\ exclusions[i,2]!=events[1]);


constraint forall(i in 1..numConditions)(
    conditions[i, 1] != conditions[i, 2]
);

constraint forall(i in 1..numResponses)(
    responses[i, 1] != responses[i, 2] 
);

constraint forall(i in 1..numInclusions)(
    inclusions[i, 1] in events /\
    inclusions[i, 2] in events /\
    inclusions[i, 1] != inclusions[i, 2]
);

constraint forall(i in 1..numExclusions)(
    exclusions[i, 1] in events /\
    exclusions[i, 2] in events /\
    exclusions[i, 1] != exclusions[i, 2]
);

constraint forall(i, j in 1..numConditions where i != j)(
    conditions[i, 1] != conditions[j, 1] \/ conditions[i, 2] != conditions[j, 2]
);

constraint forall(i, j in 1..numResponses where i != j)(
    responses[i, 1] != responses[j, 1] \/ responses[i, 2] != responses[j, 2]
);

constraint forall(i, j in 1..numInclusions where i != j)(
    inclusions[i, 1] != inclusions[j, 1] \/ inclusions[i, 2] != inclusions[j, 2]
);

constraint forall(i, j in 1..numExclusions where i != j)(
    exclusions[i, 1] != exclusions[j, 1] \/ exclusions[i, 2] != exclusions[j, 2]
);

constraint l[events[1]]== Act[1];
constraint forall(i in events where i != events[1])(l[i]!=Act[1]);

solve :: seq_search([
             int_search(conditions, first_fail, indomain_random),
             int_search(responses, first_fail, indomain_random),
             int_search(inclusions, first_fail, indomain_random),
             int_search(exclusions, first_fail, indomain_random),
             int_search(l, first_fail, indomain_random)])
       satisfy;


% enum events;
% enum Act;

% int: numConditions;
% int: numResponses;
% int: numInclusions;
% int: numExclusions;

% array [1..numConditions, 1..2] of var events: conditions;
% array [1..numResponses, 1..2] of var events: responses;
% array [1..numInclusions, 1..2] of var events: inclusions;
% array [1..numExclusions, 1..2] of var events: exclusions;
% array [events] of var Act: l;

% constraint forall(i in 1..numConditions)(
%     conditions[i, 1] != conditions[i, 2] /\
%     conditions[i, 1] in events /\
%     conditions[i, 2] in events
% );

% constraint forall(i in 1..numResponses)(
%     responses[i, 1] != responses[i, 2] /\
%     responses[i, 1] in events /\
%     responses[i, 2] in events
% );

% constraint forall(i in 1..numInclusions)(
%     inclusions[i, 1] in events /\
%     inclusions[i, 2] in events /\
%     inclusions[i, 1] != inclusions[i, 2]
% );

% constraint forall(i in 1..numExclusions)(
%     exclusions[i, 1] in events /\
%     exclusions[i, 2] in events /\
%     exclusions[i, 1] != exclusions[i, 2]
% );

% constraint forall(i in 1..numConditions, j in 1..numResponses)(
%     conditions[i, 1] != responses[j, 1] /\
%     conditions[i, 2] != responses[j, 2]
% );

% constraint forall(i in 1..numInclusions, j in 1..numResponses)(
%     inclusions[i, 1] != responses[j, 1] /\
%     inclusions[i, 2] != responses[j, 2]
% );

% constraint forall(i in 1..numExclusions, j in 1..numConditions)(
%     exclusions[i, 1] != conditions[j, 1] /\
%     exclusions[i, 2] != conditions[j, 2]
% );

% constraint l[events[1]] == Act[1];
% constraint forall(i in events where i != events[1]) (l[i] != Act[1]);

% solve :: seq_search([
%     int_search(conditions, first_fail, indomain_random),
%     int_search(responses, first_fail, indomain_random),
%     int_search(inclusions, first_fail, indomain_random),
%     int_search(exclusions, first_fail, indomain_random),
%     int_search(l, first_fail, indomain_random)
% ]) satisfy;