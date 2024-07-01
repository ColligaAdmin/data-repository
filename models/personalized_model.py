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

from utility_functions import (
    unfold_features,
     label_dataset,
     
    read_data,
    process_features,
    
     filter_output,
     get_features,
     positive_negative_stat
    
   
    )
import argparse, os

import pandas as pd, numpy as np



from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedShuffleSplit

import warnings
warnings.filterwarnings("ignore")



def kfold_cross_val(k, data,labels, test_size):
    try:
        #Stratified sampling is used to reduce sampling erros
        sss = StratifiedShuffleSplit(n_splits=k, test_size=test_size)
        preds, truths = [], []
   
        for train_index, test_index in sss.split(data, labels):
            x_train, x_test = data[train_index], data[test_index]
            y_train, y_test = labels[train_index], labels[test_index]

            total_features=len(x_train[0])/3
            new_x_train,new_y_train=unfold_features(x_train,y_train,total_features,multifactor=3)
            new_x_test,new_y_test=unfold_features(x_test,y_test,total_features,multifactor=3)
            new_x_train,new_y_train,new_x_test,new_y_test=np.array(new_x_train),np.array(new_y_train),np.array(new_x_test),np.array(new_y_test)
            # feature preprocess
            scaler = StandardScaler()
            #normaize train dataset features
            new_x_train = scaler.fit_transform(new_x_train)
            #normalize test dataset features
            new_x_test = scaler.transform(new_x_test)
        
            model= SVC(class_weight="balanced") 
    
        
            model.fit(new_x_train, new_y_train)
        
       
            preds.extend(model.predict(new_x_test))
            truths.extend(new_y_test)
    except Exception:
        return None

    
    return classification_report(truths, preds, zero_division=0,output_dict=True)
    

def run_model(feature_person_1,feature_names,output,tolerance,dataset_directory):
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
    return [-1,-1,-1,-1,-1,-1,-1,-1,]
  
  data=get_features(data=data,tolerance=tolerance,output_data=output_data)
  
  if len(data)<2:
    print("Not enough output samples having relevant features")
    return [-1,-1,-1,-1,-1,-1,-1,-1,]
  data=label_dataset(data)
  
  
  samples, features=3*len(data), (len(data[3])-1)/3
  percentage_positive_samples=positive_negative_stat(data)
  
  result=kfold_cross_val(10, data[:,:-1], data[:,-1], test_size=0.25)
  if result is None:
      #it was not possible to build classification model due to very few samples or all samples belonging to one positive/negative class
      return [-1,-1,-1,-1,-1,features,samples,percentage_positive_samples]
  
  one='1.0'
  if one not in result:
      one='1'
  zero='0.0'
  if zero not in result:
      zero='0'
  if one not in result:
      sensitivity=-1
      f1_score_positive=-1
  else:
      sensitivity=result[one]['recall']
      f1_score_positive=result[one]['f1-score']

  if zero not in result:
      specificity=-1
  else:
      specificity=result[zero]['recall']
      
  
  f1_macro,f1_weighted=result['macro avg']['f1-score'],result['weighted avg']['f1-score']
  return [sensitivity,specificity,f1_score_positive,f1_macro,f1_weighted,features, samples, percentage_positive_samples]

	
def get_output(feature_person_1,outcome,feature_sets,dataset_directory):
    #replace fix_features_set1 with fix_features_set2 to use different feature set  
    data=read_data(os.path.join(dataset_directory,feature_person_1+'_merged.csv'))     
    feature_names=data.columns
    feature_names=[x for x in feature_names if 'survey' not in x]
    
    selected_features=[]
    if 'activity' in feature_sets or 'alls' in feature_sets:
        selected_features=selected_features+[x for x in feature_names if x in activity_features]
    if 'sleep' in feature_sets or 'alls' in feature_sets:
        selected_features=selected_features+[x for x in feature_names if x in sleep_features]
    if 'environment' in feature_sets or 'alls' in feature_sets:
        selected_features=selected_features+[x for x in feature_names if x in environment_features]
    if 'speech' in feature_sets or 'alls' in feature_sets:
        selected_features=selected_features+[x for x in feature_names if x in speech_features]
    if 'interaction' in feature_sets or 'alls' in feature_sets:
        selected_features=selected_features+[x for x in feature_names if 'time_spent_with' in x or 'time-spent-with' in x or 'proximity_to_linked' in x or 'proximity-to-linked' in x]
    if 'others' in feature_sets or 'alls' in feature_sets:
        selected_features=selected_features+[x for x in feature_names if x in other_features]
    feature_names=selected_features
    
    main_result=[]
    
    for output in outcome:
      
      
      temp_result=run_model(feature_person_1=feature_person_1,feature_names=feature_names,output=output,tolerance=30,dataset_directory=dataset_directory)
      temp_result=[feature_person_1,output]+temp_result
      main_result.append(temp_result)
     
      
    return main_result
def get_parser():
    parser = argparse.ArgumentParser(description='Provide feature_sets and dataset directory for personalized model')
    
    parser.add_argument('--feature_set', type=str,default='alls',
                    required=False)
    parser.add_argument('--dataset_directory', type=str,default=os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)),'dataset'),
                    required=False)
    args = parser.parse_args()
    return args
    
if __name__=="__main__":
    
    outcome_parent=['p_Happiness','p_Sadness','p_Anxiousness','p_Angriness','p_Stress','p_Quality_time',
             'p_Closeness','p_Positivity','p_Negativity','p_Conflict','p_Aggression']
    
    #For smoke test you can just include one care giver in the folloing a
    persons=['SBIR-004-1', 'SBIR-005-1', 'SBIR-005-2', 'SBIR-006-1', 'SBIR-007-1', 'SBIR-012-1', 'SBIR-015-1', 'SBIR-018-1', 'SBIR-023-1', 'SBIR-030-1', 'SBIR-034-1', 'SBIR-040-2', 'SBIR-047-1', 'SBIR-056-1', 'SBIR-067-1', 'STTR1-028-1', 'STTR1-031-1', 'STTR1-045-1', 'STTR1-049-1', 'STTR1-058-1', 'STTR1-069-1', 'STTR1-071-1', 'STTR1-074-1', 'STTR1-092-1', 'STTR1-095-1', 'STTR1-098-1', 'STTR1-001-1', 'STTR1-001-2', 'STTR1-002-1', 'STTR1-019-1', 'STTR1-019-2', 'STTR1-024-1', 'STTR1-036-1', 'STTR1-038-1', 'STTR1-039-1', 'STTR1-042-1']
    
    

    
    args=get_parser()
    
    main_result=[]
    feature_sets = args.feature_set
    dataset_directory=args.dataset_directory
    for person in persons:
        
        temp_result=get_output(feature_person_1= person,outcome=outcome_parent,feature_sets=feature_sets,dataset_directory=dataset_directory)
        main_result=main_result+temp_result
        
    columns=["care giver","output","sensitivity","specificity","f1_positive_class", "f1_macro_avg", "f1_weighted_avg", "#features", "#samples", "percentage of positive samples"]
    main_result=pd.DataFrame(data=main_result,columns=columns)
    main_result.to_excel('personalized_model_result.xlsx',index=False)
    
    
   
