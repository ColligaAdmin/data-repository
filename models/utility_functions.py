import numpy as np, pandas as pd, math
from datetime import timedelta


def unfold_features(x,y,total_features,multifactor=3):
  x_new,y_new=[],[]
  for i in range(len(y)):
    for j in range(multifactor):
      y_new.append(y[i])
      x_new.append(x[i][int(j*total_features):int((j+1)*total_features)])
  return x_new,y_new

def label_dataset(Result):
    proportion_of_samples_median_strategy_1,Result_median_strategy_1=binarization(Result=Result,strategy=1)
    proportion_of_samples_median_std_strategy_2,Result_median_std_strategy_2=binarization(Result=Result,strategy=2)
    proportion_of_samples_median_std_strategy_3,Result_median_std_strategy_3=binarization(Result=Result,strategy=3)

    if proportion_of_samples_median_strategy_1 <= proportion_of_samples_median_std_strategy_2 and proportion_of_samples_median_strategy_1 <= proportion_of_samples_median_std_strategy_3:
        print('used median for binarization')
        return Result_median_strategy_1
    elif proportion_of_samples_median_std_strategy_2 <= proportion_of_samples_median_strategy_1 and proportion_of_samples_median_std_strategy_2 <= proportion_of_samples_median_std_strategy_3:
        print('used median - std for binarization')
        return Result_median_std_strategy_2
    else: 
        print('used median + std for binarization')
        return Result_median_std_strategy_3
    
def read_data(file):
    
    data=pd.read_csv(file)
    #conversion of date-time
    data.loc[:,'Time Stamp'] = pd.to_datetime(data['Time Stamp']) 
    return data

def process_features(data,
                 feature_names):
    
   
    #Resulting columns: Time Stamp, all  Features
    selected_columns=['Time Stamp']+feature_names
    
    data=data[selected_columns]
    

    #drop empty columns
    data.dropna(axis=1,how='all',inplace=True)
    columns=data.columns
    
    categorical_columns=find_categorical_columns(data)
    
    #Add forward and backward interpolation for all the columns except the timestamp
    
    for i in range(1,len(columns)):
         data.loc[:,columns[i]].interpolate(method='linear',limit_direction='both',inplace=True)
    
    
    #any empty feature values filled with nearest values 
    
    data.fillna(method='ffill',inplace=True)
   
    data.fillna(method='bfill',inplace=True)
    #Fix the data type
    for i in range(1,len(columns)):
        if columns[i] not in categorical_columns:
            data.loc[:,columns[i]] = data.loc[:,columns[i]].astype('float64')
        else:
            data.loc[:,columns[i]] = data.loc[:,columns[i]].astype('category')
    
    
    return data

def filter_output(output_data,output,output_map,count_thresold=3):
   output_column=output_map[output]
   output_data=output_data[['Time Stamp',output_column]]
   #Only keep the rows with emotion output
   output_data=output_data[~pd.isnull(output_data[output_column])]
   if len(output_data)==0:
       return output_data
   prev_survey_time=output_data.iloc[0,0]
   filtered_survey_data=[[output_data.iloc[0,0],output_data.iloc[0,1]]]
   for i in range(1, len(output_data)):
      next_survey_time=output_data.iloc[i,0]
      time_diff=(next_survey_time-prev_survey_time).total_seconds()/3600
      #only consider surveys that are atleast 2 hours apart
      if time_diff<2.0:
          continue
      filtered_survey_data.append([output_data.iloc[i,0], output_data.iloc[i, 1]])
      prev_survey_time=next_survey_time
   filtered_survey_data=pd.DataFrame(data=filtered_survey_data,columns=['Time Stamp',output_column])
   return filtered_survey_data


def get_features(data,tolerance,output_data):
    #data contains features and output_data contains time stamp and outcomes
    Result=[]
    #Iterate through all the survey points
    for i in range(len(output_data)):
        
        feature1,feature2,feature3,end_index=extract_feature(tolerance=tolerance,data=data,survey_time=output_data.iloc[i][0])
        feature1,is_null1=extract_feature_for_model(feature1)
        feature2,is_null2=extract_feature_for_model(feature2)
        feature3,is_null3=extract_feature_for_model(feature3)
        #Got valid features 
        if is_null1==False and is_null2==False and is_null3==False:
              Result.append(feature1+feature2+feature3+list([output_data.iloc[i][1]]))
              
        
        if end_index>=len(data):
            # Reached end of file
            break
   
    Result=np.array(Result)
    
    return Result

def find_categorical_columns(data):
  #data:time stamp + features
  categorical_columns=[]
  columns=data.columns
  for i in range(1,len(columns)):
    #any feature having less than or equal to 5 unique values are counted as categorical feature
    if data[columns[i]].unique().size<=5:
      categorical_columns.append(columns[i])
  return set(categorical_columns)


def extract_feature(tolerance,data,survey_time):
  feature1,feature2,feature3=[],[],[]
  survey_time=pd.to_datetime(survey_time)
  delta = timedelta(minutes=tolerance)
 
  #To increase sample converage, use three different time ranges
  between1 = lambda x, y: (x >= y -  2*delta) and (x < y -delta )
  between2 = lambda x, y: (x >= y - delta) and (x < y + delta )
  between3 = lambda x, y: (x >= y + delta) and (x < y + 2*delta)
  for i in range(len(data)):
    #Extract time of feature point
    time=pd.to_datetime(data.iloc[i][0])
    
    if between1(time,survey_time):
        
        feature1.append(list(data.iloc[i][1:].to_numpy()))
    elif between2(time,survey_time):
        
        feature2.append(list(data.iloc[i][1:].to_numpy()))
    elif between3(time,survey_time):
        
        feature3.append(list(data.iloc[i][1:].to_numpy()))
    elif time>= survey_time+2*delta:
        return list(feature1),list(feature2),list(feature3),i+1

  return list(feature1),list(feature2),list(feature3),len(data)+1

def binarization(Result,strategy=1):
    Result=Result.copy()
    #Get mean and std of the outcomes
    median,standard_deviation=np.median(Result[:,-1]),np.std(Result[:,-1])
    neg,pos=0.0,0.0
    if strategy==1:
      thresold=median
    elif strategy==2:
      thresold=median-standard_deviation
    else:
      thresold=median+standard_deviation

    for i in range(len(Result)):
      #binarize the outcomes
      if Result[i][-1]<=thresold:
          Result[i][-1]='0'
          neg=neg+1
      else:
          Result[i][-1]='1'
          pos=pos+1
    if pos==0 or neg==0:
      #All samples have same label not possible to build model
      return 100000000, Result
    #Return the ratio of pos/neg samples
    return abs((max(pos,neg)/min(pos,neg))), Result

def extract_feature_for_model(feature):
  #Return average feature and False if there is no empty feature array otherwise return [] and True

  if len(feature)==0:
    #No available features
    return [],True
  feature=np.array(feature)
  #Take the mean of each feature across the time window
  column_wise_avg=feature.mean(axis=0)
  column_wise_avg=list(column_wise_avg)
  
  for feature_index in range(len(column_wise_avg)):
    #If any particular feature is empty, return []
    if(math.isnan(column_wise_avg[feature_index])):
        return [],True
  #Return aggregated feature means
  return column_wise_avg,False

def find_categorical_column_indices(data,labels):
  
  total_features=len(data[0])/3
  new_data,new_labels=unfold_features(data,labels,total_features,multifactor=3)
  new_data=np.array(new_data)
  categorical_columns=[]
  for i in range(new_data.shape[1]):
    if len(np.unique(new_data[:,i]))<=5:
      categorical_columns.append(i)
  return categorical_columns

def filter_features(data,feature_names):
  #exclude features that the users mention but missing in the data
  feature_names_filtered=[]
  feature_set=set(data.columns)
  for feature in feature_names:
    if feature in feature_set:
      feature_names_filtered.append(feature)
  feature_names=feature_names_filtered
  return feature_names


def positive_negative_stat(data):
    outcome=data[:,-1]
    pos=0
    for yy in outcome:
        if yy==1:
            pos+=1
    
    return (pos/len(outcome))*100