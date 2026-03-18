import streamlit as st
import pandas as pd
from difflib import get_close_matches

st.set_page_config(page_title="AI Market Intelligence System", layout="wide")

st.title("AI-Powered UK Market Intelligence System")
st.write("Ask a business question and get a structured insight, recommendation, confidence level, and business impact.")

@st.cache_data
def load_data():
    df = pd.read_excel(
        "../ai-engine/ai_market_intelligence_engine_light.xlsx",
        sheet_name="05_User_Query_Interface"
    )
    return df

def find_best_match(user_input, questions):
    matches = get_close_matches(user_input.lower(), [q.lower() for q in questions], n=1, cutoff=0.4)
    if matches:
        matched_lower = matches[0]
        for q in questions:
            if q.lower() == matched_lower:
                return q
    return None

try:
    df = load_data()

    # Make sure expected columns exist
    expected_columns = [
        "User Question",
        "Suggested Output",
        "Recommended Action",
        "Confidence Level",
        "Business Impact"
    ]

    missing_cols = [col for col in expected_columns if col not in df.columns]
    if missing_cols:
        st.error(f"Missing columns in Excel sheet: {missing_cols}")
    else:
        user_input = st.text_input("Enter your question:")

        if user_input:
            questions_list = df["User Question"].dropna().tolist()
            best_match = find_best_match(user_input, questions_list)

            if best_match:
                result = df[df["User Question"] == best_match].iloc[0]

                st.subheader("Best Match Found")
                st.write(best_match)

                st.subheader("Insight")
                st.write(result["Suggested Output"])

                st.subheader("Recommended Action")
                st.write(result["Recommended Action"])

                st.subheader("Confidence Level")
                st.write(result["Confidence Level"])

                st.subheader("Business Impact")
                st.write(result["Business Impact"])
            else:
                st.warning("No close match found. Try rephrasing your question.")

except Exception as e:
    st.error(f"Error loading system: {e}")
