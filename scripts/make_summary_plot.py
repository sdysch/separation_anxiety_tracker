import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

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
"""
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

fig.savefig('docs/plot.png')
"""

df = df.sort_values(by=x)
fig = px.scatter(
    df,
    x=x,
    y=y,
    symbol='rating',
    color='rating'
)

fig.add_scatter(
    x=df[x],
    y=df[y],
    mode='lines',
    line=dict(color='gray'),
    showlegend=False
)

# update symbol size
fig.update_traces(marker=dict(size=14))

# update font size
fig.update_layout(
    xaxis=dict(
        title_font=dict(size=18),
        tickfont=dict(size=14)
    ),
    yaxis=dict(
        title_font=dict(size=18),
        tickfont=dict(size=14)
    )
)

# fig.show()
fig.write_html('docs/plot.html')

