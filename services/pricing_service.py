

class PricingService:
    # Constants for price calculations (adjustable)
    BASE_SHIPPING_FEE = 2.50   # Base cost in dollars
    RATE_PER_KM = 0.01         # $0.01 per kilometer
    RATE_PER_KG = 0.25         # $0.25 per kilogram

    @staticmethod
    def calculate_shipping_cost(distance_km, weight_kg):
        """ Calculates the total price of shipping based on distance and weight. """
        if distance_km is None:
            raise ValueError("Distance cannot be None. Check city coordinates.")
        
        billable_distance = max(distance_km, 0.1)
        if weight_kg <= 0:
            raise ValueError("Package weight must be greater than zero.")

        distance_cost = billable_distance * PricingService.RATE_PER_KM
        weight_cost = weight_kg * PricingService.RATE_PER_KG
        
        total_price = PricingService.BASE_SHIPPING_FEE + distance_cost + weight_cost
        
        return round(total_price, 2)

    @staticmethod
    def generate_invoice_data(city1, city2, distance, weight, cost):
        """ Formats the data specifically for the 'Display Invoice' use case. """
        return {
            "Route": f"{city1} to {city2}",
            "Distance": f"{distance:.2f} km",
            "Weight": f"{weight:.2f} kg",
            "Total Price": f"${cost:.2f}"
        }