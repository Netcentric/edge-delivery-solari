import json
import logging
import uuid
import random

from dotenv import load_dotenv
from langchain import LLMChain, PromptTemplate, OpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate

Logger = logging.getLogger()
Logger.setLevel(logging.INFO)
load_dotenv()

template = """You are an AI assistant responsible for generating creative content for a large database of engines of futuristic spaceships to travel around the universe.
Your task is to fill in missing information for a given record of an engine. You will be provided with the usage of the engine (this is, the purposes that the ship to which it is attached serves to) and the number of passengers that the ship it is attached to can fit. Consider that the more passengers it can fit, the bigger the ship will be, and therefore the bigger the engine should be as well.
The longDescription should contain some information about the technology behind the engine, and MUST be ONE paragraph long. The shortDescription MUST be a summary of the longDescription and MAXIMUM 10 words long.
Use the provided record as a reference, but do not repeat the information that was given to you.
As an example, consider this complete record: {{
    "engineName": "Pulsar Pulse Engine",
    "usage": ["leisure, interstellar collaboration"],
    "redundantSystems": "Backup propulsion system.",
    "efficiency": "Optimizes power usage during various mission phases",
    "numberOfPassengers": "2 to 5",
    "length": "11 meters, 36 feet",
    "width": "4 meters, 13 feet",
    "maxSpeed": "0.0013 c, 0.39 km/s, 0.24 miles/s",
    "range": "180000 kilometers, 111847 miles",
    "longDescription": "Welcome aboard the next generation of leisure travel with the Pulsar Pulse Engine, revolutionizing your cosmic voyages with unparalleled efficiency and comfort. Engineered to propel leisure ships with unmatched speed and stability, the Pulsar Pulse Engine harnesses the raw power of pulsars, channeling their energetic pulses into a seamless propulsion system. Integrated with state-of-the-art temperature regulation technology, maintaining an optimal temperature of 1.0 Kelvin, this engine ensures a smooth and luxurious journey through the depths of space. Say goodbye to mundane travel constraints and embrace a new era of leisure exploration with the Pulsar Pulse Engine.",
    "shortDescription": "Luxurious speed with 1.0 Kelvin precision."
        }}
Based on this, please provide suitable values for the description fields that are missing. Your answer MUST be in JSON format, and it should be the full JSON, this is, all fields MUST appear in your answer. This means, as if the answer was the content of JSON file. Remember that this means that the answer you provide MUST be between curly brackets. This is the incomplete JSON file:
-------------------------------------------
Incomplete engine:
{incomplete_engine}
-------------------------------------------
You CANNOT use the following names for the engines:
{forbidden_names}
-------------------------------------------
Your answer in JSON format: """

def design_engines(event, purposes, passengers, forbidden_names):
    json_engine=json.loads(event["body"])
    incomplete_engine=json.dumps(json_engine)
    prompt = PromptTemplate.from_template(template=template)
    chatgpt_chain = LLMChain(
            llm=ChatOpenAI(temperature=1.0, model="gpt-4"),
            prompt=prompt,
            verbose=True
    )
    result = chatgpt_chain({
        "incomplete_engine":incomplete_engine,
        "forbidden_names": forbidden_names
    })
    engine_json = json.loads(result["text"])
    
    with open('enginedescription_markdown_template.md', 'r') as f:
        engine_description = f.read()
    with open('enginefeatures_markdown_template.md', 'r') as f:
        engine_features = f.read()
    
    #Replace user data in the templates
    # engine_description = engine_description.replace("imageUrl", "images/engines/engine_0" + str(i) + "a.png")
    engine_description = engine_description.replace("engineName", engine_json["engineName"])
    forbidden_names.append(engine_json["engineName"])
    engine_features = engine_features.replace("engineName", engine_json["engineName"])
    engine_description = engine_description.replace("shortDescription", engine_json["shortDescription"])
    engine_features = engine_features.replace("shortDescription", engine_json["shortDescription"])
    engine_description = engine_description.replace("longDescription", engine_json["longDescription"])
    engine_description = engine_description.replace("specsUrl", "https://main--edge-delivery-solari--netcentric.hlx.page/specifications/engines/" + engine_json["engineName"].lower().replace(" ", "-"))
    engine_features = engine_features.replace("redSys", engine_json["redundantSystems"])
    engine_features = engine_features.replace("PURPOSES", ', '.join(purposes))
    engine_features = engine_features.replace("efficiency", engine_json["efficiency"])
    engine_features = engine_features.replace("crew", passengers)
    engine_features = engine_features.replace("length", engine_json["length"])
    engine_features = engine_features.replace("width", engine_json["width"])
    engine_features = engine_features.replace("maxSpeed", engine_json["maxSpeed"])
    engine_features = engine_features.replace("range", engine_json["range"])
    
    engine_json["uniqueID"] = str(uuid.uuid4())
    
    with open("./starship_data/json/engines/" + engine_json["engineName"] + ".json", 'w') as f:
        json.dump(engine_json, f)
    
    with open("./starship_data/markdown/engines/focus/" + engine_json["engineName"] + ".md", 'w') as f:
        f.write(engine_description)
        
    with open("./starship_data/markdown/engines/specifications/" + engine_json["engineName"] + ".md", 'w') as f:
        f.write(engine_features)

passengers_options = ["6 to 12", "13 to 20", "21 to 50 ", "51 to 100"]
purposes_options = [["connect with other cultures", "scientific research"], ["leisure", "interstellar collaboration"], ["exploring", "earth observation"]]
forbidden_names = ["Harmony Helix Engine", "Nova Thrust Engine", "TerraTrekker Observation Engine"]

#Generate several engines
# i = 1
for passengers in passengers_options:
    for purposes in purposes_options:
        il = json.dumps(
            {
                "numberOfPassengers": passengers,
                "usage": purposes,
            }
        )
        event = {"body": f"{il}"}
        design_engines(event, purposes, passengers, forbidden_names)
        # i = i+1
      