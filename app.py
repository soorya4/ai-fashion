import os
import json
import re
import requests
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure OpenRouter (OpenAI-compatible free API)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
if OPENROUTER_API_KEY == "your_openrouter_api_key_here":
    OPENROUTER_API_KEY = ""
OPENROUTER_MODEL = "google/gemma-3-27b-it"

client = None
if OPENROUTER_API_KEY:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )

# Fashion style categories
STYLE_CATEGORIES = [
    "Streetwear", "Casual", "Formal", "Bohemian", "Athleisure",
    "Vintage", "Minimalist", "Maximalist", "Cottagecore", "Y2K",
    "Grunge", "Preppy", "Gothic", "Business Casual", "Resort Wear"
]

# Color palettes
COLOR_PALETTES = {
    "Monochrome": ["#000000", "#333333", "#666666", "#999999", "#FFFFFF"],
    "Earth Tones": ["#8B4513", "#D2691E", "#DEB887", "#F4A460", "#FFDEAD"],
    "Pastels": ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF"],
    "Bold Primaries": ["#FF0000", "#0000FF", "#FFFF00", "#00FF00", "#FF6600"],
    "Ocean": ["#006994", "#0099CC", "#00CED1", "#40E0D0", "#7FFFD4"],
    "Sunset": ["#FF4500", "#FF6347", "#FF7F50", "#FFD700", "#FFA500"],
    "Forest": ["#228B22", "#2E8B57", "#3CB371", "#90EE90", "#98FB98"],
    "Jewel Tones": ["#9B59B6", "#2980B9", "#27AE60", "#E74C3C", "#F39C12"]
}


def chat_completion(system_prompt):
    """Call OpenRouter API with a prompt and return the text response."""
    response = client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=[{"role": "user", "content": system_prompt}],
    )
    return response.choices[0].message.content.strip()


def generate_fashion_design(prompt, style, color_palette, occasion, gender):
    """Generate fashion design description using OpenRouter."""
    if not client:
        return {"success": False, "error": "AI generation is unavailable. Configure an OpenRouter API key to create designs."}

    try:
        system_prompt = f"""You are an expert fashion designer and stylist. Create a detailed, 
        creative clothing design based on the user's request. 

        User Request: {prompt}
        Style Category: {style}
        Color Palette: {color_palette}
        Occasion: {occasion}
        For: {gender}

        Provide a structured JSON response with the following fields:
        {{
            "design_name": "Creative name for the design",
            "description": "Detailed description of the overall look (2-3 sentences)",
            "garments": [
                {{
                    "type": "garment type (e.g., Top, Pants, Dress)",
                    "name": "specific item name",
                    "description": "detailed description",
                    "fabric": "fabric type",
                    "color": "color description",
                    "details": ["key design detail 1", "key design detail 2", "key design detail 3"]
                }}
            ],
            "accessories": ["accessory 1", "accessory 2", "accessory 3"],
            "styling_tips": ["tip 1", "tip 2", "tip 3"],
            "color_story": "Brief story about the color choices",
            "season": "Best season(s) for this outfit",
            "price_range": "Estimated budget range (e.g., $50-$150)",
            "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"]
        }}

        Be creative, specific, and fashion-forward. Focus on wearable, realistic designs."""

        text = chat_completion(system_prompt)

        # Extract JSON from response
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            design_data = json.loads(json_match.group())
            return {"success": True, "design": design_data}
        else:
            return {"success": False, "error": "Could not parse design data", "raw": text}

    except Exception as e:
        return {"success": False, "error": str(e)}


def get_product_suggestions(design_data, budget_level="mid"):
    """Generate product suggestions based on design using OpenRouter."""
    if not client:
        return {"success": False, "error": "Product suggestions are unavailable. Configure an OpenRouter API key to get recommendations."}

    try:
        design_summary = json.dumps(design_data.get("design", {}), indent=2)

        prompt = f"""Based on this fashion design, suggest 6 specific affordable products that 
        students can actually buy online. Budget level: {budget_level}

        Design:
        {design_summary}

        Return a JSON array with 6 product suggestions:
        [
            {{
                "name": "Product Name",
                "type": "Category (e.g., Top, Pants, Shoes)",
                "brand": "Suggested brand (e.g., Zara, H&M, ASOS, Shein, Uniqlo, Primark)",
                "price": "$XX-$XX",
                "description": "Why this matches the design",
                "search_query": "exact search query to find it online",
                "where_to_buy": ["Store1", "Store2"],
                "color": "color variant to look for"
            }}
        ]

        Focus on affordable, accessible brands like Zara, H&M, ASOS, Shein, Uniqlo, Forever 21, 
        Target, Old Navy, ThredUp (secondhand). Keep prices student-friendly ($10-$80 per item)."""

        text = chat_completion(prompt)

        json_match = re.search(r'\[.*\]', text, re.DOTALL)
        if json_match:
            products = json.loads(json_match.group())
            return {"success": True, "products": products}
        else:
            return {"success": False, "error": "Could not parse product suggestions."}

    except Exception as e:
        return {"success": False, "error": str(e)}


def get_style_advice(design_data, user_body_type="", preferences=""):
    """Get personalized styling advice using OpenRouter."""
    if not client:
        return {"success": False, "error": "AI advice is unavailable. Configure an OpenRouter API key to get styling advice."}

    try:
        design_name = design_data.get("design", {}).get("design_name", "your design")

        prompt = f"""As a fashion stylist, provide personalized styling advice for "{design_name}".
        Body type consideration: {user_body_type if user_body_type else "general"}
        Personal preferences: {preferences if preferences else "none specified"}

        Return JSON:
        {{
            "body_type_tips": ["tip1", "tip2"],
            "how_to_wear": ["step1", "step2", "step3"],
            "occasions": ["occasion1", "occasion2", "occasion3"],
            "what_to_avoid": ["avoid1", "avoid2"],
            "seasonal_variations": {{
                "summer": "summer variation tip",
                "winter": "winter variation tip"
            }},
            "confidence_boost": "Motivational fashion tip"
        }}"""

        text = chat_completion(prompt)

        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            advice = json.loads(json_match.group())
            return {"success": True, "advice": advice}
        else:
            return {"success": False, "error": "Could not parse styling advice."}

    except Exception as e:
        return {"success": False, "error": str(e)}


@app.route("/")
def index():
    return render_template("index.html",
                           styles=STYLE_CATEGORIES,
                           palettes=list(COLOR_PALETTES.keys()))


@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "")
    style = data.get("style", "Casual")
    color_palette = data.get("color_palette", "Monochrome")
    occasion = data.get("occasion", "Everyday")
    gender = data.get("gender", "Any")

    if not prompt:
        return jsonify({"success": False, "error": "Please provide a design prompt"}), 400

    result = generate_fashion_design(prompt, style, color_palette, occasion, gender)
    return jsonify(result)


@app.route("/api/products", methods=["POST"])
def products():
    data = request.get_json()
    design_data = data.get("design_data", {})
    budget = data.get("budget", "mid")
    result = get_product_suggestions(design_data, budget)
    return jsonify(result)


@app.route("/api/advice", methods=["POST"])
def advice():
    data = request.get_json()
    design_data = data.get("design_data", {})
    body_type = data.get("body_type", "")
    preferences = data.get("preferences", "")
    result = get_style_advice(design_data, body_type, preferences)
    return jsonify(result)


@app.route("/api/palettes", methods=["GET"])
def palettes():
    return jsonify(COLOR_PALETTES)


@app.route("/api/status", methods=["GET"])
def status():
    has_key = bool(OPENROUTER_API_KEY)
    return jsonify({
        "api_configured": has_key,
        "mode": "AI-Powered" if has_key else "Unavailable",
        "model": OPENROUTER_MODEL if has_key else None
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
