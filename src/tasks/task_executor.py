# task_executor.py

import re
from src.tools.database_tool import DatabaseTool
from src.tools.pdf_tool import PDFTool
from src.tools.json_tool import JSONTool
from src.tools.optimizer_tool import OptimizerTool
from src.tools.email_tool import EmailTool

from tasks.task_decider import decide_tasks

def extract_campaign_id(query: str) -> str:
    match = re.search(r'campaign id (\d+)', query, re.IGNORECASE)
    return match.group(1) if match else None

def extract_email(query: str) -> str:
    match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', query)
    return match.group(0) if match else 'default@example.com'

def kickoff_process(query: str, llm):
    try:
        print(f"[kickoff_process] Query : {query}")
        campaign_id = extract_campaign_id(query)
        user_email = extract_email(query)
        print(f"User email found from extract_email is {user_email}")

        if not campaign_id:
            raise ValueError("Campaign ID not found in the query.")

        print(f"Extracted campaign_id: {campaign_id}")
        print(f"Extracted user_email: {user_email}")

        tasks_list = decide_tasks(query, llm)
        print(f"Tasks List: {tasks_list}")

        if not tasks_list:
            return {"tasks_executed": [], "final_output": {}}

        result = {}
        for task_info in tasks_list:
            task_name = task_info.get('task')
            tools = task_info.get('tools', [])
            print(f"Executing task: {task_name}")

            tool_results = {}
            for tool_name in tools:
                tool_instance = globals().get(tool_name)()
                print(f"Using tool: {tool_instance.name}")

                # Prepare the input for each tool based on its type
                if isinstance(tool_instance, DatabaseTool):
                    tool_input = {'campaign_id': campaign_id}
                elif isinstance(tool_instance, JSONTool):
                    tool_input = {'data': result.get('campaign_data', {})}
                elif isinstance(tool_instance, OptimizerTool):
                    tool_input = {'insights': result.get('insights', {})}
                elif isinstance(tool_instance, EmailTool):
                    optimizations = result.get('optimizations', 'No optimizations available')
                    tool_input = {
                        'recipient': user_email,
                        'content': optimizations if optimizations != 'No optimizations available' else {'message': 'No specific optimizations suggested based on available data'}
                    }
                else:
                    tool_input = {'data': result.get('campaign_data', {})}

                tool_result = tool_instance._run(tool_input)
                tool_results[tool_instance.name] = tool_result

                # Update result dictionary based on tool type
                if isinstance(tool_instance, DatabaseTool):
                    result['campaign_data'] = tool_result
                elif isinstance(tool_instance, JSONTool):
                    result['insights'] = tool_result
                elif isinstance(tool_instance, PDFTool):
                    result['pdf_report'] = tool_result
                elif isinstance(tool_instance, OptimizerTool):
                    result['optimizations'] = tool_result

            result[task_name] = tool_results

        # Send emails after processing all tasks
        for task_info in tasks_list:
            task_name = task_info.get('task')
            if task_name == 'send_report_through_email':
                tool_instance = EmailTool()
                tool_input = {
                    'recipient': user_email,
                    'content': result.get('pdf_report', 'No report available')
                }
                tool_instance._run(tool_input)
            elif task_name == 'send_optimization_suggestions_through_email':
                tool_instance = EmailTool()
                optimizations = result.get('optimizations', 'No optimizations available')
                tool_input = {
                    'recipient': user_email,
                    'content': optimizations if optimizations != 'No optimizations available' else {'message': 'No specific optimizations suggested based on available data'}
                }
                tool_instance._run(tool_input)

        final_result = {
            'tasks_executed': [task_info['task'] for task_info in tasks_list],
            'final_output': result
        }
        return final_result
    except Exception as e:
        print(f"Error in process execution: {e}")
        return None
