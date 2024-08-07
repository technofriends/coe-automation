from langchain.tools import BaseTool

class EmailTool(BaseTool):
    name = "Email Tool"
    description = "Send emails with the specified content"

    def _run(self, tool_input: dict) -> str:
        print(f"[EmailTool] Running with input: {tool_input}")
        recipient = tool_input.get('recipient', 'default@example.com')
        content = tool_input.get('content', '')
        formatted_content = self.format_content(content)
        print(f"Sending email to {recipient} with content:\n{formatted_content}")
        return f"Email sent to {recipient}"

    def format_content(self, content):
        if isinstance(content, dict):
            formatted_content = "\n".join([f"{key}: {value}" for key, value in content.items()])
        else:
            formatted_content = content
        return formatted_content