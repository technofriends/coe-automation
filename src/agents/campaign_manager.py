from crewai import Agent
from langchain.llms import OpenAI
from tools.database_tool import DatabaseTool
from tools.pdf_tool import PDFTool
from tools.json_tool import JSONTool
from tools.optimizer_tool import OptimizerTool
from tools.email_tool import EmailTool

def create_campaign_manager(llm):
    return Agent(
        role='Campaign Manager',
        goal='Oversee the campaign management process and delegate tasks effectively.',
        backstory='A seasoned campaign manager with a knack for understanding user queries and effectively delegating tasks to specialized agents.',
        allow_delegation=True,
        llm=llm,
        tools=[DatabaseTool(), PDFTool(), JSONTool(), OptimizerTool(), EmailTool()],
        verbose=True
    )