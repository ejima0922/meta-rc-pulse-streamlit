import math

TSUBO_TO_SQM = 3.30578

SPEC = {
    "ceiling_above_mm": 2100,
    "ceiling_basement_mm": 3000,
    "slab_standard_mm": 180,
    "slab_basement_mm": 300,
    "slab_roof_mm": 220,
    "unit_size_avg_sqm": 18,
    "studio_type_b_sqm": 14,
    "studio_type_c_sqm": 18,
    "studio_booking_unit": 50,
    "studio_open_hours": 16,
    "studio_occupancy": 0.60,
    "room_occupancy": 0.95,
    "target_floors_above": 4,
    "target_height_m": 10,
}

COST_ABOVE_PER_SQM = 550000
COST_BASEMENT_PER_SQM = 1050000

UNIT_INTERIOR_TOTAL = 3920000
STUDIO_ROOM_TOTAL = 10350000
FIXED_COSTS_TOTAL = 208750000
CONTINGENCY_RATE = 0.12
DESIGN_RATE = 0.06

OWNER_NET_RATE = 0.50
DELIVERY_COST_PER_UNIT = 20000
DELIVERY_MARKUP = 0.20
DELIVERY_OWNER = 0.10
VENDING_MONTHLY = 30000
VENDING_OWNER = 0.50

def run_17steps(site_area, site_width, site_depth, coverage_ratio, far, road_width, market_hourly_studio, market_monthly_room, loan_amount=0, loan_rate=0.015, loan_years=30):
    setback = max(0.5, road_width * 0.1) if road_width < 4.0 else 0.0
    effective_area = site_area - (site_width * setback)
    max_building = effective_area * (coverage_ratio / 100)
    practical = max_building * 0.92
    max_far = effective_area * (far / 100)
    above_area = min(practical * 4, max_far)
    basement_area = practical
    unit_count = max(1, int(practical * 3 * 0.9 / 18))
    studio_rooms = 4
    above_cost = int(above_area * COST_ABOVE_PER_SQM)
    basement_cost = int(basement_area * COST_BASEMENT_PER_SQM)
    unit_cost = UNIT_INTERIOR_TOTAL * unit_count
    studio_cost = STUDIO_ROOM_TOTAL * studio_rooms
    subtotal = int(above_cost + basement_cost + unit_cost + studio_cost + FIXED_COSTS_TOTAL)
    total_cost = int(subtotal * (1 + DESIGN_RATE + CONTINGENCY_RATE))
    studio_rate = int(market_hourly_studio * 1.2)
    room_rent = int(market_monthly_room * 1.2)
    studio_monthly = int(studio_rate * (50/60) * 19.2 * 30 * 0.6 * 4)
    room_monthly = int(room_rent * unit_count * 0.95)
    delivery_charge = int(DELIVERY_COST_PER_UNIT * unit_count * 1.2)
    delivery_owner = int(delivery_charge * 0.10)
    vending_owner = int(VENDING_MONTHLY * 0.50)
    owner_from_rent = int(room_monthly * 0.50)
    owner_total = owner_from_rent + int(studio_monthly * 0.50) + delivery_owner + vending_owner
    loan_monthly = 0
    if loan_amount > 0:
        r = loan_rate / 12
        n = loan_years * 12
        loan_monthly = int(loan_amount * r * (1+r)**n / ((1+r)**n - 1))
    net_monthly = owner_total - loan_monthly
    gross_yield = round((room_monthly + studio_monthly) * 12 / total_cost * 100, 2) if total_cost else 0
    net_yield = round(owner_total * 12 / total_cost * 100, 2) if total_cost else 0
    return {
        "unit_count": unit_count,
        "total_cost": total_cost,
        "studio_rate": studio_rate,
        "room_rent": room_rent,
        "studio_monthly": studio_monthly,
        "room_monthly": room_monthly,
        "owner_total": owner_total,
        "delivery_owner": delivery_owner,
        "vending_owner": vending_owner,
        "loan_monthly": loan_monthly,
        "net_monthly": net_monthly,
        "gross_yield": gross_yield,
        "net_yield": net_yield,
    }
