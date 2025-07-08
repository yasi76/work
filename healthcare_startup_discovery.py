#!/usr/bin/env python3
"""
Healthcare Startup URL Discovery System
======================================

A comprehensive, scalable solution for discovering URLs of digital healthcare
startups and SMEs across Germany and Europe using asynchronous web scraping,
NLP filtering, and multiple data sources.

Author: AI Assistant
Date: 2024
"""

import asyncio
import aiohttp
import aiofiles
import json
import csv
import re
import time
import random
from typing import List, Dict, Set, Optional, Tuple
from urllib.parse import urlparse, urljoin, urlunparse
from dataclasses import dataclass
from datetime import datetime
import logging
from pathlib import Path

# Third-party imports
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from loguru import logger
from tqdm import tqdm
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

@dataclass
class CompanyData:
    """Data class for storing company information."""
    name: str
    url: str
    description: str
    source: str
    country: str
    confidence_score: float
    timestamp: str

class HealthcareKeywordFilter:
    """NLP-based filter to identify healthcare-related companies."""
    
    def __init__(self):
        self.healthcare_keywords = {
            'digital_health': [
                'telemedicine', 'telehealth', 'digital health', 'healthtech', 'health tech',
                'mhealth', 'mobile health', 'ehealth', 'e-health', 'healthcare technology',
                'healthcare software', 'healthcare platform', 'healthcare app', 'healthcare api'
            ],
            'medical_devices': [
                'medical device', 'medical technology', 'medtech', 'biomedical',
                'diagnostic', 'monitoring', 'sensor', 'wearable', 'implant'
            ],
            'healthcare_services': [
                'healthcare service', 'medical service', 'patient care', 'clinical',
                'healthcare provider', 'healthcare management', 'healthcare administration'
            ],
            'pharmaceutical': [
                'pharmaceutical', 'pharma', 'drug discovery', 'biotech', 'biotechnology',
                'clinical trial', 'drug development', 'therapeutics'
            ],
            'mental_health': [
                'mental health', 'psychology', 'psychiatry', 'therapy', 'counseling',
                'wellness', 'mindfulness', 'mental wellness'
            ],
            'ai_healthcare': [
                'ai healthcare', 'artificial intelligence healthcare', 'machine learning healthcare',
                'healthcare ai', 'predictive analytics', 'healthcare analytics'
            ]
        }
        
        # Load stopwords
        self.stop_words = set(stopwords.words('english') + stopwords.words('german'))
        
        # Create TF-IDF vectorizer for similarity matching
        self.vectorizer = TfidfVectorizer(
            stop_words=list(self.stop_words),
            ngram_range=(1, 2),
            max_features=1000
        )
        
        # Prepare keyword vectors
        self._prepare_keyword_vectors()
    
    def _prepare_keyword_vectors(self):
        """Prepare TF-IDF vectors for healthcare keywords."""
        all_keywords = []
        for category, keywords in self.healthcare_keywords.items():
            all_keywords.extend(keywords)
        
        # Fit vectorizer on healthcare keywords
        self.vectorizer.fit(all_keywords)
        self.keyword_vectors = self.vectorizer.transform(all_keywords)
    
    def is_healthcare_related(self, text: str, threshold: float = 0.3) -> Tuple[bool, float]:
        """
        Determine if text is healthcare-related using NLP techniques.
        
        Args:
            text: Text to analyze
            threshold: Similarity threshold for classification
            
        Returns:
            Tuple of (is_healthcare, confidence_score)
        """
        if not text or len(text.strip()) < 10:
            return False, 0.0
        
        # Clean and tokenize text
        text_lower = text.lower()
        tokens = word_tokenize(text_lower)
        
        # Remove stopwords and short tokens
        tokens = [token for token in tokens if token not in self.stop_words and len(token) > 2]
        
        if not tokens:
            return False, 0.0
        
        # Check for direct keyword matches
        text_words = set(tokens)
        keyword_matches = 0
        
        for category, keywords in self.healthcare_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    keyword_matches += 1
        
        # Calculate keyword density
        keyword_density = keyword_matches / len(tokens) if tokens else 0
        
        # Use TF-IDF similarity for more sophisticated matching
        try:
            text_vector = self.vectorizer.transform([text])
            similarities = cosine_similarity(text_vector, self.keyword_vectors)
            max_similarity = np.max(similarities)
        except Exception:
            max_similarity = 0
        
        # Combine keyword density and similarity
        confidence_score = (keyword_density * 0.6) + (max_similarity * 0.4)
        
        return confidence_score >= threshold, confidence_score

class URLValidator:
    """Validates and cleans URLs."""
    
    def __init__(self):
        self.social_media_domains = {
            'facebook.com', 'twitter.com', 'linkedin.com', 'instagram.com',
            'youtube.com', 'tiktok.com', 'snapchat.com', 'pinterest.com'
        }
        
        self.excluded_extensions = {'.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx'}
    
    def is_valid_url(self, url: str) -> bool:
        """Check if URL is valid and not a social media page."""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # Check if it's a social media domain
            if any(social in domain for social in self.social_media_domains):
                return False
            
            # Check for excluded file extensions
            path = parsed.path.lower()
            if any(path.endswith(ext) for ext in self.excluded_extensions):
                return False
            
            # Must have a valid scheme and netloc
            return parsed.scheme in ('http', 'https') and parsed.netloc
            
        except Exception:
            return False
    
    def clean_url(self, url: str) -> str:
        """Clean and normalize URL."""
        try:
            parsed = urlparse(url)
            # Remove fragments and normalize
            cleaned = urlunparse((
                parsed.scheme,
                parsed.netloc.lower(),
                parsed.path,
                parsed.params,
                parsed.query,
                ''  # Remove fragment
            ))
            return cleaned
        except Exception:
            return url

class AsyncWebScraper:
    """Asynchronous web scraper with retry logic and rate limiting."""
    
    def __init__(self, max_concurrent: int = 10, delay_range: Tuple[float, float] = (1, 3)):
        self.max_concurrent = max_concurrent
        self.delay_range = delay_range
        self.session = None
        self.ua = UserAgent()
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def __aenter__(self):
        """Async context manager entry."""
        connector = aiohttp.TCPConnector(limit=self.max_concurrent, limit_per_host=5)
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={'User-Agent': self.ua.random}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def fetch_with_retry(self, url: str, max_retries: int = 3) -> Optional[str]:
        """
        Fetch URL content with retry logic and rate limiting.
        
        Args:
            url: URL to fetch
            max_retries: Maximum number of retry attempts
            
        Returns:
            HTML content or None if failed
        """
        async with self.semaphore:
            for attempt in range(max_retries):
                try:
                    # Random delay to avoid rate limiting
                    await asyncio.sleep(random.uniform(*self.delay_range))
                    
                    async with self.session.get(url) as response:
                        if response.status == 200:
                            return await response.text()
                        elif response.status == 429:  # Rate limited
                            wait_time = (attempt + 1) * 5
                            logger.warning(f"Rate limited for {url}, waiting {wait_time}s")
                            await asyncio.sleep(wait_time)
                            continue
                        else:
                            logger.warning(f"HTTP {response.status} for {url}")
                            
                except asyncio.TimeoutError:
                    logger.warning(f"Timeout for {url} (attempt {attempt + 1})")
                except Exception as e:
                    logger.error(f"Error fetching {url}: {e}")
                
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
            
            return None

class HealthcareStartupDiscovery:
    """Main class for discovering healthcare startup URLs."""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.keyword_filter = HealthcareKeywordFilter()
        self.url_validator = URLValidator()
        self.discovered_companies: Set[str] = set()
        self.company_data: List[CompanyData] = []
        
        # Configure logging
        logger.add(
            self.output_dir / "discovery.log",
            rotation="10 MB",
            retention="7 days",
            level="INFO"
        )
    
    async def discover_from_websites(self) -> List[CompanyData]:
        """Discover companies from healthcare-related websites."""
        websites = [
            "https://www.digital-health-summit.de/",
            "https://www.healthcare-startups.de/",
            "https://www.digital-health-germany.de/",
            "https://www.healthcare-innovation.de/",
            "https://www.telemedizin.de/",
            "https://www.ehealth-europe.de/",
            "https://www.digital-health-europe.com/",
            "https://www.healthtech-europe.com/"
        ]
        
        results = []
        async with AsyncWebScraper() as scraper:
            tasks = [self._scrape_website(scraper, url) for url in websites]
            website_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in website_results:
                if isinstance(result, list):
                    results.extend(result)
        
        return results
    
    async def _scrape_website(self, scraper: AsyncWebScraper, url: str) -> List[CompanyData]:
        """Scrape a single website for company information."""
        try:
            html = await scraper.fetch_with_retry(url)
            if not html:
                return []
            
            soup = BeautifulSoup(html, 'html.parser')
            companies = []
            
            # Extract links that might be company websites
            links = soup.find_all('a', href=True)
            
            for link in links:
                href = link.get('href')
                text = link.get_text(strip=True)
                
                if not href or not text:
                    continue
                
                # Convert relative URLs to absolute
                if href.startswith('/'):
                    href = urljoin(url, href)
                elif not href.startswith('http'):
                    continue
                
                # Validate URL
                if not self.url_validator.is_valid_url(href):
                    continue
                
                # Check if it's healthcare-related
                is_healthcare, confidence = self.keyword_filter.is_healthcare_related(text)
                
                if is_healthcare and confidence > 0.4:
                    company = CompanyData(
                        name=text[:100],  # Limit name length
                        url=self.url_validator.clean_url(href),
                        description=text,
                        source=url,
                        country=self._detect_country(href),
                        confidence_score=confidence,
                        timestamp=datetime.now().isoformat()
                    )
                    companies.append(company)
            
            return companies
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return []
    
    def _detect_country(self, url: str) -> str:
        """Detect country from URL or domain."""
        try:
            domain = urlparse(url).netloc.lower()
            
            # German domains
            if domain.endswith('.de') or 'germany' in domain or 'deutschland' in domain:
                return 'Germany'
            
            # European domains
            eu_domains = {
                '.fr': 'France', '.it': 'Italy', '.es': 'Spain', '.nl': 'Netherlands',
                '.be': 'Belgium', '.at': 'Austria', '.ch': 'Switzerland', '.se': 'Sweden',
                '.no': 'Norway', '.dk': 'Denmark', '.fi': 'Finland', '.pl': 'Poland'
            }
            
            for ext, country in eu_domains.items():
                if domain.endswith(ext):
                    return country
            
            return 'Unknown'
            
        except Exception:
            return 'Unknown'
    
    async def discover_from_directories(self) -> List[CompanyData]:
        """Discover companies from startup directories."""
        # This would integrate with APIs like Crunchbase, AngelList, etc.
        # For now, we'll simulate with some known healthcare startup directories
        
        directories = [
            "https://www.crunchbase.com/search/organizations/field/organizations/categories/healthcare",
            "https://angel.co/companies?markets[]=Healthcare",
            "https://www.startupblink.com/startups/healthcare"
        ]
        
        # Placeholder for directory scraping
        # In a real implementation, you would need API keys and proper integration
        logger.info("Directory discovery would require API integration")
        return []
    
    async def discover_from_apis(self) -> List[CompanyData]:
        """Discover companies from structured APIs."""
        # Placeholder for API integrations
        # Examples: LinkedIn API, healthcare-specific APIs
        logger.info("API discovery would require proper API keys and integration")
        return []
    
    def deduplicate_companies(self, companies: List[CompanyData]) -> List[CompanyData]:
        """Remove duplicate companies based on URL and name similarity."""
        seen_urls = set()
        seen_names = set()
        unique_companies = []
        
        for company in companies:
            # Check URL similarity
            if company.url in seen_urls:
                continue
            
            # Check name similarity (simple approach)
            name_lower = company.name.lower()
            if any(self._similar_names(name_lower, seen) for seen in seen_names):
                continue
            
            seen_urls.add(company.url)
            seen_names.add(name_lower)
            unique_companies.append(company)
        
        return unique_companies
    
    def _similar_names(self, name1: str, name2: str, threshold: float = 0.8) -> bool:
        """Check if two company names are similar."""
        # Simple similarity check - in production, use more sophisticated NLP
        words1 = set(name1.split())
        words2 = set(name2.split())
        
        if not words1 or not words2:
            return False
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        similarity = len(intersection) / len(union) if union else 0
        return similarity >= threshold
    
    def save_results(self, companies: List[CompanyData], format: str = "csv"):
        """Save results to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format.lower() == "csv":
            filename = self.output_dir / f"healthcare_startups_{timestamp}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Name', 'URL', 'Description', 'Source', 'Country',
                    'Confidence Score', 'Timestamp'
                ])
                
                for company in companies:
                    writer.writerow([
                        company.name, company.url, company.description,
                        company.source, company.country, company.confidence_score,
                        company.timestamp
                    ])
        
        elif format.lower() == "json":
            filename = self.output_dir / f"healthcare_startups_{timestamp}.json"
            
            companies_dict = []
            for company in companies:
                companies_dict.append({
                    'name': company.name,
                    'url': company.url,
                    'description': company.description,
                    'source': company.source,
                    'country': company.country,
                    'confidence_score': company.confidence_score,
                    'timestamp': company.timestamp
                })
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(companies_dict, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Results saved to {filename}")
        return filename
    
    async def run_discovery(self, save_format: str = "csv") -> str:
        """
        Run the complete discovery process.
        
        Args:
            save_format: Output format ('csv' or 'json')
            
        Returns:
            Path to saved results file
        """
        logger.info("Starting healthcare startup discovery...")
        
        # Run all discovery methods
        tasks = [
            self.discover_from_websites(),
            self.discover_from_directories(),
            self.discover_from_apis()
        ]
        
        results = await asyncio.gather(*tasks)
        all_companies = []
        
        for result in results:
            if isinstance(result, list):
                all_companies.extend(result)
        
        # Deduplicate and filter
        unique_companies = self.deduplicate_companies(all_companies)
        
        # Filter by confidence score
        filtered_companies = [
            company for company in unique_companies
            if company.confidence_score >= 0.3
        ]
        
        # Sort by confidence score
        filtered_companies.sort(key=lambda x: x.confidence_score, reverse=True)
        
        logger.info(f"Discovered {len(filtered_companies)} unique healthcare companies")
        
        # Save results
        filename = self.save_results(filtered_companies, save_format)
        
        # Print summary
        self._print_summary(filtered_companies)
        
        return filename
    
    def _print_summary(self, companies: List[CompanyData]):
        """Print a summary of discovered companies."""
        if not companies:
            logger.info("No companies discovered")
            return
        
        logger.info(f"\n=== DISCOVERY SUMMARY ===")
        logger.info(f"Total companies: {len(companies)}")
        
        # Country distribution
        countries = {}
        for company in companies:
            countries[company.country] = countries.get(company.country, 0) + 1
        
        logger.info(f"Countries: {countries}")
        
        # Top companies by confidence
        top_companies = sorted(companies, key=lambda x: x.confidence_score, reverse=True)[:10]
        logger.info(f"\nTop 10 companies by confidence:")
        for i, company in enumerate(top_companies, 1):
            logger.info(f"{i}. {company.name} ({company.country}) - Score: {company.confidence_score:.3f}")

async def main():
    """Main function to run the discovery system."""
    discovery = HealthcareStartupDiscovery()
    
    try:
        filename = await discovery.run_discovery(save_format="csv")
        print(f"\nDiscovery completed! Results saved to: {filename}")
        
    except KeyboardInterrupt:
        logger.info("Discovery interrupted by user")
    except Exception as e:
        logger.error(f"Discovery failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())