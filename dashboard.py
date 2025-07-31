import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# loading data
@st.cache_data(ttl=3600)
def load_data():

    conn = sqlite3.connect('sa_training.db')

    # load data 
    df = pd.read_sql_query("""
        SELECT timestamp, actual_duration_seconds, rating FROM departures
    """, conn)

    conn.close()

    return df


def make_plotly_fig(df):
    y = 'actual_duration_mins'
    x = 'timestamp'

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

    return fig


def main():

    # page config
    st.set_page_config(page_title='Max SA Tracker', layout='centered')
    st.title('🐾 Max SA Training')
    st.set_page_config(layout='wide')

    # prepare data
    df = load_data()
    df['actual_duration_mins'] = df['actual_duration_seconds'] / 60.

    col1, col2 = st.columns(2)

    # most recent
    with col1:
        st.subheader('📅 Most Recent Session')
        latest = df.sort_values(by='timestamp', ascending=False).iloc[0]

        st.markdown(
            f"**Date**: {latest['timestamp']}  \n"
            f"**Actual Duration**: {latest['actual_duration_mins']} min  \n"
            f"**Outcome**: {latest['rating']}"
        )

    # progress over time
    with col2:
        st.subheader("📈 Actual Duration Over Time")
        # df_sorted = df.sort_values(by='timestamp')
        # st.line_chart(df_sorted.set_index('timestamp')['actual_duration_mins'])
        fig = make_plotly_fig(df)
        st.plotly_chart(fig, use_container_width=True)

    # overall outcomes
    st.subheader("✅ Outcomes Overview")
    outcome_counts = df['rating'].value_counts()
    st.bar_chart(outcome_counts)



if __name__ == '__main__':
    main()

