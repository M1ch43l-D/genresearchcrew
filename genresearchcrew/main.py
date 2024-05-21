import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task
from agents import ResearchAgents
from tasks import ResearchTasks

load_dotenv()

# Initialize tasks and agents
tasks = ResearchTasks()
agents = ResearchAgents()

# Define the topic and information
topic = "Remote Entry Level Tech Jobs for AI and Cyber Security"
info = "Salary, Required Experience, Application Link, Date Posted, Company Name, Expected Company Size, Job Role, Job Description"

# Initialize agents
web_researcher = agents.web_researcher()
data_organizer = agents.data_organizer()

# Create the research task
web_search = tasks.get_research_task(web_researcher, topic, info)

# Initialize the crew for the research task
research_crew = Crew(
    agents=[web_researcher],
    tasks=[web_search],
    verbose=True,
    memory=True,
    process=Process.sequential
)

# Kick off the research task
research_results = research_crew.kickoff()

if research_results:
    # Extract gathered data from research results
    gathered_data = research_results['outputs']  # Adjust this based on actual output structure

    # Create the data compilation task with the gathered data
    data_entry = tasks.get_data_compilation_task(data_organizer, gathered_data)

    # Initialize the crew for the data entry task
    data_crew = Crew(
        agents=[data_organizer],
        tasks=[data_entry],
        verbose=True,
        process=Process.sequential
    )

    # Kick off the data entry task
    entry_results = data_crew.kickoff(inputs={'data': gathered_data})

    # Print the results
    print("\n\n########################")
    print("## Here are the results of the web research and data entry")
    print("########################\n")
    print("Web Research Output:")
    print(research_results)
    print("Data Entry Output:")
    print(entry_results)
