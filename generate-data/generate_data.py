import json
import logging
import os
import random

import openai
from dotenv import load_dotenv
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.llms import OpenAI
from langchain.prompts.prompt import PromptTemplate

Logger = logging.getLogger()
Logger.setLevel(logging.INFO)
load_dotenv()
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

template = """You are an AI assistant responsible for generating creative content for a large database of futuristic spaceships to travel around the universe.
Your task is to fill in missing information for a given record of a spaceship. There can be different combinations of travel purpose, ammenities the client will look for and capacity of the ship. You should provide information of both the looks of the spaceship and its technical characteristics. When defining the size of the starship, consider that all the passengers must fit comfortably in it. Consider at least 5 cubic meters per passenger, plus the cargo capacity. You are given the passenger capacity, the purposes of the travel and the issues that are important for the user:
{incomplete_starship}
Use the provided record as a reference, but do not repeat the information that was given to you.
As an example, consider this complete record: {{
        "baseModelName": "Harmony Starcruiser",
        "shortDescription": "Embark on a celestial journey with the Harmony Starcruiser, a small spacecraft designed for both leisure and interstellar collaboration. This compact vessel comfortably accommodates 2-5 passengers, fostering an atmosphere of camaraderie and shared exploration.",
        "purposes": ["leisure", "interstellar collaboration"],
        "importantForUser": ["sustainability", "performance"],
        "passengerCapacity": "2 to 5 individuals",
        "length": "25 meters, 82 feet",
        "width": "15 meters, 49 feet",
        "height": "8 meters, 26 feet",
        "weight": "50000 kilograms",
        "range": "100000 light-years",
        "cargoCapacity": "500 cubic meters",
        "exteriorDescription": ["Customizable Hull Lights: Express individuality with customizable hull lights that not only add a touch of personal style but also contribute to the spacecraft's visibility in the vastness of space.", 
        "Compact Form Factor: Designed for agility and easy maneuverability, the compact form factor of the Harmony Starcruiser ensures versatility in navigating both bustling spaceports and remote celestial destinations.", 
        "Interstellar Collaboration Hub: Featuring collaborative docking stations and communication arrays, the spacecraft is equipped to facilitate interstellar partnerships and joint ventures, enhancing its functionality beyond leisure."],
        "interiorDescription": "With plush seating, panoramic windows, and collaborative workspaces, the Harmony Starcruiser seamlessly blends relaxation and productivity, making it the ideal choice for those seeking leisure and interstellar teamwork amidst the vast wonders of space."
        }}
Based on this, please provide only one suitable value for only the FIELDDESCRIPTION in JSON format.
Your answer should be only FIELDNAME field in JSON format. This means, as if the answer was the content of JSON file. Remember that this means that the answer you provide MUST be between curly brackets."""

def document_features(document, new_name, result_replace, prompt_text):
    prompt = PromptTemplate(input_variables=["FEATURE"], template=prompt_text)
    chatgpt_chain = LLMChain(
        llm=OpenAI(temperature=0.5),
        prompt=prompt,
        verbose=True,
        memory=ConversationBufferWindowMemory(k=5)
    )
    result = chatgpt_chain.predict(
        FEATURE=new_name
    )
    document = document.replace(result_replace, result)
    return document, result  

def get_features_data(this_ship_funcs_necs, shipfeatures_markdown_template, shipdescription_markdown_template):
    i = 1
    for item in this_ship_funcs_necs:
        shipfeatures_markdown_template = shipfeatures_markdown_template.replace("FEATURE" + str(i), item)
        shipfeatures_markdown_template, name_result = document_features(shipfeatures_markdown_template, item, "feature" + str(i) + "Name", "Please name one feature for {FEATURE} in a spaceship. Only name it, use maximum five words.")
        shipfeatures_markdown_template = shipfeatures_markdown_template.replace("feature" + str(i) + "Name", name_result)
        shipdescription_markdown_template = shipdescription_markdown_template.replace("#### feature" + str(i) + "Name", "#### " + name_result)
        shipdescription_markdown_template, _ = document_features(shipdescription_markdown_template, name_result, "feature" + str(i) + "Description", "Please provide a detailed description of {FEATURE} in a spaceship. It should be two to four lines long.")
        i=i+1
        
    return shipfeatures_markdown_template, shipdescription_markdown_template


def lambda_handler(event, passengers, purposes, this_ship_funcs_necs, context):
    with open('shipfeatures_markdown_template.md', 'r') as f:
        shipfeatures_markdown_template = f.read()
    with open('shipdescription_markdown_template.md', 'r') as f:
        shipdescription_markdown_template = f.read()
    shipfeatures_markdown_template, shipdescription_markdown_template = get_features_data(this_ship_funcs_necs, shipfeatures_markdown_template, shipdescription_markdown_template)
    shipfeatures_markdown_template = shipfeatures_markdown_template.replace("PURPOSES", purposes)
    shipfeatures_markdown_template = shipfeatures_markdown_template.replace("minCrew", str(passengers[0]))
    shipfeatures_markdown_template = shipfeatures_markdown_template.replace("maxCrew", str(passengers[1]))
    list_fields=[["a cool name for the starship that has some relation to the purposes given, temperature 1.0 and frequency penalty 2.0,", "baseModelName"], ["short description of the vessel, including some main features of it", "shortDescription"], ["length of the ship both in metres and feet, with no decimals", "length"], ["width of the ship both in metres and feet, with no decimals", "width"], ["height of the ship both in metres and feet, with no decimals", "height"], ["weight of the ship in kilograms", "weight"], ["distance the starship can travel without refuelling in light-years", "range"], ["cargo capacity in cubic meters", "cargoCapacity"]]
    #short description of the starship based on all the information already provided, mentioning most of the data already known relative to the starhip
    json_starship=json.loads(event["body"])
    for item in list_fields:
        incomplete_starship=json.dumps(json_starship)
        template_field=template.replace("FIELDDESCRIPTION", item[0])
        template_field=template.replace("FIELDNAME", item[1])
        prompt = PromptTemplate(input_variables=["incomplete_starship"], template=template_field)
        chatgpt_chain = LLMChain(
            llm=OpenAI(temperature=0.5),
            prompt=prompt,
            verbose=True,
            memory=ConversationBufferWindowMemory(k=2)
        )
        Logger.info(f"Checking starship: {incomplete_starship}")
        result = chatgpt_chain.predict(
            incomplete_starship=incomplete_starship
        )

        print(f"Bot answer: {result}")
        json_starship[item[1]]=json.loads(result)[item[1]]
        shipfeatures_markdown_template = shipfeatures_markdown_template.replace(item[1], json_starship[item[1]])
    
    #Save the generated response in a json file
    ship_name = json_starship["baseModelName"]
    shipdescription_markdown_template = shipdescription_markdown_template.replace("baseModelName", ship_name)
    shipdescription_markdown_template, _ = document_features(shipdescription_markdown_template, shipfeatures_markdown_template, "longDescription", "Please provide a detailed description based on the data contained {FEATURE} in a spaceship. The description should cover all of the features information in it, and it should be exactly two paragraphs long.")
    shipdescription_markdown_template, _ = document_features(shipdescription_markdown_template, ship_name, "interiorDescription", "Please provide a detailed description of the interior (rooms, design...) of the spaceship {FEATURE} considering the information from the previous prompts. The description should be exactly two paragraphs long.")
    passengers_str = json_starship["passengerCapacity"]
    json_file_name = "./starship_data/json/" + ship_name + " " + passengers_str + ".json"
    md_features_file_name = "./starship_data/markdown/" + ship_name + " " + passengers_str + " features.md"
    md_description_file_name = "./starship_data/markdown/" + ship_name + " " + passengers_str + " description.md"
    
    with open(json_file_name, 'w') as f:
        json.dump(json_starship, f)
    
    with open(md_features_file_name, 'w') as f:
        f.write(shipfeatures_markdown_template)
    
    with open(md_description_file_name, 'w') as f:
        f.write(shipdescription_markdown_template)

    return {"statusCode": 200, "body": result}

#passenger_options = ["2 to 5 people", "6 to 12 people", "13 to 20 people", "21 to 50 people", "50 to 100 people"]
passenger_options = [["50 to 100 people", [13, 20]]]
#purposes_options = [["colonization", "scientific research"], ["leisure", "interstellar colaboration"], ["exploring", "earth observation"]]
purposes_options = [["leisure", "interstellar colaboration"]]
spaceship_functions_necessities = [
    "Life support",
    "Navigation",
    "Propulsion",
    "Communication",
    "Power generation",
    "Hull integrity",
    "Environmental control",
    "Gravity generation",
    "Emergency systems",
    "Waste management",
    "Cargo handling",
    "Medical facilities",
    "Food production",
    "Water recycling",
    "Airlock operation",
    "Maneuvering thrusters",
    "Heat dissipation",
    "Emergency power",
    "Security",
    "Remote sensing",
    "Emergency beacon",
    "Backup systems",
    "Sleeping quarters",
    "Entertainment",
    "Research",
    "Fire suppression",
    "Repair equipment",
    "Maintenance robotics",
    "Gravity control",
    "Landing operations",
    "Recreational facilities",
    "Computer systems",
    "Emergency evacuation",
    "Shielding",
    "External inspection",
    "Docking procedures",
    "Self-destruct mechanism",
    "Extra-vehicular activity (EVA)",
    "Hydroponics/greenhouses",
    "Planetary exploration",
    "Emergency communication",
    "Backup propulsion",
    "Navigation aids",
    "Escape systems",
    "Long-term storage",
    "Backup life support",
    "Redundant systems",
    "Emergency medical procedures",
    "Escape capsules"
]
#focus_options = ["safety", "durability"]
for passengers in passenger_options:
    for purposes in purposes_options:
        this_ship_funcs_necs = random.sample(spaceship_functions_necessities, 5)
        il = json.dumps(
            {
                "purposes": purposes,
                "passengerCapacity": passengers[0],
            }
        )
        event = {"body": f"{il}"}
        lambda_handler(event, passengers[1], purposes[0], this_ship_funcs_necs, None)
      