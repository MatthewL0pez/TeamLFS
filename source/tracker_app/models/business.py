# Creates a BUSINESSPROFILE object that represents a buissness profile


# BusinessProfile example:
# 
# This file creates a "BusinessProfile" class.
# A BusinessProfile is data we store about a business:

# - business_id      (number assigned by storage later)
# - business_name    (buissness name chosen)
# - location_city    (city from data/locations.json)
#
# **business_id**    <<<<<< NOTE
# the storage layer will assign business_id = 1, 2, 3, ... to be pulled from

class BuissnessProfile:         # profile of buissness 

    def __init__(self, buissness_name, location_city, buissness_id = None):
        self.buissness_id = buissness_id        #(1, 2, 3, ...)
        self.buisness_name = buissness_name     # Buisness name string
        self.location_city = location_city      # city from locations.json

    def dictionary_conversion(self): # takes the JSON into a dictionary since it cant be 
                                     #saved as a python object
        return {
            "business_id": self.business_id,
            "business_name": self.business_name,
            "location_city": self.location_city
        }

    @staticmethod # function doesnt need a self input argument <<
    
    def from_dictionary(d):         # turns the JSON dicitionaries into a BuissnessProfile class object
        return {
            business_name=d.get("business_name", ""),
            location_city=d.get("location_city", ""),
            business_id=d.get("business_id", None)
        }     
    
    @staticmethod

    def is_location_allowed(city_name, allowed_city_names):    #checks if the city location is allowed 
        return city_name in allowed_city_names
        
    # Example implmentation: ^^^^^
    # allowed = location_service.list_city_names()
    # if not BusinessProfile.is_location_allowed(city, allowed):
    #     print("Pick a valid city.")

#  Example file use:

# 1. UI will show city options from locations.json like:

#   cities = location_service.list_city_names()
#   print(cities)


# 2.  User chooses one city from json. and create the business:
#     bizz = BusinessProfile("Name of the Business", "New York City")
#
# 3. Storage assigns Business ID later:
#     biz.business_id = 1
#
# 4. Save it to json.
#     json_ready = biz.to_dict() 
#
# Logging out should NOT erase biz.location_city.
# Instead, the app_state should clear the currently selected business:
#   state["active_business_id"] = None
# so the business/location is not selected anymore.