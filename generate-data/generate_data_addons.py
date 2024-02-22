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

template = """You are an AI assistant responsible for generating creative content for a large database of external features for futuristic spaceships to travel around the universe.
You will be provided a JSON file that you should fill. The fields that are provided are:
featureName: This is the name of the feature
mainFeature: This is the category into which the feature falls into. There are seven different categories: Safety, Cargo Space, Sustainability, Luxury, Range, Research and Communication.
Your task is to make two different descriptions of how these features would look like and, if it applies, a brief explanation of the technology behind it. These are the fields:
shortDescription: This is a very short description, of MAXIMUM ten words, that is considered a first quick sight of what the feature can offer. It is just a quick presentation of the feature. This description should not contain the name of the feature.
longDescription: This MUST be a ONE paragraph description of the interior design. It can contain things such as a physical description of the feature, what added value it provides to the ship, how it works and the technology behind it. Remember, it HAS TO BE ONLY ONE PARAGRAPH LONG. Make it catchy.
As an example, consider the following complete record: {{
    "featureName": "Quantum Entanglement Communication Relay",
    "mainFeature": "Communicaton",
    "shortDescription": "Revolutionary technology enables instant interstellar communication without boundaries.",
    "longDescription": "Introducing our cutting-edge innovation: the Quantum Entanglement Communication Relay! Seamlessly transcending the bounds of conventional communication, this marvel harnesses the enigmatic power of quantum entanglement to forge instantaneous connections across vast cosmic distances. Imagine relaying critical data, messages, and even emotions with absolute immediacy, unimpeded by the constraints of space and time. With our Quantum Entanglement Communication Relay, the cosmos becomes your playground, enabling unprecedented real-time interaction and collaboration among the stars. Join us as we redefine the boundaries of interstellar communication and embark on a journey toward a future where connectivity knows no bounds."
}}

Based on this, please provide suitable values for the description fields that are missing.
Your answer MUST be in JSON format, and it should be the full JSON, this is, all fields (featureName, mainFeature, shortDescription and longDescription) MUST appear in your answer. This means, as if the answer was the content of JSON file. Remember that this means that the answer you provide MUST be between curly brackets. Here is the incomplete description JSON file to which you should add "shortDescription" and "longDescription" fields, with your answers:
-------------------------------------------
Incomplete starship:
{incomplete_starship}
-------------------------------------------
Your answer in JSON format: """

def design_addons(event):
    json_starship=json.loads(event["body"])
    incomplete_starship=json.dumps(json_starship)
    prompt = PromptTemplate.from_template(template=template)
    chatgpt_chain = LLMChain(
            llm=ChatOpenAI(temperature=1.0, model="gpt-4"),
            prompt=prompt,
            verbose=True
    )
    result = chatgpt_chain({
        "incomplete_starship":incomplete_starship
    })
    addons_json = json.loads(result["text"])
    
    with open('addonsdescription_markdown_template.md', 'r') as f:
        addons_description = f.read()
    with open('addonsfeatures_markdown_template.md', 'r') as f:
        addons_features = f.read()
    
    #Replace user data in the templates
    addons_features = addons_features.replace("featureName", addons_json["featureName"])
    addons_features = addons_features.replace("shortDescription", addons_json["shortDescription"])
    addons_features = addons_features.replace("mainFeature", addons_json["mainFeature"])
    addons_description = addons_description.replace("featureName", addons_json["featureName"])
    addons_description = addons_description.replace("shortDescription", addons_json["shortDescription"])
    addons_description = addons_description.replace("longDescription", addons_json["longDescription"])
    addons_description = addons_description.replace("specsUrl", "https://main--edge-delivery-solari--netcentric.hlx.page/specifications/accessories/" + addons_json["featureName"].lower().replace(" ", "-"))
    
    addons_json["uniqueID"] = str(uuid.uuid4())
    
    with open("./starship_data/json/accessories/" + addons_json["featureName"] + ".json", 'w') as f:
        json.dump(addons_json, f)
    
    with open("./starship_data/markdown/accessories/focus/" + addons_json["featureName"] + ".md", 'w') as f:
        f.write(addons_description)
    with open("./starship_data/markdown/accessories/specifications/" + addons_json["featureName"] + ".md", 'w') as f:
        f.write(addons_features)

#Standard user data
features = ["Safety", "Cargo Space", "Sustainability", "Luxury", "Range", "Research", "Communication"]

spaceship_safety_features = [
    "Radiation shielding",
    "Redundant life support systems",
    "Emergency escape pods",
    "Automated collision avoidance systems",
    "Fire suppression systems",
    "Hull integrity monitoring and repair systems"
]

spaceship_cargo_features = [
    "Secure cargo storage compartments",
    "Internal cargo management systems",
    "Cargo tracking and inventory management",
    "Adjustable cargo restraints for zero-gravity",
    "Temperature and humidity control for perishable goods",
    "Cargo loading and unloading automation"
]

spaceship_sustainability_features = [
    "Solar panels",
    "Closed-loop recycling systems for water and air",
    "Regenerative life support systems",
    "Reusable components and materials",
    "Minimal waste production and management systems",
    "Ion thrusters"
]

spaceship_luxury_features = [
    "Luxurious sleeping quarters with adjustable beds",
    "Elegant common areas with panoramic views",
    "Gourmet dining options",
    "Relaxation facilities",
    "Virtual reality entertainment suites",
    "Personalized concierge"
]

spaceship_range_features = [
    "Propulsion System Efficiency",
    "Fuel Capacity",
    "Energy Management Systems",
    "Advanced Engine Technology",
    "Weight Optimization",
    "Navigation and Route Planning"
]

scientific_research_features = [
    "Laboratory Facilities",
    "Data Acquisition Systems",
    "Remote Sensing Capabilities",
    "Sample Collection and Analysis Tools",
    "Microgravity environment",
    "Collaboration Platforms"
]

communication_features = [
    "Holographic communication array",
    "Long-range subspace antenna array",
    "Quantum entanglement communication relay",
    "Advanced laser-based communication beacon",
    "Multi-spectral communication dish",
    "Adaptive electromagnetic interference shielding"
]


def addons_switcher(flavor):
    switcher = {
        "Safety": spaceship_safety_features,
        "Cargo Space": spaceship_cargo_features,
        "Sustainability": spaceship_sustainability_features,
        "Luxury": spaceship_luxury_features,
        "Range": spaceship_range_features, 
        "Research": scientific_research_features, 
        "Communication": communication_features
    }
    return switcher.get(flavor)


#Generate several starships
for feature in features:
    interior_names = addons_switcher(feature)
    print(interior_names) 
    for name in interior_names:
            il = json.dumps(
                {
                    "featureName": name,
                    "mainFeature": feature,
                }
            )
            event = {"body": f"{il}"}
            design_addons(event)
      