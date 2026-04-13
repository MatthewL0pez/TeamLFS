class FinanceService:
    # Estimated cost for the business to move a vehicle 1km
    # (Fuel + Maintenance + Insurance)
    OPERATIONAL_COST_PER_KM = 0.005  
    FIXED_HANDLING_COST = 1.00 # Cost of labor/packaging per box

    @staticmethod
    def calculate_business_report(packages):
        """Aggregates financial data for a specific business."""
        if not packages:
            return None

        total_revenue = sum(p.shipping_cost for p in packages)
        total_weight = sum(p.weight for p in packages)
        package_count = len(packages)
        
        total_op_expenses = sum(
            (p.distance_km * FinanceService.OPERATIONAL_COST_PER_KM) + 
            FinanceService.FIXED_HANDLING_COST
            for p in packages
        )
        
        net_profit = total_revenue - total_op_expenses
        margin = (net_profit / total_revenue) * 100 if total_revenue > 0 else 0

        return {
            "revenue": total_revenue,
            "expenses": total_op_expenses,
            "profit": net_profit,
            "margin": margin,
            "total_weight": total_weight,
            "package_count": package_count,
            "avg_pkg_price": total_revenue / package_count if package_count > 0 else 0,
            "avg_weight_per_pkg": total_weight / package_count if package_count > 0 else 0
        }

    @staticmethod
    def calculate_user_expenditures(packages):
        """Calculates how much a specific user has spent."""
        total_spent = sum(p.shipping_cost for p in packages)
        pkg_count = len(packages)
        return {
            "total_spent": total_spent,
            "package_count": pkg_count,
            "avg_cost_per_pkg": total_spent / pkg_count if pkg_count > 0 else 0,
        }