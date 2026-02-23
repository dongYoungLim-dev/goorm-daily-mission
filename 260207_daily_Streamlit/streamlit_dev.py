import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_ydata_profiling import st_profile_report
from datetime import datetime

st.header("Data Profile Report (streamlit_ydata_profiling)")

df = pd.read_csv("https://raw.githubusercontent.com/dataprofessor/data/master/penguins_cleaned.csv")


st.title("Data Profile Report (streamlit_ydata_profiling)")
st.code("""
from ydata_profiling import ProfileReport
from streamlit_ydata_profiling import st_profile_report
""")

st.dataframe(df)

st.sidebar.title("Options")
st.sidebar.checkbox("Show raw data", value=True)
st.sidebar.selectbox("Select a column", df.columns)
st.sidebar.text_input("Search for a value", value="")
st.sidebar.text_area("Comment", value="")
st.sidebar.slider("Select a number", min_value=0, max_value=100, value=50)
st.sidebar.date_input("Select a date", value=datetime.now())


# pr = ProfileReport(df, minimal=True)
# st_profile_report(pr)
