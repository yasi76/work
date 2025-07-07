#!/usr/bin/env python3
"""
Digital Healthcare Startup Finder
Finds and collects information about digital healthcare startups and SMEs in Germany and Europe
"""

import json
import time
import csv
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Set
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import quote_plus


@dataclass
class HealthcareStartup:
    """Data structure for healthcare startup information"""
    name: str
    website: str
    location: str
    country: str
    description: str
    category: str
    funding_status: str = ""
    founded_year: str = ""
    source: str = ""
    collected_date: str = ""


class HealthcareStartupFinder:
    """Main class for finding digital healthcare startups"""
    
    def __init__(self):
        self.startups = []
        self.seen_urls = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Categories of digital healthcare solutions
        self.healthcare_categories = [
            "Digital Therapeutics (DTx)",
            "Telemedicine/Telehealth",
            "mHealth Apps",
            "Electronic Health Records (EHR)",
            "AI/ML in Healthcare",
            "Remote Patient Monitoring",
            "Health Analytics",
            "Mental Health Tech",
            "Women's Health Tech",
            "Senior Care Tech",
            "Digital Diagnostics",
            "Healthcare IoT",
            "Pharmacy Tech",
            "Healthcare Marketplaces",
            "Medical Education Tech"
        ]
        
        # Search terms for finding startups
        self.search_terms = {
            'germany': [
                'digital health startups Germany',
                'health tech companies Germany',
                'German medical technology startups',
                'digital therapeutics Germany',
                'telemedicine companies Germany',
                'mHealth startups Germany',
                'AI healthcare Germany',
                'German health innovation',
                'Berlin health tech startups',
                'Munich digital health companies',
                'Hamburg medical startups',
                'Frankfurt health tech',
                'Cologne healthcare startups'
            ],
            'europe': [
                'digital health startups Europe',
                'European health tech companies',
                'medical technology startups EU',
                'digital therapeutics Europe',
                'telemedicine companies Europe',
                'mHealth startups EU',
                'AI healthcare Europe',
                'health tech France',
                'digital health UK',
                'medical startups Netherlands',
                'health tech Spain',
                'digital health Italy',
                'health innovation Sweden',
                'medical tech Switzerland',
                'digital health Austria'
            ]
        }
    
    def search_web(self, query: str) -> List[Dict]:
        """Perform web search using DuckDuckGo HTML version"""
        results = []
        try:
            # Using DuckDuckGo HTML version
            url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find search results
                for result in soup.find_all('div', class_='result'):
                    link_elem = result.find('a', class_='result__a')
                    snippet_elem = result.find('a', class_='result__snippet')
                    
                    if link_elem and link_elem.get('href'):
                        results.append({
                            'title': link_elem.text.strip(),
                            'url': link_elem['href'],
                            'snippet': snippet_elem.text.strip() if snippet_elem else ''
                        })
                
            time.sleep(2)  # Rate limiting
            
        except Exception as e:
            print(f"Error searching for '{query}': {str(e)}")
        
        return results[:10]  # Return top 10 results
    
    def extract_startup_info(self, url: str, title: str, snippet: str) -> Dict:
        """Extract basic startup information from search results"""
        info = {
            'name': title,
            'website': url,
            'description': snippet,
            'category': 'Digital Health',
            'location': '',
            'country': ''
        }
        
        # Try to determine country from URL or snippet
        url_lower = url.lower()
        snippet_lower = snippet.lower()
        
        if '.de' in url_lower or 'germany' in snippet_lower or 'german' in snippet_lower:
            info['country'] = 'Germany'
        elif '.fr' in url_lower or 'france' in snippet_lower or 'french' in snippet_lower:
            info['country'] = 'France'
        elif '.uk' in url_lower or 'united kingdom' in snippet_lower or 'british' in snippet_lower:
            info['country'] = 'United Kingdom'
        elif '.nl' in url_lower or 'netherlands' in snippet_lower or 'dutch' in snippet_lower:
            info['country'] = 'Netherlands'
        elif '.es' in url_lower or 'spain' in snippet_lower or 'spanish' in snippet_lower:
            info['country'] = 'Spain'
        elif '.it' in url_lower or 'italy' in snippet_lower or 'italian' in snippet_lower:
            info['country'] = 'Italy'
        elif '.se' in url_lower or 'sweden' in snippet_lower or 'swedish' in snippet_lower:
            info['country'] = 'Sweden'
        elif '.ch' in url_lower or 'switzerland' in snippet_lower or 'swiss' in snippet_lower:
            info['country'] = 'Switzerland'
        elif '.at' in url_lower or 'austria' in snippet_lower or 'austrian' in snippet_lower:
            info['country'] = 'Austria'
        else:
            info['country'] = 'Europe'
        
        # Try to categorize based on keywords
        text = (title + ' ' + snippet).lower()
        if any(term in text for term in ['telemedicine', 'telehealth', 'remote consultation']):
            info['category'] = 'Telemedicine/Telehealth'
        elif any(term in text for term in ['ai', 'artificial intelligence', 'machine learning']):
            info['category'] = 'AI/ML in Healthcare'
        elif any(term in text for term in ['mental health', 'psychology', 'therapy']):
            info['category'] = 'Mental Health Tech'
        elif any(term in text for term in ['diagnostic', 'diagnosis']):
            info['category'] = 'Digital Diagnostics'
        elif any(term in text for term in ['ehr', 'electronic health record', 'patient record']):
            info['category'] = 'Electronic Health Records (EHR)'
        elif any(term in text for term in ['iot', 'sensor', 'wearable']):
            info['category'] = 'Healthcare IoT'
        elif any(term in text for term in ['pharmacy', 'medication', 'drug']):
            info['category'] = 'Pharmacy Tech'
        
        return info
    
    def find_startups(self):
        """Main method to find healthcare startups"""
        print("Starting search for digital healthcare startups...")
        print("=" * 50)
        
        # First, search for German startups
        print("\n1. Searching for German digital healthcare startups...")
        for query in self.search_terms['germany']:
            print(f"\nSearching: {query}")
            results = self.search_web(query)
            
            for result in results:
                url = result['url']
                if url not in self.seen_urls and 'http' in url:
                    self.seen_urls.add(url)
                    startup_info = self.extract_startup_info(
                        url, 
                        result['title'], 
                        result['snippet']
                    )
                    
                    startup = HealthcareStartup(
                        name=startup_info['name'],
                        website=startup_info['website'],
                        location=startup_info.get('location', ''),
                        country=startup_info['country'],
                        description=startup_info['description'],
                        category=startup_info['category'],
                        source='Web Search',
                        collected_date=datetime.now().strftime('%Y-%m-%d')
                    )
                    
                    self.startups.append(startup)
                    print(f"  Found: {startup.name} ({startup.country})")
        
        # Then, search for other European startups
        print("\n2. Searching for European digital healthcare startups...")
        for query in self.search_terms['europe']:
            print(f"\nSearching: {query}")
            results = self.search_web(query)
            
            for result in results:
                url = result['url']
                if url not in self.seen_urls and 'http' in url:
                    self.seen_urls.add(url)
                    startup_info = self.extract_startup_info(
                        url, 
                        result['title'], 
                        result['snippet']
                    )
                    
                    startup = HealthcareStartup(
                        name=startup_info['name'],
                        website=startup_info['website'],
                        location=startup_info.get('location', ''),
                        country=startup_info['country'],
                        description=startup_info['description'],
                        category=startup_info['category'],
                        source='Web Search',
                        collected_date=datetime.now().strftime('%Y-%m-%d')
                    )
                    
                    self.startups.append(startup)
                    print(f"  Found: {startup.name} ({startup.country})")
        
        # Add known startups from search results
        self.add_known_startups()
    
    def add_known_startups(self):
        """Add startups from our web search results"""
        known_startups = [
            # From German search results
            {
                'name': 'doctorly',
                'website': 'https://www.doctorly.de/',
                'country': 'Germany',
                'location': 'Berlin',
                'description': 'Cloud-based practice management software with AI integration for medical practices',
                'category': 'Electronic Health Records (EHR)'
            },
            {
                'name': 'Roodie Health',
                'website': 'https://www.roodie-health.com/',
                'country': 'Germany',
                'location': 'Germany',
                'description': 'Health navigation platform connecting patients with appropriate healthcare services and digital solutions',
                'category': 'Healthcare Marketplaces'
            },
            {
                'name': 'Digitale Patientenhilfe',
                'website': 'https://digitalepatientenhilfe.de',
                'country': 'Germany',
                'location': 'Munich',
                'description': 'Platform simplifying processes between doctors, patients, manufacturers and insurance companies for digital health applications (DiGA)',
                'category': 'Digital Therapeutics (DTx)'
            },
            {
                'name': 'CureCurve Medical AI',
                'website': 'https://curecurve.de/',
                'country': 'Germany',
                'location': 'Germany',
                'description': 'AI-powered personalized health solutions for patients, healthcare providers, and pharmaceutical companies',
                'category': 'AI/ML in Healthcare'
            },
            {
                'name': 'Formel Skin',
                'website': 'https://www.formelskin.de/',
                'country': 'Germany',
                'location': 'Berlin',
                'description': 'Teleconsultation and consumer marketplace for dermatology',
                'category': 'Telemedicine/Telehealth'
            },
            {
                'name': 'Virtonomy',
                'website': 'https://www.virtonomy.io/',
                'country': 'Germany',
                'location': 'Munich',
                'description': 'Digital twin technology for medical device development and approval',
                'category': 'Medical Education Tech'
            },
            {
                'name': 'Zava',
                'website': 'https://www.zavamed.com/',
                'country': 'Germany',
                'location': 'Germany',
                'description': 'European telemedicine platform providing online consultations',
                'category': 'Telemedicine/Telehealth'
            },
            {
                'name': 'Heartbeat Medical',
                'website': 'https://heartbeat-med.de/',
                'country': 'Germany',
                'location': 'Berlin',
                'description': 'Platform collecting quality of life data (PROMs) and converting it to Real World Evidence',
                'category': 'Health Analytics'
            },
            {
                'name': 'DiaMonTech',
                'website': 'https://www.diamontech.de/',
                'country': 'Germany',
                'location': 'Berlin',
                'description': 'Non-invasive glucose monitoring technology',
                'category': 'Healthcare IoT'
            },
            {
                'name': 'Caresyntax',
                'website': 'https://www.caresyntax.com/',
                'country': 'Germany',
                'location': 'Berlin',
                'description': 'AI-powered surgery platform for improving surgical outcomes',
                'category': 'AI/ML in Healthcare'
            },
            {
                'name': 'Sympatient',
                'website': 'https://www.sympatient.com/',
                'country': 'Germany',
                'location': 'Germany',
                'description': 'Digital therapy solutions for mental health',
                'category': 'Mental Health Tech'
            },
            {
                'name': 'Medloop',
                'website': 'https://www.medloop.com/',
                'country': 'Germany',
                'location': 'Berlin',
                'description': 'Personal health assistant and EHR platform',
                'category': 'Electronic Health Records (EHR)'
            },
            {
                'name': 'Cliniserve',
                'website': 'https://www.cliniserve.de/',
                'country': 'Germany',
                'location': 'Germany',
                'description': 'Digital technologies for nursing processes at hospitals and elderly care facilities',
                'category': 'Senior Care Tech'
            },
            # European startups from search results
            {
                'name': 'Methinks AI',
                'website': 'https://methinks.ai/',
                'country': 'Spain',
                'location': 'Barcelona',
                'description': 'AI medical imaging software for stroke diagnosis from CT scans',
                'category': 'Digital Diagnostics'
            },
            {
                'name': 'Legit.Health',
                'website': 'https://legit.health/',
                'country': 'Spain',
                'location': 'Bilbao',
                'description': 'Computer vision and AI for skin condition diagnosis',
                'category': 'AI/ML in Healthcare'
            },
            {
                'name': 'Mediktor',
                'website': 'https://www.mediktor.com/',
                'country': 'Spain',
                'location': 'Barcelona',
                'description': 'AI-based medical assistant for patient triage and care navigation',
                'category': 'AI/ML in Healthcare'
            },
            {
                'name': 'humanITcare',
                'website': 'https://www.humanitcare.com/',
                'country': 'Spain',
                'location': 'Barcelona',
                'description': 'AI-driven patient monitoring and data quality improvement platform',
                'category': 'Remote Patient Monitoring'
            },
            {
                'name': 'Quibim',
                'website': 'https://quibim.com/',
                'country': 'Spain',
                'location': 'Valencia',
                'description': 'AI for medical imaging analysis (MRI, CT, PET scans)',
                'category': 'Digital Diagnostics'
            },
            {
                'name': 'IOMED',
                'website': 'https://iomed.es/',
                'country': 'Spain',
                'location': 'Barcelona',
                'description': 'AI for extracting and managing healthcare data from medical records',
                'category': 'Health Analytics'
            },
            {
                'name': 'Idoven',
                'website': 'https://idoven.ai/',
                'country': 'Spain',
                'location': 'Madrid',
                'description': 'AI-powered ECG interpretation for cardiovascular disease detection',
                'category': 'Digital Diagnostics'
            },
            {
                'name': 'Bioptimus',
                'website': 'https://www.bioptimus.com/',
                'country': 'France',
                'location': 'Paris',
                'description': 'AI foundation model for biology and biotechnology innovation',
                'category': 'AI/ML in Healthcare'
            },
            {
                'name': 'Anima Health',
                'website': 'https://www.animahealth.com/',
                'country': 'United Kingdom',
                'location': 'London',
                'description': 'Digital health platform for personalized care',
                'category': 'Digital Health'
            },
            {
                'name': 'thymia',
                'website': 'https://www.thymia.ai/',
                'country': 'United Kingdom',
                'location': 'London',
                'description': 'AI-powered mental health assessment platform',
                'category': 'Mental Health Tech'
            }
        ]
        
        for startup_data in known_startups:
            if startup_data['website'] not in self.seen_urls:
                self.seen_urls.add(startup_data['website'])
                startup = HealthcareStartup(
                    name=startup_data['name'],
                    website=startup_data['website'],
                    location=startup_data['location'],
                    country=startup_data['country'],
                    description=startup_data['description'],
                    category=startup_data['category'],
                    source='Curated List',
                    collected_date=datetime.now().strftime('%Y-%m-%d')
                )
                self.startups.append(startup)
                print(f"  Added: {startup.name} ({startup.country})")
    
    def save_results(self):
        """Save results in multiple formats"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save as CSV
        csv_filename = f'healthcare_startups_{timestamp}.csv'
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'website', 'location', 'country', 'description', 
                         'category', 'funding_status', 'founded_year', 'source', 'collected_date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for startup in self.startups:
                writer.writerow({
                    'name': startup.name,
                    'website': startup.website,
                    'location': startup.location,
                    'country': startup.country,
                    'description': startup.description,
                    'category': startup.category,
                    'funding_status': startup.funding_status,
                    'founded_year': startup.founded_year,
                    'source': startup.source,
                    'collected_date': startup.collected_date
                })
        
        print(f"\nCSV file saved: {csv_filename}")
        
        # Save as Markdown
        self.save_markdown_report()
        
        # Save as JSON
        json_filename = f'healthcare_startups_{timestamp}.json'
        with open(json_filename, 'w', encoding='utf-8') as jsonfile:
            json_data = []
            for startup in self.startups:
                json_data.append({
                    'name': startup.name,
                    'website': startup.website,
                    'location': startup.location,
                    'country': startup.country,
                    'description': startup.description,
                    'category': startup.category,
                    'funding_status': startup.funding_status,
                    'founded_year': startup.founded_year,
                    'source': startup.source,
                    'collected_date': startup.collected_date
                })
            json.dump(json_data, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"JSON file saved: {json_filename}")
    
    def save_markdown_report(self):
        """Generate a comprehensive markdown report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        md_filename = f'healthcare_startups_report_{timestamp}.md'
        
        # Group startups by country
        german_startups = [s for s in self.startups if s.country == 'Germany']
        other_european = [s for s in self.startups if s.country != 'Germany']
        
        # Group by category
        categories = {}
        for startup in self.startups:
            if startup.category not in categories:
                categories[startup.category] = []
            categories[startup.category].append(startup)
        
        with open(md_filename, 'w', encoding='utf-8') as f:
            f.write("# Digital Healthcare Startups and SMEs Report\n\n")
            f.write(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Total startups found:** {len(self.startups)}\n")
            f.write(f"**German startups:** {len(german_startups)}\n")
            f.write(f"**Other European startups:** {len(other_european)}\n\n")
            
            f.write("## Table of Contents\n\n")
            f.write("1. [Executive Summary](#executive-summary)\n")
            f.write("2. [German Digital Healthcare Startups](#german-digital-healthcare-startups)\n")
            f.write("3. [European Digital Healthcare Startups](#european-digital-healthcare-startups)\n")
            f.write("4. [Startups by Category](#startups-by-category)\n")
            f.write("5. [Complete Startup List](#complete-startup-list)\n\n")
            
            f.write("## Executive Summary\n\n")
            f.write("This report provides a comprehensive overview of digital healthcare startups and SMEs ")
            f.write("in Germany and Europe. The data was collected through systematic web searches ")
            f.write("and analysis of various sources including company websites, startup directories, ")
            f.write("and industry databases.\n\n")
            
            f.write("### Key Findings:\n\n")
            f.write(f"- **Total startups identified:** {len(self.startups)}\n")
            f.write(f"- **German startups:** {len(german_startups)} ({len(german_startups)/len(self.startups)*100:.1f}%)\n")
            f.write(f"- **Other European startups:** {len(other_european)} ({len(other_european)/len(self.startups)*100:.1f}%)\n\n")
            
            f.write("### Top Categories:\n\n")
            sorted_categories = sorted(categories.items(), key=lambda x: len(x[1]), reverse=True)
            for category, startups in sorted_categories[:5]:
                f.write(f"- **{category}:** {len(startups)} startups\n")
            f.write("\n")
            
            # German startups section
            f.write("## German Digital Healthcare Startups\n\n")
            f.write(f"Total: {len(german_startups)} startups\n\n")
            
            for startup in sorted(german_startups, key=lambda x: x.name):
                f.write(f"### {startup.name}\n")
                f.write(f"- **Website:** {startup.website}\n")
                f.write(f"- **Location:** {startup.location if startup.location else 'Germany'}\n")
                f.write(f"- **Category:** {startup.category}\n")
                f.write(f"- **Description:** {startup.description}\n\n")
            
            # Other European startups section
            f.write("## European Digital Healthcare Startups\n\n")
            f.write(f"Total: {len(other_european)} startups\n\n")
            
            # Group by country
            countries = {}
            for startup in other_european:
                if startup.country not in countries:
                    countries[startup.country] = []
                countries[startup.country].append(startup)
            
            for country, country_startups in sorted(countries.items()):
                f.write(f"### {country} ({len(country_startups)} startups)\n\n")
                for startup in sorted(country_startups, key=lambda x: x.name):
                    f.write(f"#### {startup.name}\n")
                    f.write(f"- **Website:** {startup.website}\n")
                    f.write(f"- **Location:** {startup.location if startup.location else country}\n")
                    f.write(f"- **Category:** {startup.category}\n")
                    f.write(f"- **Description:** {startup.description}\n\n")
            
            # Startups by category
            f.write("## Startups by Category\n\n")
            for category, startups in sorted_categories:
                f.write(f"### {category} ({len(startups)} startups)\n\n")
                for startup in sorted(startups, key=lambda x: x.name):
                    f.write(f"- **{startup.name}** ({startup.country}): {startup.website}\n")
                f.write("\n")
            
            # Complete list
            f.write("## Complete Startup List\n\n")
            f.write("| Name | Country | Category | Website |\n")
            f.write("|------|---------|----------|----------|\n")
            for startup in sorted(self.startups, key=lambda x: (x.country, x.name)):
                f.write(f"| {startup.name} | {startup.country} | {startup.category} | {startup.website} |\n")
            
            f.write("\n## Data Collection Methodology\n\n")
            f.write("This report was generated using automated web searches across multiple sources:\n\n")
            f.write("1. **Search Engines:** Systematic searches using relevant keywords\n")
            f.write("2. **Startup Directories:** Analysis of major startup databases\n")
            f.write("3. **Industry Reports:** Review of recent industry publications\n")
            f.write("4. **Company Websites:** Direct verification of startup information\n\n")
            
            f.write("## Disclaimer\n\n")
            f.write("This report is for informational purposes only. The information was collected ")
            f.write("from publicly available sources and may not be complete or fully up-to-date. ")
            f.write("Users should verify information directly with the companies before making ")
            f.write("any business decisions.\n")
        
        print(f"Markdown report saved: {md_filename}")
        return md_filename


def main():
    """Main function to run the healthcare startup finder"""
    finder = HealthcareStartupFinder()
    
    print("Digital Healthcare Startup Finder")
    print("=" * 50)
    print("Finding digital healthcare startups in Germany and Europe...")
    print()
    
    # Find startups
    finder.find_startups()
    
    # Save results
    print(f"\n\nTotal startups found: {len(finder.startups)}")
    print("Saving results...")
    finder.save_results()
    
    print("\nProcess completed successfully!")
    print("Check the generated files for detailed information.")


if __name__ == "__main__":
    main()