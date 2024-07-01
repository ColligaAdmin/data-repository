
'''
The column namings of quality_time, closeness, negativity, conflict, and agression change across different families
so we have two fidderent mappings from column names to emotion states
'''
output_map_old={

    'p_Happiness':'survey_1. Rate the extent to which you feel happy',
    'p_Sadness':'survey_2. Rate the extent to which you feel sad',
    'p_Anxiousness':'survey_3. Rate the extent to which you feel anxious',
    'p_Angriness':'survey_4. Rate the extent to which you feel angry',
    'p_Stress':'survey_5. Rate the extent to which you feel stressed',
    
    'p_Quality_time':'survey_6f. Rate the extent to which you are spending quality time with this child',
    'p_Closeness':'survey_6g. Rate the extent to which you feel close to this child',
    'p_Positivity':'survey_6h. Rate the extent to which you and this child are having a good time together',
    'p_Negativity':'survey_6i. Rate the extent to which you and this child are having a bad time together',
    'p_Conflict':'survey_6j. Rate the extent to which you are having conflict with this child',
    'p_Aggression':'survey_6k. Rate the extent to which you are being aggressive toward this child',
     
}
output_map_new={

    'p_Happiness':'survey_1. Rate the extent to which you feel happy',
    'p_Sadness':'survey_2. Rate the extent to which you feel sad',
    'p_Anxiousness':'survey_3. Rate the extent to which you feel anxious',
    'p_Angriness':'survey_4. Rate the extent to which you feel angry',
    'p_Stress':'survey_5. Rate the extent to which you feel stressed',
    
    'p_Quality_time':'survey_6h. Rate the extent to which you are spending quality time with this child',
    'p_Closeness':'survey_6i. Rate the extent to which you feel close to this child',
    'p_Positivity':'survey_6j. Rate the extent to which you and this child are having a good time together',
    'p_Negativity':'survey_6k. Rate the extent to which you and this child are having a bad time together',
    'p_Conflict':'survey_6l. Rate the extent to which you are having conflict with this child',
    'p_Aggression':'survey_6m. Rate the extent to which you are being aggressive toward this child',
     
}
#0 for one columns mappings, 1 for another column mappings from emotion states to actual column names
mapping_of_new_old_families={
    'SBIR-004-1':1,
    'SBIR-005-1':1,
    'SBIR-005-2':1,
    'SBIR-006-1':1,
    'SBIR-007-1':1,
    'SBIR-012-1':1,
    'SBIR-015-1':1,
    'SBIR-018-1':1,
    'SBIR-023-1':1,
    'SBIR-030-1':1,
    'SBIR-034-1':1,
    'SBIR-040-2':1,
    'SBIR-047-1':1,
    'SBIR-056-1':1,
    'SBIR-067-1':1,
    'STTR1-028-1':1,
    'STTR1-031-1':1,
    'STTR1-045-1':1,
    'STTR1-049-1':1,
    'STTR1-058-1':1,
    'STTR1-069-1':1,
    'STTR1-071-1':1,
    'STTR1-074-1':1,
    'STTR1-092-1':1,
    'STTR1-095-1':1,
    'STTR1-098-1':1,
    'STTR1-001-1':0,
    'STTR1-001-2':0,
    'STTR1-002-1':0,
    'STTR1-019-1':0,
    'STTR1-019-2':0,
    'STTR1-024-1':0,
    'STTR1-036-1':0,
    'STTR1-038-1':0,
    'STTR1-039-1':0,
    'STTR1-042-1':0

    }





other_features={
    
     'calendar_event_frequency_num_events','calendar-event-frequency_num_events',
   
    'call-frequency-android-only_Value', 'call_frequency_android_only_Value',
    'sms_frequency_android_only_Value','sms-frequency-android-only_Value',
    #'healthkit_mindfulne_Time (sec)',
    }

sleep_features={
    'fitbit_sleep_deep_sleep','sleep_deepSleep','fitbit_sleep_deepSleep',
    
    'fitbit_sleep_lightSleep','sleep_lightSleep',  'fitbit_sleep_light_sleep',
    
    'sleep_totalMinutesInBed','fitbit_sleep_totalMinutesInBed','healthkit_sleep_InBed',
    
    'sleep_totalMinutesAsleep','fitbit_sleep_totalMinutesAsleep','healthkit_sleep_Asleep',
    
    'fitbit_sleep_efficiency','sleep_efficiency',
    
    'sleep_rem','fitbit_sleep_REM',
    
    'sleep_mainSleep','fitbit_sleep_mainSleep',
    
   'fitbit_sleep_numAwakenings','sleep_numAwakenings',
   'sleep_wake',
    }

activity_features={
    'gyroscope_X','gyroscope_Y','gyroscope_Z',
    'accelerometer_X','accelerometer_Y','accelerometer_Z',
    
    'activity_very_active_minutes','fitbit_activity_Very Active Minutes',
    
    'fitbit_activity_Fairly Active Minutes','activity_moderately_active_minutes',
    
    'activity_sedentary_minutes','fitbit_activity_Sedentary Minutes',
    
    'activity_lightly_active_minutes','fitbit_activity_Lightly Active Minutes',
    
    'fitbit_heart_rate_Value (BPM)', 'heart_rate_BPM','healthkit_heart_Value (BPM)',
	'healthkit_activity_Resting kcal',
    'healthkit_activity_Active kcal',
     'healthkit_activity_Stand Minutes',
    'step_count_Value','step_Steps',
    'distance_Value', 'distance_Distance',
}

environment_features={
    'ambient-noise_Value','ambient-noise_Value (db)','ambient_noise_Value (db)',
    
    'ambient-light_Value','ambient_light_Value (lux)','ambient-light_Value (lux)',
    
    'humidity_Value (°C)',
    
    'barometer_Value','barometer_Value (mbar)',

    
    'healthkit_hearing_Environmental Sound Level',
    'healthkit_hearing_Headphone Audio Level',
    
    'time-spent-at-linked-location_Home','time_spent_at_linked_location_Home',
    
    'time_spent_at_linked_location_School','time-spent-at-linked-location_School',
    
    'time_spent_at_linked_location_Work','time-spent-at-linked-location_Work',
    
    'proximity_to_set_location_Home','proximity-to-set-location_Home',
    
    'proximity-to-set-location_School','proximity_to_set_location_School',
    
     'proximity-to-set-location_Work','proximity_to_set_location_Work',
    
      
}

speech_features={
    'language_Num_offense',
    'language_Negative',
    'language_Polar',
    'language_Subjective',
    'language_Positive',
    'language_Neutral',
}
