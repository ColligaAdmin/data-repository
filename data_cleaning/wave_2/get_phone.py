import glob, numpy as np, pandas as pd
from translate_dict import parse_dict


def process_surveys(survey_path):
    surveys = pd.DataFrame()
    for filepath in glob.glob(survey_path + "/*survey*.csv"):
        data = pd.read_csv(filepath)
        # assert we do not have data from other participants
        assert len(data["Participant Name"].unique()) == 1, "mixed subjects"
        # discard participant column
        data = data.drop(columns=["Participant Name"])
        # convert time stamp to datetime and sort
        data["Time Stamp"] = pd.to_datetime(
            data["Time Stamp"], infer_datetime_format=True
        )
        data = data.sort_values(by=["Time Stamp"]).set_index("Time Stamp")
        # convert 'object' column types to float
        for col in data:
            data[col] = pd.to_numeric(data[col], errors="coerce")
        surveys = pd.concat([surveys, data])
    return surveys


def get_calendar_events(data):
    # just count the number of events
    data["num_events"] = np.nan
    for i, entry in enumerate(data["Data"]):
        temp = 0
        if type(entry) != str:
            continue
        dct = parse_dict(entry)
        for p in dct["calendar_event_frequency"]:
            if not len(p):
                continue
            temp += len(p["calendar_events"])
        ind = data.iloc[i].name
        data.at[ind, "num_events"] = temp
    return data.drop(columns=["Data"])
