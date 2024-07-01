import os, pandas as pd
import argparse, numpy as np
from main import Family_Data, process
from translate_dict import parse_dict


class Fitbit_Data(Family_Data):
    def __init__(self, family_path):
        super().__init__(family_path)
        self.datatypes = {
            "fitbit_sleep": self.get_sleep,
            "fitbit_activity": self.get_activity,
            "fitbit_heart_rate": self.get_heart_rate,
        }

    def get_sleep(self):
        self.dataset["totalMinutesAsleep"] = np.nan
        self.dataset["totalMinutesInBed"] = np.nan
        self.dataset["numAwakenings"] = np.nan
        self.dataset["efficiency"] = np.nan
        self.dataset["mainSleep"] = np.nan
        self.dataset["lightSleep"] = np.nan
        self.dataset["deepSleep"] = np.nan
        self.dataset["REM"] = np.nan

        self.dataset = self.dataset.set_index("Time Stamp")
        self.dataset = self.dataset[~self.dataset.index.duplicated(keep="first")]
        memory_bank = []

        for entry in self.dataset["Data"]:
            if type(entry) == str:
                dct = parse_dict(entry)["sleep"]  # dct keys: [sleep, summary]
                if not dct["sleep"]:
                    continue

                dt = pd.to_datetime(dct["sleep"][0]["startTime"])
                if dt not in memory_bank:
                    memory_bank.append(dt)
                    ind = self.dataset.index.get_indexer([dt], method="nearest")
                    ind = self.dataset.iloc[ind[0]].name

                    self.dataset.at[ind, "totalMinutesAsleep"] = dct["summary"][
                        "totalMinutesAsleep"
                    ]
                    self.dataset.at[ind, "totalMinutesInBed"] = dct["summary"][
                        "totalTimeInBed"
                    ]
                    self.dataset.at[ind, "numAwakenings"] = dct["sleep"][0][
                        "awakeningsCount"
                    ]
                    self.dataset.at[ind, "efficiency"] = dct["sleep"][0]["efficiency"]
                    self.dataset.at[ind, "mainSleep"] = (
                        True if dct["sleep"][0]["isMainSleep"] == "true" else False
                    )
                    if "stages" in dct["summary"]:
                        self.dataset.at[ind, "light_sleep"] = dct["summary"]["stages"][
                            "light"
                        ]
                        self.dataset.at[ind, "deep_sleep"] = dct["summary"]["stages"][
                            "deep"
                        ]
                        self.dataset.at[ind, "REM"] = dct["summary"]["stages"]["rem"]

        self.dataset = self.dataset.drop(columns=["Data"]).reset_index()


    def get_heart_rate(self):
        self.dataset = self.dataset.drop(columns=["Data"])
        # replace 0 with np.nan
        self.dataset.loc[self.dataset["Value (BPM)"] == 0, "Value (BPM)"] = np.nan
        # OUTPUT [Time Stamp] : [BPM]
        # RESOLUTION: 1 min

    def get_activity(self):
        """
        --- CaloriesBMR Column ---
        Basal Metabolic Rate (BMR) is the number of calories
        required to keep body functioning at rest (metabolism)
        --- CaloriesOut Column ---
        Estimated number of calories spent through Activity
        --- Floor/Elevation Columns ---
        Fitbit has an altimeter sensor that detects when you go up in elevation
        end registers 1 floor when you climb about 3 meters. Not reliable
        """
        self.dataset = self.dataset.drop(
            columns=["Floor", "Elevation", "CaloriesOutUnestimated"],
            errors="ignore",
        )
        # OUTPUT [Time Stamp] : [Activity cols]
        # RESOLUTION: 1 min


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="STTR")
    parser.add_argument("--stream")
    args = parser.parse_args()

    path = ...
    clean_path = path.replace("STTRp", "STTR_clean")
    for family in os.listdir(path):
        print(f"\n{args.stream} for family {family}:\n")
        process(args, Fitbit_Data(path + family))
