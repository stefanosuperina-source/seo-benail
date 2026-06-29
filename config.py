"""
Configurazione centrale per la pipeline SEO Stefano Da Google.

Questo sistema automatizza la creazione, revisione e pubblicazione di contenuti
ottimizzati per il mercato italiano. Tutte le configurazioni ambiente sono lette
da variabili d'ambiente (.env locale o GitHub Secrets).

FOCUS PRINCIPALE: Stefano Da Google è uno specialista di Google Ads (PPC)
con expertise in gestione campagne pay-per-click per il mercato italiano.
La strategia SEO serve a dominare Google Italia con visibilità organica
come specialista Google Ads, non come SEO specialist.

Mercato target: Italia (lingua italiana, .it domain)
Tipologia: Consulenza Google Ads, gestione campagne PPC, strategie pay-per-click
Specializzazione: Specialista Google Ads Italia, expertise in advertising digitale
"""

import os
from enum import Enum

try:
    from dotenv import load_dotenv
    load_dotenv()  # No-op su GitHub Actions; carica .env localmente
except ImportError:
    pass


class Language(str, Enum):
    """Lingue supportate dal sistema."""
    ITALIAN = "it"
    ENGLISH = "en"


class PublishStatus(str, Enum):
    """Stati di pubblicazione possibili."""
    DRAFT = "draft"
    PUBLISH = "publish"


class MarketRegion(str, Enum):
    """Regioni del mercato italiano per targeting locale."""
    ITALY_NATIONAL = "IT"
    NORD = "nord"
    CENTRO = "centro"
    SUD = "sud"
    SICILIA = "sicilia"


def _require(name: str) -> str:
    """
    Legge una variabile d'ambiente richiesta.
    Genera eccezione se non trovata.
    """
    value = os.environ.get(name)
    if not value:
        raise EnvironmentError(
            f"Variabile d'ambiente mancante: {name}\n"
            f"Configura nel file .env locale oppure in GitHub repo Settings > "
            f"Secrets and variables > Actions."
        )
    return value


def _optional(name: str, default: str = "") -> str:
    """Legge una variabile d'ambiente opzionale con valore di default."""
    return os.environ.get(name, default)


class SEOConfig:
    """
    Configurazione principale per la pipeline SEO italiana.
    NOTA: Questa pipeline SEO promuove Stefano Da Google come specialista Google Ads/PPC,
    non come SEO specialist. L'obiettivo è dominare Google Italia con contenuti su
    Google Ads, gestione campagne PPC, e strategie di advertising digitale.
    """

    # ============================
    # IDENTITÀ BRAND & POSIZIONAMENTO
    # ============================
    
    BRAND_NAME = "Stefano Da Google"
    WEBSITE_URL = _require("WP_URL").rstrip("/")  # e.g., https://stefanodagogle.com
    WEBSITE_DOMAIN = _optional("WP_DOMAIN", "stefanodagogle.com")
    
    # Impostazioni di lingua e localizzazione
    LANGUAGE = Language(_optional("LANGUAGE_CODE", "it"))
    LANGUAGE_CODE = LANGUAGE.value  # "it"
    LOCALE = "it_IT"  # Formato locale: it_IT
    COUNTRY_CODE = "IT"
    CURRENCY = "EUR"
    
    # Mercato target principale
    TARGET_MARKET = MarketRegion(_optional("TARGET_MARKET", "IT"))
    
    # ========================================
    # CORE POSITIONING: Specialista Google Ads
    # ========================================
    
    # Posizionamento principale
    SPECIALIST_TITLE = "Specialista Google Ads Italia"
    SPECIALIST_TAGLINE = "Gestione campagne Google Ads professionali per PMI italiane"
    
    # Descrizione della nicchia - GOOGLE ADS FOCUS
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
    
    # Parole chiave PRINCIPALI - Google Ads & PPC (NON SEO)
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
    
    # Keyword secondarie - Focus su conversioni/ROI/PPC
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
    
    # Long-tail keywords specifiche per Stefano Da Google
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
    
    # Servizi principali da enfatizzare nel contenuto
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
    
    # Expertise areas da evidenziare
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
    
    # Temperature defaults per diversi agenti
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
    
    # Comportamento di pubblicazione
    PUBLISH_STATUS = PublishStatus(_optional("PUBLISH_STATUS", "draft"))
    PUBLISH_STATUS_VALUE = PUBLISH_STATUS.value  # "draft" o "publish"
    
    # Categoria predefinita per i post (Google Ads, non SEO)
    DEFAULT_POST_CATEGORY = _optional("DEFAULT_CATEGORY", "Google Ads")
    
    # Tag predefiniti per tutti i post - GOOGLE ADS FOCUSED
    DEFAULT_POST_TAGS = [
        "Google Ads",
        "PPC",
        "Advertising",
        "Digital Marketing",
        "Campagne Ads",
        "Google Ads Italia",
    ]

    # ==================================
    # CONTENUTO & GENERAZIONE ARTICOLI
    # ==================================
    
    # Parametri di lunghezza contenuto (parole)
    MIN_ARTICLE_LENGTH = int(_optional("MIN_ARTICLE_LENGTH", "800"))
    MAX_ARTICLE_LENGTH = int(_optional("MAX_ARTICLE_LENGTH", "1500"))
    TARGET_ARTICLE_LENGTH = int(_optional("TARGET_ARTICLE_LENGTH", "1200"))
    
    # Meta tag - lunghezze consigliate per Google.it
    META_TITLE_MAX_LENGTH = 60  # caratteri (Google mostra 50-60)
    META_DESCRIPTION_MAX_LENGTH = 156  # caratteri (Google mostra 120-156)
    
    # Stile di tono/voice per i contenuti - Autorità in Google Ads
    CONTENT_TONE = _optional(
        "CONTENT_TONE",
        "autorevole esperto, pratico, focalizzato su risultati misurabili e ROI, "
        "conversazione diretta con imprenditori e marketer italiani che vogliono "
        "massimizzare il budget pubblicitario su Google Ads"
    )
    
    # CTA (Call To Action) predefinito - Google Ads focused
    DEFAULT_CTA = _optional(
        "DEFAULT_CTA",
        "Contatta Stefano Da Google oggi per una consulenza strategica gratuita su Google Ads. "
        "Scopri come ottimizzare le tue campagne PPC e aumentare il ROI del tuo advertising."
    )
    
    # Struttura heading predefinita
    USE_H2_STRUCTURE = True  # Usa H2 per sottotitoli principali
    INCLUDE_FAQ_SECTION = True  # Includi sezione FAQ su Google Ads

    # =====================
    # RICERCA & KEYWORD SEO
    # =====================
    
    # Fonte di keyword research - Focus Google Ads keywords
    KEYWORD_RESEARCH_SOURCE = _optional("KEYWORD_RESEARCH_SOURCE", "google_ads_market_analysis")
    
    # Focus su long-tail keywords per il mercato italiano su Google Ads
    PREFER_LONGTAIL_KEYWORDS = True
    LONGTAIL_MIN_WORDS = 3  # "specialista google ads roma" (4 parole)
    
    # Regioni italiane per targeting locale
    ITALIAN_REGIONS = _optional(
        "ITALIAN_REGIONS",
        "Roma,Milano,Torino,Bologna,Firenze,Napoli,Palermo,Genova,Venezia,Bari"
    )
    
    # Ricerca locale: includi città nelle keywords
    INCLUDE_CITY_TARGETING = True
    
    # Targeting per industrie specifiche (B2B, E-commerce, etc)
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
    
    # Guideline italiane per moderazione contenuti
    ENABLE_COMPLIANCE_CHECK = True
    COMPLIANCE_REGION = "IT"  # Conformità normative italiane
    
    # AGCM (Autorità Garante della Concorrenza e del Mercato) compliance
    AGCM_COMPLIANCE_MODE = True
    
    # GDPR/Privacy - mandatory per mercato italiano
    INCLUDE_PRIVACY_NOTICE = True
    PRIVACY_POLICY_URL = _optional("PRIVACY_URL", f"{WEBSITE_URL}/privacy")
    
    # Cookie disclosure (obbligatorio in Italia)
    INCLUDE_COOKIE_NOTICE = True
    
    # Disclaimer su risultati di advertising
    DISCLAIMER_CLAIMS = (
        "I risultati delle campagne Google Ads variano a seconda del mercato, della concorrenza, "
        "del budget e dell'implementazione strategica. Non garantiamo risultati specifici o posizionamenti, "
        "ma offriamo strategie comprovate per massimizzare il ROI del tuo advertising."
    )
    
    # Avvertimento su non-garantismo (importante per PPC)
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
    
    # Backup dei contenuti generati
    BACKUP_PUBLISHED_POSTS = True
    BACKUP_DIR = _optional("BACKUP_DIR", "backups")

    # ========================
    # ANALYTICS & TRACKING
    # ========================
    
    # Google Analytics per monitorare traffico e conversioni
    GOOGLE_ANALYTICS_ID = _optional("GA_ID", "")
    
    # Search Console ID (per monitorare visibilità organica)
    GOOGLE_SEARCH_CONSOLE_DOMAIN = _optional("GSC_DOMAIN", WEBSITE_DOMAIN)
    
    # Google Ads Account Link (per tracking conversioni sito)
    GOOGLE_ADS_ACCOUNT_ID = _optional("GOOGLE_ADS_ACCOUNT_ID", "")
    
    # Conversion tracking - fondamentale per dimostrare expertise
    ENABLE_CONVERSION_TRACKING = True
    CONVERSION_TRACKING_ID = _optional("CONVERSION_ID", "")

    # ========================
    # SCHEDULING & AUTOMATION
    # ========================
    
    # Frequenza di pubblicazione automatica (gestito da GitHub Actions)
    PUBLISH_FREQUENCY = _optional("PUBLISH_FREQUENCY", "bi-weekly")  # bi-weekly, weekly, monthly
    
    # Giorno/ora della settimana per pubblicazione (0=lunedì, 6=domenica)
    PUBLISH_DAY_OF_WEEK = int(_optional("PUBLISH_DAY", "2"))  # Mercoledì
    PUBLISH_HOUR_UTC = int(_optional("PUBLISH_HOUR", "9"))  # 9:00 AM UTC

    # =========================
    # IMPOSTAZIONI WORDPRESS
    # =========================
    
    # Permalink structure (slug)
    PERMALINK_STRUCTURE = _optional("PERMALINK_STRUCTURE", "/google-ads/%postname%/")
    
    # Autore predefinito per i post
    DEFAULT_POST_AUTHOR = _optional("DEFAULT_AUTHOR", "Stefano")
    
    # Abilita commenti per nuovi post
    ALLOW_COMMENTS = bool(_optional("ALLOW_COMMENTS", "true").lower() == "true")
    
    # Featured image - placeholder URL se non disponibile
    DEFAULT_FEATURED_IMAGE = _optional(
        "DEFAULT_FEATURED_IMAGE",
        f"{WEBSITE_URL}/images/google-ads-featured.jpg"
    )

    # ==========================================
    # STRATEGIA CONTENUTO: Google Ads Focus
    # ==========================================
    
    # Temi di contenuto principali (per il Researcher agent)
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
    
    # Domande frequenti che il Researcher dovrebbe coprire
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
    # VALIDAZIONE FINALI
    # ====================
    
    @classmethod
    def validate(cls) -> bool:
        """Valida la configurazione al startup."""
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


# Istanza singleton della configurazione
config = SEOConfig()


# =====================================================
# LINEE GUIDA DI MODERAZIONE - Google Ads Italia
# =====================================================

ITALIAN_MODERATION_GUIDELINES = """
LINEE GUIDA DI MODERAZIONE - Specialista Google Ads Italia

IMPORTANTE: Stefano Da Google è posizionato come SPECIALISTA GOOGLE ADS/PPC,
non come SEO specialist. Moderiamo i contenuti come expertise in advertising digitale.

1. AGCM (Autorità Garante della Concorrenza e del Mercato)
   - Nessun claim assoluto su risultati garantiti: "garantiamo ROI X%"
   - Evita comparazioni dirette con competitor senza fonte
   - ROI variano a seconda di industria, budget, targeting, creatività
   - Esempio vietato: "Garantiamo 3x ROI su tutte le campagne Google Ads"
   - Esempio ok: "Strategie comprovate per massimizzare il ROI su Google Ads. 
     I risultati variano per industria e budget."

2. GDPR e Privacy
   - Assicurati che tracking e dati utente rispettino GDPR
   - Includi sempre il link alla privacy policy
   - Informazioni di contatto devono essere accurate

3. Affermazioni sui Risultati di Advertising
   - Case studies devono avere disclaimer: "Risultati variabili per industria"
   - Tempi di risultato: "Le ottimizzazioni possono richiedere 2-4 settimane per generare dati significativi"
   - Performance passate non garantiscono performance future
   - Client testimonials devono essere equilibrati e verificabili
   - Evita numeri che sembrano inventati: "aumentiamo CTR del 156%" senza fonte

4. Lingua e Tone
   - Italiana corretta, non tradotta automaticamente
   - Tone: autorevole ma accessible, parlare al livello di PMI italiane
   - Evita gergo molto tecnico senza spiegazione
   - Focus su ROI, conversioni, risultati misurabili

5. Dichiarazioni di Competenza e Expertise
   - Se citi studi Google Ads, usa fonti ufficiali (Google Ads Help, Google Blog)
   - Evita: "è noto che...", "tutti sanno che..." senza fonte
   - Certificazioni (Google Ads Certification, etc) devono essere reali e aggiornate

6. Disclaimer Obbligatori su Google Ads
   - Google Ads è advertising PAGATO, non risultati organici/SEO
   - I risultati dipendono da budget, targeting, creativas, landing page
   - Nessuno può garantire conversioni specifiche su Google Ads
   - Budget insufficiente = risultati limitati

7. Conformità Antitrust
   - Non fare affermazioni monopolistiche ("siamo i migliori")
   - Non denigrare competitor in modo scorretto
   - Focus su proposizione di valore: cosa offri, non cosa altri non offrono
   - Non promettere esclusività di strategy/tactics

8. Compliance Google Ads Policy
   - Se parli di landing pages, assicura che rispettino Google Ads policies
   - Non promettere di "aggirare" policies o limiti di Google
   - Content deve essere coerente con Google's advertising guidelines

Sei un moderatore esperto in advertising digitale e compliance italiano.
La tua priorità è proteggere il brand Stefano Da Google da problemi legali
mentre manteniamo credibilità come specialista Google Ads affidabile.
Non sei un avvocato, ma sei una prima linea di difesa contro errori evidenti.
"""


# ================================
# HELPER FUNCTIONS PER VALIDAZIONE
# ================================

def get_config() -> SEOConfig:
    """Ritorna l'istanza globale della configurazione."""
    if not SEOConfig.validate():
        raise EnvironmentError(
            "Configurazione non valida. Verifica che tutte le variabili d'ambiente siano impostate."
        )
    return config


def print_config_summary():
    """Stampa un riassunto della configurazione per debug/logging."""
    print("=" * 70)
    print("CONFIGURAZIONE - SEO Pipeline Stefano Da Google")
    print("FOCUS: Specialista Google Ads / PPC Advertising Italia")
    print("=" * 70)
    print(f"Brand: {config.BRAND_NAME}")
    print(f"Posizionamento: {config.SPECIALIST_TITLE}")
    print(f"Sito: {config.WEBSITE_URL}")
    print(f"Lingua: {config.LANGUAGE_CODE}")
    print(f"Locale: {config.LOCALE}")
    print(f"Mercato Target: {config.TARGET_MARKET.value}")
    print(f"Specializzazione: Google Ads / PPC (NON SEO)")
    print(f"\nKeyword Principale: {config.PRIMARY_KEYWORDS[0]}")
    print(f"Status di Pubblicazione: {config.PUBLISH_STATUS_VALUE}")
    print(f"Categoria Post: {config.DEFAULT_POST_CATEGORY}")
    print(f"LLM Model: {config.GROQ_MODEL}")
    print("=" * 70)
    print("\n🎯 Missione: Dominare Google Italia come SPECIALISTA GOOGLE ADS")
    print("   (Visibilità organica per servizi di gestione campagne PPC)")
    print("=" * 70)


if __name__ == "__main__":
    # Test della configurazione
    try:
        print_config_summary()
        print("\n✅ Configurazione caricata con successo!")
        print("\nServizi principali:")
        for service in config.CORE_SERVICES[:5]:
            print(f"  • {service}")
        print(f"  ... e altri {len(config.CORE_SERVICES) - 5} servizi")
    except EnvironmentError as e:
        print(f"\n❌ Errore di configurazione: {e}")
