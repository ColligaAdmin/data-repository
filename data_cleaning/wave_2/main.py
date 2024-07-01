import os, pandas as pd
import glob, warnings

warnings.filterwarnings("ignore")

from streams import *
from get_audio import *
from get_phone import *
from get_fitbit import *
from get_proximity import *


def process_sensing(filepath, stream):
    data = pd.read_csv(filepath)
    if "call-duration" in stream or "sms-transcripts" in stream or "typed" in stream:
        return pd.DataFrame()

    # assert we do not have data from other recordings
    assert len(data["Participant Name"].unique()) == 1, "mixed participants"
    assert len(data["Data Stream"].unique()) == 1, "mixed streams"
    data = data.drop(columns=["Data Stream", "Participant Name", "Timezone"])

    # special processing
    if "proximity-to-linked-people" in stream:
        data = get_proximity_people(data)
    elif "time-spent-with-linked-people" in stream:
        data = get_time_spent_people(data)
    elif "time-spent-at-linked-locations" in stream:
        data = get_time_spent_locations(data)
    elif "charging-metrics" in stream:
        data["Battery level"] = data["Battery level"].str.replace("%", "")
    elif "calendar" in stream:
        data = get_calendar_events(data)
    if "Location" in data:
        data = data.drop(columns=["Location"])

    # convert time stamp to datetime and sort
    data["Time Stamp"] = pd.to_datetime(data["Time Stamp"], infer_datetime_format=True)
    data = data.sort_values(by=["Time Stamp"]).set_index("Time Stamp")

    # handle missing values
    missing = sum(1 * data["Reason"].notnull().values)
    total = len(data["Reason"])
    if missing == total:
        print(f"Discarding {stream} due to missing values")
        return pd.DataFrame()
    else:
        data = data.drop(columns=["Reason"])
        # convert 'object' column types to float
        for col in data:
            data[col] = pd.to_numeric(data[col], errors="coerce")
        return data


def merge_proximity(df, members):
    for m in members:
        if m == member:
            continue
        for col in df.columns:
            if m == col:
                continue
            n, i = m[-4:-2], m[-1]
            if f"{n}_{i}" in col or f"{n}-{i}" in col:
                if m not in df.columns:
                    df = df.rename(columns={col: m})
                else:
                    df[m] = df[m].combine_first(df[col])
                    df = df.drop(columns=[col])
            elif n not in col:
                df = df.drop(columns=[col])
    return df


path = ...
clean_path = ...
os.makedirs(clean_path, exist_ok=True)

for family_path in glob.glob(path + "S*"):
    family = family_path.split("/")[-1]
    if family in os.listdir(clean_path):
        continue
    clean_family_path = os.path.join(clean_path, family)
    os.makedirs(clean_family_path, exist_ok=True)

    members = glob.glob(family_path + f"/*")
    members = [m.split("/")[-1] for m in members]
    members = [m.replace("_", "-").replace("STTR-", "STTR1-") for m in members]

    for member_path in glob.glob(family_path + f"/*"):
        member = member_path.split("/")[-1]
        member = member.replace("_", "-").replace("STTR-", "STTR1-")
        clean_member_path = os.path.join(clean_family_path, member)
        os.makedirs(clean_member_path, exist_ok=True)

        print("\n", member)
        member_dct = {}

        # fitbit (alt)
        fitbit_path = glob.glob(member_path + f"/*_Fitbit*")
        if fitbit_path:
            fit_path = os.path.join(fitbit_path[0], "Physical Activity")
            member_dct = process_fitbit(fit_path)
            sleep_path = os.path.join(fitbit_path[0], "Sleep")
            member_dct["sleep"] = process_fitbit_sleep(sleep_path)

        for week_path in glob.glob(member_path + "/Week*"):
            # surveys
            survey_path = glob.glob(week_path + "/Survey*")
            for spath in survey_path:
                surveys = process_surveys(spath)
                member_dct["survey"] = (
                    pd.concat([member_dct["survey"], surveys])
                    if "survey" in member_dct
                    else surveys
                )

            # audio
            audio_path = glob.glob(week_path + "/Audio")
            if audio_path and os.listdir(audio_path[0]) != []:
                sent_path = glob.glob(audio_path[0] + "/Sentiment*")
                if sent_path:
                    sentiment = process_sentiment(sent_path[0])
                    member_dct["language"] = (
                        pd.concat([member_dct["language"], sentiment])
                        if "language" in member_dct
                        else sentiment
                    )

            # sensing
            other_path = glob.glob(week_path + "/Other")
            if not other_path:
                continue
            for filepath in glob.glob(other_path[0] + "/s*.csv"):
                if "vocal" in filepath:
                    continue
                if "audio" in filepath:
                    continue

                # extract file info
                stream, start_d, end_d = filepath.replace(" ", "_")[:-4].split("_")[-3:]
                start_d, end_d = pd.to_datetime(start_d), pd.to_datetime(end_d)
                if stream in fitbit_streams:
                    continue
                if stream not in all_streams:
                    print(f"Unknown stream: {stream}")
                    continue

                this_stream = process_sensing(filepath, stream)
                if "people" in stream:
                    this_stream = merge_proximity(this_stream, members)
                member_dct[stream] = (
                    pd.concat([member_dct[stream], this_stream])
                    if stream in member_dct
                    else this_stream
                )

        # merge and save for each stream
        for stream in member_dct.keys():
            if member_dct[stream].empty:
                continue
            # sort per timestamp
            if "Time Stamp" in member_dct[stream]:
                # make it index
                member_dct[stream] = member_dct[stream].set_index("Time Stamp")
            member_dct[stream] = member_dct[stream].sort_index()
            # merge rows with same timestamp by joining values
            save_path = os.path.join(clean_member_path, f"{member}_{stream}.csv")
            member_dct[stream].to_csv(save_path)
