import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
import json
import requests


def app():
    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    st.title("Automatic Logging and tracking")
    st.balloons()
    lottie_img = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_qudievat.json")
    st_lottie(lottie_img,height=750, width=750)


    st.subheader("Check current logged ins")
    if st.button("show logins"):
        df1 = pd.read_csv("Logged_ins.csv")
        df1.columns =['Name', 'Time','Room']
        df1 = df1.loc[::-1]
        # df1 = df1.drop_duplicates(subset ='Time',keep = 'last')
        df1 = df1.drop_duplicates(subset ='Time',keep = 'last')
        df1 = df1.set_index('Time')
        st.write(df1)


    st.subheader("Not allowed login attemp")
    if st.button("Show attempts"):
        df2 = pd.read_csv("Warnings.csv")
        df2.columns =['Name', 'Time', 'Room']
        df2 = df2.loc[::-1]
        df2 = df2.drop_duplicates(subset ='Time',keep = 'last')
        df2 = df2.set_index('Time')
        st.write(df2)
