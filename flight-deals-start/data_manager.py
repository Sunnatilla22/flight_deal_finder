import requests
from pprint import pprint

SHEETY_PRICES_ENDPOINT = 'https://api.sheety.co/d886ea813f3619317363aeb768f6a88b/flightDeals/prices'
PUT_ENDPOINT = 'https://api.sheety.co/d886ea813f3619317363aeb768f6a88b/flightDeals/prices'

# response = requests.get(SHEETY_PRICES_ENDPOINT)
# data = response.json()["prices"]
#
# print(len(data))

# pprint(data["prices"][0]["iataCode"])
# pprint(data)

# for prices in data["prices"]:
#     put_data = {
#         "prices": {
#             prices["iataCode"]: "TESTING"
#         }
#     }

# put_data = {
#     "price": {
#         "iataCode": "TESTING"
#     }
# }
# for num in range(2, len(data)+2):
#     put_response = requests.put(f"{SHEETY_PRICES_ENDPOINT}{num}", json=put_data)
#     pprint(put_response.json())
#     print(put_response.text)
#
# response = requests.get(SHEETY_PRICES_ENDPOINT)
# data = response.json()
# pprint(data)

class DataManager:
    #This class is responsible for talking to the Google Sheet.

    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        self.response = requests.get(SHEETY_PRICES_ENDPOINT)
        data = self.response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=new_data
            )
            print(response.text)