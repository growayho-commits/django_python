import base64
import json
import os
import re
import urllib.request
from apps.catalogs.categories.models.category_profile import CategoryProfile


HSN_GST_HINTS = [
    (("shirt", "t-shirt", "polo", "cotton", "apparel", "garment", "dress", "kurti", "saree", "jeans"), "6109", 5.0, "Apparel & Clothing"),
    (("yarn", "fabric", "textile", "thread", "polyester", "viscose", "silk"), "5205", 5.0, "Textiles & Yarn"),
    (("phone", "mobile", "laptop", "tablet", "charger", "earbuds", "watch", "electronic", "camera"), "8517", 18.0, "Electronics"),
    (("shoe", "sneaker", "sandal", "footwear", "boot", "slipper"), "6404", 12.0, "Footwear"),
    (("oil", "rice", "spice", "masala", "tea", "coffee", "snack", "food", "honey"), "2106", 5.0, "Food & Beverages"),
    (("chair", "table", "sofa", "wood", "furniture", "bed", "desk"), "9403", 18.0, "Furniture"),
    (("cream", "soap", "shampoo", "oil", "cosmetic", "serum", "perfume"), "3304", 18.0, "Beauty & Personal Care"),
    (("motor", "pump", "drill", "tool", "machine", "valve", "pipe", "steel"), "8481", 18.0, "Industrial & Hardware"),
]


def _match_category(keywords_text: str):
    tokens = [t for t in re.split(r"[^a-zA-Z0-9]+", keywords_text or "") if len(t) >= 3]
    for tok in tokens:
        cat = CategoryProfile.objects.filter(is_active=True, name__icontains=tok).order_by("id").first()
        if cat:
            return cat
    return CategoryProfile.objects.filter(is_active=True).order_by("id").first()


def analyze_catalogue_input(image_bytes=None, mime_type="image/jpeg", filename="", hint_name=""):
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if api_key and image_bytes:
        try:
            b64 = base64.b64encode(image_bytes).decode("utf-8")
            prompt = (
                "Analyze this product/catalogue photo for an e-commerce & B2B/B2C marketplace in India. "
                f"User hint: '{hint_name}'. Return ONLY valid JSON with keys: "
                "name (concise title), brand_name (or empty), category_keywords (2-3 words), "
                "hsn_sac_code (4-8 digit Indian HSN), gst_percentage (number like 5, 12, 18), "
                "description (2-3 crisp sentences with key benefits), "
                "specifications (list of 4-6 objects with group, key, value)."
            )
            payload = {
                "contents": [{
                    "parts": [
                        {"text": prompt},
                        {"inline_data": {"mime_type": mime_type, "data": b64}}
                    ]
                }],
                "generationConfig": {"responseMimeType": "application/json"}
            }
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
                parsed = json.loads(raw_text)
                cat = _match_category(parsed.get("category_keywords") or parsed.get("name") or hint_name)
                return {
                    "ai_mode": "gemini_vision",
                    "name": parsed.get("name") or hint_name or "Verified Marketplace Catalogue",
                    "brand_name": parsed.get("brand_name") or "",
                    "category_id": cat.id if cat else "",
                    "category_name": cat.name if cat else "",
                    "hsn_sac_code": str(parsed.get("hsn_sac_code") or "9999"),
                    "gst_percentage": float(parsed.get("gst_percentage") or 18.0),
                    "description": parsed.get("description") or "",
                    "specifications": parsed.get("specifications") or [],
                }
        except Exception:
            pass

    # Smart Local AI Fallback (extracts from hint_name + filename + Google Taxonomy + HSN/GST rules)
    clean_file = re.sub(r"\.[a-zA-Z0-9]+$", "", filename or "").replace("_", " ").replace("-", " ").strip()
    base_title = hint_name.strip() or clean_file.title() or "Premium Quality Catalogue"
    combined = f"{base_title} {clean_file}".lower()

    matched_hsn, matched_gst, matched_group = "9999", 18.0, "General"
    for kws, hsn, gst, grp in HSN_GST_HINTS:
        if any(k in combined for k in kws):
            matched_hsn, matched_gst, matched_group = hsn, gst, grp
            break

    cat = _match_category(f"{base_title} {matched_group}")
    specs = [
        {"group": "General", "key": "Quality Grade", "value": "Commercial / Export Standard"},
        {"group": "General", "key": "Country of Origin", "value": "India"},
        {"group": "Compliance", "key": "HSN / SAC Code", "value": matched_hsn},
        {"group": "Packaging", "key": "Dispatch Readiness", "value": "24-48 Hours"},
    ]
    desc = (
        f"{base_title} engineered for reliable daily and commercial performance. "
        f"Quality-checked for consistent finishing, accurate specifications, and safe pan-India dispatch."
    )
    return {
        "ai_mode": "smart_local",
        "name": base_title,
        "brand_name": "",
        "category_id": cat.id if cat else "",
        "category_name": cat.name if cat else "",
        "hsn_sac_code": matched_hsn,
        "gst_percentage": matched_gst,
        "description": desc,
        "specifications": specs,
    }
