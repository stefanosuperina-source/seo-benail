"""
PrestaShop client helpers for seo-benail repo.
Handles basic PrestaShop Webservice interactions: GET/PUT product XML, upload images,
multilang field helpers, slugify, and dry-run safety.

Usage: set PRESTA_URL and PRESTA_WS_KEY in environment (see config.py) and call
get_product_xml / update_product_xml / upload_product_image from your publish flow.
"""

import logging
import time
import unicodedata
import re
from typing import Dict, Optional
from xml.etree import ElementTree as ET
from urllib.parse import urljoin

import requests

from config import config

log = logging.getLogger(__name__)

PRESTA_URL = getattr(config, "PRESTA_URL", "").rstrip("/") if hasattr(config, "PRESTA_URL") else ""
WS_KEY = getattr(config, "PRESTA_WS_KEY", "") if hasattr(config, "PRESTA_WS_KEY") else ""
DEFAULT_LANG_ID = str(getattr(config, "PRESTA_DEFAULT_LANG_ID", 1))
HEADERS_XML = {"Content-Type": "application/xml"}


def _ws_url(path: str) -> str:
    return f"{PRESTA_URL}/api/{path.lstrip('/')}"


def _request_with_retries(method, url, **kwargs):
    """Basic requests wrapper that retries 3 times on non-successful status codes.
    Always appends ws_key as query parameter for PrestaShop webservice.
    """
    params = kwargs.pop("params", {}) or {}
    if WS_KEY:
        params.update({"ws_key": WS_KEY})
    for attempt in range(3):
        try:
            r = requests.request(method, url, params=params, timeout=30, **kwargs)
        except Exception as e:
            log.warning("Presta request exception %s %s -> %s (attempt %s)", method, url, e, attempt + 1)
            time.sleep(2 ** attempt)
            continue
        if r.status_code in (200, 201, 204):
            return r
        log.warning("Presta request failed %s %s -> %s (attempt %s)", method, url, r.status_code, attempt + 1)
        time.sleep(2 ** attempt)
    r.raise_for_status()


def get_product_xml(product_id: int) -> str:
    url = _ws_url(f"products/{product_id}")
    r = _request_with_retries("GET", url)
    return r.text


def update_product_xml(product_id: int, xml_str: str) -> None:
    # Respect dry-run config
    if getattr(config, "PRESTA_DRY_RUN", True):
        log.info("DRY RUN: update_product_xml for id=%s (skipped)", product_id)
        return
    url = _ws_url(f"products/{product_id}")
    _request_with_retries("PUT", url, headers=HEADERS_XML, data=xml_str.encode("utf-8"))
    log.info("Updated product %s", product_id)


def upload_product_image(product_id: int, image_path: str) -> None:
    if getattr(config, "PRESTA_DRY_RUN", True):
        log.info("DRY RUN: upload image %s for product %s", image_path, product_id)
        return
    url = _ws_url(f"images/products/{product_id}")
    with open(image_path, "rb") as f:
        files = {"image": f}
        _request_with_retries("POST", url, files=files)
    log.info("Uploaded image %s for product %s", image_path, product_id)


def _set_multilang_field(parent: ET.Element, tag: str, text_by_lang: Dict[str, str]):
    """Set multilingual field under a product XML node.
    text_by_lang: dict of lang_id -> string
    """
    el = parent.find(tag)
    if el is None:
        el = ET.SubElement(parent, tag)
    # Clear existing children
    for child in list(el):
        el.remove(child)
    for lang_id, text in text_by_lang.items():
        lang_el = ET.SubElement(el, "language")
        lang_el.set("id", str(lang_id))
        lang_el.text = text


def set_seo_fields_on_product_xml(product_xml_str: str,
                                  meta_title: Dict[str, str],
                                  meta_description: Dict[str, str],
                                  link_rewrite: Dict[str, str],
                                  active: Optional[int] = None) -> bytes:
    """Modify product XML and return new bytes body ready to PUT to PrestaShop.
    meta_title/meta_description/link_rewrite are dict{lang_id: text}.
    """
    root = ET.fromstring(product_xml_str)
    # product may be wrapped in <prestashop><product>...</product></prestashop>
    product = root if root.tag == "product" else root.find("product")
    if product is None:
        raise ValueError("Invalid PrestaShop product XML: no <product> found")
    _set_multilang_field(product, "meta_title", meta_title)
    _set_multilang_field(product, "meta_description", meta_description)
    _set_multilang_field(product, "link_rewrite", link_rewrite)
    if active is not None:
        active_el = product.find("active")
        if active_el is None:
            active_el = ET.SubElement(product, "active")
        active_el.text = str(active)
    return ET.tostring(root, encoding="utf-8")


def slugify(text: str) -> str:
    """Simple slugify for Italian/Latin text.
    Normalizes accents, removes non-alphanum, replaces spaces with hyphens, limits length.
    """
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9\s-]", "", text).strip().lower()
    text = re.sub(r"[\s_-]+", "-", text)
    return text[:128]
