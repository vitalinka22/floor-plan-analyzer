from google import genai
from dotenv import load_dotenv
import os 
import json 

from utils.pdf_to_image import pdf_to_images

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_floor_plan(pdf_path):
    """Analyze a floor plan PDF and return a structured JSON representation of the layout and features"""

    images = pdf_to_images(pdf_path)
    image = images[0] 

    prompt = """
    You are a real estate expert analyzing a German floor plan (Grundriss).

    Extract ALL rooms and property attributes. Return ONLY a JSON object with this exact structure:

    {
        "rooms": [
            {
                "name": "Wohnzimmer",
                "width": 4.5,
                "length": 5.2,
                "area": 23.4,
                "floor": 1,
                "type": "living"
            }
        ],
        "attributes": {
            "kitchen_type": "separate",
            "bathrooms": 1,
            "separate_wc": false,
            "balcony": true,
            "terrace": false,
            "storage_room": true,
            "floor_level": "1.OG",
            "special_features": [],
            "property_type": "apartment"
        }
    }

    Room types:
    - "living"    : Wohnzimmer, Schlafzimmer, Kinderzimmer, Esszimmer
    - "kitchen"   : Küche, EBK, Kochnische
    - "bathroom"  : Bad, Badezimmer, Duschbad
    - "wc"        : WC, Gäste-WC, Toilette
    - "hallway"   : Diele, Flur, Korridor, Eingang
    - "storage"   : Abstellraum, HWR, Abstellkammer
    - "balcony"   : Balkon, Terrasse, Loggia
    - "loft"      : DG-Zimmer, Galerie, Attic
    - "staircase" : shared Treppenhaus outside the apartment

    For kitchen_type use:
    - "open"      : kitchen is open to living/dining area
    - "separate"  : kitchen has its own walls and door
    - "kitchenette" : small cooking niche

    For property_type use:
    - "house"     : if the plan shows multiple floors (Floor 1, Floor 2, Floor 3 etc.)
    - "apartment" : if the plan shows a single floor unit
    - "townhouse" : if multi-floor but part of a terrace row

    For floor_level:
    - Single floor: write the floor name e.g. "2.OG", "EG"
    - Multi-floor: write "Floor 1-4" or similar range

    Rules:
    - Include EVERY room visible including bathrooms, hallways, storage rooms
    - If area is labeled directly (e.g. "23,40 m²") use that value
    - If width and length are labeled, calculate area = width x length
    - If the plan shows multiple floors, set property_type to "house"
    - Return ONLY the JSON, no extra text
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, image],
            config={"temperature": 0},
        )
    except Exception as e:
        raise RuntimeError(f"Gemini API call failed: {e}") from e


    text = response.text.strip()
    text = text.replace("```json", "").replace("```", "")
    result = json.loads(text)

    return result

if __name__ == "__main__":
    result = analyze_floor_plan("input/Floorplan_P1_Mosbach.pdf")
    print(json.dumps(result, indent=2))


