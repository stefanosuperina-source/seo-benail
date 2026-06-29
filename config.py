"""
Central configuration for the SEO pipeline (Italian market)
This file is an updated version with PrestaShop integration settings added.
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
    Primary configuration for the italian SEO pipeline.
    """

    # ============================
    # BRAND & POSITIONING
    # ============================
    
    BRAND_NAME = "Stefano Da Google"
    WEBSITE_URL = _require("WP_URL").rstrip("/")  # e.g., https://stefanodagogle.com
    WEBSITE_DOMAIN = _optional("WP_DOMAIN", "stefanodagogle.com")
    
    # Localization
    LANGUAGE = Language(_optional("LANGUAGE_CODE", "it"))
    LANGUAGE_CODE = LANGUAGE.value
    LOCALE = "it_IT"
    COUNTRY_CODE = "IT"
    CURRENCY = "EUR"

    TARGET_MARKET = MarketRegion(_optional("TARGET_MARKET", "IT"))

    # ========================================
    # CORE POSITIONING: Specialista Google Ads
    # ========================================
    SPECIALIST_TITLE = "Specialista Google Ads Italia"
    SPECIALIST_TAGLINE = "Gestione campagne Google Ads professionali per PMI italiane"

    STORE_NICHE = _optional(
        "STORE_NICHE",
        "Specialista Google Ads per il mercato italiano - Gestione campagne PPC, "
        "advertising digitale, ottimizzazione budget pubblicitari, strategie pay-per-click "
        "per aziende italiane che vogliono dominare Google Ads"
    )

    BUSINESS_DESCRIPTION = (
        "Stefano Da Google è uno specialista certificato di Google Ads e gestione campagne "
        "pay-per-click. Offriamo strategie di advertising digitale avanzate, ottimizzazione "
        "campagne Google Ads, gestione budget PPC, keyword research per Google Ads, e "
        "strategie di conversione per PMI e business italiani che vogliono massimizzare "
        "il ROI su Google Ads."
    )

    PRIMARY_KEYWORDS = [
        "specialista google ads italia",
        "gestione campagne google ads",
        "google ads specialist roma",
        "campagne ppc italia",
        "advertising google ads",
        "ottimizzazione google ads",
        "google ads expert italy",
        "gestione google ads roma",
        "strategia google ads",
        "consulente google ads milano",
        "gestione budget google ads",
        "campaign manager google ads",
    ]

    SECONDARY_KEYWORDS = [
        "aumento conversioni google ads",
        "roi google ads",
        "costo per clic ottimizzato",
        "quality score google ads",
        "keyword research google ads",
        "remarketing google ads",
        "google shopping ads",
        "display ads optimization",
        "search ads management",
        "performance max campaigns",
    ]

    LONGTAIL_KEYWORDS = [
        "come gestire campagne google ads in italia",
        "migliorare roi campagne ppc",
        "ridurre costo per click google ads",
        "gestione google ads per e-commerce",
        "strategia google ads piccole aziende",
        "google ads b2b italia",
        "campagne google ads high-ticket",
        "ottimizzazione quality score google ads",
    ]

    CORE_SERVICES = [
        "Gestione Campagne Google Ads",
        "Strategia PPC Personalizzata",
        "Ottimizzazione ROI Advertising",
        "Keyword Research Google Ads",
        "Gestione Budget Pubblicitario",
        "A/B Testing Campagne",
        "Conversione Landing Pages",
        "Remarketing Strategico",
        "Google Shopping Setup",
        "Performance Optimization",
    ]

    EXPERTISE_AREAS = [
        "Google Search Ads",
        "Google Display Network (GDN)",
        "Google Shopping Campaigns",
        "Performance Max Campaigns",
        "YouTube Advertising",
        "Remarketing & Retargeting",
        "Lead Generation PPC",
        "E-commerce Google Ads",
        "B2B Campaign Management",
        "International PPC Strategies",
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
    # WORDPRESS / WOOCOMMERCE
    # =============================
    WP_URL = WEBSITE_URL
    WP_USERNAME = _require("WP_USERNAME")  # Admin WordPress username
    WP_APP_PASSWORD = _require("WP_APP_PASSWORD")  # Application Password (NOT login password)

    PUBLISH_STATUS = PublishStatus(_optional("PUBLISH_STATUS", "draft"))
    PUBLISH_STATUS_VALUE = PUBLISH_STATUS.value

    DEFAULT_POST_CATEGORY = _optional("DEFAULT_CATEGORY", "Google Ads")

    DEFAULT_POST_TAGS = [
        "Google Ads",
        "PPC",
        "Advertising",
        "Digital Marketing",
        "Campagne Ads",
        "Google Ads Italia",
    ]

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
        "autorevole esperto, pratico, focalizzato su risultati misurabili e ROI, "
        "conversazione diretta con imprenditori e marketer italiani che vogliono "
        "massimizzare il budget pubblicitario su Google Ads"
    )

    DEFAULT_CTA = _optional(
        "DEFAULT_CTA",
        "Contatta Stefano Da Google oggi per una consulenza strategica gratuita su Google Ads. "
        "Scopri come ottimizzare le tue campagne PPC e aumentare il ROI del tuo advertising."
    )

    USE_H2_STRUCTURE = True
    INCLUDE_FAQ_SECTION = True

    # =====================
    # RICERCA & KEYWORD SEO
    # =====================
    KEYWORD_RESEARCH_SOURCE = _optional("KEYWORD_RESEARCH_SOURCE", "google_ads_market_analysis")
    PREFER_LONGTAIL_KEYWORDS = True
    LONGTAIL_MIN_WORDS = 3

    ITALIAN_REGIONS = _optional(
        "ITALIAN_REGIONS",
        "Roma,Milano,Torino,Bologna,Firenze,Napoli,Palermo,Genova,Venezia,Bari"
    )

    INCLUDE_CITY_TARGETING = True

    INDUSTRY_TARGETS = [
        "e-commerce",
        "agenzie immobiliari",
        "studi professionali",
        "saloni bellezza",
        "ristoranti",
        "consulenza aziendale",
        "software b2b",
    ]

    # ==============================
    # MODERAZIONE & COMPLIANCE
    # ==============================
    ENABLE_COMPLIANCE_CHECK = True
    COMPLIANCE_REGION = "IT"

    AGCM_COMPLIANCE_MODE = True

    INCLUDE_PRIVACY_NOTICE = True
    PRIVACY_POLICY_URL = _optional("PRIVACY_URL", f"{WEBSITE_URL}/privacy")

    INCLUDE_COOKIE_NOTICE = True

    DISCLAIMER_CLAIMS = (
        "I risultati delle campagne Google Ads variano a seconda del mercato, della concorrenza, "
        "del budget e dell'implementazione strategica. Non garantiamo risultati specifici o posizionamenti, "
        "ma offriamo strategie comprovate per massimizzare il ROI del tuo advertising."
    )

    PPC_DISCLAIMER = (
        "Google Ads è un canale a pagamento. I risultati dipendono da budget, targeting, "
        "creatività e ottimizzazione continua. Nessun esperto può garantire conversioni specifiche."
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

    # =========================
    # IMPOSTAZIONI WORDPRESS
    # =========================
    PERMALINK_STRUCTURE = _optional("PERMALINK_STRUCTURE", "/google-ads/%postname%/")
    DEFAULT_POST_AUTHOR = _optional("DEFAULT_AUTHOR", "Stefano")
    ALLOW_COMMENTS = bool(_optional("ALLOW_COMMENTS", "true").lower() == "true")

    DEFAULT_FEATURED_IMAGE = _optional(
        "DEFAULT_FEATURED_IMAGE",
        f"{WEBSITE_URL}/images/google-ads-featured.jpg"
    )

    # ==========================================
    # STRATEGIA CONTENUTO: Google Ads Focus
    # ==========================================
    CONTENT_THEMES = [
        "Strategie Google Ads avanzate",
        "Ottimizzazione ROI campagne PPC",
        "Gestione budget pubblicitario Google Ads",
        "Quality Score e performance ads",
        "Remarketing e retargeting strategico",
        "Google Shopping per e-commerce",
        "Lead generation con Google Ads",
        "Conversione visitors in clienti",
        "Targeting geografico e demografico",
        "Automazione campagne Google Ads",
    ]

    FAQ_TOPICS = [
        "Come iniziare con Google Ads?",
        "Qual è il budget minimo per Google Ads?",
        "Come calcolare il ROI delle campagne PPC?",
        "Cosa è il Quality Score su Google Ads?",
        "Differenza tra Search Ads e Display Ads?",
        "Come fare remarketing su Google?",
        "Come ottimizzare le parole chiave su Google Ads?",
        "Quanto costa gestire una campagna Google Ads?",
    ]

    # ====================
    # PRESTASHOP INTEGRAZIONE
    # ====================
    # PrestaShop settings (optional). Keep keys out of source control; use env or GitHub Secrets.
    PRESTA_URL = _optional("PRESTA_URL", "").rstrip("/")
    PRESTA_WS_KEY = _optional("PRESTA_WS_KEY", "")
    PRESTA_DEFAULT_LANG_ID = int(_optional("PRESTA_LANG_ID", "1"))
    PRESTA_SHOP_ID = int(_optional("PRESTA_SHOP_ID", "1"))
    PRESTA_CURRENCY = _optional("PRESTA_CURRENCY", "EUR")
    PRESTA_DRY_RUN = bool(_optional("PRESTA_DRY_RUN", "true").lower() == "true")

    # Convenience flag
    PRESTA_ENABLED = bool(PRESTA_URL and PRESTA_WS_KEY)

    # ====================
    # VALIDAZIONE FINALI
    # ====================
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration at startup."""
        required = [
            cls.GROQ_API_KEY,
            cls.WP_URL,
            cls.WP_USERNAME,
            cls.WP_APP_PASSWORD,
        ]
        for val in required:
            if not val:
                return False
        return True


# Singleton instance
config = SEOConfig()


# =====================================================
# MODERATION GUIDELINES (omitted here for brevity)
# =====================================================


def get_config() -> SEOConfig:
    if not SEOConfig.validate():
        raise EnvironmentError("Invalid configuration. Check environment variables.")
    return config


def print_config_summary():
    print("=" * 70)
    print("CONFIGURATION - SEO Pipeline Stefano Da Google")
    print("FOCUS: Specialista Google Ads / PPC Advertising Italia")
    print("=" * 70)
    print(f"Brand: {config.BRAND_NAME}")
    print(f"Site: {config.WEBSITE_URL}")
    print(f"Language: {config.LANGUAGE_CODE}")
    print(f"Presta enabled: {config.PRESTA_ENABLED}")
    print("=" * 70)
