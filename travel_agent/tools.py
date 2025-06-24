from agents import function_tool

@function_tool
def analyze_budget(amount: int) -> str:
    if amount >= 500:
        return "Luxury"
    elif 200 <= amount < 500:
        return "Premium"
    elif 100 <= amount < 200:
        return "Comfort"
    else:
        return "Budget"

@function_tool
def suggest_destination(mood: str, budget_level: str) -> dict:
    if mood.lower() == "sad" and budget_level in ["Luxury", "Premium"]:
        return {"city": "Hunza", "type": "Relaxing", "note": "Peaceful, scenic and serene valley with nature."}
    elif mood.lower() == "adventure":
        return {"city": "Skardu", "type": "Adventure", "note": "Hiking, mountain trekking and rivers."}
    else:
        return {"city": "Murree", "type": "Relaxing", "note": "Calm hills, nature, great for emotional reset."}

@function_tool
def get_must_visit_places(city: str) -> list:
    data = {
        "Hunza": ["Attabad Lake", "Baltit Fort", "Eagle’s Nest"],
        "Murree": ["Mall Road", "Patriata", "Kashmir Point"]
    }
    return data.get(city, [])

@function_tool
def get_local_food(city: str) -> list:
    food = {
        "Hunza": ["Chapshuro", "Diram Phitti", "Harissa"],
        "Murree": ["Grilled Trout", "Makki Roti & Saag"]
    }
    return food.get(city, [])

@function_tool
def suggest_hotel(city: str, budget_level: str) -> dict:
    if city == "Hunza":
        return {"name": "Eagle's Nest Hotel", "price": 100, "location": "Duikar, Hunza"}
    elif city == "Murree":
        return {"name": "Shangrila Resort", "price": 70, "location": "Mall Road, Murree"}
    return {}

@function_tool
def get_transport(origin: str, destination: str) -> str:
    if origin.lower() == "lahore" and destination == "Hunza":
        return "Take Daewoo Bus to Gilgit, then local jeep to Hunza (Approx. 18 hours)"
    elif destination == "Murree":
        return "Take bus from Lahore to Murree via Islamabad (Approx. 7 hours)"
    return "Check local transport availability."

@function_tool
def get_travel_advice(destination: str) -> str:
    if destination == "Hunza":
        return "Pack warm clothes, avoid traveling at night due to narrow roads, keep cash."
    elif destination == "Murree":
        return "Avoid weekends to escape traffic, book hotels in advance."
    return ""
@function_tool
def your_total_expense(budget: int, hotel_price: int, transport_cost: int) -> str:
    total_expense = hotel_price + transport_cost + 8000  # Assuming 8k is the average cost for food and activities
    if total_expense > budget:
        return "Your total expense exceeds your budget."
    else:
        return f"Your total expense is {total_expense}, which is within your budget."