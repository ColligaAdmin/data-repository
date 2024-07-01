import glob, pandas as pd
import json, numpy as np
from streams import *


def process_fitbit(fitbit_path):
    final_dct = {}
    for stream in fitbit_alt_streams:
        stream_df = pd.DataFrame()

        for filepath in glob.glob(fitbit_path + f"/{stream}*.json"):
            data = pd.read_json(filepath)

            # rename to Time Stamp
            data = data.rename(columns={"dateTime": "Time Stamp"})
            # convert to datetime and sort
            data["Time Stamp"] = pd.to_datetime(
                data["Time Stamp"], infer_datetime_format=True
            )
            data = data.set_index("Time Stamp").sort_index()

            # special cases
            if stream == "steps":
                data = data.rename(columns={"value": "Steps"})
                data["Steps"] = data["Steps"].fillna(0)
            elif stream == "distance":
                data = data.rename(columns={"value": "Distance"})
                data["Distance"] = data["Distance"].fillna(0)
            elif stream == "heart_rate":
                data = data.rename(columns={"value": "BPM"})
                data["BPM"] = data["BPM"].apply(
                    lambda x: x["bpm"] if x["confidence"] else np.nan
                )
                data = data.resample("min").median()
            else:
                data = data.rename(columns={"value": stream})
                data[stream] = data[stream].fillna(0)
            # add to stream_df
            stream_df = pd.concat([stream_df, data])

        # convert 'object' column types to float
        for col in stream_df:
            stream_df[col] = pd.to_numeric(stream_df[col], errors="coerce")
        final_dct[stream] = stream_df

    # merge activity minutes
    activity = pd.DataFrame()
    for stream in fitbit_alt_streams:
        if "minutes" in stream:
            activity = pd.concat([activity, final_dct[stream]], axis=1)
            final_dct.pop(stream)
    final_dct["activity"] = activity
    return final_dct


def process_fitbit_sleep(fitbit_path):
    sleep_df = pd.DataFrame(
        columns=[
            "totalMinutesAsleep",
            "totalMinutesInBed",
            "numAwakenings",
            "efficiency",
            "mainSleep",
            "lightSleep",
            "deepSleep",
            "rem",
            "wake",
        ]
    )
    for filepath in glob.glob(fitbit_path + f"/sleep*.json"):
        with open(filepath) as f:
            logs = json.load(f)

        for data in logs:
            if "restless" in data["levels"]["summary"]:
                continue
            temp = {
                "totalMinutesAsleep": data["minutesAsleep"],
                "totalMinutesInBed": data["timeInBed"],
                "numAwakenings": data["levels"]["summary"]["wake"]["count"],
                "efficiency": data["efficiency"],
                "mainSleep": data["mainSleep"],
                "lightSleep": np.nan,
                "deepSleep": np.nan,
                "rem": np.nan,
                "wake": np.nan,
            }

            start_time, end_time = data["startTime"], data["endTime"]
            # round start time to nearest minute
            if start_time[-6:-4] != "00":
                start_time = start_time[:-6] + "00.000"
            # add 1 minute to end time
            end_time = pd.to_datetime(end_time) + pd.Timedelta(minutes=1)

            temp_index = pd.date_range(start=start_time, end=end_time, freq="1T")
            for i in temp_index:
                sleep_df.loc[i] = [np.nan] * 9

            sleep_df.iloc[-1] = temp
            # convert index to datetime
            sleep_df.index = pd.to_datetime(sleep_df.index)

            # add ambulatory sleep levels
            for dt in data["levels"]["data"]:
                dt["dateTime"] = pd.to_datetime(dt["dateTime"])
                # round to nearest minute
                if dt["dateTime"].second >= 30:
                    dt["dateTime"] = dt["dateTime"] + pd.Timedelta(seconds=30)

                dt_duration = dt["dateTime"] + pd.Timedelta(minutes=dt["seconds"] // 60)
                if dt_duration < dt["dateTime"]:
                    dt_duration = dt["dateTime"]
                elif dt_duration > sleep_df.index[-1]:
                    dt_duration = sleep_df.index[-1]

                if dt["level"] == "wake":
                    sleep_df.loc[dt["dateTime"] : dt_duration, "wake"] = 1
                elif dt["level"] == "light":
                    sleep_df.loc[dt["dateTime"] : dt_duration, "lightSleep"] = 1
                elif dt["level"] == "deep":
                    sleep_df.loc[dt["dateTime"] : dt_duration, "deepSleep"] = 1
                elif dt["level"] == "rem":
                    sleep_df.loc[dt["dateTime"] : dt_duration, "rem"] = 1

        # name the index as Time Stamp
        sleep_df = sleep_df.rename_axis("Time Stamp").sort_index()

    return sleep_df


if __name__ == "__main__":
    path = ...
    df = process_fitbit_sleep(path)
    df.to_csv("sleep.csv")
