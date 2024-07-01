from scipy.stats import wilcoxon
import pandas as pd, os, numpy as np
from scipy import stats
from scipy.stats import kstest
import scipy.stats as st 
from statistics import mean, stdev
import matplotlib.pyplot as plt
from scipy.stats import shapiro
from scipy.stats import mannwhitneyu
def get_statistics( file_name,performance_metric,output=None):
    data=pd.read_excel(file_name)
    data=data[data[performance_metric]!=-1]
    if output is not None:
        data=data[data['output']==output]
    return data[performance_metric].to_numpy()

metrics=['sensitivity','specificity','f1_macro_avg']
outcomes=['p_Happiness','p_Sadness','p_Anxiousness','p_Angriness','p_Stress','p_Quality_time',
             'p_Closeness','p_Positivity','p_Negativity','p_Conflict','p_Aggression']
file_personalized_model='all_feature_personalized_model_result.xlsx'  
file_generalized_model='all_feature_generalized_model_result.xlsx'
  

for performance_metric in metrics:
    for outcome in outcomes:
        print("{outcome} {metric}".format(outcome=outcome.replace('p_',''),metric=performance_metric))
        
        metric_personalized_model=get_statistics(file_name=file_personalized_model, performance_metric=performance_metric,output=outcome)
        metric_generalized_model=get_statistics(file_name=file_generalized_model, performance_metric=performance_metric,output=outcome.replace('p_',''))
        print("avg(P)={p}, avg(G)={g}".format(p=np.average(metric_personalized_model),g=np.average(metric_generalized_model)))
        try:
            w=wilcoxon(x=metric_personalized_model-np.median(metric_generalized_model),alternative='greater')
            
            print("Z={z}, p={p}, Np={n}".format(z=w.statistic,p=w.pvalue,n=len(metric_personalized_model)))
            
        except:
            print("Exception found for {outcome} {metric}".format(outcome=outcome.replace('p_',''),metric=performance_metric))
    print('\n\n\n')
print("\n\n\n ................For all emotion states................\n\n\n")
for performance_metric in metrics:
    
    print("All emotion states {metric}".format(metric=performance_metric))
    
    metric_personalized_model=get_statistics(file_name=file_personalized_model, performance_metric=performance_metric,output=None)
    metric_generalized_model=get_statistics(file_name=file_generalized_model, performance_metric=performance_metric,output=None)
    print("avg(P)={p}, avg(G)={g}".format(p=np.average(metric_personalized_model),g=np.average(metric_generalized_model)))
    try:
        w=wilcoxon(x=metric_personalized_model-np.median(metric_generalized_model),alternative='greater')
        
        print("Z={z}, p={p}, Np={n}".format(z=w.statistic,p=w.pvalue,n=len(metric_personalized_model)))
        
    except:
        print("Exception found for All emotion states {metric}".format(metric=performance_metric))
    print('\n\n\n')

