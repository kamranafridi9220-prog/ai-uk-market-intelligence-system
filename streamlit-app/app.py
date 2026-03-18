import streamlit as st
import pandas as pd

st.title("AI Market Intelligence System")
st.write("Ask business questions and get structured insights")

@st.cache_data
def load_data():
    df = pd.read_excel("ai_market_intelligence_engine_sample.xlsx", sheet_name="05_User_Query_Test")
    return df

df = load_data()

user_input = st.text_input("Enter your question:")

if user_input:
    result = df[df["User Question"].str.lower() == user_input.lower()]
    
    if not result.empty:
        st.subheader("Insight")
        st.write(result["Suggested Output"].values[0])
        
        st.subheader("Recommended Action")
        st.write(result["Recommended Action"].values[0])
        
        st.subheader("Confidence")
        st.write(result["Confidence"].values[0])
        
        st.subheader("Business Impact")
        st.write(result["Business Impact"].values[0])
    else:
        st.write("No matching insight found. Try another question.")