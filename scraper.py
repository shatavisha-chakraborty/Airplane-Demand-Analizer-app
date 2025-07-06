import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape_routes():
    url = "https://en.wikipedia.org/wiki/List_of_busiest_passenger_air_routes"
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find_all('table', {'class': 'wikitable'})[0]
        routes = []

        for row in table.find_all('tr')[1:]:
            cols = row.find_all(['td', 'th'])
            if len(cols) >= 2:
                route = cols[0].get_text(strip=True)
                passengers = cols[1].get_text(strip=True).replace(',', '').replace(' ', '')
                try:
                    passengers = int(passengers)
                except:
                    passengers = 0
                routes.append([route, passengers])

        df = pd.DataFrame(routes, columns=["route", "passengers"])
        df.to_csv('data/routes.csv', index=False)
        print("✅ Saved to data/routes.csv")

    except Exception as e:
        print("❌ Error scraping:", e)

if __name__ == "__main__":
    scrape_routes()
