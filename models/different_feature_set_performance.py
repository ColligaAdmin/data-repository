# -*- coding: utf-8 -*-
"""
Created on Wed May 22 23:09:18 2024

@author: User
"""


import pandas as pd
import os



from scipy.stats import mannwhitneyu
folder_name="Personalized_Model_Results"

activity_feature_name="activity features"

environment_feature_name="environment features"

interaction_feature_name="interaction features"

language_feature_name="speech features"

sleep_feature_name="sleep features"

activity_sleep_feature_name="activity_sleep features"

activity_sleep_environment_feature_name="activity_sleep_environment features"



features=[activity_sleep_feature_name,
          activity_sleep_environment_feature_name,
          
          activity_feature_name,
          sleep_feature_name,
          environment_feature_name,
          
          
          language_feature_name,
          interaction_feature_name,
            ]

def get_statistics(folder_name, file_name,output=None):
    file=os.path.join(os.path.join(folder_name,file_name),"result.xlsx")
    data=pd.read_excel(file)
    data=data[data['sensitivity']!=-1]
    if output is not None:
        data=data[data['output']==output]
    sen,specificity,f1= data['sensitivity'].to_numpy(),data['specificity'].to_numpy(), data['f1_macro_avg'].to_numpy()
    return sen,specificity,f1

result=[]



Result=[]
for i in range(len(features)):
    temp=[]
    temp.append(features[i].replace(' features',''))
    for k in range(i+1):
        temp.append('N')
    for j in range(i+1,len(features)):
        sen_1,specificity_1,f1_1=get_statistics(folder_name=folder_name, file_name=features[i],output=None)
        sen_2,specificity_2,f1_2=get_statistics(folder_name=folder_name, file_name=features[j],output=None)
        
        
        U1, p = mannwhitneyu(f1_1, f1_2,alternative='greater')
        U=str(round(U1,4))
        p=str(round(p,4))
        N1=str(len(f1_1))
        N2=str(len(f1_2))
        print("mann whitney test between "+features[i].replace(' features','')+' and '+features[j].replace(' features','')+' ',end='')
        print("U= {U}, p= {p}, N1= {N1}, N2= {N2}".format(U=U,p=p,N1=N1,N2=N2))
        strings='U='+U+',\n p='+p+',\n N1='+N1+',\n N2='+N2
        temp.append(strings)
    Result.append(temp)   
    print('\n')
    
columns=['features']+[features[i].replace(' features','') for i in range(len(features))]
Result=pd.DataFrame(data=Result,columns=columns)

Result.to_excel("all emotion state"+'_feature_set_analysis.xlsx',index=False)
