import datetime

class Package:
    def __init__(self, business_id, user_id, source_city, destination_city, weight, description, shipping_cost, package_id=None, current_location="Processing", dest_lat=None, dest_lon=None, distance_km=0.0, time_created=None):
        self.package_id = package_id
        self.business_id = business_id
        self.user_id = user_id
        self.source_city = source_city
        self.destination_city = destination_city
        self.weight = weight
        self.description = description
        self.shipping_cost = shipping_cost
        self.current_location = current_location # Defaults to processing
        self.dest_lat = dest_lat
        self.dest_lon = dest_lon
        self.distance_km = distance_km
        self.time_created = time_created or datetime.datetime.now().isoformat()

    def update_status(self):
        """Calculates the status based on real-world time elapsed."""
        start_time = datetime.datetime.fromisoformat(self.time_created)
        elapsed_seconds = (datetime.datetime.now() - start_time).total_seconds()

        # LOGIC:
        # 0-30 seconds: Processing
        # 30-120 seconds: In Transit
        # > 120 seconds: Delivered
        if elapsed_seconds > 120:
            self.current_location = "Delivered"
        elif elapsed_seconds > 30:
            self.current_location = "In Transit"
        else:
            self.current_location = "Processing"

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
            "current_location": self.current_location,
            "dest_lat": self.dest_lat,
            "dest_lon": self.dest_lon,
            "distance_km": self.distance_km,
            "time_created": self.time_created
        }

    @staticmethod
    def from_dict(d):
        pkg = Package(
            package_id=d.get("package_id", None),
            business_id=d.get("business_id", None),
            user_id=d.get("user_id", None),
            source_city=d.get("source_city", ""),
            destination_city=d.get("destination_city", ""),
            weight=d.get("weight", 0.0),
            description=d.get("description", ""),
            shipping_cost=d.get("shipping_cost", 0.0),
            current_location=d.get("current_location", "Processing"),
            dest_lat=d.get("dest_lat"),
            dest_lon=d.get("dest_lon"),
            distance_km=d.get("distance_km", 0.0),
            time_created=d.get("time_created")
        )
        pkg.update_status()
        return pkg