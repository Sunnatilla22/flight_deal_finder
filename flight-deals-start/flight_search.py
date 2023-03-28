import json

import requests
from pprint import pprint
from datetime import datetime, timedelta
from flight_data import FlightData



TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
FLIGHT_SEARCH_ENDPOINT = "https://api.tequila.kiwi.com/v2/search"
TEQUILA_API_KEY = "cQgNkX211LDfv0aQz5hbC3n_2lLDL6su"

header = {
    "apikey": TEQUILA_API_KEY
}

cities_list = ["Paris", "Berlin", "Tokyo", "Miami", "Istanbul",
               "Kuala Lumpur", "New York", "San Francisco", "Cape Town"]

iata_codes = []
for city in cities_list:
    params = {
        "term": city,
        "locale": "en_US",
        "location_types": "city",
        "stop_overs": 1,

    }

    response = requests.get(url=f"{TEQUILA_ENDPOINT}/locations/query", params=params, headers=header)
    data = response.json()["locations"][0]["code"]
    # print(data)
    iata_codes.append(data)
print(iata_codes)
######################################## Flyights ###############################
tomorrow = (datetime.now() + timedelta(days=180)).strftime("%x")
time_after_6_month = (datetime.now() + timedelta(days=180)).strftime("%x")
min_date_of_trip = (datetime.now() + timedelta(days=7)).strftime("%x")
max_date_of_trip = (datetime.now() + timedelta(days=30)).strftime("%x")

print(time_after_6_month)
print(tomorrow)
print(min_date_of_trip)
print(max_date_of_trip)

for code in iata_codes:

    flight_params = {
                    "fly_from": "LON",
                    "fly_to": code,
                    "date_from ": tomorrow,
                    "date_to ": time_after_6_month,
                    "nights_in_dst_from":7,
                    "nights_in_dst_to":28,
                    "flight_type": "round",
                    "one_for_city": 1,
                    "max_stopovers": 0,
                    "curr": "GBP"
                }

    search_response = requests.get(url=FLIGHT_SEARCH_ENDPOINT, params=flight_params, headers=header)
        # search_response = requests.get(url="https://api.tequila.kiwi.com/v2/search?fly_from=LGA&fly_to=MIA&dateFrom=01/01/2023&dateTo=01/02/2023", headers=header)
    # print(search_response.text)
    res = search_response.json()
    print(f"{res['data'][0]['cityTo']}: € {res['data'][0]['price']}")

class FlightSearch:
    def get_destination_code(self, city_name):
        params = {
            "term": city_name,
            "location_types": "city",
        }

        header = {
            "apikey": TEQUILA_API_KEY
        }
        response = requests.get(url=f"{TEQUILA_ENDPOINT}/locations/query", params=params, headers=header)
        response = response.json()["locations"]
        code = response[0]["code"]
        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        print(f"Check flights triggered for {destination_city_code}")
        headers = {"apikey": os.environ["TEQUILA_API_KEY"]}
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 30,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }

        response = requests.get(
            url=f"{TEQUILA_ENDPOINT}/v2/search",
            headers=headers,
            params=query,
        )

        try:
            data = response.json()["data"][0]
        except IndexError:

            ##########################
            query["max_stopovers"] = 1
            response = requests.get(
                url=f"{TEQUILA_ENDPOINT}/v2/search",
                headers=headers,
                params=query,
            )
            data = response.json()["data"][0]
            pprint(data)
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][1]["cityTo"],
                destination_airport=data["route"][1]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][2]["local_departure"].split("T")[0],
                stop_overs=1,
                via_city=data["route"][0]["cityTo"]
            )
            return flight_data
            ###########################
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )

            return flight_data