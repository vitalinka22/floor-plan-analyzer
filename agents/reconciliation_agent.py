from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def reconcile(vision_data, extraction_data):
    """Cross-check vision AI output against raw PDF text to find inconsistencies.

    Sends both data sources to Gemini and asks it to flag mismatches —
    for example, a room area that appears in the vision output but not
    in the PDF text, or conflicting room counts.

    Args:
        vision_data: structured room data returned by the vision agent.
        extraction_data: raw word list returned by the extraction agent.

    Returns:
        dict with key "reconciliation_notes": list of warning/confirmation strings.
    """
    
    pdf_words = extraction_data.get("words", [])
    pdf_text_values = [w.get("text", "") for w in pdf_words]

    prompt = f"""
    You are a data validation expert reviewing a floor plan analysis.

    A vision AI extracted this structured data from a floor plan image:
    {json.dumps(vision_data, indent=2)}

    A PDF text extractor found these raw text values in the same document:
    {pdf_text_values}

    Please cross-check these two sources and identify:
    - Room areas or dimensions extracted by the vision AI that do not appear in the PDF text
    - Any rooms with suspiciously large or small areas
    - Inconsistencies between the rooms list and the attributes block
    - Any corrections or warnings you would suggest

    Return ONLY a JSON object like this:
    {{
        "reconciliation_notes": [
            "WARNING: Patio area 312 m² not confirmed in PDF text — stated area is 230 m²",
            "Bathroom count matches: 3 bathrooms in rooms list and attributes"
        ]
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
        result = {"reconciliation_notes": [text]}

    return result

if __name__ == "__main__":
    from agents.vision_agent import analyze_floor_plan
    from agents.extraction_agent import extract_text_with_coordinates

    pdf_path = "input/Appartment_Transvaal.pdf"

    print("Running extraction agent...")
    extraction_data = extract_text_with_coordinates(pdf_path)

    print("Running vision agent...")
    vision_data = analyze_floor_plan(pdf_path)

    print("Running reconciliation agent...")
    result = reconcile(vision_data, extraction_data)

    print(json.dumps(result, indent=2, ensure_ascii=False))