import sys
import os
from pprint import pprint

# Step 1: Construct the relative paths to the directories
current_directory = os.path.dirname(__file__)
Agent_path = os.path.join(current_directory, '..')

# Step 2: Add the directories to the Python path
sys.path.append(Agent_path)

from Agents import Agents

def main():
    # Initialize agent system
    agent_system = Agents()

    try:
        # Setup LLM
        agent_system.setup_llm(
            api_key="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"
        )

        # Set embedding model
        agent_system.set_embedding_model("BAAI/bge-small-en-v1.5")

        # Load documents
        docs = agent_system.set_input_files([
            os.path.join(current_directory, '..', '..', '..', '91653.pdf'),
            os.path.join(current_directory, '..', '..', '..', '91658.pdf')
        ])

        # Setup index and query engine
        index, query_engine, query_tool = agent_system.setup_index_and_query(docs)

        # Configure agents
        agent_configs = [
            {
                "role": "Crash Analyst",
                "goal": "Uncover insights about the accidents listed",
                "backstory": "You work for a government investigation agency...",
                "needs_tools": True
            },
            {
                "role": "Data Reporter",
                "goal": "Craft easy to understand reports",
                "backstory": "You are a renowned Data Reporter..."
            }
        ]

        # Configure tasks
        task_configs = [
            {
                "description": "Conduct a comprehensive analysis of the airplane crash",
                "expected_output": "Full analysis report in bullet points"
            },
            {
                "description": "Develop an engaging blog post",
                "expected_output": "Full blog post of at least 4 paragraphs"
            }
        ]

        # Create agents and tasks
        agent_system.create_agents(2, agent_configs)
        agent_system.create_tasks(2, task_configs)

        # Run the crew
        results = agent_system.run_crew()
        
        print("######################")
        print(results)
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()