#!/usr/bin/env python3
"""
Test Script for Healthcare Startup Discovery System
==================================================

A simple test script to demonstrate the system's capabilities.
"""

import asyncio
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from healthcare_startup_discovery import HealthcareStartupDiscovery
from advanced_scraper import AdvancedHealthcareScraper
from config import HEALTHCARE_KEYWORDS, DISCOVERY_SOURCES

async def test_basic_discovery():
    """Test the basic discovery functionality."""
    print("🧪 Testing Basic Discovery System")
    print("=" * 50)
    
    discovery = HealthcareStartupDiscovery()
    
    try:
        # Run discovery with limited sources for testing
        print("Starting discovery process...")
        filename = await discovery.run_discovery(save_format="csv")
        
        print(f"✅ Discovery completed successfully!")
        print(f"📁 Results saved to: {filename}")
        
        # Read and display results
        if Path(filename).exists():
            import pandas as pd
            df = pd.read_csv(filename)
            print(f"\n📊 Discovery Results:")
            print(f"Total companies found: {len(df)}")
            print(f"Countries represented: {df['Country'].value_counts().to_dict()}")
            
            # Show top 5 results
            print(f"\n🏆 Top 5 Companies by Confidence:")
            top_5 = df.nlargest(5, 'Confidence Score')
            for _, row in top_5.iterrows():
                print(f"  • {row['Name']} ({row['Country']}) - Score: {row['Confidence Score']:.3f}")
        
    except Exception as e:
        print(f"❌ Discovery failed: {e}")
        return False
    
    return True

async def test_advanced_scraper():
    """Test the advanced scraper with JavaScript support."""
    print("\n🧪 Testing Advanced Scraper")
    print("=" * 50)
    
    scraper = AdvancedHealthcareScraper()
    
    # Test with a simple healthcare site
    test_url = "https://www.digital-health-summit.de/"
    
    try:
        print(f"Testing scraper with: {test_url}")
        result = await scraper.scrape_healthcare_site(test_url)
        
        if result:
            print(f"✅ Successfully scraped: {result.title}")
            print(f"📊 Found {len(result.links)} links")
            print(f"📄 Content length: {len(result.content)} characters")
            
            # Extract companies
            companies = scraper.extract_companies_from_result(result)
            print(f"🏢 Extracted {len(companies)} potential companies")
            
            # Show first few companies
            for i, company in enumerate(companies[:3], 1):
                print(f"  {i}. {company['name']}: {company['url']}")
        
        else:
            print("❌ Failed to scrape test URL")
            return False
            
    except Exception as e:
        print(f"❌ Advanced scraper test failed: {e}")
        return False
    
    return True

def test_nlp_filtering():
    """Test the NLP filtering functionality."""
    print("\n🧪 Testing NLP Filtering")
    print("=" * 50)
    
    from healthcare_startup_discovery import HealthcareKeywordFilter
    
    filter_obj = HealthcareKeywordFilter()
    
    # Test cases
    test_cases = [
        ("Telemedicine Solutions - Digital Health Platform", True),
        ("AI-powered diagnostic tools for healthcare", True),
        ("Restaurant and Food Delivery Service", False),
        ("Mobile health monitoring and patient care", True),
        ("E-commerce platform for electronics", False),
        ("Mental health therapy and counseling services", True),
        ("Biotech drug discovery and development", True),
        ("Online shopping and retail platform", False)
    ]
    
    print("Testing healthcare keyword filtering:")
    correct = 0
    total = len(test_cases)
    
    for text, expected in test_cases:
        is_healthcare, confidence = filter_obj.is_healthcare_related(text)
        result = "✅" if is_healthcare == expected else "❌"
        print(f"  {result} '{text[:50]}...' - Score: {confidence:.3f}")
        
        if is_healthcare == expected:
            correct += 1
    
    accuracy = correct / total * 100
    print(f"\n📊 NLP Filtering Accuracy: {accuracy:.1f}% ({correct}/{total})")
    
    return accuracy >= 80  # Expect at least 80% accuracy

def test_url_validation():
    """Test URL validation functionality."""
    print("\n🧪 Testing URL Validation")
    print("=" * 50)
    
    from healthcare_startup_discovery import URLValidator
    
    validator = URLValidator()
    
    # Test cases
    test_urls = [
        ("https://www.healthcare-startup.com", True),
        ("https://facebook.com/company", False),  # Social media
        ("https://example.com/document.pdf", False),  # PDF file
        ("https://telemedicine-solutions.de", True),
        ("https://twitter.com/healthcare", False),  # Social media
        ("https://healthtech-germany.com", True),
        ("ftp://invalid-protocol.com", False),  # Invalid protocol
        ("https://digital-health.eu", True)
    ]
    
    print("Testing URL validation:")
    correct = 0
    total = len(test_urls)
    
    for url, expected in test_urls:
        is_valid = validator.is_valid_url(url)
        result = "✅" if is_valid == expected else "❌"
        print(f"  {result} {url} - Expected: {expected}, Got: {is_valid}")
        
        if is_valid == expected:
            correct += 1
    
    accuracy = correct / total * 100
    print(f"\n📊 URL Validation Accuracy: {accuracy:.1f}% ({correct}/{total})")
    
    return accuracy >= 90  # Expect at least 90% accuracy

def test_configuration():
    """Test configuration loading."""
    print("\n🧪 Testing Configuration")
    print("=" * 50)
    
    from config import get_config, HEALTHCARE_KEYWORDS, DISCOVERY_SOURCES
    
    try:
        config = get_config()
        
        print("✅ Configuration loaded successfully")
        print(f"📊 Configuration sections: {list(config.keys())}")
        
        # Test healthcare keywords
        print(f"🏥 Healthcare keyword categories: {len(HEALTHCARE_KEYWORDS.digital_health)} digital health keywords")
        print(f"🔬 Medical device keywords: {len(HEALTHCARE_KEYWORDS.medical_devices)}")
        
        # Test discovery sources
        print(f"🌍 German healthcare sites: {len(DISCOVERY_SOURCES.GERMAN_HEALTHCARE_SITES)}")
        print(f"🇪🇺 European directories: {len(DISCOVERY_SOURCES.EUROPEAN_DIRECTORIES)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

async def run_all_tests():
    """Run all tests."""
    print("🚀 Healthcare Startup Discovery System - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Configuration", test_configuration),
        ("URL Validation", test_url_validation),
        ("NLP Filtering", test_nlp_filtering),
        ("Advanced Scraper", test_advanced_scraper),
        ("Basic Discovery", test_basic_discovery)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            
            results.append((test_name, result))
            
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to use.")
    else:
        print("⚠️  Some tests failed. Please check the configuration and dependencies.")
    
    return passed == total

if __name__ == "__main__":
    # Run the test suite
    success = asyncio.run(run_all_tests())
    
    if success:
        print("\n🚀 Ready to discover healthcare startups!")
        print("Run: python healthcare_startup_discovery.py")
    else:
        print("\n🔧 Please fix the failing tests before proceeding.")
        sys.exit(1)