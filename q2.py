import sys
import json
from itertools import combinations

iPath = sys.argv[1]
oPath = sys.argv[2]

with open(iPath, "r") as obj:
    data = json.load(obj)

dfa_states = []
dfa_final_states = []
dfa_tm = []
dfa_letters = data['letters']
dfa_start_states = data['start_states']



#generating states for dfa:
for i in range(0,len(data['states']) + 1):
    for bracket in combinations(data['states'],i):
        dfa_states.append(list(bracket))

#generating final states for dfa
for dfa_state in dfa_states:
    for state in dfa_state:
        if state in data['final_states']:
            if dfa_state in dfa_final_states:
                continue
            else:
                dfa_final_states.append(dfa_state)


for dfa_state in dfa_states:
    for letter in dfa_letters:
        temp=[]
        for state in dfa_state:
            for transition in data['transition_matrix']:
                if(transition[0]==state and transition[1]==letter ):
                    if transition[2] in temp:
                        continue
                    else:
                        temp.append(transition[2])
        dfa_tm.append([dfa_state,letter,temp])


x = {
    "states": dfa_states,
    "letters": dfa_letters,
    "transition_matrix": dfa_tm,
    "start_states": dfa_start_states,
    "final_states": dfa_final_states
}     

with open(oPath, "w") as f:
    json.dump(x, f, indent=4)                   