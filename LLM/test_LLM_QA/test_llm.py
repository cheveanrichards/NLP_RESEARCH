import sys
import os

# Step 1: Construct the relative paths to the directories containing myclass1.py and myclass2.py
current_directory = os.path.dirname(__file__)
Recommender_path = os.path.join(current_directory, '..')

# Step 2: Add the directories to the Python path
sys.path.append(Recommender_path)

from LLM import Recommender

recommender = Recommender()

# Set the model
llama3 = "meta/meta-llama-3-8b-instruct"
recommender.set_model(llama3)

# Set the data path
current_directory = os.path.dirname(__file__)
# store_location = os.path.abspath(os.path.join(current_directory, '..', '..', 'Store'))


cluster_location = os.path.abspath(os.path.join(current_directory, '..', '..','Store', 'cluster_5'))

# Load the data and create the index
recommender.load_data(cluster_location)

# Create the query engine
recommender.create_query_engine()

# # Query the data
# response = recommender.query("How many files have fatal accidents and what is the common cause for fatal accidents. How would you prevent?")
# print(response)

# Query the data
response = recommender.query("What are the similarities in Analysis and pilot information. Provide recommendation and preventive measure")
print(response)




