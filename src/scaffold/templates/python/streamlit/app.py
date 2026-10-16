import pandas as pd
import streamlit as st

st.set_page_config(page_title="__PROJECT__", layout="wide")
st.title("__PROJECT__")

n = st.slider("Rows", 5, 100, 20)
df = pd.DataFrame({"x": range(n), "y": [i * i for i in range(n)]})
st.line_chart(df, x="x", y="y")
st.dataframe(df, width="stretch")
