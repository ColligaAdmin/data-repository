import os, pandas as pd


def make_audio_log(p, family):

    log = pd.DataFrame()
    path = os.path.join(p, family)

    conditions = [
        "speaker-identification",
        "vocal-metrics-android.csv",
        "vocal-metrics-andriod.csv",
        "vocal-metrics-andriod_20",
        "vocal-metrics-android_20",
        "transcription.csv",
        "transcription_20",
        "audio-android",
    ]

    for week in os.listdir(path):
        if week.startswith("."):
            continue
        wpath = os.path.join(path, week)
        for f in os.listdir(wpath):
            fpath = os.path.join(wpath, f)

            if any(c in f for c in conditions) and f.endswith("csv"):
                data = pd.read_csv(fpath)
                if "Time Stamp" not in data.columns:
                    continue
                data = data.drop(
                    columns=["Data Stream", "File Url", "Unnamed: 0", "Timezone"],
                    errors="ignore",
                )
                data["Time Stamp"] = pd.to_datetime(data["Time Stamp"])
                data = data.dropna(subset="File Name").drop(columns="Reason")
                log = data if log.empty else pd.concat([log, data], axis=0)
    if log.empty:
        return log

    def find(file):
        for dir, _, filenames in os.walk(p):
            filenames = [f[6:] if f.startswith("Audio-") else f for f in filenames]
            if file in filenames:
                return "/".join(dir.split("/")[5:])
        return "False"

    available = []
    for row in log.iterrows():
        filename = row[1]["File Name"]
        available.append(find(filename))
    log["Available"] = available

    log = log.groupby("Participant Name")
    members = list(log.groups.keys())
    for person in members:

        pdata = log.get_group(person)
        pdata = pdata.drop(columns=["Participant Name"])
        pdata = pdata.sort_values(by=["Time Stamp"]).reset_index(drop=True)
        pdata = pdata.set_index("Time Stamp").drop_duplicates()

        # save the clean in csv format
        person_path = os.path.join(clean_path, family, person)
        os.makedirs(person_path, exist_ok=True)
        pdata.drop_duplicates().to_csv(person_path + f"/{person}_audio_log.csv")


if __name__ == "__main__":
    path = ...
    clean_path = path.replace("STTRp", "STTR_clean")
    family_list = [fam for fam in os.listdir(clean_path) if fam.startswith("STTR1")]

    for family in family_list:
        print(f"Logging available files for family {family}")
        make_audio_log(path, family)
