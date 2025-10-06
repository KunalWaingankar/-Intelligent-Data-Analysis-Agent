# -Intelligent-Data-Analysis-Agent
The project is an Intelligent Data Analysis Agent that answers natural language questions about Olympic data. It works with a cleaned dataset containing information on athletes, countries, events, medals, and more. The goal is to allow users to ask questions in plain English and get precise answers without needing to write code or SQL queries.

The system works in a step-by-step pipeline:
Step 1: Data Preparation<br>
•	The dataset is first preprocessed to ensure consistency.<br>
•	Any missing or redundant information is removed.<br>
•	A “Total” column is added to sum up Gold, Silver, and Bronze medals for each entry.<br>
•	This ensures all numerical calculations can be performed easily.<br>
Step 2: Question Interpretation
•	The user inputs a question in plain English, like:
“Which country got the 6th highest Gold medal count in 2016?”
•	The system sends this question to the Gemini AI API.
•	The AI is guided by a prompt that provides context about the dataset:
o	Column names (Year, Gold, Silver, Bronze, region, etc.)
o	Types of queries supported (sum, mean, top, count)
o	Expected structured output format
•	The AI converts the question into a structured query dictionary, which clearly specifies:
o	operation → e.g., top, sum, mean
o	columns → which columns to work on (Gold, Total)
o	filter → any conditions like year, country, or gender
o	group_by → field to group results (e.g., region)
o	nth_place → if a specific ranking is requested
•	Example structured query for the previous question:
•	{
•	  "operation": "top",
•	  "columns": ["Gold"],
•	  "filter": {"Year": 2016},
•	  "group_by": "region",
•	  "nth_place": 6
•	}
•	This step ensures that even complex questions are converted into a machine-understandable format.
Step 3: Query Execution
•	The structured query is passed to the execution module.
•	Using pandas, the following steps are performed:
o	Apply filters to the dataset based on Year, region, gender, etc.
o	Group data if group_by is specified.
o	Perform the operation (sum, mean, top, count) on the specified columns.
o	Handle ranking operations like top N or nth_place.
•	The output is ready to be displayed.
Step 4: Logging
•	Every interaction is logged for tracking purposes.
•	Logs include the question, structured query, and the final answer.
•	This helps in debugging, improving prompts, and monitoring usage.
