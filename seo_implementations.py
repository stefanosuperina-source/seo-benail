"""
SEO Audit Implementations for Benail.it
Implements critical and important fixes from the June 2026 audit report.
"""

import json
import logging
from typing import Dict, List, Optional
from xml.etree import ElementTree as ET

from config import config

log = logging.getLogger(__name__)


class HomepageSEOOptimizer:
    """
    CRITICAL FIXES:
    1. Add H1 descriptive tag
    2. Fix meta description with CTA and USPs
    3. Optimize title tag (remove domain redundancy)
    4. Fix meta viewport (remove user-scalable restriction)
    """

    @staticmethod
    def get_homepage_meta_tags() -> Dict[str, str]:
        """Return optimized meta tags for homepage."""
        return {
            "title": config.HOMEPAGE_META_TITLE,
            "description": config.HOMEPAGE_META_DESCRIPTION,
            "viewport": config.VIEWPORT_TAG,
            "charset": "utf-8",
            "language": config.LANGUAGE_CODE,
            "country": config.COUNTRY_CODE,
        }

    @staticmethod
    def get_homepage_h1() -> str:
        """Return H1 tag text (visible, positioned above fold)."""
        return config.HOMEPAGE_H1

    @staticmethod
    def get_homepage_seo_text() -> str:
        """Return 200-300 word SEO text for homepage (below hero/products)."""
        return config.HOMEPAGE_SEO_TEXT


class ProductDescriptionOptimizer:
    """
    IMPORTANT FIX: Differentiate product descriptions
    """

    COLOR_TONES = {
        "nude": ["beige naturale", "rosa pallido", "pesca delicato"],
        "pastello": ["azzurro cielo", "rosa polvere", "giallo limone", "lilla chiaro"],
        "acceso": ["rosso fuoco", "blu cobalto", "giallo sole", "fuchsia"],
        "metallico": ["oro", "argento", "bronzo", "rame"],
    }

    FINISHES = ["lucido", "satinato", "opaco", "glitter", "effetto specchio"]
    SEASONS = ["Primavera", "Estate", "Autunno", "Inverno"]

    @staticmethod
    def generate_unique_product_description(
        product_name: str,
        color_name: str,
        tone: str = "pastello",
        finish: str = "lucido",
        season: str = "Primavera",
    ) -> str:
        """Generate unique, SEO-optimized product description (100-150 words)."""
        
        description = (
            f"Scopri {product_name} – il smalto semipermanente professionale Benail in tonalità {color_name}. "
            f"Questo colore dal finish {finish} è perfetto per {season.lower()} "
            f"e appartiene alla categoria '{tone}' con una tonalità che si adatta a ogni stile. \n\n"
            f"**Caratteristiche Tecniche:**\n"
            f"• Colore: {color_name} ({tone})\n"
            f"• Finish: {finish}\n"
            f"• Stagione consigliata: {season}\n"
            f"• Formula HEMA Free e dermatologicamente testato\n"
            f"• Applicazione facile e copertura uniforme\n"
            f"• Durabilità: fino a 3 settimane\n"
            f"• Compatibile con lampade UV e LED\n\n"
            f"**Abbinamenti Consigliati:**\n"
            f"Questo colore si sposa perfettamente con base e top coat della linea Benail Professional. "
            f"Per un effetto ombre o nail art, combina con altri colori della stessa gamma per risultati sorprendenti. "
            f"Ideale per french manicure, gradient, e decorazioni delicate.\n\n"
            f"**Per Professionisti:**\n"
            f"Prodotto ideale per nail center e onicotecniche che cercano qualità certificata, "
            f"formule innovative e colori sempre in trend. Disponibile in flacone professionale da 15ml. "
            f"Scopri tutta la linea MiriColor Benail e scegli il tuo colore preferito. "
            f"Consegna in 24h su tutto il territorio italiano. Prezzi speciali per rivenditori."
        )
        
        return description

    @staticmethod
    def batch_generate_miricolor_descriptions(color_list: List[Dict]) -> List[Dict]:
        """Batch generate unique descriptions for MiriColor line."""
        results = []
        
        for i, color in enumerate(color_list):
            tone = color.get("tone", "pastello")
            finish = ProductDescriptionOptimizer.FINISHES[i % len(ProductDescriptionOptimizer.FINISHES)]
            season = ProductDescriptionOptimizer.SEASONS[i % len(ProductDescriptionOptimizer.SEASONS)]
            
            description = ProductDescriptionOptimizer.generate_unique_product_description(
                product_name=color["name"],
                color_name=color["color"],
                tone=tone,
                finish=finish,
                season=season,
            )
            
            color["unique_description"] = description
            color["seo_focus_keywords"] = [
                color.get("color", "").lower(),
                tone,
                finish,
                "smalto semipermanente",
                "nail art",
            ]
            
            results.append(color)
            log.info(f"Generated unique description for {color['name']}")
        
        return results


class URLOptimizer:
    """
    IMPORTANT FIX: Remove PrestaShop numeric prefixes from category URLs
    """

    CATEGORY_MAPPINGS = {
        "/10-apparecchiature": "/apparecchiature-professionale/",
        "/23-semipermanenti": "/smalti-semipermanenti-professionali/",
        "/68-ricostruzione": "/gel-ricostruzione-unghie/",
        "/45-acrygel": "/acrygel-professionale/",
        "/12-gel": "/gel-professionale/",
        "/89-lampade": "/lampade-uv-led-professionali/",
        "/34-kit": "/kit-nail-art-completi/",
        "/56-attrezzature": "/attrezzature-onicotecniche/",
        "/78-base-top": "/base-top-coat-professionale/",
        "/90-accessori": "/accessori-nail-art/",
    }

    @staticmethod
    def get_redirect_rules() -> str:
        """Generate .htaccess 301 permanent redirect rules."""
        
        htaccess_rules = "# 301 Permanent Redirects - SEO Category URL Cleanup (Audit 2026)\n"
        htaccess_rules += "# These redirect old PrestaShop numeric URLs to clean SEO URLs\n\n"
        
        for old_url, new_url in URLOptimizer.CATEGORY_MAPPINGS.items():
            htaccess_rules += f'Redirect 301 "{old_url}" "{new_url}"\n'
        
        return htaccess_rules


class SchemaMarkupGenerator:
    """
    IMPORTANT FIX: Implement Schema.org markup (JSON-LD)
    """

    @staticmethod
    def generate_product_schema(product: Dict) -> str:
        """Generate JSON-LD Product schema."""
        
        schema = {
            "@context": "https://schema.org/",
            "@type": "Product",
            "name": product.get("name", ""),
            "description": product.get("description", ""),
            "image": product.get("image_url", ""),
            "brand": {
                "@type": "Brand",
                "name": product.get("brand", "Benail"),
            },
            "offers": {
                "@type": "Offer",
                "url": product.get("url", ""),
                "priceCurrency": product.get("currency", "EUR"),
                "price": product.get("price", ""),
                "availability": f"https://schema.org/{product.get('availability', 'InStock')}",
            },
        }
        
        if product.get("rating") and product.get("ratingCount"):
            schema["aggregateRating"] = {
                "@type": "AggregateRating",
                "ratingValue": product["rating"],
                "reviewCount": product["ratingCount"],
            }
        
        return json.dumps(schema, ensure_ascii=False, indent=2)

    @staticmethod
    def generate_breadcrumb_schema(breadcrumbs: List[Dict]) -> str:
        """Generate JSON-LD BreadcrumbList schema."""
        
        items = []
        for i, bc in enumerate(breadcrumbs, 1):
            items.append({
                "@type": "ListItem",
                "position": i,
                "name": bc["name"],
                "item": bc["url"],
            })
        
        schema = {
            "@context": "https://schema.org/",
            "@type": "BreadcrumbList",
            "itemListElement": items,
        }
        
        return json.dumps(schema, ensure_ascii=False, indent=2)

    @staticmethod
    def generate_faq_schema(faqs: List[Dict]) -> str:
        """Generate JSON-LD FAQPage schema."""
        
        main_entity = []
        for faq in faqs:
            main_entity.append({
                "@type": "Question",
                "name": faq["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq["answer"],
                }
            })
        
        schema = {
            "@context": "https://schema.org/",
            "@type": "FAQPage",
            "mainEntity": main_entity,
        }
        
        return json.dumps(schema, ensure_ascii=False, indent=2)
