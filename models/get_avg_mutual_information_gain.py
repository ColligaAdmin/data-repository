from generalized_model import (
    fix_column_names,
    
)

import pandas as pd, os, numpy as np



global_column_count={}

files = os.listdir('MI')
files=[os.path.join('MI',file) for file in files]
for file in files:
    data=pd.read_excel(file)
    data=fix_column_names(data)
    
    columns=set(data.columns)
    for column in columns:
        if column not in global_column_count:
            global_column_count[column]=0.0
        #Increase the appearance of feature counts in top feature calculations
        global_column_count[column]+=1
#Sort features based on importance
global_column_count = sorted(global_column_count.items(), key=lambda x:x[1],reverse = True)
global_column_count=list(global_column_count)

top_features=[]
#Get top 10 features
for i in range(1,11):
    top_features.append(global_column_count[i][0])
print('---------Top 10 features--------')
for feature in top_features:
    print(feature, end='\t')
print('\n')    
set_top_features=set(top_features)
avg_mi={}
outcomes=['Happiness','Sadness','Anxiousness','Angriness','Stress','Quality_time',
             'Closeness','Positivity','Negativity','Conflict','Aggression']  

mi_top_features={}
for outcome in outcomes:
    mi_top_features[outcome]={}
    for feature in set_top_features:
        mi_top_features[outcome][feature]=[]

for file in files:
    data=pd.read_excel(file)
    data=fix_column_names(data)
    
    for this_column in data.columns:
        if this_column in set_top_features:
            for j in range(len(outcomes)):
                mi_top_features[outcomes[j]][this_column].append(data.loc[j,this_column])
for outcome in mi_top_features:
    for feature in mi_top_features[outcome]:
        mi_top_features[outcome][feature]=np.average(mi_top_features[outcome][feature])
print("--------Average Mutual Information Gain Across All CareGivers----------")
for outcome in mi_top_features:
    print("\n\n {outcome} \n\n".format(outcome=outcome))
    for feature in top_features:
        print(feature+'\t', end='')
        print(mi_top_features[outcome][feature])