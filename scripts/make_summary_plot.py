import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

conn = sqlite3.connect('sa_training.db')

# load data 
df = pd.read_sql_query("""
    SELECT timestamp, actual_duration_seconds, rating FROM departures
""", conn)

conn.close()

# prepare data for plotting
df['timestamp'] = pd.to_datetime(df['timestamp'])

df['actual_duration_mins'] = df['actual_duration_seconds'] / 60.

# y = 'actual_duration_seconds'
y = 'actual_duration_mins'
x = 'timestamp'

# plot
fig, ax = plt.subplots(figsize=(15, 5))

sns.lineplot(
    data=df,
    x=x,
    y=y,
    color='black',
    linestyle='--',
    ax=ax
)

sns.scatterplot(
    data=df,
    x=x,
    y=y,
    style='rating',
    s=100,
    ax=ax
)

fig.savefig('plot.png')

