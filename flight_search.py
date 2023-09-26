import requests
from flight_data import FlightDataRound, FlightDataOneWay

TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com/locations/query"
TEQUILA_ENDPOINT_SEARCH = "https://api.tequila.kiwi.com/v2/search"
TEQUILA_API_KEY = "rxlLcwf1vKU5wHOcerjPrRs8f5mKgs8R"


class FlightSearch:

    def get_destination_code(self, city_name):
        headers = {"apikey": TEQUILA_API_KEY}
        params = {
            "term": city_name,
            "location_types": "city"
        }
        response = requests.get(url=TEQUILA_ENDPOINT, headers=headers, params=params)
        response.raise_for_status()
        code = response.json()['locations'][0]['code']
        return code

    def get_flight_prices_one_way(self,
                                  city_from,
                                  city_to, city_dest,
                                  date_from, date_to,
                                  flight_type,
                                  children=0, infants=0, adults=1,
                                  max_stopovers=1, currency="USD",
                                  sort_by="price", limit=20
                                  ):
        headers = {"apikey": TEQUILA_API_KEY}
        params = {
            "fly_from": city_from,
            "fly_to": city_to,
            "date_from": date_from,
            "date_to": date_to,
            "curr": currency,
            "flight_type": flight_type,
            "max_stopovers": max_stopovers,
            "sort": "price",
            "limit": limit,
            "sort_by": sort_by,
            "adults": adults,
            "children": children,
            "infants": infants,
        }
        response = requests.get(url=TEQUILA_ENDPOINT_SEARCH, headers=headers, params=params)
        response.raise_for_status()

        flight_data_list = []

        for i in range(0, 20):
            try:
                data = response.json()["data"][i]
                # pprint(data)
                flight_data = FlightDataOneWay(
                    count=(i+1),
                    price=data["price"],
                    origin_city=data["cityFrom"],
                    origin_airport=data["flyFrom"],
                    destination_city=data["cityTo"],
                    destination_airport=data["flyTo"],
                    out_date=data["local_departure"].split("T")[0],
                    out_time=data["local_departure"].split("T")[1][:5],
                    arrive_date=data["local_arrival"].split("T")[0],
                    arrive_time=data["local_arrival"].split("T")[1][:5],
                    duration=round(float(data["duration"]["total"]/3600), 2),
                    stopovers_count=(len(data["route"])-1)
                )
                flight_data_list.append(flight_data)

            except IndexError:
                break

        return flight_data_list

    def get_flight_prices_round(self,
                                city_from,
                                city_to, city_dest,
                                date_from, date_to,
                                flight_type,
                                children=0, infants=0, adults=1,
                                max_stopovers=1, currency="USD",
                                rtrn_from="", rtrn_to="",
                                sort_by="price", limit=20
                                ):
        headers = {"apikey": TEQUILA_API_KEY}
        params = {
            "fly_from": city_from,
            "fly_to": city_to,
            "date_from": date_from,
            "date_to": date_to,
            "curr": currency,
            "flight_type": flight_type,
            # "one_for_city": 1,
            "max_stopovers": max_stopovers,
            "sort": "price",
            "limit": limit,
            "return_from": rtrn_from,
            "return_to": rtrn_to,
            "sort_by": sort_by,
            "adults": adults,
            "children": children,
            "infants": infants,
        }
        response = requests.get(url=TEQUILA_ENDPOINT_SEARCH, headers=headers, params=params)
        response.raise_for_status()

        flight_data_list = []

        for i in range(0, 20):
            try:
                data = response.json()["data"][i]
                # pprint(data)
                flight_data = FlightDataRound(
                    count=(i + 1),
                    price=data["price"],
                    origin_city=data["cityFrom"],
                    origin_airport=data["flyFrom"],
                    destination_city=data["cityTo"],
                    destination_airport=data["flyTo"],
                    out_date=data["local_departure"].split("T")[0],
                    out_time=data["local_departure"].split("T")[1][:5],
                    arrive_date=data["local_arrival"].split("T")[0],
                    arrive_time=data["local_arrival"].split("T")[1][:5],
                    duration=round(float(data["duration"]["departure"] / 3600), 2),
                    stopovers_count=(len(data["route"]) - 2),
                    back_out_date=data["route"][1]["local_departure"].split("T")[0],
                    back_out_time=data["route"][1]["local_departure"].split("T")[1][:5],
                    back_arrive_date=data["route"][1]["local_arrival"].split("T")[0],
                    back_arrive_time=data["route"][1]["local_arrival"].split("T")[1][:5],
                    back_stopovers_count=(len(data["route"]) - 2),
                    back_duration=round(float(data["duration"]["return"] / 3600), 2),
                    )
                flight_data_list.append(flight_data)

            except IndexError:
                break

        return flight_data_list
