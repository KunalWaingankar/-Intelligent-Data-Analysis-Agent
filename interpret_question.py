import json
import google.generativeai as genai

def interpret_question(question: str, df_columns):
        """
        Send the natural language question to Gemini and get structured JSON query.
        """
        prompt = f"""
        You are a data analyst assistant.
        You are given a pandas DataFrame with columns: {list(df_columns)}
        Your task: Translate the natural language question into a structured JSON query that describes:
        - operation (sum, mean, max, min, count, top, metadata)
        - columns (which columns to use, e.g., Gold, Silver, Bronze)
        - filter (conditions like country, year, sport)
        - group_by (optional column)
        - top_n (optional integer when user requests top N results)
        - metadata_key (required if operation is "metadata")

        Rules:
        1. Use "sum" when the user asks for total medals.
        2. Use "mean", "max", or "min" if clearly requested.
        3. Use "count" if the user asks for number of entries **for a specific year or range of years**. Always include "group_by": "Year" in such cases.
        4. Use "top" when the user asks for the person/country/team with the most, highest, or maximum medals.
        5. Use "metadata" when the user asks for **general statistics across all years** (not filtered by a specific year), such as editions, hosts, sports, events, nations, or total athletes.
        6. When operation is "gender_stats", include "gender" field with value "M" or "F".

        Metadata keys:
        - "editions" → number of Olympic editions (unique years)
        - "hosts" → number of host cities
        - "sports" → number of sports
        - "events" → number of events
        - "nations" → number of participating nations
        - "athletes" → total number of athletes **across all years**

        Include a "top_n" field if the user specifies a number (e.g., top 3, top 5).
        Include an "nth_place" field if the user specifies an ordinal like "5th", "3rd", "2nd" etc., instead of top N.

        Examples:
        - "Who has the most gold medals in swimming?" →
        {{ "operation": "top", "columns": ["Gold"], "filter": {{ "Sport": "Swimming" }}, "group_by": "Name" }}
        - "Top 5 athletes with most gold medals in Swimming" →
        {{ "operation": "top", "columns": ["Gold"], "filter": {{ "Sport": "Swimming" }}, "group_by": "Name", "top_n": 5 }}
        - "Which country won the highest number of gold medals in 2016?" →
        {{ "operation": "top", "columns": ["Gold"], "filter": {{ "Year": [2016, 2016] }}, "group_by": "region" }}
        - "Number of Olympic editions?" →
        {{ "operation": "metadata", "metadata_key": "editions" }}
        - "How many athletes participated?" → **no year filter**
        {{ "operation": "metadata", "metadata_key": "athletes" }}
        - "Number of athletes in 1956?" → **year-specific**
        {{ "operation": "count", "columns": ["Name"], "filter": {{ "Year": [1956, 1956] }}, "group_by": "Year" }}
        - "Number of athletes between 1952 and 1956?" →
        {{ "operation": "count", "columns": ["Name"], "filter": {{ "Year": [1952, 1956] }}, "group_by": "Year" }}
        - "How many male athletes participated in 2016?" →
        {{ "operation": "gender_stats", "gender": "M", "filter": {{ "Year": [2016, 2016] }}}}
        - "Total female athletes in swimming" →
        {{ "operation": "gender_stats", "gender": "F", "filter": {{ "Sport": "Swimming" }}}}

        Question: {question}

        Respond ONLY in valid JSON. Do not include any explanation or extra text.
        """


        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)

        raw_text = response.text.strip()
        # Remove Markdown code block if present
        if raw_text.startswith("```") and raw_text.endswith("```"):
            raw_text = "\n".join(raw_text.split("\n")[1:-1]).strip()

        try:
            structured_query = json.loads(raw_text)
            return structured_query
        except Exception as e:
            return {"error": f"Failed to parse Gemini response: {e}", "raw": raw_text}