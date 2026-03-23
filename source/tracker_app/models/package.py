class Package:
    def __init__(self, business_id, user_id, source_city, destination_city, weight, description, shipping_cost, package_id=None, current_location="Processing"):
        self.package_id = package_id
        self.business_id = business_id
        self.user_id = user_id
        self.source_city = source_city
        self.destination_city = destination_city
        self.weight = weight
        self.description = description
        self.shipping_cost = shipping_cost
        self.current_location = current_location # Defaults to processing

    def to_dict(self):
        return {
            "package_id": self.package_id,
            "business_id": self.business_id,
            "user_id": self.user_id,
            "source_city": self.source_city,
            "destination_city": self.destination_city,
            "weight": self.weight,
            "description": self.description,
            "shipping_cost": self.shipping_cost,
            "current_location": self.current_location
        }

    @staticmethod
    def from_dict(d):
        return Package(
            package_id=d.get("package_id", None),
            business_id=d.get("business_id", None),
            user_id=d.get("user_id", None),
            source_city=d.get("source_city", ""),
            destination_city=d.get("destination_city", ""),
            weight=d.get("weight", 0.0),
            description=d.get("description", ""),
            shipping_cost=d.get("shipping_cost", 0.0),
            current_location=d.get("current_location", "Processing")
        )