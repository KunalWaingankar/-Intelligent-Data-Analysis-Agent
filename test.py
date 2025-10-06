import pandas as pd
from data_agent import DataAgent
import preprocessor

df = pd.read_csv("athlete_events.csv")
region_df = pd.read_csv("noc_regions.csv")
df_clean = preprocessor.preprocess(df, region_df)

agent = DataAgent(df_clean)

q1 = """How many total medals did Germany win in 2004?"""
print(q1)
print(agent.ask(q1))
