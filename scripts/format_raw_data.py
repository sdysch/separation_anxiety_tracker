import pandas as pd

filename = 'data/raw_brb_data.csv'

df = pd.read_csv(
    filename,
    sep='|',
    parse_dates=['exercise_time'],
    usecols=[
        'id',
        'exercise_time',
        'result',
        'target_duration',
       'actual_duration',
       'num_steps',
       'total_duration'
   ]
)

df['notes'] = ''

df.to_csv('data/formatted_data.csv', index=False)

