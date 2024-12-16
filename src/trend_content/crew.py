import os
import requests
from langchain_openai import ChatOpenAI
from appdirs import user_data_dir
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from dotenv import load_dotenv
from crewai_tools import SerperDevTool, DallETool


# Uncomment the following line to use an example of a custom tool
# from trend_content.tools.custom_tool import MyCustomTool

#from langtrace_python_sdk import langtrace
#langtrace.init(api_key = os.getenv('LANGTRACE_API_KEY'))


#Lade Umgebungsvariablen aus der .env-Datei
load_dotenv()

serper_api_key = os.getenv('SERPER_API_KEY')
search_tool = SerperDevTool()
image_tool = DallETool(model="dall-e-3",
                       size="1024x1024",
                       quality="standard",
                       n=1)

manager_llm = ChatOpenAI(model_name="gpt-4")

def download_image(image_url, output_path):
    try:
        print(f"Downloading image from: {image_url}")  # Debug: URL ausgeben
        response = requests.get(image_url)
        response.raise_for_status()  # Überprüfe HTTP-Fehler
        with open(output_path, "wb") as file:
            file.write(response.content)
        print(f"Bild erfolgreich gespeichert: {output_path}")
    except Exception as e:
        print(f"Fehler beim Herunterladen des Bildes: {e}")


def process_dalle_output(output, download_image_func):
    """Verarbeitet die Ausgabe des DALL·E-Tools und lädt das Bild herunter."""
    print(f"RAW OUTPUT: {output}")  # Debug: Gib die gesamte Ausgabe aus
    
    if isinstance(output, dict):
        image_url = output.get("image_url")
        print(f"Image URL: {image_url}")  # Debug: Prüfe, ob die URL vorhanden ist

        if image_url:
            # Speicherpfad vorbereiten
            os.makedirs("output", exist_ok=True)
            output_path = os.path.join("output", "generated_image.png")

            # Lade das Bild herunter
            download_image_func(image_url, output_path)
            print(f"Bild gespeichert unter: {output_path}")

            return {
                "image_description": output.get("description", ""),
                "image_url": image_url,
                "local_path": output_path
            }
        else:
            print("Keine Image URL gefunden!")
    return output



@CrewBase
class TrendContent():
	"""TrendContent crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'


	@before_kickoff # Optional hook to be executed before the crew starts
	def pull_data_example(self, inputs):
		# Example of pulling data from an external API, dynamically changing the inputs
		inputs['extra_data'] = "This is extra data"
		return inputs

	@after_kickoff # Optional hook to be executed after the crew has finished
	def log_results(self, output):
		# Example of logging results, dynamically changing the output
		print(f"Results: {output}")
		return output

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			tools=[search_tool], 
			verbose=True,
			output_processor=lambda output: str(output)
		)


	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			tools=[],
			verbose=True,
		)
	
	@agent
	def strategy_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['strategy_agent'],
			tools=[],
			verbose=True,
		)
	
	@agent
	def copy_creator(self) -> Agent:
		return Agent(
			config=self.agents_config['copy_creator'],
			tools=[],
			verbose=True,
			output_processor=lambda output: output.get("dalle_prompt", "") if isinstance(output, dict) else str(output)
		)
	
	@agent
	def content_creator(self) -> Agent:
		return Agent(
			config=self.agents_config['content_creator'],
			tools=[image_tool],
			verbose=True,
			callback=lambda output: process_dalle_output(output, download_image)
		)
				

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			output_file='output/research.md'
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			output_file='output/report.md'
		)

	@task
	def strategy_task(self) -> Task:
		return Task(
			config=self.tasks_config['strategy_task'],
			output_file='output/strategy.md'
		)

	@task
	def copy_creation_task(self) -> Task:
		return Task(
			config=self.tasks_config['copy_creation_task'],
			output_file='output/copy_creation.md'
		)

	@task
	def content_creation_task(self) -> Task:
		return Task(
			config=self.tasks_config['content_creation_task'],
			output_file='output/content_creation.md'
		)


	@crew
	def crew(self) -> Crew:
		"""Creates the TrendContent crew"""

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			planning=True,
			manager_llm=manager_llm,
			process=Process.hierarchical,
			#process=Process.sequential,
			memory=True,
			verbose=True,
		)
