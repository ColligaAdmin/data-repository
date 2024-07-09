<div align="center">

# Developing Personalized Algorithms for Sensing Mental Health Symptoms in Daily Life

Source files repository, please clone to access processed data and run modeling scripts.

Accession number: 5819360343

</div>

### Installation

We recommend using a conda environment with ``Python >= 3.9``. Go [here](https://docs.conda.io/en/latest/miniconda.html) and download the installer that matches your system. Follow the installation instructions. Afterwards you will be able to run the following commands:
```
conda create -n mhealth python=3.9
conda activate mhealth
```

Follow the instructions of the `docs/Github_Authentication.pdf` file to establish git. Clone the repository:
```
git clone https://github.com/ColligaAdmin/data-repository
cd data-repository && pip install -r requirements.txt
```

### Project Structure

Cleaning scripts, shared at `data_cleaning` read the raw CSV files (not shared) and their final output is the merged files in the `dataset` folder for each participant separately. To run the models described in the paper, follow the following procedures

### Run Personalized Model
First go to the models directory with the following script
```
cd models
python personalized_model.py --feature_set your_feature_sets --dataset_directory your_dataset_directory
```
Here, you need to include which feature sets you want to use. You can use any of the following five feature sets: ```activity, sleep, speech, interaction, environment```.
Or, you can also combine any feature sets. For example, if you want to include activity, sleep, and environment features in your personalized models, you can run the following script
```
python personalized_model.py --feature_set activity_sleep_environment
```
By default, it will choose all features if you do not specify ```--feature_set``` in your script. ```--dataset_directory``` will be the location of your dataset. By default,  the ```--dataset_directory``` will be set as the directory of the dataset in this github repository if you do not specify the ```--dataset_directory``` in your script.

### Run Generalized Model
There are two steps to run generalized models:
#### Step 1: Get Features for Generalized Model
```
cd models
python process_features_for_generalized_models.py --dataset_directory your_dataset_directory
```
This code will generate one file for each outcome and each caregiver as ```caregiver_id_outcome.xlsx``` inside the ```models``` directory. ```--dataset_directory``` will be the directory where you stored of your dataset. By default,  the ```--dataset_directory``` will be set as the directory of the dataset in this github repository.
#### Step 2: Run Generalized Model
```
cd models
python generalized_model.py --feature_directory your_feature_directory
```
```--feature_directory``` should include all your processed features from ```step 1```. For your convenience, we have included the processed features in the directory named ```models//Features_for_Generalized_Models``` and this code will select this directory by default if you do not specify the ```--feature_directory``` in your script

### Reproduce Table 3 Results in the Paper:
To regenerate the one-sample Wilcoxon Signed Rank results to compare the performance of Personalized and Generalized model performance and get the average Personalized and Generalized model results, run the following script
```
cd models
python compare_generalized_vs_personalized_model.py
```
### Reproduce Table 4 Results in the Paper:
To regenerate the better than chance statistics based on one-sample Wilcoxon Signed Rank test for both Personalized and Generalized models, run the following script
```
cd models
python better_than_chance.py
```
### Reproduce Table 7 Results in the Paper:
To regenerate the one-tailed Mann-Whitney test to compare the performance across different feature sets, run the following script
```
cd models
python different_feature_set_performance.py
```
This code will generate Mann-Whitney results reported in Table 7 in the paper and save these results in an xl file named ```all emotion state_feature_set_analysis.xlsx``` under the ```models``` directory.

### Reproduce Table 8 Results in the Paper:
To reproduce average mutual information gains between the top 10 features and each emotion state as reported in table 8, you need to follow 2 steps
#### Step 1: Generate Mutual Information Gains for Individual Caregiver:
First, you need to follow the step 1 procedure ```( Get features for generalized model)``` as noted in ```Run Generalized Model``` to get the processed features for all caregivers. We have saved these processed features in ```models/Features_for_Generalized_Models```. You have to run the following script
```
cd models
python get_individual_mutual_information_gain.py
```
This will create the ```models/MI directory``` and save the mutual information gain information between each feature and each emotion state for each caregiver in separate excel files. There will be one excel file created per caregiver as ```models//MI//caregiver_idMutual_information_gain_table.xlsx```  
#### Step 2: Generate Average Mutual Information Gains Across All Caregivers:
```
cd models
python get_avg_mutual_information_gain.py
```
This code will print the top 10 features and also the average mutual information gain between each outcome and each feature for top 10 features as reported in Table 8 in the paper.

### Citation
[Authors masked for review], [Project masked for review]. 2024: [Website masked for Review].
