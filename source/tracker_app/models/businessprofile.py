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

class BusinessProfile:
    def __init__(self, business_name, location_city, business_id=None):
        self.business_id = business_id
        self.business_name = business_name
        self.location_city = location_city

    def to_dict(self):
        return {
            "business_id": self.business_id,
            "business_name": self.business_name,
            "location_city": self.location_city
        }

    @staticmethod
    def from_dict(d):
        return BusinessProfile(
            business_name=d.get("business_name", ""),
            location_city=d.get("location_city", ""),
            business_id=d.get("business_id", None)
        )

    @staticmethod
    def is_location_allowed(city_name, allowed_city_names):
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