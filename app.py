# app.py — Airline Demand Analysis Web App with Mock‑Route Fallback
# app.py
# app.py
import os
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Load route data from file
def load_routes():
    try:
        df = pd.read_csv("data/routes.csv")
        return df.to_dict("records")
    except Exception as e:
        print("⚠ Could not read CSV. Error:", e)
        return []

# Generate insights
def generate_insights(routes):
    df = pd.DataFrame(routes)

    trends = {}
    for route in df['route']:
        base = np.random.randint(150, 400)
        prices = [base + np.random.randint(-50, 100) for _ in range(30)]
        dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(29, -1, -1)]
        trends[route] = {'dates': dates, 'prices': prices}

    # Heatmap
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    hours = [f"{h}:00" for h in range(6, 23)]
    heatmap = []
    for day in days:
        for hour in hours:
            demand = np.random.randint(30, 90)
            if day in ['Fri', 'Sun'] and int(hour.split(':')[0]) >= 16:
                demand += 30
            heatmap.append([day, hour, min(100, demand)])

    top_routes = df.sort_values('passengers', ascending=False).head(5)
    return {
        'top_routes': top_routes.to_dict('records'),
        'price_trends': trends,
        'demand_heatmap': heatmap
    }

# Dummy booking suggestions
def generate_booking_suggestions():
    return [
        "📅 Book midweek (Tuesday–Thursday) for best prices.",
        "🔁 Avoid weekends — prices tend to spike.",
        "💡 Try early morning or late night flights.",
        "⏳ Book 2-3 weeks in advance to save more.",
        "🛡 Use incognito mode to avoid dynamic price hikes."
    ]

# Dummy route coordinates for map (use airport codes as keys)
ROUTE_COORDS = {
    "SYD": {"lat": -33.8688, "lng": 151.2093},
    "MEL": {"lat": -37.8136, "lng": 144.9631},
    "BOM": {"lat": 19.0760, "lng": 72.8777},
    "DEL": {"lat": 28.6139, "lng": 77.2090},
    "BLR": {"lat": 12.9716, "lng": 77.5946},
    "HYD": {"lat": 17.3850, "lng": 78.4867}
}

# Generate dummy route map data based on top routes
def generate_route_map(top_routes):
    route_map = []
    for r in top_routes:
        parts = r['route'].split('-')
        if len(parts) == 2 and parts[0] in ROUTE_COORDS and parts[1] in ROUTE_COORDS:
            route_map.append({
                "name": r['route'],
                "from": ROUTE_COORDS[parts[0]],
                "to": ROUTE_COORDS[parts[1]],
                "passengers": r.get('passengers', 0)
            })
    return route_map

@app.route('/')
def index():
    routes = load_routes()
    return render_template('index.html', routes=routes)

@app.route('/get_insights', methods=['POST'])
def get_insights():
    route = request.form.get('route', 'SYD-MEL')
    routes = load_routes()
    insights = generate_insights(routes)
    return jsonify({
        'flights': generate_mock_flights(route),
        'price_trends': insights['price_trends'].get(route, {'dates': [], 'prices': []}),
        'demand_heatmap': insights['demand_heatmap'],
        'top_routes': insights['top_routes'],
        'suggestions': generate_booking_suggestions(),  # added dummy suggestions
        'route_map': generate_route_map(insights['top_routes'])  # added dummy route map
    })

def generate_mock_flights(route):
    airlines = ["Air India", "IndiGo", "Akasa", "Vistara"]
    flights = []
    for i in range(5):
        hour = 6 + i*2
        flights.append({
            'airline': np.random.choice(airlines),
            'flight_number': f"{np.random.choice(['AI','6E','QP','UK'])}{np.random.randint(100, 999)}",
            'departure': f"{hour:02d}:{np.random.choice(['00','15','30','45'])}",
            'arrival': f"{(hour+2)%24:02d}:{np.random.choice(['00','15','30','45'])}",
            'status': np.random.choice(['On Time', 'Delayed']),
            'price': np.random.randint(150, 500)
        })
    return flights

if __name__ == '__main__':
    app.run(debug=True, port=5001)
