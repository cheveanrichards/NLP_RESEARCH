from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import LlamaIndexTool
from llama_index.llms.groq import Groq

class Agents:
    def __init__(self):
        self.groq_llm = None
        self.crew_llm = None
        self.input_files = []
        self.embed_model = None
        self.query_tool = None
        self.agents = []
        self.tasks = []
        self._index = None
        self._query_engine = None

    def setup_llm(self, model_name="groq/llama3-70b-8192", api_key=None, temperature=0.0):
        """
        Setup LLM using CrewAI's LLM module with Groq
        """
        if not api_key:
            raise ValueError("API key is required")
        
        # Create Groq LLM instance for query engine
        self.groq_llm = Groq(
            model="llama3-70b-8192",
            api_key=api_key
        )
        
        # Create CrewAI LLM instance for agents
        self.crew_llm = LLM(
            model=model_name,
            api_key=api_key
        )
        return self

    def set_input_files(self, files):
        """
        Set input files for document processing
        """
        self.input_files = files
        reader = SimpleDirectoryReader(input_files=self.input_files)
        return reader.load_data()

    def set_embedding_model(self, model_name="BAAI/bge-small-en-v1.5"):
        """
        Set and configure embedding model
        """
        self.embed_model = HuggingFaceEmbedding(
            model_name=model_name, 
            cache_folder=None
        )
        return self

    def setup_index_and_query(self, docs, similarity_top_k=5):
        """
        Setup vector store index and query engine
        """
        if not self.groq_llm:
            raise ValueError("LLM must be configured before setting up index")
            
        if not self.embed_model:
            raise ValueError("Embedding model must be configured before setting up index")
            
        self._index = VectorStoreIndex.from_documents(
            docs,
            embed_model=self.embed_model
        )
        
        self._query_engine = self._index.as_query_engine(
            similarity_top_k=similarity_top_k, 
            llm=self.groq_llm
        )
        
        self.query_tool = LlamaIndexTool.from_query_engine(
            self._query_engine,
            name="Cluster Query Tool",
            description="Use this tool to lookup the accident json reports",
        )
        return self._index, self._query_engine, self.query_tool

    def create_agents(self, num_agents, agent_configs):
        """
        Create specified number of agents with given configurations
        """
        if len(agent_configs) != num_agents:
            raise ValueError("Number of agent configurations must match num_agents")
            
        if not self.crew_llm:
            raise ValueError("LLM must be configured before creating agents")

        for config in agent_configs:
            agent = Agent(
                role=config['role'],
                goal=config['goal'],
                backstory=config['backstory'],
                verbose=True,
                allow_delegation=False,
                tools=[self.query_tool] if config.get('needs_tools', False) else [],
                llm=self.crew_llm
            )
            self.agents.append(agent)
        return self

    def create_tasks(self, num_tasks, task_configs):
        """
        Create specified number of tasks with given configurations
        """
        if len(task_configs) != num_tasks:
            raise ValueError("Number of task configurations must match num_tasks")
            
        if len(self.agents) < num_tasks:
            raise ValueError("Not enough agents for tasks")

        for i, config in enumerate(task_configs):
            task = Task(
                description=config['description'],
                expected_output=config['expected_output'],
                agent=self.agents[i]
            )
            self.tasks.append(task)
        return self

    def run_crew(self):
        """
        Create and run the crew with configured agents and tasks
        """
        if not self.agents or not self.tasks:
            raise ValueError("Agents and tasks must be configured before running crew")
            
        crew = Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential  # Specify the process type explicitly
        )
        return crew.kickoff()