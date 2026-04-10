# Creates a BusinessProfile object that represents a business profile.


class BusinessProfile:
    def __init__(
        self,
        business_name,
        location_city,
        business_id=None,
        latitude=None,
        longitude=None,
    ):
        self.business_id = business_id
        self.business_name = business_name
        self.location_city = location_city
        self.latitude = latitude
        self.longitude = longitude

        self.employees = []
        self.sections = {}
        self.total_packages = 0

    def to_dict(self):
        return {
            "business_id": self.business_id,
            "business_name": self.business_name,
            "location_city": self.location_city,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "employees": self.employees,
            "sections": self.sections,
            "total_packages": self.total_packages,
        }

    @staticmethod
    def from_dict(data):
        business = BusinessProfile(
            business_name=data.get("business_name", ""),
            location_city=data.get("location_city", ""),
            business_id=data.get("business_id"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
        )

        employees = data.get("employees", [])
        sections = data.get("sections", {})
        total_packages = data.get("total_packages", 0)

        business.employees = employees if isinstance(employees, list) else []
        business.sections = sections if isinstance(sections, dict) else {}
        business.total_packages = total_packages if isinstance(total_packages, int) else 0

        return business

    def add_employee(self, user_id):
        if user_id not in self.employees:
            self.employees.append(user_id)

    def add_section(self, section_name):
        if section_name not in self.sections:
            self.sections[section_name] = []

    def assign_package(self, section_name, package_id):
        if section_name in self.sections:
            self.sections[section_name].append(package_id)
            self.total_packages += 1

    def move_package(self, from_section, to_section, package_id):
        if from_section in self.sections and to_section in self.sections:
            if package_id in self.sections[from_section]:
                self.sections[from_section].remove(package_id)
                self.sections[to_section].append(package_id)
