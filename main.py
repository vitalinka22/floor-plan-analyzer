import json
import os
from pathlib import Path

from agents.extraction_agent import extract_text_with_coordinates
from agents.vision_agent import analyze_floor_plan
from agents.calculation_agent import calculate_wohnflaeche
from agents.reconciliation_agent import reconcile
from agents.evaluation_agent import evaluate


def analyze(pdf_path):
    print(f"\n{'='*50}")
    print(f"Analyzing: {pdf_path}")
    print(f"{'='*50}")

    print("Step 1: Extracting text with coordinates...")
    extraction_data = extract_text_with_coordinates(pdf_path)

    print("Step 2: Analyzing floor plan with vision AI...")
    vision_data = analyze_floor_plan(pdf_path)

    print("Step 3: Calculating Wohnfläche...")
    calculation_data = calculate_wohnflaeche(vision_data)

    print("Step 4: Reconciling and validating...")
    reconciliation_data = reconcile(vision_data, extraction_data)

    print("Step 5: Producing final evaluation...")
    final_result = evaluate(vision_data, calculation_data, reconciliation_data)

    if not final_result.get("wohnflaeche_breakdown"):
        final_result["wohnflaeche_breakdown"] = calculation_data.get("breakdown", [])

    return final_result


def save_results(result, pdf_path):
    os.makedirs("output", exist_ok=True)
    stem = Path(pdf_path).stem

    json_path = f"output/{stem}_result.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"JSON saved to {json_path}")

    md_path = f"output/{stem}_report.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(generate_report(result, pdf_path))
    print(f"Report saved to {md_path}")


def generate_report(result, pdf_path):
    lines = []
    lines.append(f"# Floor Plan Analysis Report")
    lines.append(f"**File:** {pdf_path}\n")

    lines.append("## Summary")
    lines.append(f"- **Wohnfläche:** {result.get('wohnflaeche_sqm')} m²")
    lines.append(f"- **Rooms:** {result.get('rooms')}")
    lines.append(f"- **Bathrooms:** {result.get('bathrooms')}")
    lines.append(f"- **Kitchen:** {result.get('kitchen')}")
    lines.append(f"- **Balcony:** {result.get('balcony')}")
    lines.append(f"- **Terrace:** {result.get('terrace')}")
    lines.append(f"- **Storage room:** {result.get('storage_room')}")
    lines.append(f"- **Floor level:** {result.get('floor_level')}")
    lines.append(f"- **Property type:** {result.get('property_type')}")

    special = result.get("special_features", [])
    if special:
        lines.append(f"- **Special features:** {', '.join(special)}")

    lines.append("\n## Wohnfläche Breakdown")
    lines.append("| Room | Type | Area (m²) | Coefficient | Contribution (m²) |")
    lines.append("|------|------|-----------|-------------|-------------------|")
    for room in result.get("wohnflaeche_breakdown", []):
        lines.append(
            f"| {room.get('name')} | {room.get('type')} | "
            f"{room.get('area')} | {room.get('coefficient')} | "
            f"{room.get('contribution')} |"
        )

    lines.append("\n## Assumptions & Notes")
    for note in result.get("notes", []):
        lines.append(f"- {note}")

    return "\n".join(lines)


if __name__ == "__main__":
    pdf_files = [
        "input/Appartment_Transvaal.pdf",
        "input/Floorplan_P1_Mosbach.pdf",
    ]

    for pdf_path in pdf_files:
        result = analyze(pdf_path)
        save_results(result, pdf_path)

    print("\nDone! Check the output/ folder.")