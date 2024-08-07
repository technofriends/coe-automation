import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv, find_dotenv
from langchain_openai import OpenAI
from tasks.task_executor import kickoff_process

# Load environment variables
load_dotenv(find_dotenv())

# Initialize OpenAI language model
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

llm = OpenAI(temperature=0.7)

def main():
    user_query = "For campaign id 234343 send me optimization inputs. send your details to vp@gmail.com"
    print(f"Original user query: {user_query}")
    result = kickoff_process(user_query, llm)  # Pass llm here
    print("Raw Result:", result)
    if isinstance(result, dict):
        print("Crew execution completed successfully.")
        print("Final Result:")
        for key, value in result.items():
            print(f"{key.capitalize()}:")
            print(value)
            print("---")
    else:
        print("Unexpected result format. Raw output:")
        print(result)

if __name__ == "__main__":
    main()