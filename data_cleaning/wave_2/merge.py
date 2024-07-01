import os, pandas as pd

path = ...
clean_path = ...
os.makedirs(clean_path, exist_ok=True)
family_list = [fam for fam in os.listdir(clean_path) if fam.startswith("S")]
family_list = [fam for fam in family_list if not fam.endswith(".csv")]


def restrict_time(df):
    df["Time Stamp"] = pd.to_datetime(df["Time Stamp"])
    # restrict time to 12 weeks (for possible extensions)
    start = df["Time Stamp"].min().floor("D")
    end1 = df["Time Stamp"].max().ceil("D")
    end2 = start + pd.Timedelta(weeks=12)
    end = min(end1, end2)
    return df[(df["Time Stamp"] >= start) & (df["Time Stamp"] <= end)]


def merge_family(family):
    family_path = os.path.join(clean_path, family)
    for member in os.listdir(family_path):
        if member.startswith("."):
            continue
        member_path = os.path.join(family_path, member)

        # check if the member has already been merged
        if os.path.exists(f"{clean_path}{member}_merged.csv"):
            continue

        flag = False
        no_streams = [
            "merged",
            "vocal_metrics",
            "deep_audio",
            "daily_stats",
            "all_stats",
        ]
        stream_list = [
            s for s in os.listdir(member_path) if all(x not in s for x in no_streams)
        ]
        for stream in stream_list:
            file = pd.read_csv(os.path.join(member_path, stream))
            addon = stream.strip(".csv").strip(member)[1:]
            new_cols = {
                c: f"{addon}_{c}" for c in file.columns if "Time Stamp" not in c
            }
            file = file.rename(columns=new_cols)
            if not flag:
                merged = file
                flag = True
            else:
                merged = pd.concat([merged, file], join="outer")
                merged = restrict_time(merged)

        # interpolate datetime in between
        merged["Time Stamp"] = pd.to_datetime(merged["Time Stamp"])
        merged_start = merged["Time Stamp"].min().floor("D")
        merged_end_1 = merged["Time Stamp"].max().ceil("D")
        merged_end_2 = merged_start + pd.Timedelta(weeks=12)
        new_datetime = pd.date_range(
            start=merged_start,
            end=min(merged_end_1, merged_end_2),
            freq="1T",
        )
        new_datetime = pd.DataFrame({"Time Stamp": new_datetime})
        merged = merged.merge(new_datetime, how="right", on="Time Stamp")

        # save in csv format
        merged = merged.groupby("Time Stamp").max()
        merged.to_csv(f"{member_path}/{member}_merged.csv")
        merged.to_csv(f"{clean_path}{member}_merged.csv")


if __name__ == "__main__":
    for family in family_list:
        print(f"Merging for family {family}")
        merge_family(family)
