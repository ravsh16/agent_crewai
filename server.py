

from crewai import Crew, Agent, Task, LLM
import litserve as ls
from crewai_tools import SerperDevTool
import os 
from dotenv import load_dotenv

load_dotenv()
# ollama pull qwen3 in the command line.

# Uncomment the following line and also the llm=llm line in the Agents definitions.
# llm = LLM(model="ollama/qwen3")

# Initialize Anthropic Claude 3 Haiku using CrewAI's LLM class
# CrewAI automatically reads ANTHROPIC_API_KEY from environment
# Using Claude 3 Haiku (confirmed working with your API key)
llm = LLM(
    model="anthropic/claude-sonnet-4-5-20250929",
    temperature=0.5
)
class AgenticRAGAPI(ls.LitAPI):
    def setup(self, device):
        researcher_agent = Agent(
            role="Researcher",
            goal="Research about the user's query and generate insights",
            backstory="You are a helpful assistant that can answer questions about the document.",
            verbose=True,
            tools=[SerperDevTool()],
            llm=llm
        )

        writer_agent = Agent(
            role="Writer",
            goal="Use the available insights to write a concise and informative response to the user's query",
            backstory="You are a helpful assistant that can write a report about the user's query",
            verbose=True,
            llm=llm
        )
        
        researcher_task = Task(
            description="Research about the user's query and generate insights: {query}",
            expected_output="A concise and informative report about the user's query",
            agent=researcher_agent,
        )

        writer_task = Task(
            description="Use the available insights to write a concise and informative response to the user's query: {query}",
            expected_output="A concise and informative response to the user's query",
            agent=writer_agent,
        )
        
        self.crew = Crew(
            agents=[researcher_agent, writer_agent],
            tasks=[researcher_task, writer_task],
            verbose=True,
        )

    def decode_request(self, request):
        return request["query"]

    def predict(self, query):
        return self.crew.kickoff(inputs={"query": query})

    def encode_response(self, output):
        return {"output": output}

if __name__ == "__main__":
    api = AgenticRAGAPI()
    server = ls.LitServer(api)
    server.run(port=8000, generate_client_file=True)
