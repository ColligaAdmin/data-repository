import argparse, os
from main import Family_Data, process


class PhoneSense_Data(Family_Data):
    def __init__(self, family_path):
        super().__init__(family_path)
        self.datatypes = {
            "humidity": self.get_rest,
            "barometer": self.get_barometer,
            "step_count": self.get_steps,
            "accelerometer": self.get_accel,
            "distance": self.get_distance,
            "gyroscope": self.get_accel,
            "ambient_noise": self.get_noise,
            "ambient_light": self.get_rest,
        }

    def get_barometer(self):
        # resolve naming issue
        if "Value" in self.dataset.columns:
            self.dataset.rename(columns={"Value": "Value (mbar)"}, inplace=True)
        # OUTPUT [Time Stamp] : [mbar]
        # RESOLUTION: 5 min

    def get_accel(self):
        # resolve multiple timesteps issue
        self.dataset = self.dataset.groupby("Time Stamp", as_index=False).mean()
        # OUTPUT [Time Stamp] : [X, Y, Z]
        # RESOLUTION: 1 min

    def get_steps(self):
        steps = []
        for row in self.dataset.values:
            row = row[0] if str(row[0]) == "nan" else float(row[0])
            steps.append(row)

        self.dataset["Value"] = self.differentiate(
            [float(s.split()[0]) if type(s) == str else s for s in steps]
        )
        # OUTPUT [Time Stamp] : [Step count]
        # RESOLUTION: 3 min

    def get_distance(self):
        distances = []
        for row in self.dataset.values:
            row = row[0] if str(row[0]) == "nan" else float(row[0].split()[0])
            distances.append(row)

        self.dataset["Value"] = self.differentiate(
            [float(s.split()[0]) if type(s) == str else s for s in distances]
        )
        # OUTPUT [Time Stamp] : [Distance count]
        # RESOLUTION: 3 min

    def get_noise(self):
        # resolve naming issue
        if "Value" in self.dataset.keys():
            self.dataset = self.dataset.rename(columns={"Value": "Value (db)"})
        # OUTPUT [Time Stamp] : [db value]
        # RESOLUTION: 15 min


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="STTR")
    parser.add_argument("--stream")
    args = parser.parse_args()

    path = ...
    for family in os.listdir(path):
        print(f"\n{args.stream} for family {family}:\n")
        process(args, PhoneSense_Data(path + family))
