import json
import logging
import os

import openai
from dotenv import load_dotenv
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.llms import OpenAI
from langchain.prompts.prompt import PromptTemplate

from supabase import Client, create_client

Logger = logging.getLogger()
Logger.setLevel(logging.INFO)
load_dotenv()
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")


template = """You are an AI assistant responsible for generating creative content for a large database of futuristic spaceships to travel around the universe.
Your task is to fill in missing information for a given record of a spaceship. There can be different combinations of travel purpose, ammenities the client will look for and capacity of the ship. You should provide information of both the looks of the spaceship and its technical characteristics.
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
        "exterior": ["Customizable Hull Lights: Express individuality with customizable hull lights that not only add a touch of personal style but also contribute to the spacecraft's visibility in the vastness of space.", "Compact Form Factor: Designed for agility and easy maneuverability, the compact form factor of the Harmony Starcruiser ensures versatility in navigating both bustling spaceports and remote celestial destinations.", "Interstellar Collaboration Hub: Featuring collaborative docking stations and communication arrays, the spacecraft is equipped to facilitate interstellar partnerships and joint ventures, enhancing its functionality beyond leisure.", "Customizable Hull Lights: Express individuality with customizable hull lights that not only add a touch of personal style but also contribute to the spacecraft's visibility in the vastness of space.", "Compact Form Factor: Designed for agility and easy maneuverability, the compact form factor of the Harmony Starcruiser ensures versatility in navigating both bustling spaceports and remote celestial destinations."],
        "interior": "With plush seating, panoramic windows, and collaborative workspaces, the Harmony Starcruiser seamlessly blends relaxation and productivity, making it the ideal choice for those seeking leisure and interstellar teamwork amidst the vast wonders of space."
        }}
Based on this, please provide suitable values for the missing fields in the following incomplete record:
{incomplete_starship}
Your answer should be only in JSON format."""

prompt = PromptTemplate(input_variables=["incomplete_starship"], template=template)

chatgpt_chain = LLMChain(
    llm=OpenAI(temperature=0.5),
    prompt=prompt,
    verbose=True,
    memory=ConversationBufferWindowMemory(k=2),
    model="gpt-4"
)
print(chatgpt_chain)

def lambda_handler(event, context):
    incomplete_starship = event["body"]

    Logger.info(f"Checking starship: {incomplete_starship}")
    result = chatgpt_chain.predict(
        incomplete_starship=incomplete_starship,
    )

    print(f"Bot answer: {result}")
    print(f"Last charachter: " + result[-1])
    # if result[-1] != '}':
    #     continue_result = openai.OpenAI.chat.completions.create(messages = "please continue", model="gpt-3.5-turbo")
    # #     new_chain = LLMChain(
    # #                         llm=OpenAI(temperature=0.5),
    # #                         prompt=PromptTemplate(template="please continue"),
    # #                         verbose=True,
    # #                         memory=ConversationBufferWindowMemory(k=2),
    # #                     )
    # #     continue_result = new_chain.predict()
    #     print(f"Bot continue answer: {continue_result}")
    
    # with open('data.json', 'w') as f:
    #     json.dump(result, f)

    # parsedResult = json.loads(result)
    # parsedResult.pop("name", None)
    # parsedResult.pop("parentNames", None)
    # parsedResult.pop("earthAnalog", None)
    # supabase.table("space_locations").update(parsedResult).eq(
    #     "id", parsedResult["id"]
    # ).execute()

    return {"statusCode": 200, "body": result}

# NOTE: For testing in local
il = json.dumps(
    {
        "purposes": "scientific research",
        "importantForUser": ["safety", "durability"],
        "passengerCapacity": "10 to 15 people",
    }
)
event = {"body": f"{il}"}
lambda_handler(event, None)
