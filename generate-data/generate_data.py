import json
import logging
import os

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
Your task is to fill in missing information for a given record of a spaceship. There can be different combinations of travel purpose, ammenities the client will look for and capacity of the ship. You should provide information of both the looks of the spaceship and its technical characteristics. When defining the size of the starship, consider that all the passengers must fit comfortably in it. You are given the passenger capacity, the purposes of the travel and the issues that are important for the user:
{incomplete_starship}
Use the provided record as a reference, but do not repeat the information that was given to you.
As an example, consider this complete record: {{
        "baseModelName": "Harmony Starcruiser",
        "shortDescription": "Embark on a celestial journey with the Harmony Starcruiser, a small spacecraft designed for both leisure and interstellar collaboration. This compact vessel comfortably accommodates 2-5 passengers, fostering an atmosphere of camaraderie and shared exploration.",
        "purposes": ["leisure", "interstellar collaboration"],
        "importantForUser": ["sustainability", "performance"],
        "passengerCapacity": "2 to 5 individuals",
        "length": "25 meters",
        "width": "15 meters",
        "height": "8 meters",
        "weight": "50000 kilograms",
        "range": "100000 light-years",
        "cargoCapacity": "500 cubic meters",
        "exterior": ["Customizable Hull Lights: Express individuality with customizable hull lights that not only add a touch of personal style but also contribute to the spacecraft's visibility in the vastness of space.", 
        "Compact Form Factor: Designed for agility and easy maneuverability, the compact form factor of the Harmony Starcruiser ensures versatility in navigating both bustling spaceports and remote celestial destinations.", 
        "Interstellar Collaboration Hub: Featuring collaborative docking stations and communication arrays, the spacecraft is equipped to facilitate interstellar partnerships and joint ventures, enhancing its functionality beyond leisure."],
        "interior": "With plush seating, panoramic windows, and collaborative workspaces, the Harmony Starcruiser seamlessly blends relaxation and productivity, making it the ideal choice for those seeking leisure and interstellar teamwork amidst the vast wonders of space."
        }}
Based on this, please provide only one suitable value for only the FIELDDESCRIPTION in JSON format.
Your answer should be only FIELDNAME field in JSON format. This means, as if the answer was the content of JSON file. Remember that this means that the answer you provide MUST be between curly brackets."""



def lambda_handler(event, passengers, context):
    list_fields=[["the name of the base model", "baseModelName"], ["short description of the starship", "shortDescription"], ["length of the ship in metres", "length"], ["width of the ship in metres", "width"], ["height of the ship in metres", "height"], ["weight of the ship in kilograms", "weight"], ["distance the starship can travel without refuelling in light-years", "range"], ["cargo capacity in cubic meters", "cargoCapacity"], ["different components of the exterior design of the starship, and their description", "exterior"], ["description of the interior of the starship cabin", "interior"]]
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
    
    #Save the generated response in a json file
    file_name = "data_" + passengers + ".json"
    with open(file_name, 'w') as f:
        json.dump(json_starship, f)

    return {"statusCode": 200, "body": result}

passenger_options = ["2 to 5 people", "6 to 12 people", "13 to 20 people", "21 to 50 people", "50 to 100 people", ]
for passengers in passenger_options:
    il = json.dumps(
        {
            "purposes": ["colonization", "scientific research"],
            "importantForUser": ["safety", "durability"],
            "passengerCapacity": passengers,
        }
    )
    event = {"body": f"{il}"}
    lambda_handler(event, passengers, None)
