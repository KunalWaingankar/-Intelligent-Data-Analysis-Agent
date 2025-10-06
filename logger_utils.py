import pandas as pd
import json
import os
from datetime import datetime
def log_interaction(question, query_dict, answer):
        """
        Save every question + structured query + answer in logs.json
        """
        def make_serializable(obj):
            if isinstance(obj, pd.DataFrame):
                return obj.to_dict(orient="records")
            elif isinstance(obj, pd.Series):
                return obj.to_dict()
            elif isinstance(obj, (int, float, str, dict, list)):
                return obj
            else:
                return str(obj)

        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "question": question,
            "structured_query": make_serializable(query_dict),
            "answer": make_serializable(answer)
        }

        with open("logs.json", "a") as f:
            json.dump(log_entry, f)
            f.write("\n")
