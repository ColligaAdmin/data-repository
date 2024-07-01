import os, numpy as np
import re, pandas as pd


class Family_Data:
    def __init__(self, family_path):
        super().__init__()
        self.family_path = family_path
        self.datatypes = {}

    def differentiate(self, array):
        return np.concatenate(
            (
                [0],
                [max(0, array[i] - array[i - 1]) for i in range(1, len(array))],
            )
        )

    def make_datetime(self, date, time):
        date = date.split("-")
        time = time.split(":")
        temp = pd.DataFrame(
            {
                "year": [date[0]],
                "month": [date[1]],
                "day": [date[2]],
                "hour": [time[0]],
                "minute": [time[1]],
            }
        )
        return pd.to_datetime(temp)[0]

    def get_data(self, week, datatype):
        def looks_like(datatype, i):
            pattern = re.compile(r"(?<!^)(?=[A-Z])")
            camel = datatype in pattern.sub("_", i).lower()
            snake = datatype in i.replace("-", "_")
            return camel or snake

        # availability check
        assert datatype in self.datatypes, "Invalid datatype."
        self.datasets = {}

        datatypes_here = os.listdir(self.family_path + f"/{week}")
        found = [dt for dt in datatypes_here if looks_like(datatype, dt)]
        if not found:
            print(f"{week}: Does not have {datatype}")
        else:
            self.load(self.family_path + f"/{week}/{found[0]}", week)
            for person in self.datasets.keys():
                self.dataset = self.datasets[person]
                self.datatypes[datatype]()
                self.datasets[person] = self.dataset

        return self.datasets

    def load(self, file, week):
        data = pd.read_csv(file)

        # Separate family members
        data = data.groupby("Participant Name")
        self.members = list(data.groups.keys())
        for person in self.members:

            pdata = data.get_group(person)
            pdata = pdata.drop(columns=["Data Stream", "Participant Name", "Timezone"])

            # convert Time Stamp to datetime
            pdata["Time Stamp"] = pd.to_datetime(pdata["Time Stamp"])
            pdata = pdata.sort_values(by=["Time Stamp"])

            # handle missing values
            missing = sum(1 * pdata["Reason"].notnull().values)
            total = len(pdata["Reason"])
            print(f"{week}: There are {missing}/{total} missing values")
            if missing != total:
                pdata = pdata.drop(columns=["Reason"], errors="ignore")
                self.datasets[person] = pdata


def process(args, a):

    all_d = {}
    for week in os.listdir(a.family_path):
        if week.startswith("."):
            continue
        d = a.get_data(week, args.stream)
        for person in d.keys():
            all_d[person] = (
                d[person]
                if person not in all_d
                else pd.concat([all_d[person], d[person]])
            )

    for person in all_d.keys():
        if not len(all_d[person]):
            continue
        all_d[person]["Time Stamp"] = pd.to_datetime(
            all_d[person]["Time Stamp"], errors="coerce"
        )
        new_datetime = pd.date_range(
            start=all_d[person]["Time Stamp"].min().floor("D"),
            end=all_d[person]["Time Stamp"].max().ceil("D"),
            freq="1T",
        )
        new_datetime = pd.DataFrame({"Time Stamp": new_datetime})

        all_d[person] = all_d[person].drop_duplicates()
        all_d[person] = all_d[person].merge(new_datetime, how="right", on="Time Stamp")
        pdata = all_d[person].set_index("Time Stamp")

        if not pdata.dropna(how="all").empty:
            # save the clean in csv format
            clean_path = a.family_path.replace("STTRp", "STTR_clean")
            person_path = os.path.join(clean_path, person)
            os.makedirs(person_path, exist_ok=True)
            pdata.to_csv(person_path + f"/{person}_{args.stream}.csv")
