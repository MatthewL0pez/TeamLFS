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
    def __init__(self, first_name, last_name, email, phone, billing_info, business_id, user_id=None):
        self.user_id = user_id
        self.business_id = business_id

        self.first_name = first_name
        self.last_name = last_name

        self.email = email
        self.phone = phone

        # keeping billing_info as a simple string for now
        self.billing_info = billing_info    # Billing info will be used as conditional to check: (if invalid/no billing info -> do not allow package creation)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "business_id": self.business_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "billing_info": self.billing_info
        }

    @staticmethod
    def from_dict(d):
        return UserProfile(
            first_name=d.get("first_name", ""),
            last_name=d.get("last_name", ""),
            email=d.get("email", ""),
            phone=d.get("phone", ""),
            billing_info=d.get("billing_info", ""),
            business_id=d.get("business_id", None),
            user_id=d.get("user_id", None)
        )

    def belongs_to_business(self, business_id):
        return self.business_id == business_id


# Example use:
# You should only create a user after a business exists.
#
#   selected_business_id = 1
#   u = UserProfile("Matthew", "Lopez", "matthewlopez@email.com", "310-255-1234", "VISA 1111..."", selected_business_id)
#   u.user_id = 1                   # storage assigns later
#   print(u.to_dict())
