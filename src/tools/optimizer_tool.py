# src/tools/optimizer_tool.py
from langchain.tools import BaseTool

class OptimizerTool(BaseTool):
    name = "Campaign Optimizer"
    description = "Suggest optimizations based on campaign insights"

    def _run(self, tool_input: dict) -> dict:
        print(f"[OptimizerTool] Running with input: {tool_input}")
        insights = tool_input.get('insights', {})
        try:
            spend_per_conversion = insights.get('spend_per_conversion', 'N/A')
            click_through_rate = insights.get('click_through_rate', 'N/A')
            cost_per_click = insights.get('cost_per_click', 'N/A')

            optimizations = []
            if spend_per_conversion != 'N/A' and float(spend_per_conversion) > 100:
                optimizations.append("Consider optimizing landing pages to improve conversion rate")
            if click_through_rate != 'N/A' and float(click_through_rate) < 0.05:
                optimizations.append("Review ad copy and visuals to improve click-through rate")
            if cost_per_click != 'N/A' and float(cost_per_click) > 10:
                optimizations.append("Adjust bidding strategy to reduce cost per click")

            result = {"optimizations": optimizations} if optimizations else {"message": "No specific optimizations suggested based on available data"}
            print(f"[OptimizerTool] Result: {result}")
            return result
        except Exception as e:
            error_message = f"Error optimizing campaign: {str(e)}"
            print(f"[OptimizerTool] {error_message}")
            return {"error": error_message}