import os, pandas as pd

path = ...
clean_path = path.replace("STTRp", "STTR_clean")
family_list = [fam for fam in os.listdir(clean_path) if fam.startswith("STTR1")]


def merge_family(family):
    family_path = os.path.join(clean_path, family)
    for member in os.listdir(family_path):
        if member.startswith("."):
            continue
        member_path = os.path.join(family_path, member)

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
                merged = merged.merge(file, how="outer", on="Time Stamp")

        # interpolate datetime in between
        merged["Time Stamp"] = pd.to_datetime(merged["Time Stamp"])
        new_datetime = pd.date_range(
            start=merged["Time Stamp"].min().floor("D"),
            end=merged["Time Stamp"].max().ceil("D"),
            freq="1T",
        )
        new_datetime = pd.DataFrame({"Time Stamp": new_datetime})
        merged = merged.merge(new_datetime, how="right", on="Time Stamp")

        # save in csv format
        merged = merged.groupby("Time Stamp").max()
        merged.to_csv(f"{member_path}/{member}_merged.csv")


if __name__ == "__main__":
    for family in family_list:
        print(f"Merging for family {family}")
        merge_family(family)