"""
Central configuration for the SEO pipeline (Benail.it - Professional Nail Products)
Updated with SEO audit recommendations for benail.it ecommerce store.
Do NOT commit sensitive keys. Use environment variables or GitHub Secrets.
"""

import os
from enum import Enum

try:
    from dotenv import load_dotenv
    load_dotenv()  # No-op on GitHub Actions; loads .env locally
except ImportError:
    pass


class Language(str, Enum):
    """Supported languages."""
    ITALIAN = "it"
    ENGLISH = "en"


class PublishStatus(str, Enum):
    """Possible publish states."""
    DRAFT = "draft"
    PUBLISH = "publish"


class MarketRegion(str, Enum):
    """Market regions for Italian targeting."""
    ITALY_NATIONAL = "IT"
    NORD = "nord"
    CENTRO = "centro"
    SUD = "sud"
    SICILIA = "sicilia"


def _require(name: str) -> str:
    """
    Read a required environment variable. Raises if missing.
    """
    value = os.environ.get(name)
    if not value:
        raise EnvironmentError(
            f"Missing environment variable: {name}\n"
            f"Set it in your local .env or in GitHub repo Settings > Secrets and variables > Actions."
        )
    return value


def _optional(name: str, default: str = "") -> str:
    """Read an optional env var with a default."""
    return os.environ.get(name, default)


class SEOConfig:
    """
    Primary configuration for the Benail.it SEO pipeline.
    Focus: Professional nail products e-commerce optimization
    """

    # ============================
    # BRAND & POSITIONING
    # ============================
    
    BRAND_NAME = "Benail"
    WEBSITE_URL = _optional("PRESTA_URL", "https://benail.it").rstrip("/")
    WEBSITE_DOMAIN = _optional("WEBSITE_DOMAIN", "benail.it")
    
    # Localization
    LANGUAGE = Language(_optional("LANGUAGE_CODE", "it"))
    LANGUAGE_CODE = LANGUAGE.value
    LOCALE = "it_IT"
    COUNTRY_CODE = "IT"
    CURRENCY = "EUR"

    TARGET_MARKET = MarketRegion(_optional("TARGET_MARKET", "IT"))

    # =========================================
    # CORE POSITIONING: Professional Nail Products
    # =========================================
    SPECIALIST_TITLE = "Prodotti Professionali per Onicotecniche"
    SPECIALIST_TAGLINE = "Smalti semipermanenti, acrygel, gel, lampade e attrezzature HEMA Free con consegna 24h"

    STORE_NICHE = _optional(
        "STORE_NICHE",
        "E-commerce specializzato in prodotti professionali per onicotecniche - smalti semipermanenti, "
        "acrygel, gel trifasico, lampade UV/LED, attrezzature, nail art e ricostruzioni unghie. "
        "Spedizione rapida in 24h in tutta Italia. Prezzi per professionisti e rivenditori."
    )

    BUSINESS_DESCRIPTION = (
        "Benail è un e-commerce specializzato in prodotti professionali per onicotecniche e nail center. "
        "Offriamo smalti semipermanenti HEMA Free, gel trifasico, acrygel, lampade professionali UV/LED, "
        "attrezzature per nail art e ricostruzioni unghie. Consegna in 24h in tutta Italia, prezzi B2B "
        "per rivenditori e nail center professionali, marchi selezionati e certificati."
    )

    # ============================
    # PRIMARY KEYWORDS (from audit)
    # ============================
    PRIMARY_KEYWORDS = [
        "prodotti professionali onicotecniche",
        "smalti semipermanenti professionale",
        "gel acrygel onicotecniche",
        "lampade uv led professionale",
        "attrezzature nail art",
        "prodotti onicotecniche online",
        "smalto semipermanente HEMA Free",
        "acquisto prodotti nail ingrosso",
        "fornitore smalti semipermanenti professionali",
        "prodotti ricostruzione unghie",
    ]

    SECONDARY_KEYWORDS = [
        "smalti gel professione",
        "costruttore trifasico",
        "gel monofasico",
        "dual form nail",
        "lampada led onicotecnica",
        "kit ricostruzione unghie",
        "attrezzature professionali unghie",
        "nail center fornitori",
        "prezzi all'ingrosso onicotecniche",
        "marchi nail professionali",
    ]

    LONGTAIL_KEYWORDS = [
        "come fare ricostruzione unghie con gel trifasico",
        "differenza tra acrygel e gel acrilico",
        "guida scelta lampada uv led professionale",
        "come applicare smalto semipermanente senza difetti",
        "prodotti HEMA Free cosa significano",
        "miglior smalto semipermanente professionale",
        "prezzo smalti semipermanenti ingrosso",
        "fornitori prodotti nail professionali italia",
        "attrezzature onicotecniche complete",
    ]

    CORE_SERVICES = [
        "Catalogo Prodotti Professionali Nail",
        "Smalti Semipermanenti HEMA Free",
        "Gel e Acrygel Professionali",
        "Lampade UV/LED",
        "Attrezzature Nail Art",
        "Kit Ricostruzione Unghie",
        "Marchi Selezionati Certificati",
        "Consegna Rapida 24h",
        "Prezzi B2B Rivenditori",
        "Supporto Professionisti",
    ]

    EXPERTISE_AREAS = [
        "Prodotti Semipermanenti",
        "Gel Trifasico e Monofasico",
        "Acrygel",
        "Apparecchiature UV/LED",
        "Nail Art Professionale",
        "Ricostruzione Unghie",
        "Prodotti HEMA Free",
        "Marchi Premium Internazionali",
        "B2B per Nail Center",
        "Distributore Professionisti",
    ]

    # ============================
    # LLM & GROQ (API Credentials)
    # ============================
    GROQ_API_KEY = _require("GROQ_API_KEY")
    GROQ_MODEL = _optional("GROQ_MODEL", "groq/llama-3.3-70b-versatile")

    TEMPERATURE_RESEARCHER = float(_optional("TEMP_RESEARCHER", "0.6"))
    TEMPERATURE_CREATOR = float(_optional("TEMP_CREATOR", "0.7"))
    TEMPERATURE_COPYWRITER = float(_optional("TEMP_COPYWRITER", "0.5"))
    TEMPERATURE_MODERATOR = float(_optional("TEMP_MODERATOR", "0.2"))
    TEMPERATURE_EDITOR = float(_optional("TEMP_EDITOR", "0.3"))

    # =============================
    # PRESTASHOP E-COMMERCE
    # =============================
    PRESTA_URL = _optional("PRESTA_URL", "https://benail.it").rstrip("/")
    PRESTA_WS_KEY = _require("PRESTA_WS_KEY")  # PrestaShop Webservice Key
    PRESTA_DEFAULT_LANG_ID = int(_optional("PRESTA_LANG_ID", "1"))
    PRESTA_SHOP_ID = int(_optional("PRESTA_SHOP_ID", "1"))
    PRESTA_CURRENCY = _optional("PRESTA_CURRENCY", "EUR")
    PRESTA_DRY_RUN = bool(_optional("PRESTA_DRY_RUN", "true").lower() == "true")

    # Convenience flag
    PRESTA_ENABLED = bool(PRESTA_URL and PRESTA_WS_KEY)

    # ==========================
    # CONTENUTO & GENERAZIONE ARTICOLI
    # ==========================
    MIN_ARTICLE_LENGTH = int(_optional("MIN_ARTICLE_LENGTH", "800"))
    MAX_ARTICLE_LENGTH = int(_optional("MAX_ARTICLE_LENGTH", "1500"))
    TARGET_ARTICLE_LENGTH = int(_optional("TARGET_ARTICLE_LENGTH", "1200"))

    META_TITLE_MAX_LENGTH = 60
    META_DESCRIPTION_MAX_LENGTH = 156

    CONTENT_TONE = _optional(
        "CONTENT_TONE",
        "autorevole esperto, pratico, tecnico ma accessibile, focalizzato su qualità e professionalità, "
        "conversazione diretta con onicotecniche, nail center e professionisti che vogliono i migliori "
        "prodotti per nail art e ricostruzioni unghie"
    )

    DEFAULT_CTA = _optional(
        "DEFAULT_CTA",
        "Scopri il catalogo completo Benail di prodotti professionali per onicotecniche. "
        "Consegna in 24h in tutta Italia. Prezzi per rivenditori e nail center. Contattaci per diventare partner."
    )

    USE_H2_STRUCTURE = True
    INCLUDE_FAQ_SECTION = True

    # =====================
    # RICERCA & KEYWORD SEO
    # =====================
    KEYWORD_RESEARCH_SOURCE = _optional("KEYWORD_RESEARCH_SOURCE", "nail_industry_analysis")
    PREFER_LONGTAIL_KEYWORDS = True
    LONGTAIL_MIN_WORDS = 3

    ITALIAN_REGIONS = _optional(
        "ITALIAN_REGIONS",
        "Roma,Milano,Torino,Bologna,Firenze,Napoli,Palermo,Genova,Venezia,Bari"
    )

    INCLUDE_CITY_TARGETING = True

    INDUSTRY_TARGETS = [
        "nail center professionali",
        "onicotecniche",
        "centri estetici",
        "saloni bellezza",
        "studi professionali bellezza",
        "scuole onicotecnica",
        "istituti professionali",
    ]

    # ==============================
    # MODERAZIONE & COMPLIANCE
    # ==============================
    ENABLE_COMPLIANCE_CHECK = True
    COMPLIANCE_REGION = "IT"

    AGCM_COMPLIANCE_MODE = True

    INCLUDE_PRIVACY_NOTICE = True
    PRIVACY_POLICY_URL = _optional("PRIVACY_URL", f"{WEBSITE_URL}/privacy-policy")

    INCLUDE_COOKIE_NOTICE = True

    DISCLAIMER_CLAIMS = (
        "I prodotti Benail sono certificati e provengono da fornitori verificati. "
        "La qualità dei lavori eseguiti dipende dalla tecnica applicativa e dall'esperienza dell'onicotecnica. "
        "I prezzi e la disponibilità sono soggetti a variazioni. Consulta la pagina del prodotto per le condizioni attuali."
    )

    ECOMMERCE_DISCLAIMER = (
        "Benail offre una selezione di prodotti professionali certificati per onicotecniche e nail center. "
        "La consegna in 24h è per ordini effettuati entro le 12:00. Disponibilità soggetta a variazioni di stock."
    )

    # ========================
    # OUTPUT & LOGGING
    # ========================
    OUTPUT_DIR = _optional("OUTPUT_DIR", "output")
    LOG_LEVEL = _optional("LOG_LEVEL", "INFO")
    SAVE_FULL_PIPELINE_OUTPUT = True
    SAVE_INDIVIDUAL_AGENT_OUTPUTS = True

    BACKUP_PUBLISHED_POSTS = True
    BACKUP_DIR = _optional("BACKUP_DIR", "backups")

    # ========================
    # ANALYTICS & TRACKING
    # ========================
    GOOGLE_ANALYTICS_ID = _optional("GA_ID", "")
    GOOGLE_SEARCH_CONSOLE_DOMAIN = _optional("GSC_DOMAIN", WEBSITE_DOMAIN)
    GOOGLE_ADS_ACCOUNT_ID = _optional("GOOGLE_ADS_ACCOUNT_ID", "")
    ENABLE_CONVERSION_TRACKING = True
    CONVERSION_TRACKING_ID = _optional("CONVERSION_ID", "")

    # ========================
    # SCHEDULING & AUTOMATION
    # ========================
    PUBLISH_FREQUENCY = _optional("PUBLISH_FREQUENCY", "bi-weekly")
    PUBLISH_DAY_OF_WEEK = int(_optional("PUBLISH_DAY", "2"))
    PUBLISH_HOUR_UTC = int(_optional("PUBLISH_HOUR", "9"))

    # ====================
    # PRESTASHOP SEO SETTINGS
    # ====================
    PERMALINK_STRUCTURE = _optional("PERMALINK_STRUCTURE", "/{id}-{name}")
    DEFAULT_POST_AUTHOR = _optional("DEFAULT_AUTHOR", "Benail Admin")
    ALLOW_COMMENTS = bool(_optional("ALLOW_COMMENTS", "true").lower() == "true")

    # ==========================================
    # CONTENT STRATEGY: Benail Focus
    # ==========================================
    CONTENT_THEMES = [
        "Guida ai prodotti professionali per nail art",
        "Tutorial ricostruzione unghie",
        "Differenze tra gel e acrygel",
        "Prodotti HEMA Free: cosa significa",
        "Come scegliere la lampada UV/LED",
        "Consigli di applicazione smalto semipermanente",
        "Tendenze nail art professionale",
        "Cura e manutenzione attrezzature",
        "Prodotti per nail center professionali",
        "Innovazioni nell'industria onicotecnica",
    ]

    FAQ_TOPICS = [
        "Cosa significa HEMA Free?",
        "Differenza tra gel trifasico e monofasico?",
        "Come applicare bene lo smalto semipermanente?",
        "Qual è la migliore lampada UV o LED?",
        "Come fare ricostruzioni in acrygel?",
        "Quali sono i migliori marchi professionali?",
        "Quanto dura lo smalto semipermanente?",
        "Come rimuovere lo smalto semipermanente?",
        "Offrite prezzi all'ingrosso per rivenditori?",
        "Quali sono le condizioni di spedizione?",
    ]

    # ========================
    # SEO AUDIT IMPLEMENTATIONS
    # ========================
    
    # CRITICAL: H1 Homepage Tag
    HOMEPAGE_H1 = "Prodotti Professionali per Onicotecniche – Smalti, Gel, Acrygel e Attrezzature con consegna in 24h"
    
    # CRITICAL: Optimized Meta Title (50-60 chars)
    HOMEPAGE_META_TITLE = "Prodotti Onicotecniche Professionali | Consegna 24h – Benail"
    
    # CRITICAL: Optimized Meta Description (150-160 chars)
    HOMEPAGE_META_DESCRIPTION = (
        "Prodotti professionali onicotecniche: smalti semipermanenti, acrygel, gel, lampade e attrezzature "
        "HEMA Free. Spedizione 24h. Prezzi rivenditori. Scopri il catalogo Benail."
    )
    
    # CRITICAL: Meta Viewport (fix for accessibility & mobile SEO)
    VIEWPORT_TAG = "width=device-width, initial-scale=1"
    
    # IMPORTANT: Homepage SEO Text (200-300 words)
    HOMEPAGE_SEO_TEXT = (
        "Benail è l'e-commerce specializzato in prodotti professionali per onicotecniche e nail center in tutta Italia. "
        "Offriamo una selezione curata di smalti semipermanenti, gel trifasico, acrygel, lampade UV/LED professionali, "
        "e attrezzature per nail art e ricostruzioni unghie. Tutti i nostri prodotti sono certificati, HEMA Free, "
        "e provengono da marchi internazionali riconosciuti nel settore. "
        "Che tu sia un'onicotecnica indipendente, un nail center professionista, o una scuola di formazione, "
        "Benail ha tutto ciò che ti serve per offrire servizi di qualità ai tuoi clienti. "
        "Con consegna garantita in 24h su tutta Italia e prezzi speciali per rivenditori e ordini in volume, "
        "Benail è il partner ideale per i professionisti del settore nail. "
        "Scopri il nostro catalogo completo di categorie: semipermanenti, gel monofasico e trifasico, "
        "acrygel, costruttori, apparecchiature, e tutta l'attrezzatura necessaria per completare il tuo kit professionale. "
        "Affidati a Benail per la qualità, la rapidità e il supporto professionale che meriti."
    )

    # IMPORTANT: Schema Markup Configuration
    ENABLE_SCHEMA_MARKUP = True
    SCHEMA_PRODUCT_ENABLED = True
    SCHEMA_BREADCRUMB_ENABLED = True
    SCHEMA_ORGANIZATION_ENABLED = True
    SCHEMA_FAQ_ENABLED = True
    
    # Organization Schema
    ORGANIZATION_SCHEMA = {
        "name": "Benail",
        "url": WEBSITE_URL,
        "logo": f"{WEBSITE_URL}/logo.png",
        "description": "E-commerce prodotti professionali onicotecniche",
        "telephone": _optional("PHONE_NUMBER", ""),
        "address": _optional("BUSINESS_ADDRESS", "Italia"),
        "sameAs": [
            _optional("FACEBOOK_URL", ""),
            _optional("INSTAGRAM_URL", ""),
        ]
    }

    # ====================
    # VALIDAZIONE FINALI
    # ====================
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration at startup."""
        required = [
            cls.GROQ_API_KEY,
            cls.PRESTA_WS_KEY,
        ]
        for val in required:
            if not val:
                return False
        return True


# Singleton instance
config = SEOConfig()


def get_config() -> SEOConfig:
    if not SEOConfig.validate():
        raise EnvironmentError("Invalid configuration. Check environment variables.")
    return config


def print_config_summary():
    print("=" * 70)
    print("CONFIGURATION - SEO Pipeline Benail.it")
    print("FOCUS: Prodotti Professionali Onicotecniche / E-commerce Nail")
    print("=" * 70)
    print(f"Brand: {config.BRAND_NAME}")
    print(f"Site: {config.WEBSITE_URL}")
    print(f"Language: {config.LANGUAGE_CODE}")
    print(f"Presta enabled: {config.PRESTA_ENABLED}")
    print(f"Schema markup enabled: {config.ENABLE_SCHEMA_MARKUP}")
    print("=" * 70)
