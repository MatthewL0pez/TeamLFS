# Creates a UserProfile object that represents a userprofile 

# UserProfile example:

# This represents a user profile under a specific busines
# Each user should belong to a business, so we can store business_id.

# - user_id         (numaber assigned for storage later)
# - business_id     (which business this user belongs to)
# - first_name, last_name
# - email, phone
# - billing_info    (kept as simple text for now since I dont know what billing_info should be)

class UserProfile: 
    def __init__(self, first_name, last_name, email, phone, billing_info, user_id = None):
        self.user_id = user_id          # ID set to None
        self.business_id = business_id  # buissness which user belongs to
        self.first_name = first_name
        self.last_name = last_name
        self.email = email              # user contact info
        self.phone = phone

        self.billing_info = billing_info # SIMPLE SO FAR just implemented as a string <<<<

    @staticmethod # function doesnt need a self input argument <<
    def from_dictionary(d):
        return UserProfile(     # turns the JSON dicitionaries into a UserProfile class object
            first_name =d.get("first_name", ""),
            last_name = d.get("last_name", ""),
            email = d.get("email", ""),
            phone = d.get("phone", ""),
            billing_info = d.get("billing_info", ""),
            business_id = d.get("business_id", None),
            user_id =d .get("user_id", None)
        )
    
     def belongs_to_business(self, business_id): #checks if user belongs to a business 
        return self.business_id == business_id


# Example use:
# You should only create a user after a business exists.
#
#   selected_business_id = 1
#   u = UserProfile("Matthew", "Lopez", "matthewlopez@email.com", "310-255-1234", "VISA 1111..."", selected_business_id)
#   u.user_id = 1                   # storage assigns later
#   print(u.to_dict())