import pandas as pd
from preprocessor import preprocess
import json
import google.generativeai as genai
import os
from logger_utils import log_interaction
from execute_query import execute_query
from interpret_question import interpret_question

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

class DataAgent:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        if all(col in df.columns for col in ["Gold", "Silver", "Bronze"]):
            self.df["Total"] = df[["Gold","Silver","Bronze"]].sum(axis=1)

    def ask(self, question: str):
        query_dict = interpret_question(question, df_columns=self.df.columns)
        answer = execute_query(self.df, query_dict)
        log_interaction(question, query_dict, answer)
        return answer