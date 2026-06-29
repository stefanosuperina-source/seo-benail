"""
Example script to publish SEO fields to PrestaShop products.
This is a safe, idempotent example that respects PRESTA_DRY_RUN by default.
Usage:
  python scripts/publish_to_presta.py --sku LIP-ROS-001 --title "Rossetto Rosso Intenso" --description "Rossetto idratante con SPF15" --activate

Ensure PRESTA_URL and PRESTA_WS_KEY are set in env or GitHub Secrets.
"""

import argparse
import os
import time
import logging
import json
from datetime import datetime

import requests

from config import config
from prestashop_client import (
    get_product_xml,
    set_seo_fields_on_product_xml,
    update_product_xml,
    slugify,
)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def find_product_id_by_sku(sku: str):
    """Query PrestaShop for a product by reference (SKU) and return id or None."""
    base = config.PRESTA_URL.rstrip("/")
    params = {"ws_key": config.PRESTA_WS_KEY, "display": "[id,reference]", f"filter[reference]": f"[{sku}]"}
    try:
        r = requests.get(f"{base}/api/products", params=params, timeout=20)
        r.raise_for_status()
    except Exception as e:
        log.error("Error querying PrestaShop for SKU %s: %s", sku, e)
        raise
    # Very small XML parse to extract id
    from xml.etree import ElementTree as ET

    root = ET.fromstring(r.text)
    # root contains <prestashop><products><product><id>123</id>...</product></products></prestashop>
    prod = root.find('.//product')
    if prod is None:
        return None
    id_el = prod.find('id')
    if id_el is None:
        return None
    return int(id_el.text)


def backup_xml(product_id: int, xml_text: str):
    os.makedirs(config.BACKUP_DIR, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    path = os.path.join(config.BACKUP_DIR, f"product_{product_id}_{ts}.xml")
    with open(path, "w", encoding="utf-8") as f:
        f.write(xml_text)
    log.info("Backed up product XML to %s", path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sku", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--activate", action="store_true")
    parser.add_argument("--image", help="local image path to upload")
    args = parser.parse_args()

    sku = args.sku
    title = args.title
    description = args.description

    if not config.PRESTA_URL or not config.PRESTA_WS_KEY:
        log.error("PRESTA_URL and PRESTA_WS_KEY must be configured in env or .env")
        return

    product_id = find_product_id_by_sku(sku)
    if not product_id:
        log.error("Product with SKU %s not found", sku)
        return
    log.info("Found product id %s for sku %s", product_id, sku)

    xml = get_product_xml(product_id)
    backup_xml(product_id, xml)

    lang_id = config.PRESTA_DEFAULT_LANG_ID
    meta_title = {lang_id: title}
    meta_description = {lang_id: description[:156]}
    link_rewrite = {lang_id: slugify(title)}
    active = 1 if args.activate else None

    new_xml = set_seo_fields_on_product_xml(xml, meta_title, meta_description, link_rewrite, active=active)

    # Write only if changes detected (optional simple check)
    if new_xml == xml.encode("utf-8"):
        log.info("No changes detected on product %s - skipping update", product_id)
    else:
        update_product_xml(product_id, new_xml)

    if args.image:
        upload_path = args.image
        from prestashop_client import upload_product_image
        upload_product_image(product_id, upload_path)

    log.info("Done.")


if __name__ == '__main__':
    main()
