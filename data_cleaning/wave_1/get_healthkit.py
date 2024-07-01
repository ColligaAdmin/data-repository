import numpy as np, os
import argparse, pandas as pd
from datetime import datetime as dt
from datetime import timedelta as td
from main import Family_Data, process
from translate_dict import parse_dict


class Healthkit_Data(Family_Data):
    def __init__(self, family_path):
        super().__init__(family_path)
        self.datatypes = {
            "healthkit_sleep": self.get_sleep_h,
            "healthkit_mindfulness": self.get_mindfulness,
            "healthkit_activity": self.get_activity_h,
            "healthkit_heart": self.get_heart_rate_h,
            "healthkit_hearing": self.get_hearing,
        }

    def get_sleep_h(self):
        date_rng = pd.date_range(
            start=self.dataset["Time Stamp"].min().floor("D"),
            end=self.dataset["Time Stamp"].max().ceil("D"),
            freq="T",
        )
        new = pd.DataFrame(index=date_rng)
        new["InBed"] = np.nan
        new["Asleep"] = np.nan

        slept, inbed = [], []
        for i, entry in enumerate(self.dataset["Data"]):
            date = self.dataset.iloc[i]["Time Stamp"].date()
            if type(entry) == str:
                dct = parse_dict(entry)["healthkit_sleep"]
                if "asleep" in dct.keys():
                    lst = [item.split("(")[1][:-1] for item in dct["asleep"]]
                    lst = [(date, item) for item in lst]
                    slept.append(list(set(lst)))
                if "in_bed" in dct.keys():
                    lst = [item.split("(")[1][:-1] for item in dct["in_bed"]]
                    lst = [(date, item) for item in lst]
                    inbed.append(list(set(lst)))

        def get_time(tup):
            date, interval = tup
            start, end = tuple(interval.split(" - "))
            start_time = dt.strptime(start, "%I:%M %p").time()
            end_time = dt.strptime(end, "%I:%M %p").time()
            start_ts = dt.combine(date, start_time)
            end_ts = dt.combine(date, end_time)
            if end_ts < start_ts:
                start_ts = start_ts - td(days=1)
            return pd.date_range(start_ts, end_ts, freq="T")

        inbed = set([item for lst in inbed for item in lst])
        inbed = [get_time(item) for item in inbed if item != "nan"]
        for interval in inbed:
            new.loc[:, "InBed"] = np.where(new.index.isin(interval), 1, np.nan)

        slept = set([item for lst in slept for item in lst])
        slept = [get_time(item) for item in slept if item != "nan"]
        for interval in slept:
            new.loc[:, "Asleep"] = np.where(new.index.isin(interval), 1, np.nan)

        new.index.name = "Time Stamp"
        self.dataset = new.reset_index(level=0)
        # OUTPUT [Time Stamp] : [Minutes Asleep, Minutes in Bed]
        # RESOLUTION: 1 min


    def get_mindfulness(self):
        # summarize provided time
        features = []
        for entry in self.dataset["Data"]:
            if type(entry) != str:
                features.append(np.nan)
            else:
                dct = parse_dict(entry)
                time = dct["healthkit_mindfulness"].split()[0]
                features.append(float(time))

        self.dataset["Time (sec)"] = features
        self.dataset = self.dataset.drop(columns=["Data"])
        # OUTPUT [Time Stamp] : [Time spent]
        # RESOLUTION: 30 min

    def get_hearing(self):
        headphones, environment = [], []
        for row in self.dataset.iterrows():
            entry = row[1]
            if type(entry["Headphone Audio Level"]) == str:
                dct = parse_dict(entry["Headphone Audio Level"])
                value = dct["value"].split()[0]
                headphones.append(int(value))
            else:
                headphones.append(np.nan)
            if type(entry["Environmental Sound Level"]) == str:
                dct = parse_dict(entry["Environmental Sound Level"])
                value = dct["value"].split()[0]
                environment.append(int(value))
            else:
                environment.append(np.nan)

        self.dataset["Headphone Audio Level"] = headphones
        self.dataset["Environmental Sound Level"] = environment
        self.dataset = self.dataset.drop(columns=["Audiogram"])
        # OUTPUT [Time Stamp] : [Headphone audio, Environmental audio]
        # RESOLUTION: 15 min

    def get_heart_rate_h(self):
        # replace 0 with np.nan
        self.dataset.loc[self.dataset["Value (BPM)"] == 0, "Value (BPM)"] = np.nan
        # OUTPUT [Time Stamp] : [BPM]
        # RESOLUTION: 1 min

    def get_activity_h(self):
        # replace to numerical values
        stand = self.differentiate(
            [
                float(value.split()[0]) if type(value) == str else value
                for value in self.dataset["Stand Minutes"]
            ]
        )
        active = self.differentiate(
            [
                float(value.split()[0]) if type(value) == str else value
                for value in self.dataset["Active Energy"]
            ]
        )
        resting = self.differentiate(
            [
                float(value.split()[0]) if type(value) == str else value
                for value in self.dataset["Resting Energy"]
            ]
        )

        self.dataset["Stand Minutes"] = stand
        self.dataset["Active kcal"] = active
        self.dataset["Resting kcal"] = resting
        self.dataset = self.dataset.drop(
            columns=["Active Energy", "Resting Energy"],
            errors="ignore",
        )
        # OUTPUT [Time Stamp] : [Stand Minutes, Active kcal, Resting kcal]
        # RESOLUTION: 1 min


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="STTR")
    parser.add_argument("--stream")
    args = parser.parse_args()

    path = ...
    for family in os.listdir(path):
        print(f"\n{args.stream} for family {family}:\n")
        process(args, Healthkit_Data(path + family))
