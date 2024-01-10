import streamlit as st
import pandas as pd
# import altair as alt

import datetime
from datetime import timedelta

def init_app():
    page_names_to_funcs = {
        "Eletricity": elec_dashboard,
    }

    st.set_page_config(page_title="Graftool", page_icon="", layout="wide", initial_sidebar_state="expanded")
    st.markdown(""" <style> .reportview-container { margin-top: -2em; } #MainMenu {visibility: hidden;} .stDeployButton {display:none;} footer {visibility: hidden;} #stDecoration {display:none;} </style> """, unsafe_allow_html=True) 

    today = datetime.datetime.now()
    start_datetime = today-timedelta(days=365)

    with st.form("dates"):
        with st.sidebar:        
            chart_name = st.selectbox("Choose a chart", page_names_to_funcs.keys())
            
            startDate = st.date_input('Start date', start_datetime, key='start_date', format="DD/MM/YYYY")
            endDate = st.date_input("End date", today, key='end_date', format="DD/MM/YYYY")

            submitted = st.form_submit_button("Update data")

        if submitted:
            page_names_to_funcs[chart_name](startDate, endDate)
    
    #elec_dashboard(startDate, endDate)

def elec_dashboard(start_datetime, end_datetime):
    st.write("# 📈 Eletricity metrics")

    df = pd.read_csv("example/elec.csv", names=["date","value1","value2"], sep="\t")
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, format="%d-%m-%y")

    df =df[(df['date'] >= start_datetime.strftime("%Y/%m/%d") ) & (df['date'] <= end_datetime.strftime("%Y/%m/%d"))]

    df["TOTAL"] = df["value1"] + df["value2"]
    df = df.drop('value1', axis=1)
    df = df.drop('value2', axis=1)
    df["DIFF"] = df["TOTAL"].diff()
    df = df.drop('TOTAL', axis=1)
    df["DATEDIFF"] = df["date"].diff().dt.days
    df.bfill(inplace=True)
    # df = df.dropna()
    df["DIFF"] = df["DIFF"] / df["DATEDIFF"]
    df = df.drop('DATEDIFF', axis=1)
    df["consum"] = df["DIFF"].round(decimals=0)
    df = df.drop('DIFF', axis=1)

    st.line_chart(df,
                        x="date", 
                        y="consum"
                        )
    
    st.markdown(""" <hr> """, unsafe_allow_html=True)

    df

init_app()