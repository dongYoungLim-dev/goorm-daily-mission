import streamlit as st
import pandas as pd
import numpy as np

st.title('My First Streamlit App')
st.write('Hello, World!')

df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

st.write(df)

chart_data = pd.DataFrame(
  np.random.randn(20, 3),
)