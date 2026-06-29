"""
JSON-LD generator utility for product schema (schema.org Product)
Returns a string that can be embedded inside product description HTML.
"""

import json
from typing import Dict, List


def generate_product_jsonld(product: Dict) -> str:
    """product fields: name, sku, brand, price, currency, availability, url, image(list), gtin(optional)
    Returns HTML <script> tag string containing JSON-LD.
    """
    offers = {
        "@type": "Offer",
        "price": product.get("price"),
        "priceCurrency": product.get("currency", "EUR"),
        "availability": f"https://schema.org/{product.get('availability', 'InStock')}",
        "url": product.get("url"),
    }
    jsonld = {
        "@context": "https://schema.org/",
        "@type": "Product",
        "name": product.get("name"),
        "image": product.get("image", []),
        "sku": product.get("sku"),
        "brand": {"@type": "Brand", "name": product.get("brand")},
        "offers": offers,
    }
    if product.get("gtin"):
        jsonld["gtin13"] = product.get("gtin")
    return "<script type='application/ld+json'>%s</script>" % json.dumps(jsonld, ensure_ascii=False)
