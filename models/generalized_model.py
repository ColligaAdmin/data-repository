
import pandas as pd, os
import argparse
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
#Put different feature names with the same feature to the same key in the following dictionary
to_common_map={
    'calendar_event_frequency_num_events':'calendar_freq',
    'calendar-event-frequency_num_events':'calendar_freq',
    
    'call-frequency-android-only_Value':'call_freq',
    'call_frequency_android_only_Value':'call_freq',
    
    'sms_frequency_android_only_Value':'sms_freq',
    'sms-frequency-android-only_Value':'sms_freq',
    
    'fitbit_sleep_deep_sleep':'deep_sleep',
    'sleep_deepSleep':'deep_sleep',
    'fitbit_sleep_deepSleep':'deep_sleep',
    
    'fitbit_sleep_lightSleep':'light_sleep',
    'sleep_lightSleep':'light_sleep',
    'fitbit_sleep_light_sleep':'light_sleep',
    
    'sleep_totalMinutesInBed':'total_minutes_in_bed',
    'fitbit_sleep_totalMinutesInBed':'total_minutes_in_bed',
        
   
        
    'sleep_totalMinutesAsleep':'total_minutes_asleep',
    'fitbit_sleep_totalMinutesAsleep':'total_minutes_asleep',
        
   
        
    'fitbit_sleep_efficiency': 'sleep_efficiency',
    'sleep_efficiency':'sleep_efficiency',
    
    'sleep_rem':'sleep_rem',
    'fitbit_sleep_REM':'sleep_rem',
    
    'sleep_mainSleep':'main_sleep',
    'fitbit_sleep_mainSleep': 'main_sleep',
    
    'fitbit_sleep_numAwakenings': 'number_awakenings',
    'sleep_numAwakenings': 'number_awakenings',
    
    
    
    'activity_very_active_minutes':'very_active',
    'fitbit_activity_Very Active Minutes':'very_active',
    
    'fitbit_activity_Fairly Active Minutes':'fairly_active',
    'activity_moderately_active_minutes':'fairly_active',
    
    'activity_sedentary_minutes':'sedentary_active',
    'fitbit_activity_Sedentary Minutes':'sedentary_active',
    
    'activity_lightly_active_minutes':'lightly_active',
    'fitbit_activity_Lightly Active Minutes':'lightly_active',
    
    'fitbit_heart_rate_Value (BPM)':'heart_rate',
    'heart_rate_BPM':'heart_rate',
    'healthkit_heart_Value (BPM)':'heart_rate',
    
    
    'step_count_Value':'step_count',
    'step_Steps':'step_count',
    
    'distance_Value':'distance',
    'distance_Distance':'distance',
    
    'ambient-noise_Value':'ambient_noise',
    'ambient-noise_Value (db)':'ambient_noise_db',
    'ambient_noise_Value (db)':'ambient_noise_db',
    
    'ambient-light_Value':'ambient_light',
    'ambient_light_Value (lux)':'ambient_light_lx',
    'ambient-light_Value (lux)':'ambient_light_lx',
    
    'barometer_Value':'atmospheric_pressure',
    'barometer_Value (mbar)':'atmospheric_pressure',
    
    'time-spent-at-linked-location_Home':'time_spent_at_home',
    'time_spent_at_linked_location_Home':'time_spent_at_home',
    
    
    'time_spent_at_linked_location_School':'time_spent_at_school',
    'time-spent-at-linked-location_School':'time_spent_at_school',
    
    
    'time_spent_at_linked_location_Work':'time_spent_at_work',
    'time-spent-at-linked-location_Work':'time_spent_at_work',
    
    
    'proximity_to_set_location_Home':'proximity_to_home',
    'proximity-to-set-location_Home':'proximity_to_home',
    
    
    'proximity-to-set-location_School':'proximity_to_school',
    'proximity_to_set_location_School':'proximity_to_school',
    
    
     'proximity-to-set-location_Work':'proximity_to_work',
     'proximity_to_set_location_Work':'proximity_to_work',
     
    
    
    
    }

def rename_columns(columnnames):
    mapping={}
    for i in range(len(columnnames)):
        if columnnames[i] in to_common_map:
            mapping[columnnames[i]]=to_common_map[columnnames[i]]
        
        if 'time_spent_with' in columnnames[i] or 'time-spent-with' in columnnames[i]:
            if '-3' in columnnames[i]:
               mapping[columnnames[i]]='time_spent_with_child'
            elif '-2' in columnnames[i]:
                mapping[columnnames[i]]='time_spent_with_partner'
         
        
        if 'proximity-to-linked-people_' in columnnames[i] or 'proximity_to_linked_people_' in columnnames[i]:
            if '-3' in columnnames[i]:
                mapping[columnnames[i]]='proximity_to_child'
            elif '-2' in columnnames[i]:
                mapping[columnnames[i]]='proximity_to_partner'
    return mapping

#Remove proximity or time spent with one's ownself
def remove_column(data):
    for column in data.columns:
        if 'proximity-to-linked-people_' in column or 'proximity_to_linked_people_' in column:
            if '-1' in column:
                
                data = data.drop([column], axis=1)
                
        if 'time_spent_with' in column or 'time-spent-with' in column:
            if '-1' in column:
                 data = data.drop([column], axis=1)
    return data
def fetch_files(outcome,outcome_directory):
    res = []
    for path in os.listdir(outcome_directory):
            # check if current path is a file
        if os.path.isfile(os.path.join(outcome_directory, path)):
            res.append(os.path.join(outcome_directory, path))
            
    files,names=[],[]
    for i in range(len(res)):
        name=res[i]
        name=name.split('\\')[-1]
        name=name.replace('_'+outcome+'.xlsx','')
        files.append(res[i])
        names.append(name)
    return files,names

def fix_column_names(data):
    column_mapping=rename_columns(data.columns)
    data = data.rename(columns=column_mapping)
    data=remove_column(data)
    return data
    
def get_global_model_results(feature_directory,outcomes):       
    Main_result=[]
    for outcome in outcomes:
       
        
        outcome_directory=os.path.join(feature_directory,outcome)
        # Iterate directory
        files,names=fetch_files(outcome,outcome_directory)
        
        
        i=-1
        
    
        for evaluation_file in files:
            i+=1
            evaluation_data=pd.read_excel(evaluation_file)
            evaluation_data=fix_column_names(evaluation_data)
            #Get all of the available features for the evaluation data
            evaluation_columns=set(evaluation_data.columns)
            training_data=pd.DataFrame(data=(),columns=evaluation_data.columns)
            #Get all training data one by one for the evaluation data
            for file in files:
                # do not include evaluation data in training data 
                if file==evaluation_file:
                    continue
        
                data=pd.read_excel(file)
               
                data = fix_column_names(data)
                #All features of current training data
                current_file_columns=set(data.columns)
                #Check if the feature set of evaluation data is a sub set of the features of training data
                if evaluation_columns.issubset(current_file_columns):
                    #Include only common features in training data
                    data=data[list(evaluation_columns)]
                    
                    #Include the samples in the trainining data
                    training_data=pd.concat([training_data,data],ignore_index=True).reset_index(drop=True)
            #we did not find any training data having common features with this evaluation data
            if len(training_data)==0:
                Main_result.append([names[i],outcome,-1,-1,-1,-1,-1,-1])
                continue
            #Common features between train and eval set
            feature_names=[x for x in evaluation_columns if x!=outcome]
            #Include only common features for model
            x_train=training_data[feature_names].to_numpy()
            x_test=evaluation_data[feature_names].to_numpy()
            y_train=training_data[outcome].to_numpy().astype(int)
            y_test=evaluation_data[outcome].to_numpy().astype(int)
            
            #normalize features
            scaler = StandardScaler()
            x_train = scaler.fit_transform(x_train)
            x_test = scaler.transform(x_test)
        
        
            model= SVC(class_weight="balanced") 
            try:
                
                model.fit(x_train, y_train)
                preds=model.predict(x_test)
        
                result=classification_report(y_test, preds, zero_division=0,output_dict=True)
                if result is None:
                    Main_result.append([names[i],outcome,-1,-1,-1,-1,-1,-1])
                
                one='1.0'
                if one not in result:
                    one='1'
                zero='0.0'
                if zero not in result:
                    zero='0'
                if one not in result:
                    sensitivity=-1.0
                    f1_score_positive=-1.0
                else:
                    sensitivity=result[one]['recall']
                    f1_score_positive=result[one]['f1-score']
                    
                if zero not in result:
                    specificity=-1
                else:
                    specificity=result[zero]['recall']
                
                
                f1_macro,f1_weighted=result['macro avg']['f1-score'],result['weighted avg']['f1-score']
                Main_result.append([names[i],outcome,sensitivity, specificity, f1_score_positive, f1_macro, f1_weighted, len(training_data)])
            except Exception:
                print('exception found for '+names[i]+ '\t'+outcome)
                
    return Main_result
def get_parser():
    parser = argparse.ArgumentParser(description='Provide dataset directory for generalized models')

    parser.add_argument('--feature_directory', type=str,default="Features_for_Generalized_Models",
                    required=False)
    args = parser.parse_args()
    return args
if __name__=="__main__":
    outcomes=['Happiness','Sadness','Anxiousness','Angriness','Stress','Quality_time',
             'Closeness','Positivity','Negativity','Conflict','Aggression']      
    columns=["care giver","output","sensitivity","specificity","f1_positive_class", "f1_macro_avg", "f1_weighted_avg", "#samples in training data"]
    args=get_parser()
    feature_directory=args.feature_directory
    Main_result=get_global_model_results(feature_directory,outcomes)
    Main_result=pd.DataFrame(data=Main_result,columns=columns)
    Main_result.to_excel("generalized_model_results.xlsx",index=False)

