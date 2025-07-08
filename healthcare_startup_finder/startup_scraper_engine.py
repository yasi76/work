#!/usr/bin/env python3
"""
Advanced Startup Scraper Engine
Searches multiple online directories to find comprehensive startup listings
"""

import json
import csv
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Set
from urllib.parse import quote_plus, urljoin, urlparse
import re
import os

class StartupScraperEngine:
    """Advanced scraper that finds startups from multiple online directories"""
    
    def __init__(self):
        self.startups = []
        self.seen_names = set()
        self.seen_urls = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
    def add_startup(self, startup_data):
        """Add a startup if it's not a duplicate"""
        name = startup_data.get('name', '').strip()
        if not name or name.lower() in self.seen_names:
            return False
            
        self.seen_names.add(name.lower())
        startup_data['collected_date'] = datetime.now().strftime('%Y-%m-%d')
        self.startups.append(startup_data)
        print(f"  Added: {name} ({startup_data.get('country', 'Unknown')})")
        return True
    
    def search_crunchbase_style(self):
        """Search Crunchbase-style directories"""
        print("\nSearching startup databases...")
        
        # Known healthcare startup lists
        startup_lists = [
            {
                'name': 'German Health Startups Directory',
                'url': 'https://www.german-startups.de/health/',
                'pattern': 'health|medic|pharma|biotech|digital health'
            },
            {
                'name': 'EU-Startups Health',
                'url': 'https://www.eu-startups.com/category/health/',
                'pattern': 'health|medical|pharma|biotech'
            },
            {
                'name': 'StartupBlink Healthcare',
                'url': 'https://www.startupblink.com/industry/healthcare',
                'pattern': 'healthcare|medical|health tech'
            },
            {
                'name': 'F6S Healthcare Startups',
                'url': 'https://www.f6s.com/companies/health/germany/co',
                'pattern': 'health|medical|digital health'
            },
            {
                'name': 'AngelList Germany Health',
                'url': 'https://angel.co/companies?locations%5B%5D=Germany&markets%5B%5D=Healthcare',
                'pattern': 'health|medical|biotech'
            }
        ]
        
        for directory in startup_lists:
            try:
                print(f"\nSearching {directory['name']}...")
                response = self.session.get(directory['url'], timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Find startup entries
                    entries = soup.find_all(['article', 'div', 'li'], class_=re.compile('startup|company|item|card'))
                    
                    for entry in entries[:50]:  # Limit to prevent overwhelming
                        # Extract name
                        name_elem = entry.find(['h2', 'h3', 'h4', 'a'], class_=re.compile('name|title|heading'))
                        if name_elem:
                            name = name_elem.get_text().strip()
                            
                            # Extract URL
                            url_elem = entry.find('a', href=True)
                            url = url_elem['href'] if url_elem else ''
                            if url and not url.startswith('http'):
                                url = urljoin(directory['url'], url)
                            
                            # Extract description
                            desc_elem = entry.find(['p', 'div'], class_=re.compile('desc|summary|tagline'))
                            description = desc_elem.get_text().strip() if desc_elem else ''
                            
                            # Extract location
                            loc_elem = entry.find(['span', 'div'], class_=re.compile('location|city|country'))
                            location = loc_elem.get_text().strip() if loc_elem else ''
                            
                            if name and re.search(directory['pattern'], name + ' ' + description, re.I):
                                self.add_startup({
                                    'name': name,
                                    'website': url,
                                    'location': location,
                                    'country': self.determine_country(url, name, location),
                                    'description': description[:200],
                                    'category': 'Digital Health',
                                    'source': directory['name']
                                })
                    
            except Exception as e:
                print(f"  Error: {e}")
                
    def search_accelerators(self):
        """Search accelerator portfolios"""
        print("\nSearching accelerator portfolios...")
        
        accelerators = [
            {
                'name': 'Startupbootcamp Digital Health',
                'portfolio_url': 'https://www.startupbootcamp.org/accelerator/digital-health-berlin/portfolio/',
                'category': 'Digital Health Accelerator'
            },
            {
                'name': 'EIT Health',
                'portfolio_url': 'https://eithealth.eu/our-startups/',
                'category': 'European Health Innovation'
            },
            {
                'name': 'Flying Health',
                'portfolio_url': 'https://flyinghealth.com/portfolio/',
                'category': 'Digital Health Incubator'
            },
            {
                'name': 'Health Founders',
                'portfolio_url': 'https://healthfounders.de/portfolio/',
                'category': 'Healthcare Accelerator'
            },
            {
                'name': 'Techstars Healthcare',
                'portfolio_url': 'https://www.techstars.com/portfolio?industries=Healthcare',
                'category': 'Global Health Accelerator'
            }
        ]
        
        for acc in accelerators:
            try:
                print(f"\nSearching {acc['name']}...")
                response = self.session.get(acc['portfolio_url'], timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Find portfolio companies
                    companies = soup.find_all(['div', 'article', 'li'], class_=re.compile('portfolio|company|startup'))
                    
                    for company in companies[:30]:
                        name_elem = company.find(['h3', 'h4', 'a'])
                        if name_elem:
                            name = name_elem.get_text().strip()
                            
                            # Get company URL
                            url_elem = company.find('a', href=True)
                            url = url_elem['href'] if url_elem else ''
                            
                            self.add_startup({
                                'name': name,
                                'website': url,
                                'location': '',
                                'country': 'Europe',
                                'description': f"Portfolio company of {acc['name']}",
                                'category': acc['category'],
                                'source': acc['name']
                            })
                            
            except Exception as e:
                print(f"  Error: {e}")
                
    def search_vc_portfolios(self):
        """Search VC portfolios for healthcare startups"""
        print("\nSearching VC portfolios...")
        
        vcs = [
            {
                'name': 'Heal Capital',
                'url': 'https://heal.capital/portfolio/',
                'focus': 'Digital Health VC'
            },
            {
                'name': 'Earlybird Health',
                'url': 'https://earlybird.com/portfolio/',
                'focus': 'European Health Tech'
            },
            {
                'name': 'Cherry Ventures',
                'url': 'https://cherry.vc/portfolio/',
                'focus': 'European Tech VC'
            },
            {
                'name': 'HealthCap',
                'url': 'https://www.healthcap.se/portfolio/',
                'focus': 'Life Sciences VC'
            },
            {
                'name': 'MedTech Innovator',
                'url': 'https://medtechinnovator.org/companies/',
                'focus': 'Medical Technology'
            }
        ]
        
        for vc in vcs:
            try:
                print(f"\nSearching {vc['name']}...")
                response = self.session.get(vc['url'], timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Find portfolio companies
                    companies = soup.find_all(['div', 'article'], class_=re.compile('portfolio|company'))
                    
                    for company in companies[:25]:
                        name_elem = company.find(['h3', 'h4', 'a'])
                        if name_elem:
                            name = name_elem.get_text().strip()
                            
                            self.add_startup({
                                'name': name,
                                'website': '',
                                'location': '',
                                'country': 'Europe',
                                'description': f"{vc['focus']} portfolio company",
                                'category': 'Healthcare Investment',
                                'source': vc['name']
                            })
                            
            except Exception as e:
                print(f"  Error: {e}")
                
    def search_specific_directories(self):
        """Search specific healthcare startup directories"""
        print("\nSearching specialized directories...")
        
        # Healthcare-specific directories
        directories = [
            'https://www.healthcare-startups.de/',
            'https://www.digital-health-germany.com/startups',
            'https://www.medicalstartups.org/europe/',
            'https://www.healthtechinsider.com/category/startups/',
            'https://www.mobihealthnews.com/news/europe',
            'https://www.fiercehealthcare.com/digital-health',
            'https://www.digitalhealth.net/category/startups/',
            'https://www.healthcareitnews.com/directory/startups'
        ]
        
        for directory_url in directories:
            try:
                domain = urlparse(directory_url).netloc
                print(f"\nSearching {domain}...")
                
                response = self.session.get(directory_url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Find all links that might be startup pages
                    links = soup.find_all('a', href=True)
                    
                    for link in links:
                        text = link.get_text().strip()
                        href = link['href']
                        
                        # Check if it looks like a company name
                        if len(text.split()) <= 3 and text[0].isupper() and 'health' in href.lower():
                            if not href.startswith('http'):
                                href = urljoin(directory_url, href)
                                
                            self.add_startup({
                                'name': text,
                                'website': href,
                                'location': '',
                                'country': 'Europe',
                                'description': f'Found on {domain}',
                                'category': 'Digital Health',
                                'source': domain
                            })
                            
            except Exception as e:
                print(f"  Error: {e}")
                
    def determine_country(self, url, name, location=''):
        """Determine country from URL, name, or location"""
        text = f"{url} {name} {location}".lower()
        
        # Country detection patterns
        if any(x in text for x in ['.de', 'germany', 'german', 'deutschland', 'berlin', 'munich', 'hamburg', 'frankfurt']):
            return 'Germany'
        elif any(x in text for x in ['.uk', '.co.uk', 'united kingdom', 'uk', 'london', 'manchester', 'edinburgh']):
            return 'United Kingdom'
        elif any(x in text for x in ['.fr', 'france', 'french', 'paris', 'lyon', 'marseille']):
            return 'France'
        elif any(x in text for x in ['.nl', 'netherlands', 'dutch', 'amsterdam', 'rotterdam']):
            return 'Netherlands'
        elif any(x in text for x in ['.es', 'spain', 'spanish', 'madrid', 'barcelona']):
            return 'Spain'
        elif any(x in text for x in ['.it', 'italy', 'italian', 'milan', 'rome']):
            return 'Italy'
        elif any(x in text for x in ['.se', 'sweden', 'swedish', 'stockholm']):
            return 'Sweden'
        elif any(x in text for x in ['.dk', 'denmark', 'danish', 'copenhagen']):
            return 'Denmark'
        elif any(x in text for x in ['.ch', 'switzerland', 'swiss', 'zurich', 'geneva']):
            return 'Switzerland'
        elif any(x in text for x in ['.at', 'austria', 'austrian', 'vienna']):
            return 'Austria'
        elif any(x in text for x in ['.be', 'belgium', 'belgian', 'brussels']):
            return 'Belgium'
        elif any(x in text for x in ['.fi', 'finland', 'finnish', 'helsinki']):
            return 'Finland'
        elif any(x in text for x in ['.no', 'norway', 'norwegian', 'oslo']):
            return 'Norway'
        elif any(x in text for x in ['.pl', 'poland', 'polish', 'warsaw']):
            return 'Poland'
        elif any(x in text for x in ['.ie', 'ireland', 'irish', 'dublin']):
            return 'Ireland'
        else:
            return 'Europe'
            
    def save_results(self):
        """Save results to multiple formats"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save to CSV
        csv_file = f'healthcare_startups_scraped_{timestamp}.csv'
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            if self.startups:
                writer = csv.DictWriter(f, fieldnames=self.startups[0].keys())
                writer.writeheader()
                writer.writerows(self.startups)
        print(f"\nCSV saved: {csv_file}")
        
        # Save to JSON
        json_file = f'healthcare_startups_scraped_{timestamp}.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.startups, f, ensure_ascii=False, indent=2)
        print(f"JSON saved: {json_file}")
        
        return len(self.startups)
        
    def run_comprehensive_search(self):
        """Run all search methods"""
        print("\n" + "="*70)
        print("COMPREHENSIVE HEALTHCARE STARTUP SEARCH")
        print("="*70)
        
        # Run all search methods
        self.search_crunchbase_style()
        self.search_accelerators()
        self.search_vc_portfolios()
        self.search_specific_directories()
        
        # Save results
        total = self.save_results()
        
        print("\n" + "="*70)
        print(f"SEARCH COMPLETE: Found {total} unique startups")
        print("="*70)
        
        return total

def main():
    scraper = StartupScraperEngine()
    scraper.run_comprehensive_search()

if __name__ == "__main__":
    main()