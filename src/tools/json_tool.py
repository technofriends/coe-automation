# src/tools/json_tool.py
from langchain.tools import BaseTool

class JSONTool(BaseTool):
    name = "JSON Analyzer"
    description = "Analyze campaign data and provide insights"

    def _run(self, tool_input: dict) -> dict:
        print(f"[JSONTool] Running with input: {tool_input}")
        data = tool_input.get('data', {})
        try:
            spend = float(data.get('spend', 0))
            conversions = int(data.get('conversions', 1))
            impressions = int(data.get('impressions', 1))
            clicks = int(data.get('clicks', 0))
            
            insights = {
                'spend_per_conversion': spend / conversions if conversions else 'N/A',
                'click_through_rate': clicks / impressions if impressions else 'N/A',
                'cost_per_click': spend / clicks if clicks else 'N/A'
            }
            
            print(f"[JSONTool] Insights: {insights}")
            return insights
        except Exception as e:
            error_message = f"Error analyzing data: {str(e)}"
            print(f"[JSONTool] {error_message}")
            return {"error": error_message}