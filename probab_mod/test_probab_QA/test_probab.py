import sys
import os
from pprint import pprint


# Step 1: Construct the relative paths to the directories containing myclass1.py and myclass2.py
current_directory = os.path.dirname(__file__)
IncidentReporter_path = os.path.join(current_directory, '..')
KnowledgeGraph_path = os.path.join(current_directory, '..','..','data_clean_mod')


# Step 2: Add the directories to the Python path
sys.path.append(IncidentReporter_path)
sys.path.append(KnowledgeGraph_path)

from probab import IncidentCategorizer
from extract import KnowledgeGraph

test_pdf_location =  os.path.abspath(os.path.join(current_directory, '..','..', 'samplepdf'))



# Step 1 Generate KnowledgeGraph before using the probabilities module*******************************************
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

pprint(updated_knowledgeGraph)



# Step 2 Use knowledgegraph to calculate incident*******************************************

# Example usage
pattern_dict = {
    'pilot_error_pattern': [
        r"\bpilot.*(loss.*control|loss|failed.*maintain|failed|failure|alcohol|drunk|forgot|forget|did.*not|lack|error|"
        r"mistake|misjudg|miscalcula|distraction|inattention|fatigue|confusion|unfit|improper|negligence|error|"
        r"incorrect|poor.*judgment|wrong.*decision|insufficient|miscommunication|wrong.*action|incorrect.*procedure|"
        r"failure.*recognize)\b"
    ],
    'weather_condition_pattern': [
        r"\bbird.*strike\b",
        r"\blighting.*strike\b",
        r"\bbird\b",
        r"\bweather\b",
        r"\bbad.*weather\b",
        r"\bunfavorable.*weather.*conditions\b",
        r"\bstorm\b",
        r"\bwind.*speed\b",
        r"\brain\b",
        r"\bvisibility\b",
        r"\bturbulence\b",
        r"\blightning\b",
        r"\bthunderstorm\b"
    ],
    'engine_fail_pattern': [r"\b(engine|power loss|propeller|coils|distributor|failed|anomalies|loss of power)\b",
                    r"\bloss.*engine\b"] 
}


section_keys = [
    # "Aviation Investigation Final Report",
    "Analysis",
    "Probable Cause and Findings",
    "Factual Information",
    # "Pilot Information",
    # "Aircraft and Owner/Operator Information",

    # "Meteorological Information and Flight Plan",
    # "Airport Information",
    # "Wreckage and Impact Information",
    # "Administrative Information"
    ]



categorized_data = IncidentCategorizer(pattern_dict).calculate_probabilities(updated_knowledgeGraph, section_keys)


# Define thresholds
thresholds = {
    'pilot_error_pattern': (0.40, None),  # At least 0.33
    'weather_condition_pattern': (0, 1),  # Less than 0.33
    'engine_fail_pattern': (0, 1)  # At least 0.33
}

# Filter and copy incidents
source_path = test_pdf_location
dest_path = os.path.abspath(os.path.join(current_directory, 'tempdir'))
copied_files = IncidentCategorizer(pattern_dict).filter_and_copy_incidents(categorized_data, thresholds, source_path, dest_path)
print(f"Copied files: {copied_files}")
