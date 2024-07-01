import pandas as pd, os

path = ...
clean_path = path.replace("STTRp", "STTR_clean")
os.makedirs(clean_path, exist_ok=True)
os.system(f"find {path} -name '.DS_Store' -delete")

surveys = {}
for family in os.listdir(path):
    # initialize columns
    eg_survey = "/".join(
        [f"{path[:-1]}-old", "SAMPLE_SUBJECT", "Week 1", "daily-survey.csv"]
    )
    surveys[family] = pd.DataFrame(columns=pd.read_csv(eg_survey).columns)
    os.makedirs(os.path.join(clean_path, family), exist_ok=True)

for family in os.listdir(path):
    for week in os.listdir(path + family):

        wpath = os.path.join(path, family, week)
        for f in os.listdir(wpath):
            if "survey" not in f:
                continue

            data = pd.read_csv(os.path.join(wpath, f))
            for row in data.values:
                fam = row[0][:-2]
                if "STTR1" not in fam:
                    continue
                try:
                    surveys[fam].loc[len(surveys[fam])] = row
                except:
                    surveys[family] = pd.DataFrame(columns=data.columns)
                    surveys[fam].loc[len(surveys[fam])] = row

for family in surveys:
    # convert to timestamp and sort chronologically
    surveys[family]["Time Stamp"] = pd.to_datetime(surveys[family]["Time Stamp"])
    surveys[family] = surveys[family].sort_values(by=["Time Stamp"])

    # drop duplicates and restart index
    surveys[family] = surveys[family].drop_duplicates(ignore_index=True)
    # convert 'object' column types to float
    for col in surveys[family]:
        if col not in ["Participant Name", "Time Stamp"]:
            surveys[family][col] = pd.to_numeric(surveys[family][col], errors="ignore")

for family in surveys:
    # Separate family members
    data = surveys[family].groupby("Participant Name")
    members = list(data.groups.keys())
    for person in members:
        pdata = data.get_group(person)
        pdata = pdata.drop(columns=["Participant Name"])
        pdata = pdata.reset_index(drop=True).set_index("Time Stamp")

        # save the clean survey in csv format
        person_path = os.path.join(clean_path, family, person)
        os.makedirs(person_path, exist_ok=True)
        pdata.to_csv(person_path + f"/{person}_surveys.csv")

print("\nDone for all families!")
