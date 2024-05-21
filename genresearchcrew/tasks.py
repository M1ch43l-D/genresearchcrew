from crewai import Task
from agents import ResearchAgents

class ResearchTasks:
    def get_research_task(self, agent, topic, info):
        return Task(
            description=(
                f"""
                Conduct a thorough search on '{topic}' using DuckDuckGo and SerperDevTool.
                Identify relevant sources and extract key information based on '{info}'.
                Conduct a thorough web search on the following topic: {topic}.
                Focus on identifying relevant and reliable sources of information.
                Extract and compile data in a structured format, suitable for analysis and reporting.
                Emphasize the accuracy and depth of the information retrieved.
                Your final report should clearly articulate the key findings and their sources.
                """
            ),
            expected_output='A collection of URLs and user-specified information from the sources found.',
            agent=agent
        )

    def get_data_compilation_task(self, agent, data):
        return Task(
            description=(
                "Compile the research findings into a CSV file, ensuring the data is well-structured and organized "
                "according to user-specified criteria."
            ),
            expected_output='A CSV file containing URLs and user-specified information from the sources found.',
            agent=agent,
            inputs={'data': data}
        )
