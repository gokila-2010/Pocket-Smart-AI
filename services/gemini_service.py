import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from services.mock_platform_service import (
    get_home_products,
    get_party_services,
    get_jewelry_products
)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing in .env file")

client = genai.Client(api_key=api_key)


# =========================================================
# GEMINI TEXT MODELS
# =========================================================

TEXT_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-flash-latest"
]


# =========================================================
# GEMINI TEXT GENERATOR
# =========================================================

def generate_text_with_fallback(prompt):

    last_error = None

    for model in TEXT_MODELS:

        try:
            print(f"Trying Gemini model: {model}")

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            if response.text:
                print(f"Successful Gemini model: {model}")
                return response.text

        except Exception as e:

            last_error = e
            print(f"Gemini model failed: {e}")

    print("All Gemini models failed.")
    print("Using local fallback recommendation.")

    return None


# =========================================================
# HOME LOCAL FALLBACK
# =========================================================

def local_home_recommendation(
    budget,
    room_type,
    items
):

    item_text = ", ".join(items) if items else "General room requirements"

    mock_products = get_home_products(
        budget,
        items
    )

    if mock_products:
        product_text = "\n".join(
            f"- {product['name']} | "
            f"Platform: {product['platform']} (Mock Data) | "
            f"Approx. Price: ₹{product['price']}"
            for product in mock_products
        )
    else:
        product_text = "No matching mock products found within the budget."

    return f"""
🏠 PocketSmart AI - Home Recommendation

Budget: ₹{budget}
Room: {room_type}
Required Items: {item_text}

🛒 Mock Platform Recommendations:

{product_text}

💡 Budget Suggestion:

Choose products that fit within your ₹{budget} budget.

The platform information and prices shown above are
simulated/mock data for project demonstration purposes.
They are not live prices.

Note:
Prices are approximate and may vary by brand, store and location.
"""
# =========================================================
# HOME RECOMMENDATIONS
# =========================================================

def generate_home_recommendations(
    budget,
    room_type,
    items
):

    item_text = ", ".join(items) if items else "General room requirements"

    # Get matching products from our local mock platform data
    mock_products = get_home_products(budget, items)

    if mock_products:
        product_text = "\n".join(
            f"- {product['name']} | Platform: {product['platform']} | "
            f"Category: {product['category']} | Approx. Price: ₹{product['price']}"
            for product in mock_products
        )
    else:
        product_text = "No matching mock products found within the budget."

    prompt = f"""
You are PocketSmart AI, a smart budget and recommendation assistant.

The user wants to plan home shopping.

Budget: ₹{budget}
Room Type: {room_type}
Required Items: {item_text}

The following are locally stored mock platform products.
They are simulated data for demonstration purposes, NOT live listings:

{product_text}

Give practical recommendations within the budget.

For each requested item:
- Suggest suitable options.
- Use the mock platform products when relevant.
- Mention the platform name when using a mock product.
- Give an approximate price.
- Mention quantity where useful.
- Explain briefly why it is suitable.

Keep the total estimated cost within the budget.

Do not claim prices are live or exact.
Do not say that you accessed Amazon, IKEA, or any external website.
Clearly treat the platform information as simulated/mock data.

Use clear headings and bullet points.
"""

    result = generate_text_with_fallback(prompt)

    if result:
        return result

    return local_home_recommendation(
        budget,
        room_type,
        items
    )

# =========================================================
# PARTY LOCAL FALLBACK
# =========================================================

def local_party_recommendation(
    budget,
    guest_count,
    event_type,
    venue
):

    mock_services = get_party_services(
        budget,
        guest_count
    )

    if mock_services:
        service_text = "\n".join(
            f"- {service['name']} | "
            f"Platform: {service['platform']} (Mock Data) | "
            f"Estimated Cost: ₹{service.get('estimated_cost', service.get('price', 0))}"
            for service in mock_services
        )
    else:
        service_text = "No matching mock services found within the budget."

    return f"""
🎉 PocketSmart AI - Party Recommendation

Budget: ₹{budget}
Guests: {guest_count}
Event: {event_type}
Venue: {venue}

🛒 Mock Platform Recommendations:

{service_text}

💡 Budget Suggestion:

Use the available mock services that fit within your
₹{budget} budget.

The platform information and prices shown above are
simulated/mock data for project demonstration purposes.
They are not live prices.

Note:
Prices are approximate and may vary depending on location,
vendor and requirements.
"""

# =========================================================
# PARTY RECOMMENDATIONS
# =========================================================

def generate_party_recommendations(
    budget,
    guest_count,
    event_type,
    venue
):

    # Get matching services from our local mock platform data
    mock_services = get_party_services(
        budget,
        guest_count
    )

    if mock_services:
        service_text = "\n".join(
            f"- {service['name']} | Platform: {service['platform']} | "
            f"Category: {service['category']} | "
            f"Estimated Cost: ₹{service.get('estimated_cost', service.get('price', 0))}"
            for service in mock_services
        )
    else:
        service_text = "No matching mock services found within the budget."

    prompt = f"""
You are PocketSmart AI, a smart budget recommendation assistant.

Party requirements:

Budget: ₹{budget}
Guests: {guest_count}
Event: {event_type}
Venue: {venue}

The following are locally stored mock platform services.
They are simulated data for demonstration purposes, NOT live listings:

{service_text}

Create a practical party plan within the budget.

Include:

1. Catering
2. Decoration
3. Entertainment

For each category:
- Suggest a suitable option.
- Use the mock platform services when relevant.
- Mention the platform name when using a mock service.
- Give an approximate cost.
- Give a short explanation.

Keep the total estimated cost within ₹{budget}.

Do not claim prices are live or exact.
Do not say that you accessed Zomato or any external website.
Clearly treat the platform information as simulated/mock data.

Use simple headings and bullet points.
"""

    result = generate_text_with_fallback(prompt)

    if result:
        return result

    return local_party_recommendation(
        budget,
        guest_count,
        event_type,
        venue
    )
# =========================================================
# JEWELRY LOCAL FALLBACK
# =========================================================
def local_jewelry_recommendation(
    budget,
    occasion,
    style
):

    mock_products = get_jewelry_products(
        budget,
        style
    )

    if mock_products:
        product_text = "\n".join(
            f"- {product['name']} | "
            f"Platform: {product['platform']} (Mock Data) | "
            f"Approx. Price: ₹{product['price']}"
            for product in mock_products
        )
    else:
        product_text = "No matching mock jewelry products found within the budget."

    return f"""
💎 PocketSmart AI - Jewelry Recommendation

Budget: ₹{budget}
Occasion: {occasion}
Style: {style}

🛒 Mock Platform Recommendations:

{product_text}

💡 Style Suggestion:

Choose jewelry that matches the selected {style.lower()} style
and is suitable for the {occasion.lower()} occasion.

The platform information and prices shown above are
simulated/mock data for project demonstration purposes.
They are not live prices.

Since no outfit image was available, the recommendation is
based on the selected occasion, style and budget.

Note:
Prices are approximate and may vary by brand, material,
store and location.
"""
# =========================================================
# JEWELRY RECOMMENDATIONS
# =========================================================

def generate_jewelry_recommendations(
    budget,
    occasion,
    style,
    image_bytes=None,
    image_mime_type=None
):

    print("JEWELRY SERVICE CALLED")

    # Get matching products from our local mock platform data
    mock_products = get_jewelry_products(
        budget,
        style
    )

    if mock_products:
        product_text = "\n".join(
            f"- {product['name']} | Platform: {product['platform']} | "
            f"Category: {product['category']} | "
            f"Approximate Price: ₹{product['price']}"
            for product in mock_products
        )
    else:
        product_text = "No matching mock jewelry products found within the budget."

    prompt = f"""
You are PocketSmart AI, a smart budget and recommendation assistant.

User's jewelry requirements:

Budget: ₹{budget}
Occasion: {occasion}
Style: {style}

The following are locally stored mock platform products.
They are simulated data for demonstration purposes, NOT live listings:

{product_text}

Suggest suitable jewelry within the given budget.

Include:

1. Recommended jewelry type
2. Approximate price
3. Material or design suggestion
4. Why it suits the occasion and style

Use the mock platform products when relevant.
Mention the platform name when using a mock product.

Keep the total estimated cost within ₹{budget}.

Do not claim prices are live or exact.
Do not say that you accessed Amazon or any external website.
Clearly treat the platform information as simulated/mock data.

Use simple headings and bullet points.
"""

    # =====================================================
    # NO IMAGE
    # =====================================================

    if not image_bytes:

        print("No outfit image provided.")

        result = generate_text_with_fallback(prompt)

        if result:
            return result

        print("Gemini unavailable. Using local jewelry recommendation.")

        return local_jewelry_recommendation(
            budget,
            occasion,
            style
        )

    # =====================================================
    # IMAGE PROVIDED
    # =====================================================

    print("Outfit image received.")

    image_prompt = f"""
{prompt}

The user has uploaded an outfit image.

Analyze the outfit and additionally:

- Identify the main outfit colors.
- Suggest jewelry colors that coordinate with the outfit.
- Suggest jewelry designs that match the outfit style.
- Explain why the jewelry matches the outfit.
"""

    try:

        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=image_mime_type
        )

        image_models = [
            "gemini-3.8-flash",
        ]

        for model in image_models:

            try:

                print(f"Trying image model: {model}")

                response = client.models.generate_content(
                    model=model,
                    contents=[
                        image_prompt,
                        image_part
                    ]
                )

                if response.text:
                    print(f"Successful image model: {model}")
                    return response.text

            except Exception as e:

                print(f"IMAGE MODEL ERROR: {type(e).__name__}: {e}")

        print("Image analysis unavailable.")
        print("Using normal jewelry recommendation.")

        return f"""
{local_jewelry_recommendation(
    budget,
    occasion,
    style
)}

📷 Outfit Image Note:
The outfit image could not be analyzed because the Gemini image model is currently unavailable. The recommendation above is based on your budget, occasion and selected style.
"""

    except Exception as e:

        print(f"Image processing error: {e}")

        return f"""
{local_jewelry_recommendation(
    budget,
    occasion,
    style
)}

📷 Outfit Image Note:
The image could not be analyzed at this time. The recommendation above is based on your budget, occasion and selected style.
"""