#!/usr/bin/env python3
"""
Digital Healthcare Startup Finder - Simplified Version
Finds and collects information about digital healthcare startups and SMEs in Germany and Europe
"""

import json
import csv
from datetime import datetime
from typing import List, Dict


class HealthcareStartupFinderSimple:
    """Simple version for finding digital healthcare startups"""
    
    def __init__(self):
        self.startups = []
        
        # Predefined list of known startups from search results
        self.known_startups = [
            # German startups
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
            {
                'name': 'Floy',
                'website': 'https://www.floy.com/',
                'country': 'Germany',
                'location': 'Berlin',
                'description': 'AI-powered radiology diagnostics and holistic health insights',
                'category': 'Digital Diagnostics'
            },
            {
                'name': 'UniteLabs',
                'website': 'https://www.unitelabs.io/',
                'country': 'Germany',
                'location': 'Munich',
                'description': 'Operating system for AI-driven biotech research',
                'category': 'Research Solutions'
            },
            {
                'name': 'Neoplas med',
                'website': 'https://www.neoplas-med.de/',
                'country': 'Germany',
                'location': 'Greifswald',
                'description': 'High-precision medical technology for physical cold plasma application',
                'category': 'Medical Device'
            },
            {
                'name': 'Omeicos Therapeutics',
                'website': 'https://www.omeicos.com/',
                'country': 'Germany',
                'location': 'Berlin',
                'description': 'Small molecules based on Omega-3 fatty acid metabolites',
                'category': 'Biopharmaceutical'
            },
            {
                'name': 'Hema.to',
                'website': 'https://hema.to/',
                'country': 'Germany',
                'location': 'Munich',
                'description': 'AI-powered blood cancer detection platform',
                'category': 'Digital Diagnostics'
            },
            {
                'name': 'Nuuron',
                'website': 'https://www.nuuron.com/',
                'country': 'Germany',
                'location': 'Berlin',
                'description': 'Digital Alzheimer\'s therapy based on neuromodulation technology',
                'category': 'Mental Health Tech'
            },
            {
                'name': 'Differential Bio',
                'website': 'https://www.differential.bio/',
                'country': 'Germany',
                'location': 'Munich',
                'description': 'AI-powered virtual scaleup platform to optimize biomanufacturing',
                'category': 'AI/ML in Healthcare'
            },
            {
                'name': 'Lucid Genomics',
                'website': 'https://lucid-genomics.com/',
                'country': 'Germany',
                'location': 'Berlin',
                'description': 'AI-driven genetic data and insights for faster drug discovery',
                'category': 'Drug Discovery'
            },
            {
                'name': 'mo:re',
                'website': 'https://more.science/',
                'country': 'Germany',
                'location': 'Hamburg',
                'description': 'Laboratory platform automating 3D cell culture models',
                'category': 'Research Solutions'
            },
            # European startups (non-German)
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
            },
            {
                'name': 'Biloba',
                'website': 'https://www.biloba.com/',
                'country': 'France',
                'location': 'Paris',
                'description': 'Digital health solutions for patient engagement',
                'category': 'Patient Engagement'
            },
            {
                'name': 'Yazen',
                'website': 'https://www.yazen.se/',
                'country': 'Sweden',
                'location': 'Stockholm',
                'description': 'Digital weight loss clinic with medical support',
                'category': 'Telemedicine/Telehealth'
            },
            {
                'name': 'Cure51',
                'website': 'https://cure51.com/',
                'country': 'France',
                'location': 'Paris',
                'description': 'Bioinformatics platform using computational modeling for oncology therapies',
                'category': 'Drug Discovery'
            },
            {
                'name': 'Sycai Medical',
                'website': 'https://sycai.com/',
                'country': 'Spain',
                'location': 'Barcelona',
                'description': 'AI-powered medical imaging for pancreatic cancer detection',
                'category': 'Digital Diagnostics'
            },
            {
                'name': 'Eucalyptus',
                'website': 'https://www.eucalyptus.vc/',
                'country': 'Netherlands',
                'location': 'Amsterdam',
                'description': 'Digital healthcare company builder',
                'category': 'Digital Health'
            },
            {
                'name': 'Ovo Labs',
                'website': 'https://www.ovo-labs.com/',
                'country': 'Austria',
                'location': 'Vienna',
                'description': 'Therapies for IVF treatments to boost egg quality',
                'category': 'Fertility Tech'
            },
            {
                'name': 'Hello Inside',
                'website': 'https://www.helloinside.com/',
                'country': 'Austria',
                'location': 'Vienna',
                'description': 'Continuous glucose monitoring for metabolic health',
                'category': 'Women\'s Health Tech'
            }
        ]
    
    def collect_startups(self):
        """Collect all startups and add metadata"""
        print("Collecting digital healthcare startups...")
        print("=" * 50)
        
        for startup_data in self.known_startups:
            startup = {
                'name': startup_data['name'],
                'website': startup_data['website'],
                'location': startup_data['location'],
                'country': startup_data['country'],
                'description': startup_data['description'],
                'category': startup_data['category'],
                'source': 'Curated List',
                'collected_date': datetime.now().strftime('%Y-%m-%d')
            }
            self.startups.append(startup)
            print(f"  Added: {startup['name']} ({startup['country']})")
        
        print(f"\nTotal startups collected: {len(self.startups)}")
    
    def save_results(self):
        """Save results in multiple formats"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save as CSV
        csv_filename = f'healthcare_startups_{timestamp}.csv'
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'website', 'location', 'country', 'description', 
                         'category', 'source', 'collected_date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for startup in self.startups:
                writer.writerow(startup)
        
        print(f"\nCSV file saved: {csv_filename}")
        
        # Save as JSON
        json_filename = f'healthcare_startups_{timestamp}.json'
        with open(json_filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(self.startups, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"JSON file saved: {json_filename}")
        
        # Save as Markdown report
        md_filename = self.save_markdown_report(timestamp)
        
        return csv_filename, json_filename, md_filename
    
    def save_markdown_report(self, timestamp):
        """Generate a comprehensive markdown report"""
        md_filename = f'healthcare_startups_report_{timestamp}.md'
        
        # Group startups by country
        german_startups = [s for s in self.startups if s['country'] == 'Germany']
        other_european = [s for s in self.startups if s['country'] != 'Germany']
        
        # Group by category
        categories = {}
        for startup in self.startups:
            if startup['category'] not in categories:
                categories[startup['category']] = []
            categories[startup['category']].append(startup)
        
        # Count by country
        countries = {}
        for startup in self.startups:
            countries[startup['country']] = countries.get(startup['country'], 0) + 1
        
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
            f.write("in Germany and Europe. The data includes leading companies in various sectors ")
            f.write("including telemedicine, AI/ML in healthcare, digital diagnostics, and more.\n\n")
            
            f.write("### Key Findings:\n\n")
            f.write(f"- **Total startups identified:** {len(self.startups)}\n")
            f.write(f"- **German startups:** {len(german_startups)} ({len(german_startups)/len(self.startups)*100:.1f}%)\n")
            f.write(f"- **Other European startups:** {len(other_european)} ({len(other_european)/len(self.startups)*100:.1f}%)\n\n")
            
            f.write("### Geographic Distribution:\n\n")
            for country, count in sorted(countries.items(), key=lambda x: x[1], reverse=True):
                f.write(f"- **{country}:** {count} startups\n")
            f.write("\n")
            
            f.write("### Top Categories:\n\n")
            sorted_categories = sorted(categories.items(), key=lambda x: len(x[1]), reverse=True)
            for category, startups in sorted_categories[:5]:
                f.write(f"- **{category}:** {len(startups)} startups\n")
            f.write("\n")
            
            # German startups section
            f.write("## German Digital Healthcare Startups\n\n")
            f.write(f"Total: {len(german_startups)} startups\n\n")
            
            for startup in sorted(german_startups, key=lambda x: x['name']):
                f.write(f"### {startup['name']}\n")
                f.write(f"- **Website:** {startup['website']}\n")
                f.write(f"- **Location:** {startup['location'] if startup['location'] else 'Germany'}\n")
                f.write(f"- **Category:** {startup['category']}\n")
                f.write(f"- **Description:** {startup['description']}\n\n")
            
            # Other European startups section
            f.write("## European Digital Healthcare Startups\n\n")
            f.write(f"Total: {len(other_european)} startups\n\n")
            
            # Group by country
            eu_countries = {}
            for startup in other_european:
                if startup['country'] not in eu_countries:
                    eu_countries[startup['country']] = []
                eu_countries[startup['country']].append(startup)
            
            for country, country_startups in sorted(eu_countries.items()):
                f.write(f"### {country} ({len(country_startups)} startups)\n\n")
                for startup in sorted(country_startups, key=lambda x: x['name']):
                    f.write(f"#### {startup['name']}\n")
                    f.write(f"- **Website:** {startup['website']}\n")
                    f.write(f"- **Location:** {startup['location'] if startup['location'] else country}\n")
                    f.write(f"- **Category:** {startup['category']}\n")
                    f.write(f"- **Description:** {startup['description']}\n\n")
            
            # Startups by category
            f.write("## Startups by Category\n\n")
            for category, startups in sorted_categories:
                f.write(f"### {category} ({len(startups)} startups)\n\n")
                for startup in sorted(startups, key=lambda x: x['name']):
                    f.write(f"- **{startup['name']}** ({startup['country']}): {startup['website']}\n")
                f.write("\n")
            
            # Complete list
            f.write("## Complete Startup List\n\n")
            f.write("| Name | Country | Category | Website |\n")
            f.write("|------|---------|----------|----------|\n")
            for startup in sorted(self.startups, key=lambda x: (x['country'], x['name'])):
                f.write(f"| {startup['name']} | {startup['country']} | {startup['category']} | {startup['website']} |\n")
            
            f.write("\n## About This Report\n\n")
            f.write("This report contains curated information about digital healthcare startups ")
            f.write("and SMEs operating in Germany and Europe. The companies listed represent ")
            f.write("various sectors within digital health including:\n\n")
            f.write("- Digital Therapeutics (DiGA)\n")
            f.write("- Telemedicine and Telehealth\n")
            f.write("- AI/ML in Healthcare\n")
            f.write("- Digital Diagnostics\n")
            f.write("- Electronic Health Records\n")
            f.write("- Remote Patient Monitoring\n")
            f.write("- Mental Health Technology\n")
            f.write("- Healthcare IoT\n")
            f.write("- And more...\n\n")
            
            f.write("## Disclaimer\n\n")
            f.write("This report is for informational purposes only. The information was collected ")
            f.write("from publicly available sources and may not be complete or fully up-to-date. ")
            f.write("Users should verify information directly with the companies before making ")
            f.write("any business decisions.\n")
        
        print(f"Markdown report saved: {md_filename}")
        return md_filename


def main():
    """Main function to run the healthcare startup finder"""
    finder = HealthcareStartupFinderSimple()
    
    print("Digital Healthcare Startup Finder - Simplified Version")
    print("=" * 50)
    print("Finding digital healthcare startups in Germany and Europe...")
    print()
    
    # Collect startups
    finder.collect_startups()
    
    # Save results
    print("\nSaving results...")
    csv_file, json_file, md_file = finder.save_results()
    
    print("\nProcess completed successfully!")
    print("Generated files:")
    print(f"  - CSV: {csv_file}")
    print(f"  - JSON: {json_file}")
    print(f"  - Markdown Report: {md_file}")
    print("\nCheck the generated files for detailed information.")


if __name__ == "__main__":
    main()