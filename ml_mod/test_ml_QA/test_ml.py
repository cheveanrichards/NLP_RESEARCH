
import sys
import os

# Step 1: Construct the relative paths to the directories containing myclass1.py and myclass2.py
current_directory = os.path.dirname(__file__)
Reporter_path = os.path.join(current_directory, '..')

# Step 2: Add the directories to the Python path
sys.path.append(Reporter_path)

from ml import ReportProcessor

current_directory = os.path.dirname(__file__)
store_location = os.path.abspath(os.path.join(current_directory, '..','..','Store', 'KnowledgeGraph','myGraph.json'))
cluster_output_path = os.path.abspath(os.path.join(current_directory,'..','..','Store'))

processor = ReportProcessor(store_location)

try:
        # Get embeddings for specific sections of a specific report
        embeddings = processor.get_section_embedding('91622.pdf', ['Analysis', 'Pilot Information'])
        print(embeddings)
        
        # Get embeddings for specific sections across all reports
        all_combined_embeddings = processor.get_all_combined_embeddings(['Analysis', 'Pilot Information'])
        for report, embeddings in all_combined_embeddings.items():
            print(f"{report}: {embeddings}")
        
        # Cluster reports based on specific sections' embeddings and save to JSON files
        clustered_reports = processor.cluster_and_save_reports(['Analysis', 'Pilot Information'], cluster_output_path)
        for cluster_id, reports in clustered_reports.items():
            print(f"Cluster {cluster_id}: {reports}")
            
except (KeyError, ValueError) as e:
    print(e)