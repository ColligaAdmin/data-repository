

import  os
from utility_functions import (
    unfold_features,
     label_dataset,
    
    read_data,
    process_features,
     
     filter_output,
     get_features,
   
    )
from utility import (
    output_map_new,
    output_map_old,
    mapping_of_new_old_families, 
   
    environment_features,
    activity_features,
    sleep_features,
    other_features,
     speech_features, 
    
    )

import argparse
import pandas as pd


import warnings
warnings.filterwarnings("ignore")




def get_final_features( data,labels, feature_names,output_name):
    

    total_features=len(data[0])/3
    x,y=unfold_features(data,labels,total_features,multifactor=3)
    data=pd.DataFrame(data=x,columns=feature_names)
    data[output_name]=y
   
    return data
    

def get_features_for_model(feature_person_1,feature_names,output,tolerance,dataset_directory):
  
  data=read_data(os.path.join(dataset_directory,feature_person_1+'_merged.csv'))
  
  
  data=process_features(data=data,feature_names=feature_names)
  feature_names=data.columns
 
 
  
  output_data=read_data(os.path.join(dataset_directory,feature_person_1+'_merged.csv'))
  if mapping_of_new_old_families[feature_person_1]==0:
      output_map=output_map_old
  else:
      output_map=output_map_new
  output_data=filter_output(output_data,output,output_map)
  if len(output_data)<=2:
    print("Not enough output samples")
    return None
  
  data=get_features(data=data,tolerance=tolerance,output_data=output_data)
  
  if len(data)<=2:
    print("Not enough output samples having relevant features")
    return None
  data=label_dataset(data)
  data=get_final_features(data=data[:,:-1], labels=data[:,-1], feature_names=feature_names[1:], output_name=output.replace('p_',''))
  
  return data

	
def get_processed_features(feature_person_1,outcome,dataset_directory):
    
    data=read_data(os.path.join(dataset_directory,feature_person_1+'_merged.csv'))

    feature_names=data.columns
    feature_names=[x for x in feature_names if 'survey' not in x]
    #Include all relevant features
    feature_names=[x for x in feature_names if x in activity_features or x in sleep_features or x in environment_features or x in speech_features or x in other_features or 'time_spent_with' in x or 'time-spent-with' in x or 'proximity_to_linked' in x or 'proximity-to-linked' in x]
    data=get_features_for_model(feature_person_1=feature_person_1,feature_names=feature_names,output=outcome,tolerance=30,dataset_directory=dataset_directory)
      
    return data

def get_parser():
    parser = argparse.ArgumentParser(description='Provide dataset directory for generalized models')

    parser.add_argument('--dataset_directory', type=str,default=os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)),'dataset'),
                    required=False)
    args = parser.parse_args()
    return args

if __name__=="__main__":
    
    outcome_parent=['p_Happiness','p_Sadness','p_Anxiousness','p_Angriness','p_Stress','p_Quality_time',
         'p_Closeness','p_Positivity','p_Negativity','p_Conflict','p_Aggression']
    
    #For smoke test, you can just include one caregiver in the following list
    persons=['SBIR-004-1', 'SBIR-005-1', 'SBIR-005-2', 'SBIR-006-1', 'SBIR-007-1', 'SBIR-012-1', 'SBIR-015-1', 'SBIR-018-1', 'SBIR-023-1', 'SBIR-030-1', 'SBIR-034-1', 'SBIR-040-2', 'SBIR-047-1', 'SBIR-056-1', 'SBIR-067-1', 'STTR1-028-1', 'STTR1-031-1', 'STTR1-045-1', 'STTR1-049-1', 'STTR1-058-1', 'STTR1-069-1', 'STTR1-071-1', 'STTR1-074-1', 'STTR1-092-1', 'STTR1-095-1', 'STTR1-098-1', 'STTR1-001-1', 'STTR1-001-2', 'STTR1-002-1', 'STTR1-019-1', 'STTR1-019-2', 'STTR1-024-1', 'STTR1-036-1', 'STTR1-038-1', 'STTR1-039-1', 'STTR1-042-1']
    
    args=get_parser()
    
    
    
    dataset_directory=args.dataset_directory
    for person in persons:
        for outcome in outcome_parent:
            try:
                data=get_processed_features(feature_person_1= person,outcome=outcome,dataset_directory=dataset_directory)
       
                data.to_excel(person+'_'+outcome.replace('p_','')+'.xlsx',index=False)
            except Exception:
                print("Exception for "+person+outcome)
        
   
   
    
    
    
      
    
   
