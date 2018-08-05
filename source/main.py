import requests
import json

userKey = ""
version = "v2.1"
baseUrl = "https://developers.zomato.com/api/"


def getCurrentLocation():
    return {
        "latitude" : 12.918847,
        "longitude" : 77.629428
    }

def getCityId(latitude, longitude):
    citiesExtension = "/cities"
    url = baseUrl + version + citiesExtension
    headers = {
        "Accept" : "application/json",
        "user-key" : userKey,
    }
    params = {
        "lat" : latitude,
        "lon" : longitude
    }
    response = requests.get(url=url, headers = headers, params=params)
    data = response.json()
    cityId = data["location_suggestions"][0]["id"]
    cityName = data["location_suggestions"][0]["name"]
    print("You are in " + cityName)
    return cityId

def getCuisines(cityId):
    cuisinesExtension = "/cuisines"
    url = baseUrl + version + cuisinesExtension
    headers = {
        "Accept" : "application/json",
        "user-key" : userKey,
    }
    params = {
        "city_id" : cityId
    }
    cuisines = requests.get(url = url, headers = headers, params = params)
    return cuisines.json()

def getEntityTypeAndId(locationName):
    locationsExtension = "/locations"
    url = baseUrl + version + locationsExtension
    headers = {
        "Accept" : "application/json",
        "user-key" : userKey,
    }
    params = {
        "query" : locationName
    }
    response = requests.get(url = url, headers = headers, params = params)
    data = response.json()
    return [data["location_suggestions"][0]["entity_type"], data["location_suggestions"][0]["entity_id"]]

def getBestRatedRestaurantsNearby(entityType, entityId, averageCostForTwo, count):
    locationDetailsExtension = "/location_details"
    url = baseUrl + version + locationDetailsExtension
    headers = {
        "Accept" : "application/json",
        "user-key" : userKey,
    }
    params = {
        "entity_type" : entityType,
        "entity_id" : entityId
    }
    response = requests.get(url = url, headers = headers, params = params)
    data = response.json()
    
    bestRatedRestaurants = sorted(data["best_rated_restaurant"], 
                                  key= lambda s: s["restaurant"]["user_rating"]["aggregate_rating"])
    bRRUnderBudget = [x for x in bestRatedRestaurants if x["restaurant"]["average_cost_for_two"] <= averageCostForTwo] 
    length = len(bRRUnderBudget)
    return bRRUnderBudget[:length if length < count else count]




if __name__ == "__main__":
    print("enter user key:")
    userKey = input()
    location = getCurrentLocation()
    getCityId(location["latitude"], location["longitude"])
    locationName = "HSR"
    entity_type, entity_id = getEntityTypeAndId(locationName)
    brrUnderBudget = getBestRatedRestaurantsNearby(entityId= entity_id, 
                                  entityType = entity_type,
                                  averageCostForTwo = 1500,
                                  count = 10)
    print([x["restaurant"]["name"] for x in brrUnderBudget])




