# src/tools/pdf_tool.py
from langchain.tools import BaseTool

class PDFTool(BaseTool):
    name = "PDF Generator"
    description = "Generate a PDF report from campaign data"

    def _run(self, tool_input: dict) -> str:
        print(f"[PDFTool] Running with input: {tool_input}")
        data = tool_input.get('data', {})
        try:
            # Simulating PDF report generation...
            report = f"""
            Campaign Report:
            Campaign ID: {data.get('campaign_id', 'N/A')}
            Date Range: {data.get('date_range', 'N/A')}
            Spend: ${data.get('spend', 0)}
            Conversions: {data.get('conversions', 0)}
            Impressions: {data.get('impressions', 0)}
            Clicks: {data.get('clicks', 0)}
            """
            print(f"[PDFTool] Generated report: {report}")
            return report
        except Exception as e:
            error_message = f"Error generating PDF: {str(e)}"
            print(f"[PDFTool] {error_message}")
            return error_message