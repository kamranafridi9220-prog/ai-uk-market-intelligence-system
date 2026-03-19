import streamlit as st

st.set_page_config(
    page_title="AI Market Intelligence Engine",
    layout="wide",
)

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
h1, h2, h3 {
    color: #1f77b4;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
# 🚀 AI Market Intelligence Engine

### Turn business questions into strategic decisions using AI

---
""")

st.markdown("""
A decision intelligence platform combining:

- Semantic search (NLP embeddings)
- Structured business datasets
- GPT-powered strategic reasoning

👉 Use the sidebar to navigate through the product.
""")

st.markdown("---")

st.markdown("## 🚀 Live Product Demo")

st.write("""
This is a working prototype of an AI-powered decision intelligence system.

It demonstrates how businesses can:
- Ask natural language questions
- Retrieve structured insights
- Generate AI-driven strategic recommendations
- Export decision-ready reports

👉 Use the sidebar to explore the system.
""")

st.markdown("## 💼 Use Cases")

st.write("""
- 📊 Market expansion strategy  
- 📈 Customer behaviour analysis  
- 🧠 Sales decision support  
- 📍 Location-based intelligence  
- 📉 Risk and opportunity identification  
""")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🧠 Semantic AI")
    st.write("Understands meaning, not just keywords")

with col2:
    st.markdown("### 🤖 GPT Reasoning")
    st.write("Generates strategic business insights")

with col3:
    st.markdown("### ⚡ Real-time Decisions")
    st.write("Instant answers for business questions")

st.markdown("## What this product does")

st.write("""
This system helps users ask business questions in natural language and receive:
- matched business insights
- recommended actions
- confidence levels
- business impact
- AI strategic summaries
- downloadable AI reports
""")

st.markdown("## Product Pages")

st.write("""
Use the sidebar to access:

- *Ask AI* → Main question-answer system  
- *Upload Data* → Upload your own Excel dataset  
- *About* → Product overview and builder profile  
""")

st.markdown("---")
st.caption("AI Product Prototype | Built by Kamran Khan")
