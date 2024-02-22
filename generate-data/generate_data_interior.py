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

template = """You are an AI assistant responsible for generating creative content for a large database of interior design for futuristic spaceships to travel around the universe.
You will be provided a JSON file that you should fill. The fields that are provided are:
interiorName: This is the name of the interior design
flavor: This is the category into which the design falls into. There are eight different categories: Functional Minimalism, Futuristic elegance, Classic sci-fi vibes, Organic Integration, Higgy Harmony, Retro Space Retrograde, Nomadic tech-traveler and Futuristic bohemian fusion.
Your task is to make two differente descriptions of how these interior designs would look like and how they can make the passenger feel. These are the fields:
shortDescription: This is a very short description, of MAXIMUM ten words, that is considered a first quick sight of what the interior can offer. It is just a quick presentation of the design.
longDescription: This MUST be a ONE paragraph description of the interior design. It can contain things such as ammenities or sensorial experiences for the user. Remember, it HAS TO BE ONLY ONE PARAGRAPH LONG.
As an example, consider the following complete record: {{
    "interiorName": "Bioluminescent Ambience",
    "flavor": "Organic integration",
    "shortDescription": "Illuminate your journey with soothing, organic light",
    "longDescription": "Step into a realm of unparalleled comfort and tranquility with the Bioluminescent Ambiance, where the timeless allure of nature meets cutting-edge photon-led illumination technology for an interstellar journey unlike any other. Designed to evoke the familiar warmth of home, each room is a sanctuary adorned with ethereal forest motifs, creating an immersive experience that transports you to a serene garden oasis. Whether you're unwinding with a book or simply basking in the gentle glow, the Bioluminescent Ambiance ensures that every moment aboard your spaceship feels like a cherished escape into the heart of nature's embrace."
}}

Based on this, please provide suitable values for the description fields that are missing.
Your answer MUST be in JSON format, and it should be the full JSON, this is, all fields (interiorName, flavor, shortDescription and longDescription) MUST appear in your answer. This means, as if the answer was the content of JSON file. Remember that this means that the answer you provide MUST be between curly brackets. Here is the incomplete description JSON file to which you should add "shortDescription" and "longDescription" fields, with your answers:
-------------------------------------------
Incomplete starship:
{incomplete_starship}
-------------------------------------------
Your answer in JSON format: """

def design_interiors(event):
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
    interior_json = json.loads(result["text"])
    
    with open('interiordescription_markdown_template.md', 'r') as f:
        interior_description = f.read()
    with open('interiorfeatures_markdown_template.md', 'r') as f:
        interior_features = f.read()
    
    #Replace user data in the templates
    interior_features = interior_features.replace("interiorName", interior_json["interiorName"])
    interior_features = interior_features.replace("shortDescription", interior_json["shortDescription"])
    interior_features = interior_features.replace("flavor", interior_json["flavor"])
    interior_description = interior_description.replace("interiorName", interior_json["interiorName"])
    interior_description = interior_description.replace("shortDescription", interior_json["shortDescription"])
    interior_description = interior_description.replace("longDescription", interior_json["longDescription"])
    interior_description = interior_description.replace("specsUrl", "https://main--edge-delivery-solari--netcentric.hlx.page/specifications/interiors/" + interior_json["interiorName"].lower().replace(" ", "-"))
    
    interior_json["uniqueID"] = str(uuid.uuid4())
    
    with open("./starship_data/json/interiors/" + interior_json["interiorName"] + ".json", 'w') as f:
        json.dump(interior_json, f)
    
    with open("./starship_data/markdown/interiors/focus/" + interior_json["interiorName"] + ".md", 'w') as f:
        f.write(interior_description)
    with open("./starship_data/markdown/interiors/specifications/" + interior_json["interiorName"] + ".md", 'w') as f:
        f.write(interior_features)

# flavors = ["Functional Minimalism", "Futuristic elegance", "Classic sci-fi vibes", "Organic Integration", "Higgy Harmony", "Retro Space Retrograde", "Futuristic bohemian fusion", "Nomadic Tech Traveler"]
flavors = ["Nomadic Tech Traveler"]

functional_minimalism = ["Sleek Symmetry",
"Tech Chic",
"Mod Matrix",
"Futurist Fusion",
"Clean Cosmos",
"Aero Zen"]

futuristic_elegance = ["Chrome Chic",
"Neo Luxe",
"Tech Sleek",
"Aero Aura",
"Quantum Quarters",
"Glow Glam"]

classic_scifi = ["Retro Space Chic",
"Quantum Fusion",
"Galactic Retro Vibes",
"Astral Harmony",
"Cosmic Elegance",
"Interstellar Aura"]

organic = ["Eco Harmony",
"Nature's Embrace",
"Biomimic Elegance",
"Green Zenith",
"Organic Unity",
"Floral Fusion"]

higgy = ["Zen Zephyr",
"Serene Spectrum",
"Aura Haven",
"Elevated Equilibrium",
"Tranquil Tones",
"Soothing Serenity"]

retro = ["Cosmic Nostalgia",
"Vintage Fusion",
"Space Age Revival",
"Retro Futurism",
"Galactic Retrograde",
"Astro Antique"]

bohemian = ["Cosmic Nomad",
"Boho Nebula",
"Futurama Fusion",
"Astro Eclectic",
"Galactic Wanderer",
"Space Wanderlust"]

nomadic = ["Tech Nomad",
"Digital Wanderer",
"Future Voyager",
"Nomad Nexus",
"Cyber Odyssey",
"Tech Trekker"]

def styles_switcher(flavor):
    switcher = {
        "Functional Minimalism": functional_minimalism,
        "Futuristic elegance": futuristic_elegance,
        "Classic sci-fi vibes": classic_scifi,
        "Organic Integration": organic,
        "Higgy Harmony": higgy, 
        "Retro Space Retrograde": retro, 
        "Futuristic bohemian fusion": bohemian,
        "Nomadic Tech Traveler": nomadic
    }
    return switcher.get(flavor)


#Generate several starships
for flavor in flavors:
    interior_names = styles_switcher(flavor)
    print(interior_names) 
    for name in interior_names:
            il = json.dumps(
                {
                    "interiorName": name,
                    "flavor": flavor,
                }
            )
            event = {"body": f"{il}"}
            design_interiors(event)
      