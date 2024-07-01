import ast, os, pandas as pd


def read_audio(p, dir, f):
    p = "/".join(p.split("/")[:-2])
    try:
        data = pd.read_csv(os.path.join(p, dir, f))
    except:
        data = pd.read_csv(os.path.join(p, dir, f"Audio-{f}"))
    return data


def get_language_use(data):
    def parse_sent_text(data):
        polarity = data[data.find("=") + 1 : data.find(",")]
        data = data[data.find(",") + 1 :]
        subjectivity = data[data.find("=") + 1 : -1]
        return float(polarity), float(subjectivity)

    polar, subjective = parse_sent_text(data.loc[0]["sent_text"])
    sentiment = ast.literal_eval(data.loc[0]["sentiment"])
    offs_words = ast.literal_eval(data.loc[0]["offensive_words"])

    return {
        "Positive": sentiment["pos"],
        "Neutral": sentiment["neu"],
        "Negative": sentiment["neg"],
        "Polar": polar,
        "Subjective": subjective,
        "Num_offense": len(offs_words),
    }


def make_language_dataset(data, mpath):
    new_dataset = []
    for row in data.iterrows():
        if str(row[1]["Available"]) != "False" and row[1]["File Name"].endswith(
            "_text.csv"
        ):
            audio_data = read_audio(path, str(row[1]["Available"]), row[1]["File Name"])
            new_row = get_language_use(audio_data)
            new_row["Time Stamp"] = row[1]["Time Stamp"]
            new_dataset.append(new_row)

    new_dataset = pd.DataFrame.from_records(new_dataset)
    if not new_dataset.empty:
        member = mpath.split("/")[-1]
        new_dataset = new_dataset.set_index("Time Stamp")
        new_dataset.to_csv(mpath + f"/{member}_language.csv")


if __name__ == "__main__":
    path = ...
    clean_path = path.replace("STTRp", "STTR_clean")
    family_list = [fam for fam in os.listdir(clean_path) if fam.startswith("STTR1")]

    for family in family_list:
        print(f"Audio for family {family}")
        for member in os.listdir(clean_path + family):
            mpath = os.path.join(clean_path + family, member)
            for f in os.listdir(mpath):
                fpath = os.path.join(mpath, f)

                if "audio_log" in f:
                    data = pd.read_csv(fpath)
                    make_language_dataset(data, mpath)
