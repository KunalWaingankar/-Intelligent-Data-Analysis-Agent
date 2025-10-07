# -Intelligent-Data-Analysis-Agent
The project is an Intelligent Data Analysis Agent that answers natural language questions about Olympic data. It works with a cleaned dataset containing information on athletes, countries, events, medals, and more. The goal is to allow users to ask questions in plain English and get precise answers without needing to write code or SQL queries.

Download athlete and event CSV file from here:<br>
Link:- https://drive.google.com/file/d/1gbVxvEoeFVJG7fIsH01-noqIn80oCym8/view?usp=sharing

# Olympics DataAgent Project<br><br>

## How to Run<br>
1. Install dependencies:<br>
   pip install -r requirements.txt<br><br>
2. Place the dataset `athlete_events.csv` in this folder.<br><br>
3. Run the main file:<br>
   python test.py<br><br>
4. `test.py` demonstrates usage of the DataAgent class and sample queries.<br><br>
5. Run the Streamlit UI:<br>
   python -m streamlit run app.py<br>
   Opens a basic interactive UI in your browser:<br><br>

   

## Notes<br>
- Make sure your Gemini API key is set as an environment variable:
  export GEMINI_API_KEY="your_key_here"<br><br>

The system works in a step-by-step pipeline:<br>
Step 1: Data Preparation<br>
•	The dataset is first preprocessed to ensure consistency.<br>
•	Any missing or redundant information is removed.<br>
•	A “Total” column is added to sum up Gold, Silver, and Bronze medals for each entry.<br>
•	This ensures all numerical calculations can be performed easily.<br><br>
Step 2: Question Interpretation<br>
•	The user inputs a question in plain English, like:<br>
“Which country got the 6th highest Gold medal count in 2016?”
•	The system sends this question to the Gemini AI API.<br>
•	The AI is guided by a prompt that provides context about the dataset:<br>
o	Column names (Year, Gold, Silver, Bronze, region, etc.)<br>
o	Types of queries supported (sum, mean, top, count, etc.)<br>
o	Expected structured output format<br>
The AI converts the question into a structured query dictionary, which clearly specifies:<br>
    1.	operation → e.g., top, sum, mean<br>
    2.	columns → which columns to work on (Gold, Total)<br>
    3.	filter → any conditions like year, country, or gender<br>
    4.	group_by → field to group results (e.g., region)<br>
    5.	nth_place → if a specific ranking is requested<br>
•	Example structured query for the previous question:<br>
•	{<br>
•	  "operation": "top",<br>
•	  "columns": ["Gold"],<br>
•	  "filter": {"Year": 2016},<br>
•	  "group_by": "region",<br>
•	  "nth_place": 6<br>
•	}<br>
•	This step ensures that even complex questions are converted into a machine-understandable format.<br><br>
Step 3: Query Execution<br>
•	The structured query is passed to the execution module.<br>
•	Using pandas, the following steps are performed:<br>
o	Apply filters to the dataset based on Year, region, gender, etc.<br>
o	Group data if group_by is specified.<br>
o	Perform the operation (sum, mean, top, count) on the specified columns.<br>
o	Handle ranking operations like top N or nth_place.<br>
•	The output is ready to be displayed.<br><br>
Step 4: Logging<br>
•	Every interaction is logged for tracking purposes.<br>
•	Logs include the question, structured query, and the final answer.<br>
•	This helps in debugging, improving prompts, and monitoring usage.<br>
