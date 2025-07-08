#!/usr/bin/env python3
"""
Configuration Settings for Healthcare Startup Discovery System
===========================================================

Centralized configuration for all scraping parameters, URLs, and settings.
"""

import os
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class ScrapingConfig:
    """Configuration for web scraping parameters."""
    max_concurrent_requests: int = 10
    request_delay_range: tuple = (1, 3)
    timeout_seconds: int = 30
    max_retries: int = 3
    user_agent_rotation: bool = True
    rate_limit_delay: int = 5

@dataclass
class NLPConfig:
    """Configuration for NLP and keyword filtering."""
    confidence_threshold: float = 0.3
    keyword_density_weight: float = 0.6
    similarity_weight: float = 0.4
    min_text_length: int = 10
    max_features: int = 1000
    ngram_range: tuple = (1, 2)

@dataclass
class OutputConfig:
    """Configuration for output and file handling."""
    output_directory: str = "output"
    csv_format: bool = True
    json_format: bool = True
    log_level: str = "INFO"
    log_rotation: str = "10 MB"
    log_retention: str = "7 days"

@dataclass
class HealthcareKeywords:
    """Healthcare-related keywords for filtering."""
    digital_health: List[str] = None
    medical_devices: List[str] = None
    healthcare_services: List[str] = None
    pharmaceutical: List[str] = None
    mental_health: List[str] = None
    ai_healthcare: List[str] = None
    
    def __post_init__(self):
        if self.digital_health is None:
            self.digital_health = [
                'telemedicine', 'telehealth', 'digital health', 'healthtech', 'health tech',
                'mhealth', 'mobile health', 'ehealth', 'e-health', 'healthcare technology',
                'healthcare software', 'healthcare platform', 'healthcare app', 'healthcare api',
                'digital therapeutics', 'healthcare innovation', 'healthcare digitalization'
            ]
        
        if self.medical_devices is None:
            self.medical_devices = [
                'medical device', 'medical technology', 'medtech', 'biomedical',
                'diagnostic', 'monitoring', 'sensor', 'wearable', 'implant',
                'medical equipment', 'diagnostic tool', 'health monitoring'
            ]
        
        if self.healthcare_services is None:
            self.healthcare_services = [
                'healthcare service', 'medical service', 'patient care', 'clinical',
                'healthcare provider', 'healthcare management', 'healthcare administration',
                'healthcare consulting', 'medical consulting', 'healthcare solutions'
            ]
        
        if self.pharmaceutical is None:
            self.pharmaceutical = [
                'pharmaceutical', 'pharma', 'drug discovery', 'biotech', 'biotechnology',
                'clinical trial', 'drug development', 'therapeutics', 'medication',
                'drug research', 'pharmaceutical research'
            ]
        
        if self.mental_health is None:
            self.mental_health = [
                'mental health', 'psychology', 'psychiatry', 'therapy', 'counseling',
                'wellness', 'mindfulness', 'mental wellness', 'psychological',
                'behavioral health', 'mental healthcare'
            ]
        
        if self.ai_healthcare is None:
            self.ai_healthcare = [
                'ai healthcare', 'artificial intelligence healthcare', 'machine learning healthcare',
                'healthcare ai', 'predictive analytics', 'healthcare analytics',
                'healthcare automation', 'ai diagnostics', 'healthcare machine learning'
            ]

class DiscoverySources:
    """Sources for healthcare startup discovery."""
    
    # German and European healthcare websites
    GERMAN_HEALTHCARE_SITES = [
        "https://www.digital-health-summit.de/",
        "https://www.healthcare-startups.de/",
        "https://www.digital-health-germany.de/",
        "https://www.healthcare-innovation.de/",
        "https://www.telemedizin.de/",
        "https://www.ehealth-europe.de/",
        "https://www.digital-health-europe.com/",
        "https://www.healthtech-europe.com/",
        "https://www.healthcare-germany.de/",
        "https://www.digital-health-berlin.de/"
    ]
    
    # European healthcare directories
    EUROPEAN_DIRECTORIES = [
        "https://www.ehealth-europe.com/",
        "https://www.digital-health-europe.com/",
        "https://www.healthtech-europe.com/",
        "https://www.european-healthcare.com/",
        "https://www.healthcare-europe.eu/"
    ]
    
    # International startup directories (require JavaScript)
    INTERNATIONAL_DIRECTORIES = [
        "https://www.crunchbase.com/search/organizations/field/organizations/categories/healthcare",
        "https://angel.co/companies?markets[]=Healthcare",
        "https://www.startupblink.com/startups/healthcare",
        "https://www.pitchbook.com/profiles/company-search?filters=industry%3AHealthcare",
        "https://www.linkedin.com/search/results/companies/?keywords=healthcare%20startup"
    ]
    
    # Healthcare news and press release sites
    HEALTHCARE_NEWS_SITES = [
        "https://www.healthcareitnews.com/",
        "https://www.mobihealthnews.com/",
        "https://www.digitalhealth.net/",
        "https://www.healthcare-europe.com/",
        "https://www.healthcare-digital.com/"
    ]
    
    # German startup ecosystem sites
    GERMAN_STARTUP_ECOSYSTEM = [
        "https://www.startupdetector.de/",
        "https://www.deutsche-startups.de/",
        "https://www.gruenderszene.de/",
        "https://www.startupvalley.news/",
        "https://www.startup-radar.com/"
    ]

class APIConfig:
    """Configuration for API integrations."""
    
    # API endpoints (would require actual API keys)
    CRUNCHBASE_API = "https://api.crunchbase.com/v3.1/organizations"
    LINKEDIN_API = "https://api.linkedin.com/v2/organizations"
    ANGEL_LIST_API = "https://api.angel.co/1/companies"
    
    # Rate limiting for APIs
    API_RATE_LIMIT = 100  # requests per hour
    API_TIMEOUT = 30  # seconds
    
    # API keys (should be set via environment variables)
    CRUNCHBASE_API_KEY = os.getenv("CRUNCHBASE_API_KEY", "")
    LINKEDIN_API_KEY = os.getenv("LINKEDIN_API_KEY", "")
    ANGEL_LIST_API_KEY = os.getenv("ANGEL_LIST_API_KEY", "")

class BrowserConfig:
    """Configuration for browser automation."""
    
    # Selenium configuration
    SELENIUM_HEADLESS = True
    SELENIUM_TIMEOUT = 30
    SELENIUM_WINDOW_SIZE = (1920, 1080)
    
    # Playwright configuration
    PLAYWRIGHT_HEADLESS = True
    PLAYWRIGHT_TIMEOUT = 30000
    PLAYWRIGHT_VIEWPORT = {"width": 1920, "height": 1080}
    
    # Browser options
    CHROME_OPTIONS = [
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--disable-extensions",
        "--disable-plugins",
        "--disable-images"
    ]

class ValidationConfig:
    """Configuration for URL and data validation."""
    
    # Social media domains to exclude
    EXCLUDED_DOMAINS = {
        'facebook.com', 'twitter.com', 'linkedin.com', 'instagram.com',
        'youtube.com', 'tiktok.com', 'snapchat.com', 'pinterest.com',
        'reddit.com', 'medium.com', 'github.com'
    }
    
    # File extensions to exclude
    EXCLUDED_EXTENSIONS = {
        '.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx',
        '.zip', '.rar', '.tar', '.gz', '.mp4', '.mp3', '.avi'
    }
    
    # Minimum URL length
    MIN_URL_LENGTH = 10
    
    # Maximum URL length
    MAX_URL_LENGTH = 500

class CountryDetection:
    """Configuration for country detection."""
    
    # European country domains
    EUROPEAN_DOMAINS = {
        '.de': 'Germany',
        '.fr': 'France',
        '.it': 'Italy',
        '.es': 'Spain',
        '.nl': 'Netherlands',
        '.be': 'Belgium',
        '.at': 'Austria',
        '.ch': 'Switzerland',
        '.se': 'Sweden',
        '.no': 'Norway',
        '.dk': 'Denmark',
        '.fi': 'Finland',
        '.pl': 'Poland',
        '.pt': 'Portugal',
        '.ie': 'Ireland',
        '.uk': 'United Kingdom',
        '.eu': 'European Union'
    }
    
    # Country keywords in domains
    COUNTRY_KEYWORDS = {
        'germany': 'Germany',
        'deutschland': 'Germany',
        'france': 'France',
        'italy': 'Italy',
        'spain': 'Spain',
        'netherlands': 'Netherlands',
        'belgium': 'Belgium',
        'austria': 'Austria',
        'switzerland': 'Switzerland',
        'sweden': 'Sweden',
        'norway': 'Norway',
        'denmark': 'Denmark',
        'finland': 'Finland',
        'poland': 'Poland'
    }

# Global configuration instance
SCRAPING_CONFIG = ScrapingConfig()
NLP_CONFIG = NLPConfig()
OUTPUT_CONFIG = OutputConfig()
HEALTHCARE_KEYWORDS = HealthcareKeywords()
DISCOVERY_SOURCES = DiscoverySources()
API_CONFIG = APIConfig()
BROWSER_CONFIG = BrowserConfig()
VALIDATION_CONFIG = ValidationConfig()
COUNTRY_DETECTION = CountryDetection()

def get_config() -> Dict[str, Any]:
    """Get all configuration as a dictionary."""
    return {
        'scraping': SCRAPING_CONFIG,
        'nlp': NLP_CONFIG,
        'output': OUTPUT_CONFIG,
        'keywords': HEALTHCARE_KEYWORDS,
        'sources': DISCOVERY_SOURCES,
        'api': API_CONFIG,
        'browser': BROWSER_CONFIG,
        'validation': VALIDATION_CONFIG,
        'country_detection': COUNTRY_DETECTION
    }