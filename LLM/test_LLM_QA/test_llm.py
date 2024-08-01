import os
import sys
#  # Set your OpenAI API key
# openai_api_key = os.getenv("OPENAI_API_KEY")

#     # Ensure the API key is set
# if not openai_api_key:
#     raise ValueError("OpenAI API key not set. Please set the OPENAI_API_KEY environment variable.")


# Setup directory paths
current_directory = os.path.dirname(__file__)
Recommender_path = os.path.join(current_directory, '..')

sys.path.append(Recommender_path)


# import class
from LLM import LLM_RECOMMENDER

recommender = LLM_RECOMMENDER(api_key)

cluster_location =  os.path.abspath(os.path.join(current_directory, '..','..', 'probab_mod/test_probab_QA/tempdir'))

recommender = LLM_RECOMMENDER('')

recommender.read_all_pdfs_in_directory(cluster_location)

# # Get recommendations for a specific file
# file_name = "example.txt"
# print(recommender.analyze_file(file_name))
    
# Get general recommendations for all files
print(recommender.analyze_all_pdfs())
