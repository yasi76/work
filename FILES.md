# Healthcare Startup Discovery System - File Structure

This document provides an overview of all files in the Healthcare Startup Discovery System.

## 📁 Core Files

### Main Application
- **`healthcare_startup_discovery.py`** - Main discovery system with async scraping, NLP filtering, and comprehensive error handling
- **`advanced_scraper.py`** - Advanced scraping with Selenium and Playwright for JavaScript-heavy sites
- **`config.py`** - Centralized configuration management for all settings and parameters

### Setup and Testing
- **`setup.py`** - Automated installation and setup script
- **`test_discovery.py`** - Comprehensive test suite for all components
- **`requirements.txt`** - Python dependencies with specific versions

### Documentation
- **`README.md`** - Comprehensive documentation with installation, usage, and troubleshooting
- **`FILES.md`** - This file - overview of all components

## 🏗️ Architecture Overview

### Core Components

1. **HealthcareStartupDiscovery** (`healthcare_startup_discovery.py`)
   - Main orchestrator class
   - Manages the entire discovery process
   - Handles data collection, filtering, and output

2. **HealthcareKeywordFilter** (`healthcare_startup_discovery.py`)
   - NLP-based healthcare detection
   - TF-IDF vectorization and cosine similarity
   - Multi-category keyword filtering

3. **URLValidator** (`healthcare_startup_discovery.py`)
   - URL cleaning and validation
   - Social media and file extension filtering
   - Duplicate detection

4. **AsyncWebScraper** (`healthcare_startup_discovery.py`)
   - Asynchronous HTTP requests with aiohttp
   - Retry logic and rate limiting
   - Connection pooling and timeout handling

5. **AdvancedHealthcareScraper** (`advanced_scraper.py`)
   - Selenium and Playwright integration
   - JavaScript-heavy site handling
   - Browser automation for complex sites

### Configuration System (`config.py`)

- **ScrapingConfig** - Web scraping parameters
- **NLPConfig** - Natural language processing settings
- **OutputConfig** - File output and logging settings
- **HealthcareKeywords** - Healthcare-related keywords for filtering
- **DiscoverySources** - URLs of websites to scrape
- **APIConfig** - API integration settings
- **BrowserConfig** - Browser automation settings
- **ValidationConfig** - URL and data validation settings
- **CountryDetection** - Geographic detection settings

## 🔧 Key Features by File

### `healthcare_startup_discovery.py`
- ✅ Asynchronous web scraping with aiohttp
- ✅ NLP-based healthcare keyword filtering
- ✅ URL validation and cleaning
- ✅ Deduplication and similarity detection
- ✅ CSV/JSON output generation
- ✅ Comprehensive error handling and retry logic
- ✅ Rate limiting and respectful scraping
- ✅ Geographic country detection
- ✅ Progress tracking and logging

### `advanced_scraper.py`
- ✅ Selenium WebDriver integration
- ✅ Playwright browser automation
- ✅ JavaScript-heavy site handling
- ✅ Dynamic content extraction
- ✅ Browser session management
- ✅ Fallback mechanisms between scrapers
- ✅ Site-specific extraction patterns

### `config.py`
- ✅ Centralized configuration management
- ✅ Healthcare keyword categories
- ✅ Discovery source URLs
- ✅ Scraping parameters
- ✅ NLP settings
- ✅ Browser automation settings
- ✅ Validation rules
- ✅ Geographic detection rules

### `setup.py`
- ✅ Automated installation process
- ✅ Virtual environment creation
- ✅ Dependency installation
- ✅ Browser dependency setup
- ✅ NLTK data download
- ✅ Test suite execution
- ✅ Cross-platform support (Windows/Linux/macOS)

### `test_discovery.py`
- ✅ Configuration testing
- ✅ URL validation testing
- ✅ NLP filtering accuracy testing
- ✅ Advanced scraper testing
- ✅ Basic discovery testing
- ✅ Comprehensive test suite
- ✅ Accuracy metrics

## 📊 Data Flow

```
Input Sources → Async Scraping → NLP Filtering → Validation → Deduplication → Output
     ↓              ↓                ↓              ↓            ↓           ↓
  Websites      aiohttp/        TF-IDF +      URL Cleaning   Similarity   CSV/JSON
  Directories   Selenium/       Cosine        & Validation   Detection    Files
  APIs          Playwright      Similarity
```

## 🎯 Discovery Sources

### Website Categories (from `config.py`)

1. **German Healthcare Sites** (10 sites)
   - Digital Health Summit
   - Healthcare Startups Germany
   - Telemedicine Germany
   - Healthcare Innovation
   - E-Health Europe

2. **European Directories** (5 sites)
   - E-Health Europe
   - Digital Health Europe
   - HealthTech Europe
   - European Healthcare
   - Healthcare Europe

3. **International Directories** (5 sites)
   - Crunchbase
   - AngelList
   - StartupBlink
   - PitchBook
   - LinkedIn

4. **Healthcare News Sites** (5 sites)
   - Healthcare IT News
   - MobiHealthNews
   - Digital Health Network
   - Healthcare Europe
   - Healthcare Digital

5. **German Startup Ecosystem** (5 sites)
   - Startup Detector
   - Deutsche Startups
   - Gründerszene
   - Startup Valley News
   - Startup Radar

## 🧠 NLP Categories

### Healthcare Keywords (from `config.py`)

1. **Digital Health** (16 keywords)
   - telemedicine, telehealth, digital health, healthtech
   - mhealth, mobile health, ehealth, healthcare technology

2. **Medical Devices** (12 keywords)
   - medical device, medical technology, medtech, biomedical
   - diagnostic, monitoring, sensor, wearable, implant

3. **Healthcare Services** (10 keywords)
   - healthcare service, medical service, patient care, clinical
   - healthcare provider, healthcare management

4. **Pharmaceutical** (11 keywords)
   - pharmaceutical, pharma, drug discovery, biotech
   - clinical trial, drug development, therapeutics

5. **Mental Health** (10 keywords)
   - mental health, psychology, psychiatry, therapy
   - counseling, wellness, mindfulness

6. **AI Healthcare** (8 keywords)
   - ai healthcare, artificial intelligence healthcare
   - machine learning healthcare, predictive analytics

## 🛠️ Installation Process

### Automated Setup (`setup.py`)
1. ✅ Python version check (3.8+)
2. ✅ Virtual environment creation
3. ✅ Dependency installation (requirements.txt)
4. ✅ Browser dependency setup (Playwright/Selenium)
5. ✅ NLTK data download
6. ✅ Output directory creation
7. ✅ Test suite execution
8. ✅ Activation script creation

### Manual Setup
1. Create virtual environment
2. Install requirements: `pip install -r requirements.txt`
3. Install Playwright: `playwright install`
4. Download NLTK data
5. Run tests: `python test_discovery.py`

## 📈 Performance Features

### Scalability
- Asynchronous processing with asyncio
- Configurable concurrency limits
- Connection pooling
- Memory-efficient processing

### Reliability
- Exponential backoff retry logic
- Rate limiting and respectful scraping
- Comprehensive error handling
- Graceful degradation

### Monitoring
- Progress tracking with tqdm
- Detailed logging with loguru
- Performance metrics
- Error rate monitoring

## 🔍 Output Formats

### CSV Output
- Company name, URL, description
- Source website, country, confidence score
- Timestamp of discovery

### JSON Output
- Structured data format
- All company information
- Metadata and timestamps

### Log Files
- `output/discovery.log` - Main application logs
- `output/debug.log` - Debug information (when enabled)

## 🎯 Usage Examples

### Basic Usage
```python
from healthcare_startup_discovery import HealthcareStartupDiscovery

async def main():
    discovery = HealthcareStartupDiscovery()
    filename = await discovery.run_discovery(save_format="csv")
    print(f"Results saved to: {filename}")

asyncio.run(main())
```

### Advanced Usage
```python
from advanced_scraper import AdvancedHealthcareScraper

async def custom_scraping():
    scraper = AdvancedHealthcareScraper()
    result = await scraper.scrape_healthcare_site("https://example.com")
    companies = scraper.extract_companies_from_result(result)
    return companies
```

### Configuration
```python
from config import NLP_CONFIG, DISCOVERY_SOURCES

# Adjust NLP parameters
NLP_CONFIG.confidence_threshold = 0.4

# Add new sources
DISCOVERY_SOURCES.GERMAN_HEALTHCARE_SITES.append("https://new-site.com")
```

## 🚀 Quick Start Commands

```bash
# Automated setup
python setup.py

# Activate environment (Linux/macOS)
source activate.sh

# Activate environment (Windows)
activate.bat

# Run discovery
python healthcare_startup_discovery.py

# Run tests
python test_discovery.py
```

## 📝 File Dependencies

```
healthcare_startup_discovery.py
├── config.py
├── requirements.txt
└── output/ (created automatically)

advanced_scraper.py
├── healthcare_startup_discovery.py
└── config.py

test_discovery.py
├── healthcare_startup_discovery.py
├── advanced_scraper.py
└── config.py

setup.py
├── requirements.txt
├── test_discovery.py
└── healthcare_startup_discovery.py
```

## 🎉 System Capabilities

### Discovery Capabilities
- ✅ 30+ healthcare websites and directories
- ✅ German and European focus
- ✅ JavaScript-heavy site support
- ✅ API integration ready
- ✅ Scalable async processing

### Filtering Capabilities
- ✅ 67+ healthcare keywords across 6 categories
- ✅ NLP-based similarity detection
- ✅ Confidence scoring system
- ✅ Geographic filtering
- ✅ Duplicate removal

### Output Capabilities
- ✅ CSV and JSON formats
- ✅ Structured company data
- ✅ Confidence scores and metadata
- ✅ Geographic information
- ✅ Source attribution

This comprehensive system provides a robust, scalable solution for discovering healthcare startups across Germany and Europe with high precision and extensive coverage.