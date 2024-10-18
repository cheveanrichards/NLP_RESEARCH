from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
import json

app = FastAPI()

# Step 1: Construct the relative paths to the directories containing myclass1.py and myclass2.py
current_directory = os.path.dirname(__file__)
store_location = os.path.abspath(os.path.join(current_directory, '..','Store', 'KnowledgeGraph','myGraph.json'))
generator_path = os.path.abspath(os.path.join(current_directory, '..','Hugging_face_LLMs'))
saved_model_path = os.path.abspath(os.path.join(current_directory, '..','Hugging_face_LLMs','test_QA_LLM','saved_model'))

replicate_path = os.path.abspath(os.path.join(current_directory, '..','Replicate_LLM'))

# Step 2: Add the directories to the Python path
sys.path.append(store_location)
sys.path.append(generator_path)
sys.path.append(saved_model_path)
sys.path.append(replicate_path)

from GPT2_LLM import GPT2TextGenerator
generator = GPT2TextGenerator()

from LLM import Recommender
recommender = Recommender('')
# Set the model
llama3 = "meta/meta-llama-3-8b-instruct"
recommender.set_model(llama3)


# #load generator and provide prompt to reformat json file to provide return value
# #loading generator takes time so it is good to load on server starting then promp engine via GET,PUT, POST, DELETE 
# prompt = "refactor/ reformating prompt on a given file path or json object"
# generator.load_model(saved_model_path, temperature=0.8, top_p=0.95)
# response_after_load = generator.generate_text(prompt)
# # print(response_after_load)




origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:55722",
    "http://localhost:55257",
    "http://localhost:54128",
    "http://localhost:49333",
    "http://localhost:49958",
    "http://localhost:60543",
    "http://localhost:53536"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# New route to serve JSON file
@app.get("/knowlege_graph/")
async def serve_json():
    file_path = store_location  # Update this with your file path

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/locations" )
async def get_locations():
# read file location full knowledge graph or cluster
# use the gen ai to read a reformat in array [name, lattitude, logitude, details] provide sample format in prompt

    return [
    {
        "name": "Skwentna, Alaska",
        "lat": 61.9653,
        "long": -151.1694,
        "details": "File: 91622.pdf, Date: July 23, 2015, Aircraft: Champion 7GCBC, Injuries: 2 None, Cause: Pilot's improper decision to land on unsuitable surface"
    },
    {
        "name": "Eagles Mere, Pennsylvania",
        "lat": 41.4115,
        "long": -76.5825,
        "details": "File: 91623.pdf, Date: July 23, 2015, Aircraft: Kinner Sportster B, Injuries: 1 None, Cause: Loss of engine power, reason undetermined"
    },
    {
        "name": "Albertson, North Carolina",
        "lat": 35.2304,
        "long": -77.7180,
        "details": "File: 91627.pdf, Date: July 25, 2015, Aircraft: Cessna A188B, Injuries: 1 Minor, Cause: Pilot's failure to maintain clearance from wires due to alcohol impairment"
    }
]

# @app.post("/analyze_files/")
# async def analyze_files(file_path: str = Body(...), prompt: str = Body(...)):
#     if not os.path.exists(file_path):
#         raise HTTPException(status_code=404, detail="File path not found")

#     if not os.path.isdir(file_path):
#         raise HTTPException(status_code=400, detail="Provided path is not a directory")

#     try:
#         # Get list of JSON files in the directory
#         files = [f for f in os.listdir(file_path) if f.endswith('.json') and os.path.isfile(os.path.join(file_path, f))]

#         if not files:
#             return {
#                 "file_path": file_path,
#                 "files_analyzed": [],
#                 "analysis": "No JSON files found in the specified directory."
#             }

#         # Read contents of JSON files
#         file_contents = {}
#         for file in files:
#             file_path_full = os.path.join(file_path, file)
#             try:
#                 with open(file_path_full, 'r') as f:
#                     file_contents[file] = json.load(f)
#             except json.JSONDecodeError:
#                 print(f"Warning: {file} is not a valid JSON file. Skipping.")

#         # Prepare the prompt with file contents
#         files_prompt = "\n".join([f"File: {name}\nContents: {contents}" 
#                                   for name, contents in file_contents.items()])
#         analysis_prompt = f"Analyze the following JSON files:\n\n{files_prompt}\n\n{prompt}"

#         # Generate analysis using the GPT2 model
#         generator.load_model(saved_model_path, temperature=0.8, top_p=0.95)
#         analysis = generator.generate_text(analysis_prompt)

#         return {
#             "file_path": file_path,
#             "files_analyzed": list(file_contents.keys()),
#             "analysis": analysis
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.get("/recommender/{cluster_name}")
async def replicate_llm(cluster_name: str, prompt: str):
    cluster_location = os.path.abspath(os.path.join(current_directory, '..', 'Store', f'{cluster_name}'))

    if not os.path.exists(cluster_location):
        raise HTTPException(status_code=404, detail=f"Cluster {cluster_name} not found")

    # Load the data and create the index
    recommender.load_data(cluster_location)

    # Create the query engine
    recommender.create_query_engine()

    # Query the data using the provided prompt
    response = recommender.query(prompt)
    return response

@app.get("/directories")
async def get_directories():
    store_path = os.path.abspath(os.path.join(current_directory, '..', 'Store'))
    
    if not os.path.exists(store_path):
        raise HTTPException(status_code=404, detail="Store directory not found")
    
    try:
        # Get all directory names in the Store folder
        directories = [name for name in os.listdir(store_path) 
                    if os.path.isdir(os.path.join(store_path, name))]
        return directories
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
