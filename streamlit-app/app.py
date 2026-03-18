import streamlit as st

st.set_page_config(
    page_title="AI Market Intelligence Engine",
    layout="wide",
)

st.title("🚀 AI Market Intelligence Engine")

st.markdown("""
A decision intelligence platform combining:

- Semantic search (NLP embeddings)
- Structured business datasets
- GPT-powered strategic reasoning

👉 Use the sidebar to navigate through the product.
""")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("AI Search", "Semantic")

with col2:
    st.metric("Reasoning", "GPT-Powered")

with col3:
    st.metric("Mode", "SaaS Prototype")

st.markdown("## What this product does")

st.write("""
This system helps users ask business questions in natural language and receive:
- matched business insights
- recommended actions
- confidence levels
- business impact
- AI strategic summaries
""")

st.markdown("## Product Pages")

st.write("""
Use the sidebar to access:

- *Ask AI* → Main question-answer system
- *Upload Data* → Upload your own Excel dataset
- *About* → Product overview and builder profile
""")

st.markdown("---")
st.caption("Built by Kamran Khan | AI + Business Intelligence + Semantic Search")
