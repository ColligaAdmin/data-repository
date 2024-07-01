import argparse, os, pandas as pd
from main import Family_Data, process
from translate_dict import parse_dict


class Proximity_Data(Family_Data):
    def __init__(self, family_path):
        super().__init__(family_path)
        self.datatypes = {
            "proximity_to_linked_people": self.get_proximity_people,
            "proximity_to_set_locations": self.get_proximity_locations,
            "time_spent_with_linked_people": self.get_time_spent_people,
            "time_spent_at_linked_locations": self.get_time_spent_locations,
        }

    def get_proximity_locations(self):
        self.dataset = self.dataset.drop(columns=["Location"])

    def get_time_spent_locations(self):
        new_data = pd.DataFrame(columns=["Time Stamp", "Home", "Work", "School"])
        linked, duration, time = [], [], []

        for i, entry in enumerate(self.dataset["Data"]):
            dct = parse_dict(entry)
            for p in dct:
                new_row = self.dataset.iloc[i].copy()
                linked.append(str(p["location"]))
                duration.append(float(p["duration"]) / 60.0)
                time.append(new_row["Time Stamp"])

        # unify columns for single time steps
        new_cols = {"Home": [], "Work": [], "School": []}
        for i in range(len(time)):
            new_cols[linked[i]].append({"Time Stamp": time[i], linked[i]: duration[i]})
        for d in new_cols:
            if new_cols[d]:
                new_cols[d] = pd.DataFrame(new_cols[d])
                new_data = new_data.merge(
                    new_cols[d], how="outer", on=["Time Stamp", d]
                )

        # combine common measures for different locations
        self.dataset = new_data.groupby("Time Stamp").max().reset_index()

    def get_proximity_people(self):
        new_data = pd.DataFrame(columns=self.members + ["Time Stamp"])
        linked, distance, time = [], [], []

        for i, entry in enumerate(self.dataset["Data"]):
            dct = parse_dict(entry)
            for p in dct["role"]:
                new_row = self.dataset.iloc[i].copy()
                linked.append(str(p["participant_2"]))
                distance.append(float(p["distance"]))
                time.append(new_row["Time Stamp"])

        # unify columns for single time steps
        new_cols = {m: [] for m in self.members}
        for i in range(len(time)):
            new_cols[linked[i]].append({"Time Stamp": time[i], linked[i]: distance[i]})
        for d in new_cols:
            if new_cols[d]:
                new_cols[d] = pd.DataFrame(new_cols[d])
                new_data = new_data.merge(
                    new_cols[d], how="outer", on=["Time Stamp", d]
                )

        # combine common measures for different locations
        self.dataset = new_data.groupby("Time Stamp").max().reset_index()

    def get_time_spent_people(self):
        new_data = pd.DataFrame(columns=self.members + ["Time Stamp"])
        linked, duration, time = [], [], []

        for i, entry in enumerate(self.dataset["Data"]):
            dct = parse_dict(entry)
            for p in dct["role"]:
                new_row = self.dataset.iloc[i].copy()
                linked.append(str(p["participant_2"]))
                duration.append(float(p["duration"]) / 60.0)
                time.append(new_row["Time Stamp"])

        # unify columns for single time steps
        new_cols = {m: [] for m in self.members}
        for i in range(len(time)):
            new_cols[linked[i]].append({"Time Stamp": time[i], linked[i]: duration[i]})
        for d in new_cols:
            if new_cols[d]:
                new_cols[d] = pd.DataFrame(new_cols[d])
                new_data = new_data.merge(
                    new_cols[d], how="outer", on=["Time Stamp", d]
                )

        # combine common measures for different locations
        self.dataset = new_data.groupby("Time Stamp").max().reset_index()



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="STTR")
    parser.add_argument("--stream")
    args = parser.parse_args()

    path = ...
    for family in os.listdir(path):
        print(f"\n{args.stream} for family {family}:")
        process(args, Proximity_Data(path + family))
