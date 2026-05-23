WOHNFLAECHE_COEFFICIENTS = {
    "living":    1.0,
    "kitchen":   1.0,
    "bathroom":  1.0,
    "wc":        1.0,
    "hallway":   1.0,
    "storage":   1.0,
    "loft":      0.5,
    "balcony":   0.25,
    "staircase": 0.0,
}

def calculate_wohnflaeche(vision_data):
    """Calculate Wohnfläche (living area) per German WoFlV regulation.

    Applies a coefficient to each room's area based on its type.
    For example, balconies count at 25%, lofts at 50%, all interior
    rooms at 100%.

    Args:
        vision_data: dict with a "rooms" list from the vision agent.
                     Each room must have "name", "type", and "area".

    Returns:
        dict with keys:
            - "wohnflaeche_sqm": total living area rounded to 1 decimal
            - "breakdown": list of per-room dicts with coefficient applied
            - "assumptions": list of strings explaining the calculation rules
    """
    rooms = vision_data.get("rooms", [])
    total = 0.0
    breakdown = []

    for room in rooms:
        room_type = room.get("type", "living")
        area = room.get("area", 0.0)
        coefficient = WOHNFLAECHE_COEFFICIENTS.get(room_type, 1.0)
        contribution = round(area * coefficient, 2)

        breakdown.append({
            "name": room["name"],
            "type": room_type,
            "area": area,
            "coefficient": coefficient,
            "contribution": contribution
        })

        total += contribution

    assumptions = [
        "Balconies and terraces counted at 25% per WoFlV",
        "Loft areas counted at 50% due to unknown ceiling height",
        "All interior rooms (hallway, bathroom, storage) counted at 100%",
        "Shared staircases excluded at 0%",
        "Room dimensions taken directly from floor plan labels"
    ]

    return {
        "wohnflaeche_sqm": round(total, 1),
        "breakdown": breakdown,
        "assumptions": assumptions
    }