import glob, pandas as pd, ast


def process_sentiment(sent_path):
    sentiment = pd.DataFrame(
        columns=[
            "Time Stamp",
            "Positive",
            "Neutral",
            "Negative",
            "Polar",
            "Subjective",
            "Num_offense",
        ]
    )
    for filepath in glob.glob(sent_path + "/*.csv"):
        timestamp = filepath.split(".")[0][-15:]
        timestamp = pd.to_datetime(timestamp, format="%H%M_%d_%m_%Y")
        f = pd.read_csv(filepath)
        new_row = get_language_use(f)
        new_row["Time Stamp"] = timestamp
        sentiment = sentiment.append(new_row, ignore_index=True)

    return sentiment


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
