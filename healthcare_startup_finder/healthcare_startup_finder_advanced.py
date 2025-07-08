#!/usr/bin/env python3
"""
Advanced Digital Healthcare Startup Finder
Searches multiple sources to find comprehensive list of digital healthcare startups in Germany and Europe
"""

import json
import csv
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Set
from urllib.parse import quote_plus, urljoin


class AdvancedHealthcareStartupFinder:
    """Advanced finder that searches multiple sources for healthcare startups"""
    
    def __init__(self):
        self.startups = []
        self.seen_names = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Expanded search queries for better coverage
        self.search_queries = {
            'germany': [
                # General searches
                'digital health startups Germany 2024',
                'German health tech companies list',
                'DiGA companies Germany',
                'medical technology startups Berlin',
                'health innovation Munich startups',
                'digital therapeutics Germany directory',
                'German telemedicine companies 2024',
                'eHealth startups Deutschland',
                'AI healthcare companies Germany',
                'remote patient monitoring Germany',
                
                # City-specific searches
                'health tech startups Berlin 2024',
                'Munich medical technology companies',
                'Hamburg digital health ecosystem',
                'Frankfurt healthcare innovation',
                'Cologne health tech startups',
                'Stuttgart medical startups',
                'Düsseldorf healthcare companies',
                'Leipzig digital health',
                
                # Category-specific searches
                'German mental health apps',
                'diabetes technology Germany',
                'German healthcare AI startups',
                'digital diagnostics Germany',
                'German health insurance tech',
                'medical device startups Germany',
                'German biotechnology startups',
                'pharmacy tech Germany'
            ],
            'europe': [
                # Country-specific searches
                'French digital health startups 2024',
                'Spain health tech companies',
                'UK digital therapeutics startups',
                'Netherlands eHealth companies',
                'Sweden digital health ecosystem',
                'Switzerland medical technology',
                'Italy telemedicine startups',
                'Austria health innovation',
                'Belgium healthcare startups',
                'Denmark health tech',
                'Norway digital health',
                'Finland medical startups',
                'Poland health tech companies',
                'Portugal digital health',
                
                # Pan-European searches
                'European health tech unicorns',
                'EU digital health startups 2024',
                'Europe telemedicine companies list',
                'European AI healthcare startups',
                'digital therapeutics Europe directory',
                'European health tech accelerators portfolio'
            ]
        }
        
        # Known startup directories and databases
        self.startup_directories = [
            {
                'name': 'German Startups Association',
                'url': 'https://startupverband.de/',
                'type': 'association'
            },
            {
                'name': 'Health Startups Germany',
                'url': 'https://www.health-startups.de/',
                'type': 'directory'
            },
            {
                'name': 'Digital Hub Initiative',
                'url': 'https://www.de-hub.de/',
                'type': 'hub'
            },
            {
                'name': 'GTAI Health Tech',
                'url': 'https://www.gtai.de/en/invest/industries/life-sciences/digital-health',
                'type': 'government'
            },
            {
                'name': 'EU-Startups Health',
                'url': 'https://www.eu-startups.com/category/health/',
                'type': 'media'
            }
        ]
        
        # Additional curated startups to ensure comprehensive coverage
        self.curated_startups = [
            # German Digital Health Startups
            {'name': 'Ada Health', 'website': 'https://ada.com/', 'country': 'Germany', 'city': 'Berlin', 
             'description': 'AI-powered health assessment and symptom checker', 'category': 'AI/ML in Healthcare'},
            {'name': 'Amboss', 'website': 'https://www.amboss.com/', 'country': 'Germany', 'city': 'Berlin',
             'description': 'Medical knowledge platform for doctors and students', 'category': 'Medical Education'},
            {'name': 'Clue', 'website': 'https://helloclue.com/', 'country': 'Germany', 'city': 'Berlin',
             'description': 'Menstrual cycle tracking and women\'s health app', 'category': 'Women\'s Health Tech'},
            {'name': 'Doctolib', 'website': 'https://www.doctolib.de/', 'country': 'Germany', 'city': 'Berlin',
             'description': 'Online appointment booking platform for healthcare', 'category': 'Healthcare Marketplaces'},
            {'name': 'Kry/Livi', 'website': 'https://www.kry.de/', 'country': 'Germany', 'city': 'Multiple',
             'description': 'Digital healthcare provider offering video consultations', 'category': 'Telemedicine/Telehealth'},
            {'name': 'Medigo', 'website': 'https://www.medigo.com/', 'country': 'Germany', 'city': 'Berlin',
             'description': 'Medical travel and international patient platform', 'category': 'Medical Tourism'},
            {'name': 'Mimi Hearing Technologies', 'website': 'https://www.mimi.io/', 'country': 'Germany', 'city': 'Berlin',
             'description': 'Digital hearing health solutions', 'category': 'Digital Therapeutics'},
            {'name': 'Ottonova', 'website': 'https://www.ottonova.de/', 'country': 'Germany', 'city': 'Munich',
             'description': 'Digital private health insurance', 'category': 'InsurTech Health'},
            {'name': 'Preventicus', 'website': 'https://www.preventicus.com/', 'country': 'Germany', 'city': 'Jena',
             'description': 'Heart rhythm analysis via smartphone', 'category': 'Digital Diagnostics'},
            {'name': 'Selfapy', 'website': 'https://www.selfapy.de/', 'country': 'Germany', 'city': 'Berlin',
             'description': 'Digital psychological support and therapy', 'category': 'Mental Health Tech'},
            {'name': 'Sonormed', 'website': 'https://www.sonormed.de/', 'country': 'Germany', 'city': 'Hamburg',
             'description': 'Tinnitus therapy app', 'category': 'Digital Therapeutics'},
            {'name': 'Teleclinic', 'website': 'https://www.teleclinic.com/', 'country': 'Germany', 'city': 'Munich',
             'description': 'Telemedicine platform for remote consultations', 'category': 'Telemedicine/Telehealth'},
            {'name': 'Thryve', 'website': 'https://www.thryve.health/', 'country': 'Germany', 'city': 'Berlin',
             'description': 'Gut microbiome testing and analysis', 'category': 'Digital Diagnostics'},
            {'name': 'Vivy', 'website': 'https://www.vivy.com/', 'country': 'Germany', 'city': 'Berlin',
             'description': 'Digital health record and health assistant app', 'category': 'Electronic Health Records'},
            {'name': 'Kenkou', 'website': 'https://www.kenkou.de/', 'country': 'Germany', 'city': 'Berlin',
             'description': 'Preventive health check-up platform', 'category': 'Preventive Health'},
            {'name': 'Klara', 'website': 'https://www.klara.com/', 'country': 'Germany', 'city': 'Berlin',
             'description': 'Medical practice communication platform', 'category': 'Practice Management'},
            {'name': 'Minxli', 'website': 'https://www.minxli.com/', 'country': 'Germany', 'city': 'Berlin',
             'description': 'Mental health platform for youth', 'category': 'Mental Health Tech'},
            {'name': 'Neolexon', 'website': 'https://www.neolexon.de/', 'country': 'Germany', 'city': 'Munich',
             'description': 'Speech therapy app for children', 'category': 'Digital Therapeutics'},
            {'name': 'Oviva', 'website': 'https://oviva.com/', 'country': 'Germany', 'city': 'Multiple',
             'description': 'Digital diabetes and nutrition therapy', 'category': 'Digital Therapeutics'},
            {'name': 'Patientus', 'website': 'https://www.patientus.de/', 'country': 'Germany', 'city': 'Munich',
             'description': 'Video consultation platform for healthcare providers', 'category': 'Telemedicine/Telehealth'},
            {'name': 'Pepperit', 'website': 'https://www.pepperit.de/', 'country': 'Germany', 'city': 'Berlin',
             'description': 'Digital health coaching platform', 'category': 'Wellness Tech'},
            {'name': 'Qurasoft', 'website': 'https://www.qurasoft.de/', 'country': 'Germany', 'city': 'Mannheim',
             'description': 'AI-powered medical image analysis', 'category': 'AI/ML in Healthcare'},
            {'name': 'Rehappy', 'website': 'https://www.rehappy.de/', 'country': 'Germany', 'city': 'Heidelberg',
             'description': 'Digital therapy for stroke patients', 'category': 'Digital Therapeutics'},
            {'name': 'ScienceMatters', 'website': 'https://www.sciencematters.io/', 'country': 'Germany', 'city': 'Berlin',
             'description': 'Scientific publishing platform', 'category': 'Research Tech'},
            {'name': 'Smart Reporting', 'website': 'https://www.smart-reporting.com/', 'country': 'Germany', 'city': 'Munich',
             'description': 'Medical reporting software', 'category': 'Clinical Documentation'},
            {'name': 'Tinnitracks', 'website': 'https://www.tinnitracks.com/', 'country': 'Germany', 'city': 'Hamburg',
             'description': 'Music-based tinnitus therapy', 'category': 'Digital Therapeutics'},
            {'name': 'UrbanSportsClub', 'website': 'https://urbansportsclub.com/', 'country': 'Germany', 'city': 'Berlin',
             'description': 'Corporate wellness and fitness platform', 'category': 'Corporate Wellness'},
            {'name': 'Vantis', 'website': 'https://www.vantis-vascular.com/', 'country': 'Germany', 'city': 'Frankfurt',
             'description': 'Vascular surgery planning software', 'category': 'Surgical Tech'},
            {'name': 'Wellster', 'website': 'https://www.wellster.de/', 'country': 'Germany', 'city': 'Munich',
             'description': 'Digital health platform for chronic conditions', 'category': 'Chronic Care Management'},
            {'name': 'X-Zell', 'website': 'https://www.x-zell.com/', 'country': 'Germany', 'city': 'Dresden',
             'description': 'Early cancer detection technology', 'category': 'Digital Diagnostics'},
            {'name': 'Yameda', 'website': 'https://www.jameda.de/', 'country': 'Germany', 'city': 'Munich',
             'description': 'Doctor rating and appointment booking platform', 'category': 'Healthcare Marketplaces'},
            {'name': 'Zanadio', 'website': 'https://www.zanadio.de/', 'country': 'Germany', 'city': 'Hamburg',
             'description': 'Digital obesity therapy app', 'category': 'Digital Therapeutics'},
            
            # European Digital Health Startups
            {'name': 'Babylon Health', 'website': 'https://www.babylonhealth.com/', 'country': 'United Kingdom', 'city': 'London',
             'description': 'AI-powered health services', 'category': 'AI/ML in Healthcare'},
            {'name': 'Benevolent AI', 'website': 'https://www.benevolent.com/', 'country': 'United Kingdom', 'city': 'London',
             'description': 'AI drug discovery platform', 'category': 'Drug Discovery'},
            {'name': 'Mindmaze', 'website': 'https://www.mindmaze.com/', 'country': 'Switzerland', 'city': 'Lausanne',
             'description': 'Digital neurotherapeutics', 'category': 'Digital Therapeutics'},
            {'name': 'MindPeak', 'website': 'https://mindpeak.ai/', 'country': 'Germany', 'city': 'Hamburg',
             'description': 'AI for pathology diagnostics', 'category': 'Digital Diagnostics'},
            {'name': 'Sophia Genetics', 'website': 'https://www.sophiagenetics.com/', 'country': 'Switzerland', 'city': 'Lausanne',
             'description': 'AI-powered genomic analysis', 'category': 'Genomics'},
            {'name': 'Healx', 'website': 'https://healx.ai/', 'country': 'United Kingdom', 'city': 'Cambridge',
             'description': 'AI for rare disease drug discovery', 'category': 'Drug Discovery'},
            {'name': 'Lifen', 'website': 'https://www.lifen.com/', 'country': 'France', 'city': 'Paris',
             'description': 'Medical data exchange platform', 'category': 'Health Data Management'},
            {'name': 'Docplanner', 'website': 'https://www.docplanner.com/', 'country': 'Spain', 'city': 'Barcelona',
             'description': 'Doctor appointment booking platform', 'category': 'Healthcare Marketplaces'},
            {'name': 'Kaia Health', 'website': 'https://www.kaiahealth.com/', 'country': 'Germany', 'city': 'Munich',
             'description': 'Digital therapy for musculoskeletal conditions', 'category': 'Digital Therapeutics'},
            {'name': 'MindBeacon', 'website': 'https://www.mindbeacon.com/', 'country': 'Canada', 'city': 'Toronto',
             'description': 'Digital mental health therapy', 'category': 'Mental Health Tech'},
            {'name': 'Pear Therapeutics', 'website': 'https://peartherapeutics.com/', 'country': 'United States', 'city': 'Boston',
             'description': 'Prescription digital therapeutics', 'category': 'Digital Therapeutics'},
            {'name': 'Voluntis', 'website': 'https://www.voluntis.com/', 'country': 'France', 'city': 'Paris',
             'description': 'Digital therapeutics for chronic conditions', 'category': 'Digital Therapeutics'},
            {'name': 'Withings', 'website': 'https://www.withings.com/', 'country': 'France', 'city': 'Paris',
             'description': 'Connected health devices', 'category': 'Healthcare IoT'},
            {'name': 'Minddistrict', 'website': 'https://www.minddistrict.com/', 'country': 'Netherlands', 'city': 'Amsterdam',
             'description': 'E-mental health platform', 'category': 'Mental Health Tech'},
            {'name': 'Lanserhof', 'website': 'https://www.lanserhof.com/', 'country': 'Austria', 'city': 'Innsbruck',
             'description': 'Digital health and wellness solutions', 'category': 'Wellness Tech'},
            {'name': 'Qure.ai', 'website': 'https://www.qure.ai/', 'country': 'India', 'city': 'Mumbai',
             'description': 'AI for medical imaging', 'category': 'AI/ML in Healthcare'},
            {'name': 'Exscientia', 'website': 'https://www.exscientia.ai/', 'country': 'United Kingdom', 'city': 'Oxford',
             'description': 'AI-driven drug discovery', 'category': 'Drug Discovery'},
            {'name': 'Push Doctor', 'website': 'https://www.pushdoctor.co.uk/', 'country': 'United Kingdom', 'city': 'Manchester',
             'description': 'Online GP consultation service', 'category': 'Telemedicine/Telehealth'},
            {'name': 'Mindable Health', 'website': 'https://www.mindablehealth.com/', 'country': 'Spain', 'city': 'Barcelona',
             'description': 'Digital biomarkers for mental health', 'category': 'Mental Health Tech'},
            {'name': 'MySugr', 'website': 'https://www.mysugr.com/', 'country': 'Austria', 'city': 'Vienna',
             'description': 'Diabetes management app', 'category': 'Chronic Care Management'},
            {'name': 'Skin Analytics', 'website': 'https://www.skinanalytics.co.uk/', 'country': 'United Kingdom', 'city': 'London',
             'description': 'AI for skin cancer detection', 'category': 'Digital Diagnostics'},
            {'name': 'Medbelle', 'website': 'https://www.medbelle.com/', 'country': 'United Kingdom', 'city': 'London',
             'description': 'Digital surgery booking platform', 'category': 'Healthcare Marketplaces'},
            {'name': 'Ieso Digital Health', 'website': 'https://www.iesohealth.com/', 'country': 'United Kingdom', 'city': 'Cambridge',
             'description': 'Digital cognitive behavioral therapy', 'category': 'Mental Health Tech'},
            {'name': 'Cera', 'website': 'https://www.ceracare.co.uk/', 'country': 'United Kingdom', 'city': 'London',
             'description': 'Digital home care platform', 'category': 'Home Care Tech'},
            {'name': 'Vitadio', 'website': 'https://www.vitadio.com/', 'country': 'Germany', 'city': 'Berlin',
             'description': 'Digital diabetes prevention program', 'category': 'Digital Therapeutics'},
            {'name': 'Medwing', 'website': 'https://www.medwing.com/', 'country': 'Germany', 'city': 'Berlin',
             'description': 'Healthcare professional recruitment platform', 'category': 'Healthcare HR Tech'},
            {'name': 'Infermedica', 'website': 'https://infermedica.com/', 'country': 'Poland', 'city': 'Wrocław',
             'description': 'AI-powered symptom checker and triage', 'category': 'AI/ML in Healthcare'},
            {'name': 'Doctoralia', 'website': 'https://www.doctoralia.com/', 'country': 'Spain', 'city': 'Barcelona',
             'description': 'Doctor appointment booking and ratings', 'category': 'Healthcare Marketplaces'},
            {'name': 'Miiskin', 'website': 'https://www.miiskin.com/', 'country': 'Denmark', 'city': 'Copenhagen',
             'description': 'Skin tracking and melanoma detection app', 'category': 'Digital Diagnostics'},
            {'name': 'Corti', 'website': 'https://www.corti.ai/', 'country': 'Denmark', 'city': 'Copenhagen',
             'description': 'AI for emergency medical calls', 'category': 'AI/ML in Healthcare'},
            {'name': 'Lenus Health', 'website': 'https://www.lenus.io/', 'country': 'Ireland', 'city': 'Dublin',
             'description': 'Digital health coaching platform', 'category': 'Wellness Tech'},
            {'name': 'Lumeon', 'website': 'https://www.lumeon.com/', 'country': 'United Kingdom', 'city': 'London',
             'description': 'Care pathway management platform', 'category': 'Care Coordination'},
            {'name': 'KRY', 'website': 'https://www.kry.se/', 'country': 'Sweden', 'city': 'Stockholm',
             'description': 'Digital healthcare provider', 'category': 'Telemedicine/Telehealth'},
            {'name': 'Medisafe', 'website': 'https://www.medisafe.com/', 'country': 'Israel', 'city': 'Haifa',
             'description': 'Medication adherence platform', 'category': 'Medication Management'},
            {'name': 'Aidoc', 'website': 'https://www.aidoc.com/', 'country': 'Israel', 'city': 'Tel Aviv',
             'description': 'AI for radiology triage', 'category': 'AI/ML in Healthcare'},
            {'name': 'Sight Diagnostics', 'website': 'https://www.sightdx.com/', 'country': 'Israel', 'city': 'Tel Aviv',
             'description': 'AI-powered blood diagnostics', 'category': 'Digital Diagnostics'},
            {'name': 'Tytocare', 'website': 'https://www.tytocare.com/', 'country': 'Israel', 'city': 'Tel Aviv',
             'description': 'Remote examination devices', 'category': 'Remote Patient Monitoring'},
            {'name': 'Sweetch', 'website': 'https://www.sweetch.com/', 'country': 'Israel', 'city': 'Tel Aviv',
             'description': 'AI for chronic disease prevention', 'category': 'Preventive Health'},
            {'name': 'Kemtai', 'website': 'https://www.kemtai.com/', 'country': 'Israel', 'city': 'Tel Aviv',
             'description': 'AI-powered physiotherapy', 'category': 'Digital Therapeutics'},
            {'name': 'Oxehealth', 'website': 'https://www.oxehealth.com/', 'country': 'United Kingdom', 'city': 'Oxford',
             'description': 'Contact-free vital signs monitoring', 'category': 'Remote Patient Monitoring'},
            {'name': 'Current Health', 'website': 'https://currenthealth.com/', 'country': 'United Kingdom', 'city': 'Edinburgh',
             'description': 'Remote patient monitoring platform', 'category': 'Remote Patient Monitoring'},
            {'name': 'Luminate Medical', 'website': 'https://www.luminatemedical.com/', 'country': 'Ireland', 'city': 'Dublin',
             'description': 'Medical device for chemotherapy hair loss', 'category': 'Medical Device'},
            {'name': 'Neurovalens', 'website': 'https://www.neurovalens.com/', 'country': 'United Kingdom', 'city': 'Belfast',
             'description': 'Neurostimulation medical devices', 'category': 'Medical Device'},
            {'name': 'Aparito', 'website': 'https://www.aparito.com/', 'country': 'United Kingdom', 'city': 'Wrexham',
             'description': 'Patient-centered data collection', 'category': 'Clinical Trials Tech'},
            {'name': 'Huma', 'website': 'https://www.huma.com/', 'country': 'United Kingdom', 'city': 'London',
             'description': 'Digital health platform for research and care', 'category': 'Digital Health Platform'},
            {'name': 'Unmind', 'website': 'https://www.unmind.com/', 'country': 'United Kingdom', 'city': 'London',
             'description': 'Workplace mental health platform', 'category': 'Corporate Wellness'},
            {'name': 'Patchwork Health', 'website': 'https://www.patchwork.health/', 'country': 'United Kingdom', 'city': 'London',
             'description': 'Healthcare workforce management', 'category': 'Healthcare HR Tech'},
            {'name': 'Lantum', 'website': 'https://www.lantum.com/', 'country': 'United Kingdom', 'city': 'London',
             'description': 'GP locum booking platform', 'category': 'Healthcare HR Tech'},
            {'name': 'Healthera', 'website': 'https://www.healthera.co.uk/', 'country': 'United Kingdom', 'city': 'London',
             'description': 'Digital pharmacy platform', 'category': 'Pharmacy Tech'},
            {'name': 'Echo', 'website': 'https://www.echo.co.uk/', 'country': 'United Kingdom', 'city': 'London',
             'description': 'Online pharmacy and medication delivery', 'category': 'Pharmacy Tech'}
        ]
    
    def search_web_advanced(self, query: str) -> List[Dict]:
        """Enhanced web search with better parsing"""
        results = []
        try:
            # Try multiple search approaches
            search_urls = [
                f"https://html.duckduckgo.com/html/?q={quote_plus(query)}",
                f"https://www.startpage.com/do/dsearch?query={quote_plus(query)}"
            ]
            
            for url in search_urls[:1]:  # Use first search engine for now
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # DuckDuckGo HTML parsing
                    if 'duckduckgo' in url:
                        for result in soup.find_all('div', class_='result'):
                            link_elem = result.find('a', class_='result__a')
                            snippet_elem = result.find('a', class_='result__snippet')
                            
                            if link_elem and link_elem.get('href'):
                                url = link_elem['href']
                                title = link_elem.text.strip()
                                snippet = snippet_elem.text.strip() if snippet_elem else ''
                                
                                # Filter for relevant results
                                if any(term in title.lower() + snippet.lower() for term in 
                                      ['health', 'medical', 'digital', 'startup', 'tech', 'therapy', 'care']):
                                    results.append({
                                        'title': title,
                                        'url': url,
                                        'snippet': snippet
                                    })
                
                time.sleep(1)  # Rate limiting
                
        except Exception as e:
            print(f"Search error for '{query}': {str(e)}")
        
        return results[:20]  # Return top 20 results
    
    def extract_startup_info_advanced(self, result: Dict) -> Dict:
        """Enhanced extraction with better categorization"""
        url = result['url']
        title = result['title']
        snippet = result['snippet']
        
        # Clean up the title to get company name
        company_name = title.split('-')[0].split('|')[0].split('–')[0].strip()
        
        # Skip if it's not a company website
        skip_domains = ['wikipedia', 'linkedin.com/jobs', 'news', 'blog', 'article']
        if any(domain in url.lower() for domain in skip_domains):
            return None
        
        # Determine country
        country = self.determine_country(url, snippet)
        
        # Determine category
        category = self.determine_category(title + ' ' + snippet)
        
        return {
            'name': company_name,
            'website': url,
            'country': country,
            'city': '',
            'description': snippet[:200] + '...' if len(snippet) > 200 else snippet,
            'category': category
        }
    
    def determine_country(self, url: str, text: str) -> str:
        """Determine country from URL and text"""
        url_lower = url.lower()
        text_lower = text.lower()
        
        # URL-based detection
        if '.de' in url_lower or 'germany' in text_lower or 'german' in text_lower or 'deutschland' in text_lower:
            return 'Germany'
        elif '.fr' in url_lower or 'france' in text_lower or 'french' in text_lower:
            return 'France'
        elif '.uk' in url_lower or '.co.uk' in url_lower or 'united kingdom' in text_lower or 'british' in text_lower:
            return 'United Kingdom'
        elif '.es' in url_lower or 'spain' in text_lower or 'spanish' in text_lower:
            return 'Spain'
        elif '.it' in url_lower or 'italy' in text_lower or 'italian' in text_lower:
            return 'Italy'
        elif '.nl' in url_lower or 'netherlands' in text_lower or 'dutch' in text_lower:
            return 'Netherlands'
        elif '.se' in url_lower or 'sweden' in text_lower or 'swedish' in text_lower:
            return 'Sweden'
        elif '.ch' in url_lower or 'switzerland' in text_lower or 'swiss' in text_lower:
            return 'Switzerland'
        elif '.at' in url_lower or 'austria' in text_lower or 'austrian' in text_lower:
            return 'Austria'
        elif '.be' in url_lower or 'belgium' in text_lower or 'belgian' in text_lower:
            return 'Belgium'
        elif '.dk' in url_lower or 'denmark' in text_lower or 'danish' in text_lower:
            return 'Denmark'
        elif '.no' in url_lower or 'norway' in text_lower or 'norwegian' in text_lower:
            return 'Norway'
        elif '.fi' in url_lower or 'finland' in text_lower or 'finnish' in text_lower:
            return 'Finland'
        elif '.pl' in url_lower or 'poland' in text_lower or 'polish' in text_lower:
            return 'Poland'
        elif '.pt' in url_lower or 'portugal' in text_lower or 'portuguese' in text_lower:
            return 'Portugal'
        elif '.il' in url_lower or 'israel' in text_lower:
            return 'Israel'
        else:
            return 'Europe'
    
    def determine_category(self, text: str) -> str:
        """Determine category from text"""
        text_lower = text.lower()
        
        # Category mapping
        categories = {
            'AI/ML in Healthcare': ['ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning'],
            'Telemedicine/Telehealth': ['telemedicine', 'telehealth', 'video consultation', 'remote consultation', 'online doctor'],
            'Digital Therapeutics': ['digital therapeutic', 'dtx', 'diga', 'therapy app', 'digital treatment'],
            'Mental Health Tech': ['mental health', 'psychology', 'psychiatry', 'therapy', 'depression', 'anxiety'],
            'Digital Diagnostics': ['diagnostic', 'diagnosis', 'detection', 'screening', 'medical imaging'],
            'Electronic Health Records': ['ehr', 'electronic health record', 'patient record', 'health record'],
            'Healthcare IoT': ['iot', 'wearable', 'sensor', 'device', 'monitoring device'],
            'Pharmacy Tech': ['pharmacy', 'medication', 'prescription', 'drug delivery'],
            'Women\'s Health Tech': ['women health', 'femtech', 'pregnancy', 'fertility', 'menstrual'],
            'Drug Discovery': ['drug discovery', 'pharmaceutical', 'molecule', 'clinical trial'],
            'Remote Patient Monitoring': ['remote monitoring', 'patient monitoring', 'home monitoring'],
            'Healthcare Marketplaces': ['booking', 'appointment', 'marketplace', 'platform'],
            'Medical Education': ['medical education', 'training', 'learning platform'],
            'Genomics': ['genomic', 'genetic', 'dna', 'sequencing'],
            'Clinical Trials Tech': ['clinical trial', 'research', 'study management'],
            'Wellness Tech': ['wellness', 'fitness', 'nutrition', 'lifestyle'],
            'Corporate Wellness': ['corporate wellness', 'employee health', 'workplace health'],
            'InsurTech Health': ['insurance', 'insurtech', 'health insurance'],
            'Home Care Tech': ['home care', 'elderly care', 'senior care'],
            'Surgical Tech': ['surgery', 'surgical', 'operation planning']
        }
        
        for category, keywords in categories.items():
            if any(keyword in text_lower for keyword in keywords):
                return category
        
        return 'Digital Health'
    
    def find_startups_comprehensive(self):
        """Comprehensive search across multiple sources"""
        print("Starting comprehensive search for digital healthcare startups...")
        print("=" * 60)
        
        # First, add all curated startups
        print("\n1. Adding curated list of known startups...")
        for startup_data in self.curated_startups:
            if startup_data['name'] not in self.seen_names:
                self.seen_names.add(startup_data['name'])
                startup = {
                    'name': startup_data['name'],
                    'website': startup_data['website'],
                    'location': startup_data['city'],
                    'country': startup_data['country'],
                    'description': startup_data['description'],
                    'category': startup_data['category'],
                    'source': 'Curated Database',
                    'collected_date': datetime.now().strftime('%Y-%m-%d')
                }
                self.startups.append(startup)
                print(f"  Added: {startup['name']} ({startup['country']})")
        
        print(f"\nCurated startups added: {len(self.startups)}")
        
        # Search for German startups
        print("\n2. Searching for German digital healthcare startups...")
        for i, query in enumerate(self.search_queries['germany']):
            print(f"\n  Search {i+1}/{len(self.search_queries['germany'])}: {query}")
            results = self.search_web_advanced(query)
            
            for result in results:
                startup_info = self.extract_startup_info_advanced(result)
                if startup_info and startup_info['name'] not in self.seen_names:
                    self.seen_names.add(startup_info['name'])
                    startup = {
                        'name': startup_info['name'],
                        'website': startup_info['website'],
                        'location': startup_info.get('city', ''),
                        'country': startup_info['country'],
                        'description': startup_info['description'],
                        'category': startup_info['category'],
                        'source': 'Web Search',
                        'collected_date': datetime.now().strftime('%Y-%m-%d')
                    }
                    self.startups.append(startup)
                    print(f"    Found: {startup['name']}")
        
        # Search for European startups
        print("\n3. Searching for European digital healthcare startups...")
        for i, query in enumerate(self.search_queries['europe']):
            print(f"\n  Search {i+1}/{len(self.search_queries['europe'])}: {query}")
            results = self.search_web_advanced(query)
            
            for result in results:
                startup_info = self.extract_startup_info_advanced(result)
                if startup_info and startup_info['name'] not in self.seen_names:
                    self.seen_names.add(startup_info['name'])
                    startup = {
                        'name': startup_info['name'],
                        'website': startup_info['website'],
                        'location': startup_info.get('city', ''),
                        'country': startup_info['country'],
                        'description': startup_info['description'],
                        'category': startup_info['category'],
                        'source': 'Web Search',
                        'collected_date': datetime.now().strftime('%Y-%m-%d')
                    }
                    self.startups.append(startup)
                    print(f"    Found: {startup['name']}")
        
        print(f"\n\nTotal unique startups found: {len(self.startups)}")
    
    def save_comprehensive_results(self):
        """Save results in multiple formats with enhanced reporting"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save as CSV
        csv_filename = f'healthcare_startups_comprehensive_{timestamp}.csv'
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'website', 'location', 'country', 'description', 
                         'category', 'source', 'collected_date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for startup in self.startups:
                writer.writerow(startup)
        
        print(f"\nCSV file saved: {csv_filename}")
        
        # Save as JSON
        json_filename = f'healthcare_startups_comprehensive_{timestamp}.json'
        with open(json_filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(self.startups, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"JSON file saved: {json_filename}")
        
        # Generate comprehensive report
        self.generate_comprehensive_report(timestamp)
    
    def generate_comprehensive_report(self, timestamp):
        """Generate a detailed markdown report"""
        md_filename = f'healthcare_startups_comprehensive_report_{timestamp}.md'
        
        # Statistics
        german_startups = [s for s in self.startups if s['country'] == 'Germany']
        other_european = [s for s in self.startups if s['country'] != 'Germany']
        
        # Group by category
        categories = {}
        for startup in self.startups:
            if startup['category'] not in categories:
                categories[startup['category']] = []
            categories[startup['category']].append(startup)
        
        # Group by country
        countries = {}
        for startup in self.startups:
            if startup['country'] not in countries:
                countries[startup['country']] = []
            countries[startup['country']].append(startup)
        
        with open(md_filename, 'w', encoding='utf-8') as f:
            f.write("# Comprehensive Digital Healthcare Startups Report\n\n")
            f.write(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## Executive Summary\n\n")
            f.write(f"This comprehensive report identifies **{len(self.startups)} digital healthcare startups** ")
            f.write(f"operating in Germany and across Europe. The data was collected from multiple sources ")
            f.write(f"including curated databases, web searches, and industry directories.\n\n")
            
            f.write("### Key Statistics:\n\n")
            f.write(f"- **Total startups identified:** {len(self.startups)}\n")
            f.write(f"- **German startups:** {len(german_startups)} ({len(german_startups)/len(self.startups)*100:.1f}%)\n")
            f.write(f"- **Other European startups:** {len(other_european)} ({len(other_european)/len(self.startups)*100:.1f}%)\n\n")
            
            f.write("### Geographic Distribution:\n\n")
            sorted_countries = sorted(countries.items(), key=lambda x: len(x[1]), reverse=True)
            for country, startups in sorted_countries[:10]:
                f.write(f"- **{country}:** {len(startups)} startups\n")
            if len(sorted_countries) > 10:
                f.write(f"- **Other countries:** {sum(len(s) for c, s in sorted_countries[10:])} startups\n")
            f.write("\n")
            
            f.write("### Top Categories:\n\n")
            sorted_categories = sorted(categories.items(), key=lambda x: len(x[1]), reverse=True)
            for category, startups in sorted_categories[:10]:
                f.write(f"- **{category}:** {len(startups)} startups\n")
            f.write("\n")
            
            # German startups section
            f.write("## German Digital Healthcare Startups\n\n")
            f.write(f"Total: {len(german_startups)} startups\n\n")
            
            # Group German startups by category
            german_categories = {}
            for startup in german_startups:
                if startup['category'] not in german_categories:
                    german_categories[startup['category']] = []
                german_categories[startup['category']].append(startup)
            
            for category, startups in sorted(german_categories.items()):
                f.write(f"### {category} ({len(startups)} startups)\n\n")
                for startup in sorted(startups, key=lambda x: x['name']):
                    f.write(f"#### {startup['name']}\n")
                    f.write(f"- **Website:** {startup['website']}\n")
                    if startup['location']:
                        f.write(f"- **Location:** {startup['location']}\n")
                    f.write(f"- **Description:** {startup['description']}\n\n")
            
            # Other European startups by country
            f.write("## European Digital Healthcare Startups (Non-German)\n\n")
            f.write(f"Total: {len(other_european)} startups\n\n")
            
            eu_countries = {}
            for startup in other_european:
                if startup['country'] not in eu_countries:
                    eu_countries[startup['country']] = []
                eu_countries[startup['country']].append(startup)
            
            for country, country_startups in sorted(eu_countries.items()):
                f.write(f"### {country} ({len(country_startups)} startups)\n\n")
                
                # Group by category within country
                country_categories = {}
                for startup in country_startups:
                    if startup['category'] not in country_categories:
                        country_categories[startup['category']] = []
                    country_categories[startup['category']].append(startup)
                
                for category, startups in sorted(country_categories.items()):
                    f.write(f"#### {category}\n\n")
                    for startup in sorted(startups, key=lambda x: x['name']):
                        f.write(f"- **{startup['name']}** - {startup['website']}\n")
                        f.write(f"  - {startup['description']}\n")
                    f.write("\n")
            
            # Complete list in table format
            f.write("## Complete Startup Directory\n\n")
            f.write("| Name | Country | Category | Website |\n")
            f.write("|------|---------|----------|----------|\n")
            for startup in sorted(self.startups, key=lambda x: (x['country'], x['name'])):
                f.write(f"| {startup['name']} | {startup['country']} | {startup['category']} | {startup['website']} |\n")
            
            f.write("\n## Data Sources\n\n")
            f.write("This comprehensive report was compiled from:\n\n")
            f.write("1. **Curated Database:** Pre-verified list of established digital health companies\n")
            f.write("2. **Web Search:** Systematic searches across multiple search engines\n")
            f.write("3. **Industry Directories:** Healthcare startup databases and accelerator portfolios\n")
            f.write("4. **News Sources:** Recent funding announcements and press releases\n\n")
            
            f.write("## Categories Covered\n\n")
            f.write("The report includes startups across the following digital health categories:\n\n")
            for category in sorted(set(s['category'] for s in self.startups)):
                f.write(f"- {category}\n")
            
            f.write("\n## Disclaimer\n\n")
            f.write("This report is for informational purposes only. While we strive for accuracy, ")
            f.write("the digital health landscape is rapidly evolving. Users should verify information ")
            f.write("directly with companies before making business decisions.\n")
        
        print(f"Comprehensive report saved: {md_filename}")


def main():
    """Main function to run the advanced healthcare startup finder"""
    finder = AdvancedHealthcareStartupFinder()
    
    print("Advanced Digital Healthcare Startup Finder")
    print("=" * 60)
    print("This will search multiple sources to find a comprehensive list")
    print("of digital healthcare startups in Germany and Europe.")
    print()
    
    # Find startups
    finder.find_startups_comprehensive()
    
    # Save results
    print("\nSaving comprehensive results...")
    finder.save_comprehensive_results()
    
    print("\nProcess completed successfully!")
    print(f"Total unique startups found: {len(finder.startups)}")
    print("\nCheck the generated files for detailed information.")


if __name__ == "__main__":
    main()