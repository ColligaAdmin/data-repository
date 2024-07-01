import pandas as pd
from translate_dict import parse_dict


def get_proximity_people(data):
    linked, distance, time = [], [], []
    for i, entry in enumerate(data["Data"]):
        dct = parse_dict(entry)
        for p in dct["role"]:
            new_row = data.iloc[i].copy()
            linked.append(str(p["participant_2"]))
            distance.append(float(p["distance"]))
            time.append(new_row["Time Stamp"])

    # unify columns for single time steps
    new_cols = {m: [] for m in list(set(linked))}
    for i in range(len(time)):
        new_cols[linked[i]].append({"Time Stamp": time[i], linked[i]: distance[i]})
    # keep non-empty columns
    new_cols = {k: v for k, v in new_cols.items() if v}

    # create new data frame
    new_data = pd.DataFrame(columns=["Time Stamp", *list(set(linked))])
    for d in new_cols:
        new_cols[d] = pd.DataFrame(new_cols[d])
        new_data = new_data.merge(new_cols[d], how="outer", on=["Time Stamp", d])
    # append the "Reason" column
    new_data["Reason"] = data["Reason"]
    return new_data.groupby("Time Stamp").max().reset_index()


def get_time_spent_people(data):
    linked, duration, time = [], [], []
    for i, entry in enumerate(data["Data"]):
        dct = parse_dict(entry)
        for p in dct["role"]:
            new_row = data.iloc[i].copy()
            linked.append(str(p["participant_2"]))
            duration.append(float(p["duration"]) / 60.0)
            time.append(new_row["Time Stamp"])

    # unify columns for single time steps
    new_cols = {m: [] for m in list(set(linked))}
    for i in range(len(time)):
        new_cols[linked[i]].append({"Time Stamp": time[i], linked[i]: duration[i]})
    # keep non-empty columns
    new_cols = {k: v for k, v in new_cols.items() if v}

    # create new data frame
    new_data = pd.DataFrame(columns=["Time Stamp", *list(set(linked))])
    for d in new_cols:
        new_cols[d] = pd.DataFrame(new_cols[d])
        new_data = new_data.merge(new_cols[d], how="outer", on=["Time Stamp", d])
    # append the "Reason" column
    new_data["Reason"] = data["Reason"]
    return new_data.groupby("Time Stamp").max().reset_index()


def get_time_spent_locations(data):
    linked, duration, time = [], [], []
    for i, entry in enumerate(data["Data"]):
        dct = parse_dict(entry)
        for p in dct:
            new_row = data.iloc[i].copy()
            linked.append(str(p["location"]))
            duration.append(float(p["duration"]) / 60.0)
            time.append(new_row["Time Stamp"])

    # unify columns for single time steps
    new_cols = {"Home": [], "Work": [], "School": []}
    for i in range(len(time)):
        new_cols[linked[i]].append({"Time Stamp": time[i], linked[i]: duration[i]})
    # keep non-empty columns
    new_cols = {k: v for k, v in new_cols.items() if v}

    new_data = pd.DataFrame(columns=["Time Stamp", "Home", "Work", "School"])
    for d in new_cols:
        new_cols[d] = pd.DataFrame(new_cols[d])
        new_data = new_data.merge(new_cols[d], how="outer", on=["Time Stamp", d])
    # append the "Reason" column
    new_data["Reason"] = data["Reason"]
    return new_data.groupby("Time Stamp").max().reset_index()
