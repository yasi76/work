# Healthcare Startup Discovery System

A comprehensive, scalable Python solution for discovering URLs of digital healthcare startups and SMEs across Germany and Europe using asynchronous web scraping, NLP filtering, and multiple data sources.

## 🚀 Features

### Core Capabilities
- **Asynchronous Web Scraping**: High-performance scraping using `aiohttp` and `asyncio`
- **NLP-Based Filtering**: Intelligent healthcare keyword detection using TF-IDF and cosine similarity
- **Multi-Source Discovery**: Scrapes websites, directories, and APIs
- **JavaScript Support**: Handles dynamic content with Selenium and Playwright
- **Geographic Focus**: Prioritizes German and European companies
- **Data Validation**: Cleans and validates URLs, removes duplicates and social media
- **Flexible Output**: Exports to CSV or JSON format

### Advanced Features
- **Retry Logic**: Robust error handling with exponential backoff
- **Rate Limiting**: Respectful scraping with configurable delays
- **Modular Architecture**: Clean, well-structured, and extensible code
- **Comprehensive Logging**: Detailed logging with rotation and retention
- **Configuration Management**: Centralized settings for easy customization

## 📋 Requirements

### System Requirements
- Python 3.8+
- Chrome/Chromium browser (for Selenium)
- 4GB+ RAM recommended
- Stable internet connection

### Python Dependencies
All dependencies are listed in `requirements.txt`:

```bash
aiohttp==3.9.1
asyncio==3.4.3
selenium==4.15.2
playwright==1.40.0
beautifulsoup4==4.12.2
pandas==2.1.3
numpy==1.25.2
scikit-learn==1.3.2
nltk==3.8.1
spacy==3.7.2
requests==2.31.0
lxml==4.9.3
aiofiles==23.2.1
fake-useragent==1.4.0
python-dotenv==1.0.0
tqdm==4.66.1
loguru==0.7.2
urllib3==2.1.0
certifi==2023.11.17
```

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd healthcare-startup-discovery
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Browser Dependencies
```bash
# Install Playwright browsers
playwright install

# For Selenium (Chrome should be installed on your system)
# On Ubuntu/Debian:
# sudo apt-get install chromium-browser
# On macOS:
# brew install --cask google-chrome
```

### 5. Download NLTK Data
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

## 🚀 Quick Start

### Basic Usage
```python
from healthcare_startup_discovery import HealthcareStartupDiscovery

async def main():
    discovery = HealthcareStartupDiscovery()
    filename = await discovery.run_discovery(save_format="csv")
    print(f"Results saved to: {filename}")

# Run the discovery
import asyncio
asyncio.run(main())
```

### Command Line Usage
```bash
python healthcare_startup_discovery.py
```

## 📊 Output Format

### CSV Output
```csv
Name,URL,Description,Source,Country,Confidence Score,Timestamp
Telemedicine Solutions,https://example.com,Digital health platform,https://source.com,Germany,0.85,2024-01-15T10:30:00
HealthTech Startup,https://startup.com,AI-powered diagnostics,https://source.com,France,0.72,2024-01-15T10:30:00
```

### JSON Output
```json
[
  {
    "name": "Telemedicine Solutions",
    "url": "https://example.com",
    "description": "Digital health platform",
    "source": "https://source.com",
    "country": "Germany",
    "confidence_score": 0.85,
    "timestamp": "2024-01-15T10:30:00"
  }
]
```

## 🔧 Configuration

### Main Configuration File (`config.py`)

The system uses a centralized configuration system with the following components:

- **ScrapingConfig**: Web scraping parameters
- **NLPConfig**: Natural language processing settings
- **OutputConfig**: File output and logging settings
- **HealthcareKeywords**: Healthcare-related keywords for filtering
- **DiscoverySources**: URLs of websites to scrape
- **APIConfig**: API integration settings
- **BrowserConfig**: Browser automation settings

### Customizing Sources

Edit `config.py` to add or modify discovery sources:

```python
# Add new healthcare websites
GERMAN_HEALTHCARE_SITES = [
    "https://www.digital-health-summit.de/",
    "https://your-new-site.com/",
    # ... more sites
]
```

### Adjusting NLP Parameters

```python
# Modify confidence threshold
NLP_CONFIG.confidence_threshold = 0.4

# Adjust keyword weights
NLP_CONFIG.keyword_density_weight = 0.7
NLP_CONFIG.similarity_weight = 0.3
```

## 🏗️ Architecture

### Core Components

1. **HealthcareStartupDiscovery**: Main orchestrator class
2. **HealthcareKeywordFilter**: NLP-based healthcare detection
3. **URLValidator**: URL cleaning and validation
4. **AsyncWebScraper**: Asynchronous web scraping
5. **AdvancedHealthcareScraper**: JavaScript-heavy site handling

### Data Flow

```
Input Sources → Async Scraping → NLP Filtering → Validation → Deduplication → Output
     ↓              ↓                ↓              ↓            ↓           ↓
  Websites      aiohttp/        TF-IDF +      URL Cleaning   Similarity   CSV/JSON
  Directories   Selenium/       Cosine        & Validation   Detection    Files
  APIs          Playwright      Similarity
```

## 🔍 Discovery Sources

### Website Categories

1. **German Healthcare Sites**
   - Digital Health Summit
   - Healthcare Startups Germany
   - Telemedicine Germany

2. **European Directories**
   - E-Health Europe
   - Digital Health Europe
   - HealthTech Europe

3. **International Directories** (JavaScript-heavy)
   - Crunchbase
   - AngelList
   - StartupBlink
   - PitchBook

4. **Healthcare News Sites**
   - Healthcare IT News
   - MobiHealthNews
   - Digital Health Network

## 🧠 NLP Filtering

### Healthcare Categories

The system recognizes healthcare companies in these categories:

- **Digital Health**: Telemedicine, healthtech, mobile health
- **Medical Devices**: Medtech, diagnostics, wearables
- **Healthcare Services**: Patient care, clinical services
- **Pharmaceutical**: Drug discovery, biotech
- **Mental Health**: Psychology, therapy, wellness
- **AI Healthcare**: Machine learning, predictive analytics

### Filtering Algorithm

1. **Keyword Density**: Count healthcare keywords in text
2. **TF-IDF Similarity**: Compare with healthcare keyword vectors
3. **Confidence Scoring**: Weighted combination of both methods
4. **Threshold Filtering**: Only companies above confidence threshold

## 🛡️ Error Handling & Reliability

### Retry Logic
- Exponential backoff for failed requests
- Configurable retry attempts
- Rate limiting to avoid being blocked

### Rate Limiting
- Random delays between requests
- Per-host connection limits
- Respectful scraping practices

### Data Validation
- URL format validation
- Social media exclusion
- File extension filtering
- Duplicate detection

## 📈 Performance Optimization

### Scalability Features
- Asynchronous processing
- Configurable concurrency limits
- Connection pooling
- Memory-efficient processing

### Monitoring
- Progress tracking with tqdm
- Detailed logging with loguru
- Performance metrics
- Error rate monitoring

## 🔧 Advanced Usage

### Custom Scraping

```python
from advanced_scraper import AdvancedHealthcareScraper

async def custom_scraping():
    scraper = AdvancedHealthcareScraper()
    
    # Scrape specific sites
    result = await scraper.scrape_healthcare_site("https://example.com")
    
    # Extract companies
    companies = scraper.extract_companies_from_result(result)
    return companies
```

### API Integration

```python
# Set API keys in environment variables
export CRUNCHBASE_API_KEY="your-api-key"
export LINKEDIN_API_KEY="your-api-key"

# The system will automatically use these for API-based discovery
```

### Custom Output Formats

```python
# Save in custom format
discovery.save_results(companies, format="json")

# Access raw data
for company in companies:
    print(f"{company.name}: {company.url} (Score: {company.confidence_score})")
```

## 🐛 Troubleshooting

### Common Issues

1. **Chrome/Selenium Issues**
   ```bash
   # Install Chrome
   sudo apt-get install chromium-browser
   
   # Or use Playwright instead
   playwright install chromium
   ```

2. **NLTK Data Missing**
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

3. **Rate Limiting**
   - Increase delays in `config.py`
   - Reduce concurrent requests
   - Use proxy rotation (not implemented)

4. **Memory Issues**
   - Reduce `max_concurrent_requests`
   - Process in smaller batches
   - Increase system RAM

### Debug Mode

```python
# Enable debug logging
from loguru import logger
logger.add("debug.log", level="DEBUG")

# Run with verbose output
discovery = HealthcareStartupDiscovery()
await discovery.run_discovery()
```

## 📝 Logging

### Log Files
- `output/discovery.log`: Main application logs
- `output/debug.log`: Debug information (when enabled)

### Log Levels
- **INFO**: General progress and results
- **WARNING**: Rate limiting, timeouts
- **ERROR**: Failed requests, exceptions
- **DEBUG**: Detailed debugging information

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Code Style
- Follow PEP 8
- Add type hints
- Include docstrings
- Write comprehensive tests

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- NLTK for natural language processing
- BeautifulSoup for HTML parsing
- aiohttp for asynchronous HTTP requests
- Selenium and Playwright for browser automation
- scikit-learn for machine learning components

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs in `output/`
3. Open an issue on GitHub
4. Contact the development team

---

**Note**: This system is designed for research and discovery purposes. Please respect website terms of service and robots.txt files when scraping. Consider implementing proper rate limiting and user agent rotation for production use.