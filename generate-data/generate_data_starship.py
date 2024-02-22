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

template = """You are an AI assistant responsible for generating creative content for a large database of futuristic spaceships to travel around the universe.
Your task is to fill in missing information for a given record of a spaceship. There can be different combinations of travel purpose and capacity of the ship. You should provide information of both the looks of the spaceship and its technical characteristics. When defining the size of the starship, consider that all the passengers must fit comfortably in it. Consider at least 5 cubic meters per passenger, plus the cargo capacity.
Use the provided record as a reference, but do not repeat the information that was given to you.
As an example, consider this complete record: {{
        "baseModelName": "Harmony Starcruiser",
        "shortDescription": "Embark on a celestial journey with the Harmony Starcruiser, a small spacecraft designed for both leisure and interstellar collaboration. This compact vessel comfortably accommodates 2-5 passengers, fostering an atmosphere of camaraderie and shared exploration.",
        "purposes": ["leisure", "interstellar collaboration"],
        "importantFeatures": ["sustainability", "performance"],
        "numberOfPassengers": "2 to 5 individuals",
        "length": "25 meters, 82 feet",
        "width": "15 meters, 49 feet",
        "height": "8 meters, 26 feet",
        "weight": "50 tonnes, 7874 stones",
        "range": "100000 light-years",
        "cargoCapacity": "500 cubic meters, 17657 cubic feet",
        "features": ["Customizable Hull Lights: Express individuality with customizable hull lights that not only add a touch of personal style but also contribute to the spacecraft's visibility in the vastness of space.", 
        "Compact Form Factor: Designed for agility and easy maneuverability, the compact form factor of the Harmony Starcruiser ensures versatility in navigating both bustling spaceports and remote celestial destinations.", 
        "Interstellar Collaboration Hub: Featuring collaborative docking stations and communication arrays, the spacecraft is equipped to facilitate interstellar partnerships and joint ventures, enhancing its functionality beyond leisure."],
        "interiorDescription": "With plush seating, panoramic windows, and collaborative workspaces, the Harmony Starcruiser seamlessly blends relaxation and productivity, making it the ideal choice for those seeking leisure and interstellar teamwork amidst the vast wonders of space."
        }}
Based on this, please provide ONLY one suitable value for ONLY {field_description} in JSON format.
Your answer should be ONLY {field_name} field in JSON format. This means, as if the answer was the content of JSON file. Remember that this means that the answer you provide MUST be between curly brackets. 
If the field is shortDescription, take into account the weights of each purpose, explained in the focus field of the provided incomplete starship.
If the field is baseModelName, provide a different one from the names provided here:
-------------------------------------------
Base Model names:
{base_model_names}
-------------------------------------------
Incomplete starship:
{incomplete_starship}
-------------------------------------------
Your answer in JSON format: """

def generate_firefly_prompt(shipdescription_markdown_template, prompt_text):
    prompt = PromptTemplate(input_variables=["FEATURE"], template=prompt_text)
    chatgpt_chain = LLMChain(
        llm=ChatOpenAI(temperature=0.5),
        prompt=prompt,
        verbose=True
    )
    result = chatgpt_chain.predict(
        FEATURE=shipdescription_markdown_template
    )
    with open("./starship_data/firefly_prompts/firefly_prompts.txt", 'w') as f:
        f.write(result)
    

def document_features(document, new_name, result_replace, prompt_text):
    prompt = PromptTemplate(input_variables=["FEATURE"], template=prompt_text)
    chatgpt_chain = LLMChain(
        llm=ChatOpenAI(temperature=0.8),
        prompt=prompt,
        verbose=True
    )
    result = chatgpt_chain.predict(
        FEATURE=new_name
    )
    document = document.replace(result_replace, result)
    return document, result  

def get_features_data(this_ship_funcs_necs, shipfeatures_markdown_template, shipdescription_markdown_template):
    i = 1
    features = []
    for item in this_ship_funcs_necs:
        shipfeatures_markdown_template = shipfeatures_markdown_template.replace("FEATURE" + str(i), item)
        shipfeatures_markdown_template, name_result = document_features(shipfeatures_markdown_template, item, "feature" + str(i) + "Name", "Please name one feature for {FEATURE} in a spaceship. This feature should be located in the exterior of the spaceship, not in the interior. Only name it, use maximum five words.")
        shipfeatures_markdown_template = shipfeatures_markdown_template.replace("feature" + str(i) + "Name", name_result)
        shipdescription_markdown_template = shipdescription_markdown_template.replace("### feature" + str(i) + "Name", "### " + name_result)
        shipdescription_markdown_template, feature_description = document_features(shipdescription_markdown_template, name_result, "feature" + str(i) + "Description", "Please provide a detailed description of {FEATURE} in a spaceship. It should be two to four lines long.")
        this_feature = name_result + ": " + feature_description
        features.append(this_feature)
        i=i+1
        
    return shipfeatures_markdown_template, shipdescription_markdown_template, features

def generate_starships(event, passengers, purposes, this_ship_funcs_necs, base_model_names, list_fields):
    #Open markdown templates
    with open('shipfeatures_markdown_template.md', 'r') as f:
        shipfeatures_markdown_template = f.read()
    with open('shipdescription_markdown_template.md', 'r') as f:
        shipdescription_markdown_template = f.read()
    
    #Replace user data in the templates
    shipfeatures_markdown_template = shipfeatures_markdown_template.replace("PURPOSES", ', '.join(purposes))
    shipfeatures_markdown_template = shipfeatures_markdown_template.replace("minCrew", str(passengers[0]))
    shipfeatures_markdown_template = shipfeatures_markdown_template.replace("maxCrew", str(passengers[1]))
    
    #Stringify the starship provided data in json format
    json_starship=json.loads(event["body"])
    
    #Generate the features of the starship
    shipfeatures_markdown_template, shipdescription_markdown_template, features = get_features_data(this_ship_funcs_necs, shipfeatures_markdown_template, shipdescription_markdown_template)
    json_starship["features"] = ', '.join(features)
    
    #Prepare prompt and model for the content generation
    prompt = PromptTemplate.from_template(template=template)
    chatgpt_chain = LLMChain(
            llm=ChatOpenAI(temperature=1.0, model="gpt-4"),
            prompt=prompt,
            verbose=True
        )
    
    #Generate data for the different fields, and fill the documents with it
    for item in list_fields:
        incomplete_starship=json.dumps(json_starship)
        Logger.info(f"Checking starship: {incomplete_starship}")
        result = chatgpt_chain(
            {
            "incomplete_starship":incomplete_starship,
            "field_description":item[0],
            "field_name":item[1],
            "base_model_names": base_model_names
            }
        )

        print(result["text"])
        json_starship[item[1]]=json.loads(result["text"])[item[1]]
        shipfeatures_markdown_template = shipfeatures_markdown_template.replace(item[1], json_starship[item[1]])
        
    #Add the new ship name to the list in order to keep it unique
    ship_name = json_starship["baseModelName"]
    base_model_names.append(ship_name)
    
    #Generate ship's and interior's descriptions and save them in the corresponding files
    shipdescription_markdown_template = shipdescription_markdown_template.replace("baseModelName", ship_name)
    shipdescription_markdown_template, longDescription = document_features(shipdescription_markdown_template, shipfeatures_markdown_template, "longDescription", 
                                                             """Please provide a short description of the spaceship based on the data contained in: 
                                                            {FEATURE} 
                                                             The description should mention some of the features, which can be found in the features table in it. There is no need to get into detail about them. In this description, avoid by any circumstance to provide any information about the specifications table. The generated text has to be exactly two paragraphs long.""")
    print(longDescription)
    json_starship["longDescription"]=longDescription
    
    #Generate unique identifiers for each document
    ship_identifier = str(uuid.uuid4())
    json_starship["uniqueID"]=ship_identifier
    
    #Add metadata information to the description document
    shipdescription_markdown_template = shipdescription_markdown_template.replace("specsUrl", "https://main--edge-delivery-solari--netcentric.hlx.page/specifications/ships/" + ship_name.lower().replace(" ", "-"))
    
    # generate_firefly_prompt(shipdescription_markdown_template, """I need to create an image of a starship using Firefly. I am going to provide you a markdown document that contains the general description of the ship, and the description of some external features. I want that the generated image contains ONLY the starship in a white background. The looks of the starship should be corresponding to what is said in the description, and should also present the features described in it, which should be visible on the exteriors of the starship. The document is the following:
    #                         {FEATURE}
    #                         Please, provide an appropriate prompt that contains the name, and a proper description of the starship and its external features based on what there is in the document that I am giving to you. The text that you are giving me, is the exact text that I am going to give to Firefly so that it generates the image. So please, give me a proper prompt that Firefly can understand so that it gives me an appropriate image of the starship.""")
    
    #Save the markdown and json files
    json_file_name = "./starship_data/json/ships/" + ship_name + ".json"
    md_features_file_name = "./starship_data/markdown/ships/specifications/" + ship_name + ".md"
    md_description_file_name = "./starship_data/markdown/ships/focus/" + ship_name + ".md"
    
    with open(json_file_name, 'w') as f:
        json.dump(json_starship, f)
    
    with open(md_features_file_name, 'w') as f:
        f.write(shipfeatures_markdown_template)
    
    with open(md_description_file_name, 'w') as f:
        f.write(shipdescription_markdown_template)

    return {"statusCode": 200, "body": result}


#Standard user data
passenger_options = [["2 to 5 people", [2, 5]], ["6 to 12 people", [6, 12]], ["13 to 20 people", [13, 20]], ["21 to 50 people", [21, 50]], ["51 to 100 people", [51, 100]]]
focus_options = [["give more weight to the first purpose rather than to the second purpose"], ["give equal weight to both purposes"], ["give more weight to the second purpose rather than to the first purpose"]]
purposes_options = [["connect with other cultures", "scientific research"], ["leisure", "interstellar collaboration"], ["exploring", "earth observation"]]
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

# starship_exterior_features = [
#     "Fusion Reactor Exhaust Vents",
#     "Quantum Hull Plating",
#     "Graviton Thruster Arrays",
#     "Photon Sail Array",
#     "Plasma Shield Emitters",
#     "Antimatter Engine Nozzles",
#     "Ion Accelerator Cannons",
#     "Tachyon Deflector Dish",
#     "Neutrino Detector Arrays",
#     "Nanofiber Reinforced Hull",
#     "Magnetic Field Generators",
#     "Solar Panel Arrays",
#     "Holographic Cloaking System",
#     "Hyperspace Jump Rings",
#     "Sonic Resonance Emitters",
#     "Plasma Cannon Turrets",
#     "Particle Beam Emitters",
#     "Exotic Matter Collector Arrays",
#     "Gravity Well Manipulators",
#     "Electromagnetic Pulse Cannons",
#     "Chronal Stabilizer Arrays",
#     "Interstellar Communication Antennas",
#     "Quantum Entanglement Beacons",
#     "Subspace Field Projectors",
#     "Quantum Shielding Panels",
#     "Anti-Gravity Propulsion Pods",
#     "Higgs Boson Energy Converters",
#     "Dark Matter Resonance Chambers",
#     "Plasma Stream Diverters",
#     "Asteroid Deflection Shields",
#     "Thermal Dissipation Fins",
#     "Energy Refraction Arrays",
#     "Exoplanet Landing Struts",
#     "Magnetic Confinement Rings",
#     "Kinetic Energy Absorbers",
#     "Laser Defense Grid",
#     "Spatial Anomaly Sensors",
#     "Phase Shift Cloaking Panels",
#     "Gravity Lensing Arrays",
#     "Sonic Boom Suppressors",
#     "Thermal Insulation Coating",
#     "Magnetic Suspension Landing Gear",
#     "Radar Absorbing Material",
#     "Energy Feedback Dampeners",
#     "Pulse Drive Nacelles",
#     "Plasma Wave Scramblers",
#     "Hyperdimensional Rift Stabilizers",
#     "Quantum Encryption Transponders",
#     "Electromagnetic Railgun Cannons",
#     "Neutronium Armor Plating"
# ]

#Forbidden ship names
base_model_names = ["Galactic Voyager", "Galactic Explorer", "Celestial Pathfinder", "Observant Pathfinder"]

#Fields of the documents that are to be generated
list_fields=[["a cool name for the starship that has some relation to the purposes given", "baseModelName"], 
             ["short description of the vessel, including some main features of it", "shortDescription"], 
             ["cargo capacity both in cubic meters and cubic feet, with no decimals", "cargoCapacity"],
             ["length of the ship both in metres and feet, with no decimals", "length"], 
             ["width of the ship both in metres and feet, with no decimals", "width"], 
             ["height of the ship both in metres and feet, with no decimals", "height"], 
             ["weight of the ship both in tonnes and stones, with no decimals", "weight"], 
             ["distance the starship can travel without refuelling in light-years", "range"]] 

#Generate several starships
for passengers in passenger_options:
    for focus in focus_options:
        for purposes in purposes_options:
            this_ship_funcs_necs = random.sample(spaceship_functions_necessities, 3)
            il = json.dumps(
                {
                    "purposes": purposes,
                    "focus": focus,
                    "numberOfPassengers": passengers[0],
                }
            )
            event = {"body": f"{il}"}
            generate_starships(event, passengers[1], purposes, this_ship_funcs_necs, base_model_names, list_fields)
      