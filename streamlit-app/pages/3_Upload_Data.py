import streamlit as st
import pandas as pd

st.set_page_config(page_title="Upload Data", layout="wide")

st.title("📂 Upload Data")

st.write("Upload an Excel file to preview your data structure.")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.success("File uploaded successfully.")
    st.subheader("Preview")
    st.dataframe(df.head(10))
else:
    st.info("No file uploaded yet.")
