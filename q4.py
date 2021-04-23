import sys
import json

iPath = sys.argv[1]
oPath = sys.argv[2]

with open(iPath, "r") as obj:
    data = json.load(obj)

dfa_states = []
dfa_final_states = data['final_states']
dfa_tm = data['transition_matrix']
dfa_letters = data['letters']
dfa_start_states = data['start_states']

a= data["states"]
visited ={}
v=set()
stack=[]
for state in a:
    visited[state] =0

for s in dfa_start_states:
    stack.append(s)
    while(len(stack) > 0):
        temp = stack.pop()
        if(visited[temp]):
            continue
        visited[temp]=1
        v.add(temp)
        for letter in dfa_letters:
            for t in dfa_tm:
                if(t[0]==temp and t[1]==letter):
                    if(visited[t[2]]==1):
                        break
                    stack.append(t[2])
                    break
a =list(v)
for i in a:
    dfa_states.append(i)


def samecheck(i,j,p):
    for letter in dfa_letters:
        idest='a' 
        jdest='a'
        for t in dfa_tm:
            if(t[1]==letter and t[0]==i):
                idest=t[2]
            if(t[1]==letter and t[0]==j):
                jdest=t[2]
        
        for s in p:
            if idest in s:
                if jdest in s:
                    h1=0
                else:
                    return 0
    return 1


def compare(ans,p):
    if(len(ans)!=len(p)):
        return 0
    a1=[]
    a2=[]
    for i in range(len(ans)):
        a1.append(sorted(ans[i]))
        a2.append(sorted(p[i]))
    a1=sorted(a1)
    a2=sorted(a2)
    if(a1==a2):
        return 1
    else:
        return 0
    

p = []
p.append(list(set(dfa_final_states)))
p.append(list(set(dfa_states)- set(dfa_final_states)))



while(1):
    ans=[]
    for s in p: # s of the type [q1,q2,q3,q4]
        l=len(s)
        checked=[]
        for_a_set=[]
        for temp in range(l):
            checked.append(0)
        for i in range(l): # i of the type q1

            if(checked[i]==1):
                continue
            
            for_a_index=[]
            

            for j in range(i,l): # j of the type q1
                if(checked[j]==1):
                    continue
                if(samecheck(s[i],s[j],p)==1):
                    for_a_index.append(s[j])
                    checked[j]=1
            for_a_set.append(for_a_index)
        for temp in for_a_set:
            ans.append(temp)
    
    if(compare(ans,p)):
        break
    else:
        p=[]
        for element in ans:
            p.append(element)

# for the next dfa:
ans_dfa_states = ans
ans_dfa_final_states = []
ans_dfa_tm = []
ans_dfa_letters = data['letters']
ans_dfa_start_states = []


# for start states
for i in range(len(ans_dfa_states)):
    for j in range(len(ans_dfa_states[i])):
        if ans_dfa_states[i][j] in dfa_start_states:
            ans_dfa_start_states.append(ans_dfa_states[i])
            break



# for end states:
for array in ans_dfa_states:
    for state in array:
        if state in dfa_final_states:
            ans_dfa_final_states.append(array)
            break

#for transition matrix:
for array in ans_dfa_states:

    for letter in ans_dfa_letters:

        for state in array:

            for t in dfa_tm:

                if(t[0]==state and t[1]==letter):
                    temp=t[2]
                    break
            for array1 in ans_dfa_states:
                if temp in array1:
                    ans_dfa_tm.append([array,letter,array1])
                    break
            break
        
        
x = {
    "states": ans_dfa_states,
    "letters": ans_dfa_letters,
    "transition_matrix": ans_dfa_tm,
    "start_states": ans_dfa_start_states,
    "final_states": ans_dfa_final_states
}     

with open(oPath, "w") as f:
    json.dump(x, f, indent=4)                   