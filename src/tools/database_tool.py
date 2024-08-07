# src/tools/database_tool.py
from langchain.tools import BaseTool

class DatabaseTool(BaseTool):
    name = "Database"
    description = "Fetch campaign data from the database"

    def _run(self, tool_input: dict) -> dict:
        print(f"[DatabaseTool] Running with input: {tool_input}")
        campaign_id = tool_input.get('campaign_id')
        # Simulated database fetch
        result = {
            'campaign_id': str(campaign_id),
            'spend': 5000,
            'conversions': 10,
            'impressions': 10000,
            'clicks': 200,
            'date_range': '2024-06-01 to 2024-06-30'
        }
        print(f"[DatabaseTool] Result: {result}")
        return result