


import pandas as pd

from sklearn.feature_selection import mutual_info_classif


import os

import warnings
warnings.filterwarnings("ignore")

def find_categorical_columns2(data):
  #data:time stamp + features
  categorical_columns=[]
  columns=data.columns
  for i in range(1,len(columns)):
    if data[columns[i]].unique().size<=3:
      categorical_columns.append(columns[i])
  return set(categorical_columns)


    





    
def get_MI(data,r_p):
    feature_names=[x for x in data.columns[:-1]]
    output_name=data.columns[-1]
    feature_data=data[feature_names]
    feature_output=data[[output_name]]
    discrete_features=[]
    categorical_columns=find_categorical_columns2(feature_data)
    for feature in feature_names:
        if feature in categorical_columns:
            discrete_features.append(True)
        else:
            discrete_features.append(False)
    i=0
    mutual_info=[]
    for feature in feature_names:
        mutual_info.append(mutual_info_classif(X=feature_data[feature].to_numpy().reshape(-1,1), y=feature_output[output_name].to_numpy(), discrete_features=[discrete_features[i]])[0])
        i+=1
    
    mutual_info = pd.Series(mutual_info)
    mutual_info.index = feature_data.columns
    mutual_info=mutual_info.sort_values(ascending=False)
    top_2_columns=[x for x in mutual_info.index[:2]]
    r_p[output_name]={}
    i=0
    for feature in mutual_info.index:
        r_p[output_name][feature]=mutual_info[i]
        i+=1
    return top_2_columns,r_p, mutual_info
def create_MI_directory():
    if not os.path.exists('MI'):
        # Create the directory
        os.makedirs('MI')
if __name__=="__main__":
    create_MI_directory()
    
    outcome_parent=['p_Happiness','p_Sadness','p_Anxiousness','p_Angriness','p_Stress','p_Quality_time',
         'p_Closeness','p_Positivity','p_Negativity','p_Conflict','p_Aggression']
   
    #For smoke test you can just include one care giver in the folloing a
    persons=['SBIR-004-1', 'SBIR-005-1', 'SBIR-005-2', 'SBIR-006-1', 'SBIR-007-1', 'SBIR-012-1', 'SBIR-015-1', 'SBIR-018-1', 'SBIR-023-1', 'SBIR-030-1', 'SBIR-034-1', 'SBIR-040-2', 'SBIR-047-1', 'SBIR-056-1', 'SBIR-067-1', 'STTR1-028-1', 'STTR1-031-1', 'STTR1-045-1', 'STTR1-049-1', 'STTR1-058-1', 'STTR1-069-1', 'STTR1-071-1', 'STTR1-074-1', 'STTR1-092-1', 'STTR1-095-1', 'STTR1-098-1', 'STTR1-001-1', 'STTR1-001-2', 'STTR1-002-1', 'STTR1-019-1', 'STTR1-019-2', 'STTR1-024-1', 'STTR1-036-1', 'STTR1-038-1', 'STTR1-039-1', 'STTR1-042-1']
    
    for person in persons:
        r_p={}
        selected_columns=set()
        should_go=1
        for outcome in outcome_parent:
            try:
                data=pd.read_excel("Features_for_Generalized_Models//"+outcome.replace('p_','')+"//"+person+'_'+outcome.replace('p_','')+'.xlsx')
           
                top_2_columns,r_p,mutual_info=get_MI(data,r_p)
                selected_columns=selected_columns.union(top_2_columns)
                
            except:
                should_go=0
                break
            
        if should_go==0:
            continue
        selected_columns=list(selected_columns)
        Result=[]
        for output in r_p.keys():
            temp_array=[output]
            
            temp_array=[output]+[r_p[output][feature] for feature in selected_columns]
            Result.append(temp_array)
        Result=pd.DataFrame(data=Result, columns=['emotion_state']+selected_columns)
        Result.to_excel("MI//"+person+"Mutual_information_gain_table.xlsx",index=False)
    
    
      
    
   
