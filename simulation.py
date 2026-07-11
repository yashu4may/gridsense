import random

# Global weather variable
current_temp = 30

# Generate 50 virtual houses
houses = []
for i in range(1, 51):
    houses.append({
        'id': i,
        # Base load is 0.4 to 0.8 kW per house
        'base_load': random.uniform(0.4, 0.8),
        'geyser_on': random.choice([True, False]),
        'geyser_load': 2.0,
        'ev_plugged_in': random.choice([True, False]),
        'paused_by_ai': False  # Track if the AI turned this geyser off
    })

def get_current_load():
    """Calculates total power and applies weather/V2G physics."""
    global current_temp
    total = 0
    for house in houses:
        # Randomly turn appliances on/off very slowly for a stable, readable simulation
        if random.random() < 0.02:
            house['geyser_on'] = not house['geyser_on']
            house['paused_by_ai'] = False  # Reset AI pause if it toggles naturally

        load = house['base_load']

        if current_temp > 35:
            load *= 2.80  # AC surge in heatwave (guarantees exceeding 100 kW to trigger AI defense)

        if house['geyser_on']:
            load += house['geyser_load']

        total += load

    # V2G: If Heatwave, EVs discharge to help the grid
    if current_temp > 35:
        for house in houses:
            if house['ev_plugged_in']:
                total -= 0.5  # Moderate discharge to show V2G reduction without completely wiping out the load

    return total