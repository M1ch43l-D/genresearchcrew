import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task
from agents import ResearchAgents
from tasks import ResearchTasks

load_dotenv()

tasks = ResearchTasks()
agents = ResearchAgents()

topic = "Remote Entry Level Tech Jobs for Cyber Security"
info = "Salary, Required Experience, Application Link, Date Posted, Company Name, Expected Company Size, Job Role, Job Description"

web_researcher = agents.web_researcher()
data_organizer = agents.data_organizer()

web_search = tasks.get_research_task(web_researcher, topic, info)

research_crew = Crew(
    agents=[web_researcher],
    tasks=[web_search],
    verbose=True,
    memory=True,
    process=Process.sequential
)

research_results = research_crew.kickoff()

if research_results:
    gathered_data = research_results['outputs']

    data_entry = tasks.get_data_compilation_task(data_organizer, gathered_data)

    data_crew = Crew(
        agents=[data_organizer],
        tasks=[data_entry],
        verbose=True,
        process=Process.sequential
    )

    entry_results = data_crew.kickoff(inputs={'data': gathered_data})

    print("\n\n########################")
    print("## Here are the results of the web research and data entry")
    print("########################\n")
    print("Web Research Output:")
    print(research_results)
    print("Data Entry Output:")
    print(entry_results)
