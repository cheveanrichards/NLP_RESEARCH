import sys
import os
from pprint import pprint

# Step 1: Construct the relative paths to the directories containing myclass1.py and myclass2.py
current_directory = os.path.dirname(__file__)
KnowledgeGraph_path = os.path.join(current_directory, '..')

# Step 2: Add the directories to the Python path
sys.path.append(KnowledgeGraph_path)

from extract import KnowledgeGraph


test_pdf_location =  os.path.abspath(os.path.join(current_directory, '..','..', 'samplepdf'))
test_dict = {
    "Aviation Investigation Final Report": [20, "Analysis"],
    "Analysis": [20, "Probable Cause and Findings"],
    "Probable Cause and Findings": [20, "Factual Information"],

    "Factual Information": [20, "Pilot Information"],
    "Pilot Information": [60, "Aircraft and Owner/Operator Information"],
    "Aircraft and Owner/Operator Information": [60, "Meteorological Information and Flight Plan"],

    "Meteorological Information and Flight Plan": [60, "Airport Information"],
    "Airport Information": [60, "Wreckage and Impact Information"],
    "Wreckage and Impact Information": [30, "Administrative Information"],
    "Administrative Information": [6, "Investigation Docket:"],

}

myTestKnowledgeGraph = KnowledgeGraph()

myTestKnowledgeGraph.process_pdfs_in_directory(test_pdf_location,test_dict)
# pprint(myTestKnowledgeGraph.process_pdfs_in_directory(test_pdf_location,test_dict))


# Modify Knowledge graph by removing words ("keys") from sections
removal_dict = {"Aviation Investigation Final Report": ["location","aircraft damage","defining event",
                                                                               "injuries","accident number","aircraft",
                                                                               " flight conducted under", "date time", "registration","part"],

                                                                               "Probable Cause and Findings": ["personnel issues", "environmental issues", "aicraft", "not determined"],

                                                                               "Factual Information": ["initial climb", "history of flight", "emergency descent"],

                                                                               "Pilot Information": ["certificate", "age", "airplane rating s", "seat occupied", "other aircraft rating s", " restraint used", "instrument rating s", "second pilot present", "instructor rating s", "toxicology performed",
                                                                                                     "medical certification", "last faa medical exam", "occupational pilot", "last flight review or equivalent", "flight time"],

                                                                               "Aircraft and Owner/Operator Information": ["aircraft make","registration","aircraft category","serial number",
                                                                                                                            "year of manufacture", "amateur built","airworthiness certificate", "landing gear type",
                                                                                                                            "seats", "of last inspection","certified max gross wt","time since last inspection","engines",
                                                                                                                            "airframe total time","engine manufacturer","elt","engine","registered owner","rated power","operator",
                                                                                                                            "operating certificate s","held"],


                                                                               "Meteorological Information and Flight Plan": ["conditions at accident site","condition of light","observation facility elevation",
                                                                                                                              "ft msl", "distance from accident site", "nautical miles","observation time", "local",
                                                                                                                              "direction from accident site", "lowest cloud condition", "visibility", "miles", "lowest ceiling",
                                                                                                                              "visibility rvr", "rvr", "knots", "turbulence type", "wind direction", "turbulence severity", "altimeter setting",
                                                                                                                              "inches hg", "point", "precipitation and obscuration", "departure point", "type of flight plan filed",
                                                                                                                              "destination","type of clearance", "departure time", "type of airspace", "class", "wind"],

                                                                               "Airport Information": ["airport", "elevation","condition of light","runway surface type",
                                                                                                        "ft msl", "airport elevation", "runway surface condition", "runway used", "ifr approach", "runway", "vfr"],


                                                                               "Wreckage and Impact Information": ["crew injuries", "aircraft damage","passenger injuries","aircraft fire",
                                                                                                        "ground injuries", "aircraft explosion", "total injuries", "latitude", "longitude", "est"],

                                                                               "Administrative Information": ["investigator in charge iic", "additional participating persons","original publish date"],

                                                                               }


updated_knowledgeGraph = myTestKnowledgeGraph.word_removal(removal_dict)

myTestKnowledgeGraph.to_json(updated_knowledgeGraph,os.path.join(current_directory, '.','myGraph'))

pprint(updated_knowledgeGraph)