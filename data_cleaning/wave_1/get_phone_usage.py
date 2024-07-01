import argparse, os, numpy as np
from main import Family_Data, process
from translate_dict import parse_dict


class PhoneUsage_Data(Family_Data):
    def __init__(self, family_path):
        super().__init__(family_path)
        self.datatypes = {
            "calendar_event_frequency": self.get_calendar_events,
            "sms_frequency_android_only": self.get_rest,
            "call_frequency_android_only": self.get_rest,
        }


    def get_calendar_events(self):
        # just count the number of events
        self.dataset["num_events"] = np.nan

        for i, entry in enumerate(self.dataset["Data"]):
            temp = 0
            if type(entry) != str:
                continue
            dct = parse_dict(entry)
            for p in dct["calendar_event_frequency"]:
                if not len(p):
                    continue
                temp += len(p["calendar_events"])

            ind = self.dataset.iloc[i].name
            self.dataset.at[ind, "num_events"] = temp

        self.dataset = self.dataset.drop(columns=["Data"])

    def get_rest(self):
        pass


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="STTR")
    parser.add_argument("--stream")
    args = parser.parse_args()

    path = ...
    for family in os.listdir(path):
        print(f"\n{args.stream} for family {family}:\n")
        process(args, PhoneUsage_Data(path + family))
