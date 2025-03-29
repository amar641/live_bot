import json

def load_database():
    with open("database.json", "r") as file:
        return json.load(file)

def save_database(data):
    with open("database.json", "w") as file:
        json.dump(data, file, indent=4)

def calculate_probability():
    data = load_database()

    total_spaces = data["parking_lot"]["total_spaces"]
    free_spaces = data["parking_lot"]["free_spaces"]
    occupied_spaces = total_spaces - free_spaces

    booking_count = len(data.get("bookings", []))
    visit_count = len(data.get("website_visits", []))

    # Avoid division by zero
    visit_factor = (0.2 / max(1, visit_count)) if visit_count > 0 else 0

    probability = max(0, 100 - ((occupied_spaces / total_spaces) * 100) - (booking_count * (1 / total_spaces * 100)) - (visit_count * visit_factor))
    
    data["parking_lot"]["probability"] = round(probability, 2)
    save_database(data)

    return round(probability, 2)
