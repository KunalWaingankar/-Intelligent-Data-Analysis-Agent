import streamlit as st
import pandas as pd
from data_agent import DataAgent
from preprocessor import preprocess

# Load and preprocess data
@st.cache_data
def load_data():
    df = pd.read_csv("athlete_events.csv")
    region_df = pd.read_csv("noc_regions.csv")
    df_clean = preprocess(df, region_df)
    return df_clean

df_clean = load_data()
agent = DataAgent(df_clean)

# Streamlit UI
st.title("🏅 Olympic Data Agent")
st.write("Ask any question about Olympic medals, athletes, or countries!")

question = st.text_input("Enter your question:")

if st.button("Ask"):
    if question.strip() == "":
        st.warning("Please enter a question!")
    else:
        with st.spinner("Thinking..."):
            answer = agent.ask(question)
        st.success("Answer:")
        if isinstance(answer, dict):
            st.json(answer)
        else:
            st.json({str(answer)})

