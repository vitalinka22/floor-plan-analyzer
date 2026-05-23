from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def evaluate(vision_data, calculation_data, reconciliation_data):
    """Produce the final property summary by resolving conflicts across all agents.

    Sends all three data sources to Gemini and asks it to reconcile
    disagreements, apply German conventions (e.g. room count excludes
    bathrooms and hallways), and return a clean final JSON report.

    Args:
        vision_data: structured room data from the vision agent.
        calculation_data: Wohnfläche totals from the calculation agent.
        reconciliation_data: warnings and notes from the reconciliation agent.

    Returns:
        dict with keys: wohnflaeche_sqm, rooms, bathrooms, balcony, terrace,
        kitchen, storage_room, floor_level, property_type, special_features,
        notes, wohnflaeche_breakdown.
    """
    
    prompt = f"""
    You are a real estate analyst producing a final property report.

    You have three sources of data from a floor plan analysis:

    1. VISION EXTRACTION (AI-extracted rooms and attributes):
    {json.dumps(vision_data, indent=2)}

    2. WOHNFLÄCHE CALCULATION:
    {json.dumps(calculation_data, indent=2)}

    3. RECONCILIATION NOTES (conflicts and warnings found):
    {json.dumps(reconciliation_data, indent=2)}

    Your job:
    - Resolve any conflicts flagged in the reconciliation notes intelligently
    - If the PDF states a total area, prefer that over the calculated sum
    - If a room is missing, note it
    - Count only living/bedroom/kitchen rooms for the "rooms" field (German convention)
    - If rooms span multiple floors, set property_type to "house" not "apartment"
    - If rooms span multiple floors, set floor_level to the full range e.g. "Floor 1-4"
    - If storage rooms are listed in the rooms data, set storage_room to true
    - Produce the final clean property summary

    Return ONLY a JSON object in this exact format:
    {{
        "wohnflaeche_sqm": 78.5,
        "rooms": 3,
        "bathrooms": 1,
        "balcony": true,
        "terrace": false,
        "kitchen": "open",
        "storage_room": true,
        "floor_level": "2.OG",
        "property_type": "apartment",
        "special_features": [],
        "notes": [
            "Balcony counted at 25% per WoFlV",
            "One room may be missing from extraction — PDF states 6 rooms"
        ],
        "wohnflaeche_breakdown": []
    }}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt],
            config={"temperature": 0},
        )
    except Exception as e:
        raise RuntimeError(f"Gemini API call failed: {e}") from e

    text = response.text.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        raise ValueError(f"Failed to parse evaluation response as JSON:\n{text}")

    return result