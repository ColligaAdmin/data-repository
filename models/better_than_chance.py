from scipy.stats import wilcoxon
import pandas as pd


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
  
print('\n\n\n............Personalized models............\n\n\n')
for performance_metric in metrics:
    for outcome in outcomes:
        print("{outcome} {metric}".format(outcome=outcome.replace('p_',''),metric=performance_metric))
        
        metric_personalized_model=get_statistics(file_name=file_personalized_model, performance_metric=performance_metric,output=outcome)
        
        try:
            w=wilcoxon(x=metric_personalized_model-0.5,alternative='greater')
            
            print("Z={z}, p={p}, N={n}".format(z=w.statistic,p=w.pvalue,n=len(metric_personalized_model)))
            
        except:
            print("Exception found for personalized model for {outcome} {metric}".format(outcome=outcome.replace('p_',''),metric=performance_metric))
    print('\n\n\n')
    
print('\n\n\n............Generalized models............\n\n\n')
for performance_metric in metrics:
    for outcome in outcomes:
        print("{outcome} {metric}".format(outcome=outcome.replace('p_',''),metric=performance_metric))
        
        metric_generalized_model=get_statistics(file_name=file_generalized_model, performance_metric=performance_metric,output=outcome.replace('p_',''))
        
        try:
            w=wilcoxon(x=metric_generalized_model-0.5,alternative='greater')
            
            print("Z={z}, p={p}, N={n}".format(z=w.statistic,p=w.pvalue,n=len(metric_generalized_model)))
            
        except:
            print("Exception found for Generalized model for {outcome} {metric}".format(outcome=outcome.replace('p_',''),metric=performance_metric))
    print('\n\n\n')

print("\n\n\n ................For all emotion states Personalized models................\n\n\n")

for performance_metric in metrics:
    
    print("All emotion state {metric}".format(metric=performance_metric))
    
    metric_personalized_model=get_statistics(file_name=file_personalized_model, performance_metric=performance_metric,output=None)
    
    try:
        w=wilcoxon(x=metric_personalized_model-0.5,alternative='greater')
        
        print("Z={z}, p={p}, N={n}".format(z=w.statistic,p=w.pvalue,n=len(metric_personalized_model)))
        
    except:
        print("Exception found for personalized model for all emotion states {metric}".format(metric=performance_metric))
    print('\n\n\n')
    
print("\n\n\n ................For all emotion states Generalized models................\n\n\n")
for performance_metric in metrics:
    
    print("All emotion state {metric}".format(metric=performance_metric))
    
    metric_generalized_model=get_statistics(file_name=file_generalized_model, performance_metric=performance_metric,output=None)
    
    try:
        w=wilcoxon(x=metric_generalized_model-0.5,alternative='greater')
        
        print("Z={z}, p={p}, N={n}".format(z=w.statistic,p=w.pvalue,n=len(metric_generalized_model)))
        
    except:
        print("Exception found for Generalized model for all emotion states {metric}".format(metric=performance_metric))
    print('\n\n\n')
