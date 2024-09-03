from fastapi import FastAPI, HTTPException
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

# Step 2: Add the directories to the Python path
sys.path.append(store_location)
sys.path.append(generator_path)
sys.path.append(saved_model_path)


from GPT2_LLM import GPT2TextGenerator
generator = GPT2TextGenerator()

#load generator and provide prompt to reformat json file to provide return value
#loading generator takes time so it is good to load on server starting then promp engine via GET,PUT, POST, DELETE 
prompt = "refactor/ reformating prompt on a given file path or json object"
generator.load_model(saved_model_path, temperature=0.8, top_p=0.95)
response_after_load = generator.generate_text(prompt)
# print(response_after_load)




origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:55722",
    "http://localhost:57299",
    "http://localhost:54128"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    return {"message": "Hello World"}

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



