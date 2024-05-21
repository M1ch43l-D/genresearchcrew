import os
from textwrap import dedent
from crewai import Agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_groq import ChatGroq
from tools.search_tools import SearchTools
from tools.csvtool import CSVCreationTool



class ResearchAgents:
    def __init__(self):
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama3-70b-8192"
        )

    def web_researcher(self):
        return Agent(
            role="Web Researcher",
            goal="Retrieve accurate and relevant data from the web.",
            backstory=dedent("""\
                Driven by curiosity, adept at navigating complex information landscapes,
                this agent thrives on uncovering information that is both relevant and precise,
                ensuring the data's accuracy and relevance for downstream processing."""),
            tools=[
                SearchTools.search_internet,
                SearchTools.search_instagram,
                DuckDuckGoSearchRun()

            ],
            llm=self.llm,
            verbose=True,
            memory=True,
            allow_delegation=True
        )

    def data_organizer(self):
        return Agent(
            role="Data Organizer",
            goal=dedent("""\
                Organize and store data in a structured format in a CSV file,
                ensuring that data is not only accurately inputted but also easily accessible
                for further analysis and reporting."""),
            backstory=dedent("""\
                Methodical and meticulous, the Data Organizer values structure and clarity,
                specializing in the systematic organization of information to ensure accuracy
                and accessibility within digital formats."""),
            tools=[
            ],
            llm=self.llm,
            verbose=True,
            allow_delegation=True
        )