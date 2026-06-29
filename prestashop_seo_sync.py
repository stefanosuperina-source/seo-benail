"""
PrestaShop SEO Sync
Synchronizes SEO audit implementations to PrestaShop products and pages.
Handles meta tags, descriptions, H1, schema markup, and URL rewrites.
"""

import logging
import json
from typing import Dict, List, Optional
from xml.etree import ElementTree as ET

from config import config
from prestashop_client import (
    get_product_xml,
    update_product_xml,
    set_seo_fields_on_product_xml,
    slugify,
)
from seo_implementations import (
    HomepageSEOOptimizer,
    ProductDescriptionOptimizer,
    SchemaMarkupGenerator,
    URLOptimizer,
)

log = logging.getLogger(__name__)


class PrestaShopSEOSync:
    """
    Synchronize SEO audit recommendations to PrestaShop via Webservice API.
    """

    @staticmethod
    def sync_homepage_meta_tags() -> bool:
        """
        CRITICAL: Sync optimized homepage meta tags.
        Note: Homepage meta tags are typically set in PrestaShop backend > SEO & URLs.
        This is a reference for manual implementation or custom homepage code.
        """
        log.info("HOMEPAGE META TAGS - Manual Update Required")
        log.info(f"Title: {config.HOMEPAGE_META_TITLE}")
        log.info(f"Description: {config.HOMEPAGE_META_DESCRIPTION}")
        log.info(f"Viewport: {config.VIEWPORT_TAG}")
        
        return True

    @staticmethod
    def sync_homepage_h1(homepage_content: str) -> str:
        """
        CRITICAL: Ensure H1 is visible on homepage.
        This function injects the H1 tag into content.
        """
        h1_tag = f"<h1>{config.HOMEPAGE_H1}</h1>"
        
        # If content doesn't already have H1, prepend it
        if "<h1" not in homepage_content.lower():
            homepage_content = h1_tag + "\n" + homepage_content
            log.info("Added H1 tag to homepage")
        else:
            log.info("H1 tag already present on homepage")
        
        return homepage_content

    @staticmethod
    def sync_homepage_viewport() -> str:
        """
        CRITICAL: Fix meta viewport tag (remove user-scalable=no).
        Return the correct meta viewport tag for inclusion in <head>.
        """
        return f'<meta name="viewport" content="{config.VIEWPORT_TAG}" />'

    @staticmethod
    def sync_product_descriptions_miricolor(product_ids: List[int]) -> Dict[int, bool]:
        """
        IMPORTANT: Differentiate MiriColor product descriptions.
        
        Args:
            product_ids: List of PrestaShop product IDs in MiriColor line
        
        Returns:
            Dict mapping product_id -> success (True/False)
        """
        
        results = {}
        
        for idx, product_id in enumerate(product_ids):
            try:
                # Fetch current product XML
                xml_str = get_product_xml(product_id)
                root = ET.fromstring(xml_str)
                
                product_elem = root if root.tag == "product" else root.find("product")
                if product_elem is None:
                    log.warning(f"Product {product_id}: No product element found")
                    results[product_id] = False
                    continue
                
                # Extract current product name
                name_elem = product_elem.find("name/language")
                current_name = name_elem.text if name_elem is not None else f"MiriColor {idx}"
                
                # Generate unique description
                tone = ["pastello", "nude", "acceso", "metallico"][idx % 4]
                finish = ProductDescriptionOptimizer.FINISHES[idx % len(ProductDescriptionOptimizer.FINISHES)]
                season = ProductDescriptionOptimizer.SEASONS[idx % len(ProductDescriptionOptimizer.SEASONS)]
                
                unique_desc = ProductDescriptionOptimizer.generate_unique_product_description(
                    product_name=current_name,
                    color_name=current_name,
                    tone=tone,
                    finish=finish,
                    season=season,
                )
                
                # Update description in XML
                description_elem = product_elem.find("description/language")
                if description_elem is None:
                    description_elem = ET.SubElement(product_elem.find("description"), "language")
                    description_elem.set("id", str(config.PRESTA_DEFAULT_LANG_ID))
                description_elem.text = unique_desc
                
                # Update product XML
                new_xml = ET.tostring(root, encoding="utf-8").decode("utf-8")
                update_product_xml(product_id, new_xml)
                
                log.info(f"Product {product_id}: Description updated successfully")
                results[product_id] = True
                
            except Exception as e:
                log.error(f"Product {product_id}: Failed to update - {e}")
                results[product_id] = False
        
        return results

    @staticmethod
    def generate_category_url_redirect_config() -> str:
        """
        IMPORTANT: Generate URL redirect configuration for PrestaShop.
        
        PrestaShop uses .htaccess for URL rewrites.
        This returns the .htaccess redirect rules.
        
        To implement:
        1. Backup current .htaccess
        2. Add these rules BEFORE the existing RewriteRules
        3. Clear PrestaShop cache
        """
        
        return URLOptimizer.get_redirect_rules()

    @staticmethod
    def add_product_schema_markup(product_id: int, product_data: Dict) -> str:
        """
        IMPORTANT: Generate JSON-LD Product schema for a product.
        
        Returns JSON-LD string ready to be injected into product page <head>.
        """
        
        return SchemaMarkupGenerator.generate_product_schema(product_data)

    @staticmethod
    def add_breadcrumb_schema_markup(breadcrumbs: List[Dict]) -> str:
        """
        IMPORTANT: Generate BreadcrumbList schema markup.
        
        Returns JSON-LD string ready to be injected into page <head>.
        """
        
        return SchemaMarkupGenerator.generate_breadcrumb_schema(breadcrumbs)

    @staticmethod
    def sync_product_seo_fields(
        product_id: int,
        meta_title: str,
        meta_description: str,
        link_rewrite: Optional[str] = None,
    ) -> bool:
        """
        IMPORTANT: Sync SEO fields (meta_title, meta_description, link_rewrite) to PrestaShop product.
        
        Args:
            product_id: PrestaShop product ID
            meta_title: Optimized meta title (60 chars max)
            meta_description: Optimized meta description (156 chars max)
            link_rewrite: Optional clean URL slug (auto-slugified if not provided)
        
        Returns:
            True if successful, False otherwise
        """
        
        try:
            # Fetch current product XML
            xml_str = get_product_xml(product_id)
            
            # Prepare multilingual fields
            default_lang_id = str(config.PRESTA_DEFAULT_LANG_ID)
            meta_title_dict = {default_lang_id: meta_title}
            meta_desc_dict = {default_lang_id: meta_description}
            link_rewrite_dict = {default_lang_id: link_rewrite or slugify(meta_title)}
            
            # Update XML with SEO fields
            new_xml = set_seo_fields_on_product_xml(
                xml_str,
                meta_title=meta_title_dict,
                meta_description=meta_desc_dict,
                link_rewrite=link_rewrite_dict,
            )
            
            # Push back to PrestaShop
            update_product_xml(product_id, new_xml.decode("utf-8"))
            
            log.info(f"Product {product_id}: SEO fields synced successfully")
            return True
            
        except Exception as e:
            log.error(f"Product {product_id}: Failed to sync SEO fields - {e}")
            return False

    @staticmethod
    def generate_faq_page_content(faqs: List[Dict]) -> str:
        """
        OPPORTUNITY: Generate FAQ page with schema markup.
        
        Returns complete HTML for FAQ page with JSON-LD embedded.
        """
        
        schema_json = SchemaMarkupGenerator.generate_faq_schema(faqs)
        
        html = f'''
<script type="application/ld+json">
{schema_json}
</script>

<div class="faq-container">
  <h1>Domande Frequenti – Benail</h1>
  
'''
        
        for idx, faq in enumerate(faqs, 1):
            html += f'''
  <div class="faq-item" id="faq-{idx}">
    <h3>{faq["question"]}</h3>
    <p>{faq["answer"]}</p>
  </div>
'''
        
        html += '''
</div>

<style>
.faq-container { max-width: 800px; margin: 40px auto; }
.faq-item { margin: 20px 0; padding: 15px; border-left: 4px solid #007bff; background: #f8f9fa; }
.faq-item h3 { margin: 0 0 10px 0; color: #333; }
.faq-item p { margin: 0; color: #666; line-height: 1.6; }
</style>
'''
        
        return html

    @staticmethod
    def remove_obsolete_meta_tags(page_html: str) -> str:
        """
        IMPORTANT: Remove obsolete meta keywords tag from page HTML.
        
        This tag has been ignored by Google since 2009 and devalued by Bing.
        Removing it is part of the audit cleanup.
        """
        
        import re
        
        # Remove all meta keywords tags
        page_html = re.sub(r'<meta\s+name\s*=\s*["\']keywords["\']\s+content\s*=\s*["\'][^"\']*["\']\s*/?\s*>', '', page_html, flags=re.IGNORECASE)
        
        log.info("Removed obsolete meta keywords tags from page")
        return page_html

    @staticmethod
    def generate_implementation_checklist() -> str:
        """
        Generate a checklist of all SEO audit implementations.
        Use this to track progress on manual/automated tasks.
        """
        
        checklist = """
╔════════════════════════════════════════════════════════════════════════╗
║                 SEO AUDIT IMPLEMENTATION CHECKLIST                     ║
║                   Benail.it - Giugno 2026                             ║
╚════════════════════════════════════════════════════════════════════════╝

CRITICO (Da fare immediatamente):
  ☐ H1 Homepage: Aggiungere tag H1 visibile sopra la fold
    Title: "Prodotti Professionali per Onicotecniche..."
  
  ☐ Meta Description: Aggiornare a 150-160 caratteri con CTA e USP
    New: "Prodotti professionali onicotecniche: smalti, acrygel, lampade..."
  
  ☐ Title Tag: Ottimizzare rimuovendo ".it" ridondante
    New: "Prodotti Onicotecniche Professionali | Consegna 24h – Benail"
  
  ☐ Meta Viewport: Rimuovere user-scalable=no
    New: <meta name="viewport" content="width=device-width, initial-scale=1">

IMPORTANTE (Da fare entro 30-60 giorni):
  ☐ Contenuto Duplicato MiriColor: Generare descrizioni uniche per 30+ prodotti
    - Aggiungere nome colore, tonalità, finish, stagione
    - Minimo 100-150 parole per prodotto differenziate
  
  ☐ Testo SEO Homepage: Aggiungere sezione 200-300 parole
    - Chi è Benail, a chi si rivolge, cosa distingue il catalogo
    - Posizionare sotto i prodotti in evidenza
  
  ☐ URL Categorie: Rimuovere prefissi numerici con redirect 301
    /10-apparecchiature → /apparecchiature-professionale/
    /23-semipermanenti → /smalti-semipermanenti-professionali/
    (E altri 8+ URL)
  
  ☐ Schema Markup: Implementare Product, BreadcrumbList, Organization
    - Product schema su ogni pagina prodotto
    - BreadcrumbList per navigazione gerarchica
    - Organization + WebSite sulla homepage
  
  ☐ Meta Keywords: Rimuovere tag obsoleto da tutte le pagine
    (Ignorato da Google dal 2009, svalutato da Bing)
  
  ☐ Piano Editoriale Blog: Avviare 2 articoli/mese
    - "Come fare ricostruzione con gel trifasico"
    - "Differenza acrygel vs gel acrilico"
    - "Guida scelta lampada UV/LED"
    (Minimo 800-1500 parole per articolo)

OPPORTUNITÀ (Da pianificare nei prossimi 60-90 giorni):
  ☐ Landing Page Rivenditori: Creare pagina B2B dedicata
    /rivenditori/ o /prezzi-professionali/
  
  ☐ Open Graph Dinamico: Immagine unica per ogni prodotto/categoria
    (Non logo statico per tutte le pagine)
  
  ☐ Widget Recensioni: Integrare sezione su homepage con markup schema
  
  ☐ Internal Linking: Implementare "Usato insieme a", "Completa il kit"
  
  ☐ FAQ Page + Glossario: 15-20 domande con markup FAQPage
    - Spiegare termini tecnici (HEMA Free, tissotropico, ecc.)

═══════════════════════════════════════════════════════════════════════
Monitoraggio: Controllare posizioni su GSC a 30, 60, 90 giorni
═══════════════════════════════════════════════════════════════════════
"""
        
        return checklist


# Example usage / testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print(PrestaShopSEOSync.generate_implementation_checklist())
