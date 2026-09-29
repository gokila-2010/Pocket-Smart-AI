HOME_PRODUCTS = [
    {
        "platform": "IKEA",
        "name": "LACK Side Table",
        "category": "Furniture",
        "price": 1999,
    },
    {
        "platform": "Amazon",
        "name": "LED Ceiling Light",
        "category": "Lights",
        "price": 2499,
    },
    {
        "platform": "Amazon",
        "name": "Modern Ceiling Fan",
        "category": "Fans",
        "price": 3299,
    },
    {
        "platform": "IKEA",
        "name": "Dining Table Set",
        "category": "Dining Table",
        "price": 8999,
    },
    {
        "platform": "IKEA",
        "name": "3-Seater Sofa",
        "category": "Sofa",
        "price": 14999,
    },
]


PARTY_SERVICES = [
    {
        "platform": "Zomato",
        "name": "Catering Service",
        "category": "Catering",
        "price_per_guest": 250,
    },
    {
        "platform": "Zomato",
        "name": "Party Food Package",
        "category": "Food",
        "price_per_guest": 350,
    },
    {
        "platform": "Local Vendor",
        "name": "Basic Decoration Package",
        "category": "Decoration",
        "price": 5000,
    },
    {
        "platform": "Local Vendor",
        "name": "Premium Decoration Package",
        "category": "Decoration",
        "price": 10000,
    },
]


JEWELRY_PRODUCTS = [
    {
        "platform": "Amazon",
        "name": "Gold-Plated Necklace Set",
        "category": "Traditional",
        "price": 2499,
    },
    {
        "platform": "Amazon",
        "name": "Minimal Pendant Set",
        "category": "Minimal",
        "price": 1799,
    },
    {
        "platform": "Amazon",
        "name": "Bridal Jewelry Set",
        "category": "Bridal",
        "price": 5999,
    },
    {
        "platform": "Amazon",
        "name": "Modern Earrings",
        "category": "Modern",
        "price": 1299,
    },
]


def get_home_products(budget, items):
    results = []

    for product in HOME_PRODUCTS:
        if product["price"] <= budget:
            if not items or product["category"] in items:
                results.append(product)

    return results


def get_party_services(budget, guest_count):
    results = []

    for service in PARTY_SERVICES:
        if "price_per_guest" in service:
            estimated_cost = service["price_per_guest"] * guest_count

            if estimated_cost <= budget:
                item = service.copy()
                item["estimated_cost"] = estimated_cost
                results.append(item)

        else:
            if service["price"] <= budget:
                results.append(service)

    return results


def get_jewelry_products(budget, style):
    results = []

    for product in JEWELRY_PRODUCTS:
        if product["price"] <= budget:
            if not style or product["category"] == style:
                results.append(product)

    return results