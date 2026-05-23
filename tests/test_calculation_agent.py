from agents.calculation_agent import calculate_wohnflaeche

def test_basic_living_room():

    vision_data = {
        "rooms": [
            {
                "name": "Wohnzimmer", 
                "type": "living", 
                "area":20.0
            }
        ]
    }

    result = calculate_wohnflaeche(vision_data)
    assert result["wohnflaeche_sqm"] == 20.0

def test_balcony_counts_as_25_percent():

    vision_data = {
        "rooms": [
            {
                "name": "Balkon", 
                "type": "balcony", 
                "area": 12.0
            }
        ]
    }

    result = calculate_wohnflaeche(vision_data)
    assert result["wohnflaeche_sqm"] == 3.0

def test_staircase_is_excluded():
    vision_data = {
        "rooms": [
            {"name": "Treppenhaus", "type": "staircase", "area": 15.0}
        ]
    }
    result = calculate_wohnflaeche(vision_data)
    assert result["wohnflaeche_sqm"] == 0.0

def test_loft_counts_at_50_percent():
    vision_data = {
        "rooms": [
            {"name": "DG-Zimmer", "type": "loft", "area": 20.0}
        ]
    }
    result = calculate_wohnflaeche(vision_data)
    assert result["wohnflaeche_sqm"] == 10.0

def test_empty_rooms_returns_zero():
    vision_data = {"rooms": []}
    result = calculate_wohnflaeche(vision_data)
    assert result["wohnflaeche_sqm"] == 0.0

def test_mixed_rooms():
    vision_data = {
        "rooms": [
            {"name": "Wohnzimmer", "type": "living", "area": 20.0},
            {"name": "Balkon",     "type": "balcony", "area": 10.0},
            {"name": "Treppenhaus","type": "staircase", "area": 5.0},
        ]
    }
    result = calculate_wohnflaeche(vision_data)
    assert result["wohnflaeche_sqm"] == 22.5

def test_unknown_room_type_defaults_to_full():
    vision_data = {
        "rooms": [
            {"name": "Hobbyraum", "type": "hobby", "area": 15.0}
        ]
    }
    result = calculate_wohnflaeche(vision_data)
    assert result["wohnflaeche_sqm"] == 15.0

def test_breakdown_contains_correct_keys():
    vision_data = {
        "rooms": [
            {"name": "Küche", "type": "kitchen", "area": 12.0}
        ]
    }
    result = calculate_wohnflaeche(vision_data)
    breakdown = result["breakdown"]

    assert len(breakdown) == 1
    assert breakdown[0]["name"] == "Küche"
    assert breakdown[0]["coefficient"] == 1.0
    assert breakdown[0]["contribution"] == 12.0


