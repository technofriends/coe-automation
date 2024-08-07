# task_decider.py

import json
import re
# from langchain.chains import LLMChain
from langchain_openai import OpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate


def decide_tasks(query: str, llm) -> list:
    template = """
    You are an intelligent assistant designed to interpret user queries about marketing campaigns and decide the necessary tasks and tools required to fulfill the request.

    User Query: "{query}"

    Based on the user query, determine the tasks and tools needed. Here are the possible tasks:
    - 'generate_campaign_report': Generate a comprehensive report on campaign performance.
    - 'extract_insights_from_report': Analyze the campaign report to extract key insights and trends.
    - 'identify_optimization_opportunities': Review the campaign data and insights to identify areas for improvement. This task should always use the OptimizerTool.
    - 'send_report_through_email': Send the generated report through email.
    - 'send_optimization_suggestions_through_email': Send the optimization suggestions through email.

    Here are the available tools:
    - 'DatabaseTool': Fetch campaign data from the database.
    - 'PDFTool': Generate a PDF report from campaign data.
    - 'JSONTool': Analyze campaign data and provide insights.
    - 'OptimizerTool': Suggest optimizations based on campaign insights.
    - 'EmailTool': Send emails with the specified content.

    Provide a list of tasks with the required tools for each task in JSON format. Ensure each task includes the "task" and "tools" keys.

    Example:
    User Query: "Give me the report for campaign id 234343, which was run in Jun 2024. Send me the report through email. I am also keen on knowing what are the various optimizations we can perform to improve the campaign performance overall."
    Output:
    [
        {{"task": "generate_campaign_report", "tools": ["DatabaseTool", "PDFTool"]}},
        {{"task": "extract_insights_from_report", "tools": ["JSONTool"]}},
        {{"task": "identify_optimization_opportunities", "tools": ["DatabaseTool", "JSONTool", "OptimizerTool"]}},
        {{"task": "send_report_through_email", "tools": ["EmailTool"]}},
        {{"task": "send_optimization_suggestions_through_email", "tools": ["EmailTool"]}}
    ]

    User Query: "{query}"
    Output:
    """

    prompt = PromptTemplate(template=template, input_variables=["query"])
    chain = prompt | llm

    try:
        print(f"Sending request to LLM for query: {query}")
        result = chain.invoke({"query": query})
        print(f"Raw LLM output: {result}")
        
        # Clean up JSON string to handle trailing commas
        result = re.sub(r',\s*(\]|\})', r'\1', result)
        print(f"Cleaned LLM output: {result}")
        
        # Extract the JSON list part from the output
        list_match = re.search(r'\[.*\]', result, re.DOTALL)
        if list_match:
            list_str = list_match.group(0)
            print(f"Extracted JSON string: {list_str}")
            tasks_list = json.loads(list_str)
            print(f"Parsed tasks list: {tasks_list}")
            
            # Validate tasks list format
            for task in tasks_list:
                if "task" not in task or "tools" not in task:
                    raise ValueError(f"Invalid task format: {task}")
            return tasks_list
        else:
            print("Could not find a list in the LLM output")
            print(f"LLM Output: {result}")
            return []
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        print(f"LLM Output: {result}")
        return []
    except Exception as e:
        print(f"Error deciding tasks: {e}")
        return []

