env_streams = [
    "humidity",
    "barometer",
    "ambient-light",
    "ambient-noise",
]

motion_streams = [
    "gyroscope",
    "accelerometer",
]

fitbit_alt_streams = [
    "steps",
    "distance",
    "heart_rate",
    "sedentary_minutes",
    "lightly_active_minutes",
    "moderately_active_minutes",
    "very_active_minutes",
]

social_streams = [
    "proximity-to-linked-people",
    "proximity-to-set-locations",
    "time-spent-with-linked-people",
    "time-spent-at-linked-locations",
]

phone_streams = [
    "calendar-event-frequency",
    "call-frequency-android-only",
    "sms-frequency-android-only",
]

all_streams = (
    env_streams + motion_streams + fitbit_alt_streams + social_streams + phone_streams
)
